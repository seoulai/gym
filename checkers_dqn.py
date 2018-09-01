"""
Martin Kersner, m.kersner@gmail.com
seoulai.com
2018

Agent inspired by PyTorch Reinforcement Learning (DQN) tutorial
https://pytorch.org/tutorials/intermediate/reinforcement_q_learning.html
"""

import copy
import math
import logging
import random
import warnings
from argparse import Namespace
from argparse import ArgumentParser
from collections import namedtuple
from itertools import count
from typing import List
from typing import Tuple
from pathlib import Path

from visdom import Visdom
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F

import seoulai_gym as gym
from seoulai_gym.envs.checkers.base import Constants
from seoulai_gym.envs.checkers.agents import Agent
from seoulai_gym.envs.checkers.agents import RandomAgentDark
from seoulai_gym.envs.checkers.utils import board_list2numpy

# TODO load pretrained model
# TODO save models
# TODO remove all additional float call
# TODO remove magic constants

logging.basicConfig(level=logging.INFO)


class Line(object):
    def __init__(
        self,
        activated: bool,
    ):
        self._activated = activated
        if self._activated:
            self.viz = Visdom()
            self.lines = []

    def __call__(
        self,
        title: str,
        legend: List[str]=[""],
    ):
        if self._activated:
            win = self.viz.line(
                Y=[0],
                X=[0],
                opts=dict(
                    title=title,
                    showlegend=True,
                    legend=legend,
                ),
            )

        def update(X, Y):
            if self._activated and win is not None:
                self.viz.line(
                    win=win,
                    X=[X],
                    Y=[Y],
                    opts=dict(
                        showlegend=True,
                    ),
                    update="append",
                )
        return update


Transition = namedtuple("Transition",
                        (
                            "state",
                            "action",
                            "next_state",
                            "reward",
                        ))

class FinalAgent(Agent):
    def __init__(
        self,
        name: str,
        ptype: int,
        model_path: Path,
        device: str,
    ):
        super().__init__(name, ptype)
        self.device = device
        self.net = DQN().to(self.device)
        self.net.load_state_dict(torch.load(model_path))
        self.net.eval()

    def act(
        self,
        board: List[List],
    ) -> Tuple[int, int, int, int]:
        obs = self.init_board_torch(board, self.device)
        action = self.net(obs).max(2)[0][0].long()
        action = tuple(int(a) for a in action.tolist())
        return action

    def consume(
        self,
        obs,
        reward: float,
        done: bool,
    ) -> None:
        pass

    # TODO refactor with DQNAgent
    @staticmethod
    def init_board_torch(
        board: List[List],
        device: str,
    ) -> torch.tensor:
        """
        todo:
            remove float()

        args:
            board: (list[list])
            device: (str)

        return:
            torch.tensor
        """
        board_size = len(board)
        board_tensor_shape = (1, 1, board_size, board_size)
        return torch.from_numpy(board_list2numpy(board)).float().view(*board_tensor_shape).to(device)


