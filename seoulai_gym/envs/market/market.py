"""
Stock Market
Cinyoung Hur, cinyoung.hur@gmail.com
James Park, laplacian.k@gmail.com
seoulai.com
2018
"""
from seoulai_gym.envs.market.api import BaseAPI
from seoulai_gym.envs.market.base import Constants


class Market(BaseAPI):
    def __init__(
        self,
        state: str = None,
    ) -> None:
        """Initialize market and its visualization.
        Args:
            state: Optional, path to saved game state. TODO
        Returns:
            None
        """
        # graphics is for visualization
        # self.graphics = Graphics()
        # self.pause = False

    def select(
        self,
        exchange
    ) -> None:

        data = dict(exchange=exchange,)
        self.fee_rt = self.api_get("select", data)

    def reset(
        self,
    ):
        """Reset all variables and initialize trading game.
        Returns:
            state: Information about trading parameters.
        """
        data = dict(agent_id="RESET",    # TODO: change id
                    step_type=Constants.LOCAL,    # Local
                    decision=Constants.HOLD,
                    trad_qty=0.0,
                    trad_price=0.0,)
        state, _, _, _ = self.api_post("step", data)
        return state

    def step(
        self,
        env_type: int,
        agent_id: int,
        decision: int,
        trad_qty: float,
        trad_price: float,
    ):
        """Make a step (= move) within market.
        Args:
            agent: Agent name(id)
            decision : buy, sell or hold. Agent position.
            trad_price: Price that Agent want to trade.
            trad_qty: Quantity that Agent want to trade.
        Returns:
            obs: Information of price history and fee ratio.
            rew: Reward for perfomed step.
            done: Information about end of game.
            info: Additional information about current step.
        """
        data = dict(env_type=env_type,
                    agent_id=agent_id,
                    decision=decision,
                    trad_qty=trad_qty,
                    trad_price=trad_price,
                    )
        r = self.api_post("step", data)

        next_state = r.get("next_state")
        reward = r.get("reward")
        done = r.get("done")
        info = r.get("info")

        return next_state, reward, done, info

    def render(
        self,
        agent,
        info,
        decision,
    ) -> None:
        """Display current state of board.
        Returns:
            None
        """
        pass

    def paused(self):
        pass

    def close(
        self,
    ) -> None:
        pass