class DQNAgent(Agent):
    def __init__(
        self,
        name: str,
        ptype: int,  # FIXME not int
        device: str,
        args: Namespace,
        is_training: bool=False,
        board_size: int=8,
    ) -> None:
        """Initialize DQN agent.

        Args:
            name: (str) name of agent.
            ptype: (int) type of piece that agent is responsible for.
            device: (str) type of device to be used for training.
            args:
            is_training: (bool) If True, DQN model is training. If False, model is loaded and
                executed.
            board_size: (int) number of fields in board across one dimension

        Return:
            None
        """
        super().__init__(name, ptype)

        self.device = device
        self.args = args
        self.is_training = is_training
        self.board_size = board_size

        self.steps_done = 0  # TODO rename

        # TODO difference between policy net and target net?
        # TODO remove target net
        self.policy_net = DQN().to(self.device)
        self.target_net = DQN().to(self.device)
        self.target_net.load_state_dict(self.policy_net.state_dict())
        self.target_net.eval()

        self.optimizer = optim.SGD(self.policy_net.parameters(), lr=self.args.lr)
        self.scheduler = optim.lr_scheduler.ReduceLROnPlateau(
            self.optimizer,
            mode="min",
            factor=1e-1,
            patience=16_000,
            verbose=True,
            threshold=1e-4,
            threshold_mode="rel",
            cooldown=1_000,
            min_lr=0,
            eps=1e-08,
        )
        self.memory = ReplayMemory(self.args.replay_memory_size)

    @property
    def train_loss(self):
        try:
            return self._train_loss
        except AttributeError:
            self._train_loss = []
            return self._train_loss

    @train_loss.setter
    def train_loss(self, loss):
        try:
            self._train_loss.append(loss)
        except AttributeError:
            self._train_loss = []
            self._train_loss.append(loss)

    @train_loss.deleter
    def train_loss(self):
        try:
            del self._train_loss
        except AttributeError:
            self._train_loss = []

    def train(self):
        self._mode = "train"

    def evaluate(self, episode: int):
        self._mode = "evaluate"
        self.update_target_net()
        torch.save(
            self.target_net.state_dict(),
            Path("out") / f"{episode}.pt",  # TODO  build save path
        )

    @property
    def is_train(self):
        try:
            if self._mode == "train":
                return True
            else:
                return False
        except AttributeError:
            self.train()
            return True

    @property
    def is_evaluate(self):
        try:
            if self._mode == "evaluate":
                return True
            else:
                return False
        except AttributeError:
            self.train()
            return False

    @property
    def mode(self):
        try:
            return self._mode
        except AttributeError:
            self.train()
            return self._mode

    def act_constant(
        self,
        board: List[List],
    ) -> Tuple[int, int, int, int]:
        """Generate constant move. This move can be invalid.

        Args:
            board: (List[List]) information about positions of pieces

        Return:
            action: (Tuple[int, int, int, int]) current and new location of piece
        """
        warnings.warn("act_constant generate constant invalid move.")
        from_row = from_col = to_row = to_col = 0

        self.before_obs = self.init_board_torch(board, self.device)
        action = from_row, from_col, to_row, to_col
        self.action = torch.tensor(action, device=self.device)
        return copy.deepcopy(action)

    @property
    def epsilon_threshold(self):
        return self.args.eps_end + \
            (self.args.eps_start-self.args.eps_end) * math.exp(-1.0*self.steps_done / self.args.eps_decay)

    def act(
        self,
        board: List[List],
    ) -> Tuple[int, int, int, int]:
        """
        Args:
            board: (List[List]) information about positions of pieces on board

        Return:
            action: (Tuple[int, int, int, int]) current and new location of piece
        """
        self.before_obs = self.init_board_torch(board, self.device)

        if self.mode == "eval" or random.random() > self.epsilon_threshold:
            with torch.no_grad():
                # self.action = self.policy_net(self.before_obs).max(2)[0][0].long()
                self.action = self.policy_net(self.before_obs).max(2)[1][0].long()
                action = tuple(int(a) for a in self.action.tolist())
        else:
            valid_moves = self.generate_valid_moves(board, self.ptype, self.board_size)
            rand_from_row, rand_from_col = random.choice(list(valid_moves.keys()))
            rand_to_row, rand_to_col = random.choice(valid_moves[(rand_from_row, rand_from_col)])
            action = rand_from_row, rand_from_col, rand_to_row, rand_to_col
            self.action = torch.tensor(action, device=self.device, dtype=torch.long)

        self.steps_done += 1
        return copy.deepcopy(action)

    def consume(
        self,
        board: List[List],
        reward: float,
        done: bool,
    ) -> None:
        """Save movememt to `ReplayMemory` and optimize DQN model.

        Args:
            board: (List[List]) information about positions of pieces on board
            reward: (float) reward for perfomed step
            done: (bool) information about end of game

        Return:
            None
        """
        if self.mode == "train":
            reward = torch.tensor([reward], device=self.device)

            if done:
                after_obs = None
            else:
                after_obs = self.init_board_torch(board, self.device)

            self.memory.push(self.before_obs, self.action.unsqueeze(0), after_obs, reward)
            self.optimize_model()

    def optimize_model(self) -> None:
        if len(self.memory) < self.args.batch_size:
            logging.debug("nothing to optimize yet")
            return

        transitions = self.memory.sample(self.args.batch_size)
        # Transpose the batch (see http://stackoverflow.com/a/19343/3343043 for detailed explanation).
        # TODO check it
        batch = Transition(*zip(*transitions))

        # Compute a mask of non-final states and concatenate the batch elements
        non_final_mask = torch.tensor(tuple(map(lambda s: s is not None,
                                            batch.next_state)), device=self.device, dtype=torch.uint8)

        non_final_next_states = torch.cat([s for s in batch.next_state if s is not None])
        state_batch = torch.cat(batch.state)

        action_batch = torch.cat(batch.action)
        reward_batch = torch.cat(batch.reward)

        # Compute Q(s_t, a) - the model computes Q(s_t), then we select the columns of actions taken
        # FIXME
        # state_action_values = self.policy_net(state_batch).gather(1, action_batch)
        # [4, batch_size]
        state_action_values = self.policy_net(state_batch)

        state_action_values = state_action_values.gather(0, action_batch.unsqueeze(2).expand_as(state_action_values))

        # Compute V(s_{t+1}) for all next states.
        next_state_values = torch.zeros(self.args.batch_size, 4, 8, device=self.device)  # FIXME magic number
        # next_state_values[non_final_mask] = self.target_net(non_final_next_states).max(1)[0].detach()

        next_state_values[non_final_mask] = self.target_net(non_final_next_states).detach().float()  # FIXME detach()?

        # Compute the expected Q values
        expected_state_action_values = (next_state_values * self.args.gamma) \
            + reward_batch.unsqueeze(1).unsqueeze(1).expand_as(next_state_values)

        # Compute Huber loss
        loss = F.smooth_l1_loss(state_action_values.float(), expected_state_action_values)
        self.scheduler.step(loss)
        self.train_loss = float(loss)

        # Optimize the model
        self.optimizer.zero_grad()
        loss.backward()
        for param in self.policy_net.parameters():
            param.grad.data.clamp_(-1, 1)
        self.optimizer.step()

    @property
    def lr(self):
        lr = []
        for param_group in self.optimizer.param_groups:
            lr.append(param_group["lr"])
        assert len(lr) == 1
        return lr[0]

    def update_target_net(self):
        """Call in repetitive intervals at the end of episode."""
        self.target_net.load_state_dict(self.policy_net.state_dict())

    @staticmethod
    def get_random_value(
        max_val: int,
    ) -> int:
        def rand_fn():
            return random.randint(0, max_val-1)
        return rand_fn

    @staticmethod
    def init_board_torch(
        board: List[List],
        device: str,
    ) -> torch.tensor:
        """
        todo:
            remove float()

        args:
            board: (list[list])
            device: (str)

        return:
            torch.tensor
        """
        board_size = len(board)
        board_tensor_shape = (1, 1, board_size, board_size)
        return torch.from_numpy(board_list2numpy(board)).float().view(*board_tensor_shape).to(device)


class ReplayMemory(object):
    def __init__(
        self,
        capacity: int,
    ):
        self.capacity = capacity
        self.memory = []
        self.position = 0
        self.full_memory = False

    def push(
        self,
        *args,
    ):
        """Saves a transition."""
        # TODO replace old ones
        if len(self.memory) < self.capacity:
            # FIXME why not in one step?
            self.memory.append(None)
            self.memory[self.position] = Transition(*args)
            self.position = (self.position + 1) % self.capacity
        else:
            if not self.full_memory:
                self.full_memory = True
                logging.info("Replay memory is full")

            position = random.randint(0, self.capacity-1)
            self.memory[position] = Transition(*args)
            logging.debug("Replay memory updated")

    def sample(
        self,
        batch_size: int,
    ):
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)


class DQN(nn.Module):
    def __init__(self):
        super().__init__()

        # [batch, 1, 8, 8]
        self.conv1 = nn.Conv2d(1, 16, kernel_size=3, stride=1, padding=1)
        # [batch, 16, 8, 8]
        self.bn1 = nn.BatchNorm2d(16)
        # [batch, 16, 8, 8]
        self.conv2 = nn.Conv2d(16, 32, kernel_size=5, stride=1, padding=1)
        # [batch, 32, 6, 6]
        self.bn2 = nn.BatchNorm2d(32)
        # [batch, 32, 6, 6]
        self.conv3 = nn.Conv2d(32, 32, kernel_size=5, stride=1, padding=1)
        # [batch, 32, 4, 4]
        self.bn3 = nn.BatchNorm2d(32)
        # [batch, 32, 4, 4]

        lin_in_features = 32*4*4
        lin_out_features = 8
        self.head_from_row = nn.Linear(lin_in_features, lin_out_features)
        self.head_from_col = nn.Linear(lin_in_features, lin_out_features)
        self.head_to_row = nn.Linear(lin_in_features, lin_out_features)
        self.head_to_col = nn.Linear(lin_in_features, lin_out_features)

        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.kaiming_normal_(m.weight, mode="fan_out", nonlinearity="relu")
            elif isinstance(m, nn.BatchNorm2d):
                nn.init.constant_(m.weight, 1)
                nn.init.constant_(m.bias, 0)

    def forward(self, x):
        x = F.relu(self.bn1(self.conv1(x)))
        x = F.relu(self.bn2(self.conv2(x)))
        x = F.relu(self.bn3(self.conv3(x)))

        inter_out = x.view(x.size(0), -1)

        from_row = self.head_from_row(inter_out).unsqueeze(1)
        from_col = self.head_from_col(inter_out).unsqueeze(1)
        to_row = self.head_to_row(inter_out).unsqueeze(1)
        to_col = self.head_to_col(inter_out).unsqueeze(1)

        out = torch.cat([
            from_row,
            from_col,
            to_row,
            to_col,
        ], dim=1)

        return out


def main(args: Namespace):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    env = gym.make("Checkers")
    line = Line(args.visdom_activated)
    dqn_agent = DQNAgent(
        name="DQNLightAgent",
        ptype=Constants().LIGHT,
        device=device,
        args=args,  # TODO remove args dependency
        is_training=args.is_training,
    )
    random_agent = RandomAgentDark("RangomDarkAgent")

    train_game_length_line = line("Train length of game", [""])
    train_dqn_win_line = line("Train win ratio", ["dqn/random ratio"])
    train_loss_line = line("Train loss", ["loss"])
    eval_game_length_line = line("Eval length of game", [""])
    eval_dqn_win_line = line("Eval win ratio", ["dqn/random ratio"])
    lr_line = line("Learning rate", [""])
    eps_line = line("Epsilon threshold", ["eps"])

    train_dqn_agent_num_wins = train_random_agent_num_wins = 1
    eval_dqn_agent_num_wins = eval_random_agent_num_wins = 1

    for ep in range(args.num_episodes):
        obs = env.reset()

        current_agent = dqn_agent
        next_agent = random_agent

        if (ep+1) % args.eval_frequency == 0:
            dqn_agent.evaluate(ep+1)
            eval_num_games = args.eval_num_games

        for step in count():
            action = current_agent.act(obs)
            obs, reward, done, info = env.step(current_agent, *action)
            current_agent.consume(obs, reward, done)

            if done:
                logging.info(f"{dqn_agent.mode}:{ep}:Game over! {current_agent} agent wins in {step} steps.")  # TODO correct?
                if dqn_agent.is_train:
                    if str(current_agent) == "DQNLightAgent":
                        train_dqn_agent_num_wins += 1
                    else:
                        train_random_agent_num_wins += 1

                    train_game_length_line(X=[ep], Y=[step])
                    train_dqn_win_line(X=[ep], Y=[train_dqn_agent_num_wins/train_random_agent_num_wins])
                    train_loss_line(X=[ep], Y=[np.mean(dqn_agent.train_loss)])
                    lr_line(X=np.array([ep]), Y=np.array([dqn_agent.lr]))
                    eps_line(X=np.array([ep]), Y=np.array([dqn_agent.epsilon_threshold]))
                    del(dqn_agent.train_loss)
                elif dqn_agent.is_evaluate:
                    eval_num_games -= 1

                    if eval_num_games == 0:
                        dqn_agent.train()
                    else:
                        if str(current_agent) == "DQNLightAgent":
                            eval_dqn_agent_num_wins += 1
                        else:
                            eval_random_agent_num_wins += 1

                        eval_game_length_line(X=[ep], Y=[step])
                        eval_dqn_win_line(X=[ep], Y=[eval_dqn_agent_num_wins/eval_random_agent_num_wins])
                else:
                    raise NotImplementedError

                break

            # switch agents
            temporary_agent = current_agent
            current_agent = next_agent
            next_agent = temporary_agent

            # env.render()

    env.close()


if __name__ == "__main__":
    # TODO help description
    parser = ArgumentParser()
    parser.add_argument("--batch_size", type=int, default=1_024)
    parser.add_argument("--gamma", type=float, default=0.999)
    parser.add_argument("--eps_start", type=float, default=0.9)
    parser.add_argument("--eps_end", type=float, default=0.05)
    parser.add_argument("--eps_decay", type=int, default=40_000)
    # parser.add_argument("--target_update", type=int, default=10)
    parser.add_argument("--replay_memory_size", type=int, default=100_000)
    parser.add_argument("--num_episodes", type=int, default=1_000_000)
    parser.add_argument("--lr", type=float, default=1e-3)

    # Evaluation
    parser.add_argument("--eval_frequency", type=float, default=50)
    parser.add_argument("--eval_num_games", type=float, default=10)

    parser.add_argument("--train", dest="is_training", action="store_true")
    parser.add_argument("--evaluate", dest="is_training", action="store_false")
    parser.set_defaults(is_training=True)

    parser.add_argument("--visdom", dest="visdom_activated", action="store_true")
    parser.add_argument("--no-visdom", dest="visdom_activated", action="store_false")
    parser.set_defaults(visdom_activated=False)

    args = parser.parse_args()
    main(args)
