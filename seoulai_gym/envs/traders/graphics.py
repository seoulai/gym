"""
Cinyoung Hur, cinyoung.hur@gmail.com
seoulai.com
2018
"""
from typing import List

import matplotlib.backends.backend_agg as agg
import matplotlib.pyplot as plt
import pylab
import pygame

from seoulai_gym.envs.traders.base import Constants


class Graphics(Constants):
    def __init__(
        self,
        window_size: int=600,
    ):
        self.window_size = window_size
        self.initialized_window = False
        self.fig = pylab.figure(
            figsize=[4, 4],  # Inches
            dpi=100,  # 100 dots per inch, so the resulting buffer is 400x400 pixels
        )

    def _init_window(
        self,
    ):
        """Initialize window separately from constructor. Window is initialized only when graphics
        is rendered for the first time.

        Returns:
            None
        """
        if not self.initialized_window:
            pygame.init()
            pygame.display.set_caption("Traders")
            self.window = pygame.display.set_mode([self.window_size] * 2)
            self.screen = pygame.display.get_surface()
            self.font = pygame.font.SysFont("monospace", 15)

    def _setup_colors(
        self,
    ) -> None:
        """Setup colors used for drawing ticks.

        Returns: None
        """
        pass

    def update(
        self,
        prices: List,
        wallet: int=10000,
        decision: str=Constants.BUY
    ) -> None:
        """Update visualization of prices and profits with respect to the current state.
        Agent"s decisions at certain timestamp are displayed.

        Args:
            prices: Information about prices.
            wallet: Information about agent"s wallet.
            decision: Agent"s decisions at certain timestamp.

        Returns:
            None
        """
        self._init_window()

        # render prices
        ax = self.fig.gca()
        ax.plot(prices)
        ax.text(len(prices)-1, prices[-1], decision)

        canvas = agg.FigureCanvasAgg(self.fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        plt.cla()

        raw_data = renderer.tostring_rgb()
        size = canvas.get_width_height()
        surf = pygame.image.fromstring(raw_data, size, "RGB")
        self.screen.blit(surf, (0, 0))

        # render wallet
        wallet_str = "Wallet {wallet}".format(wallet=round(wallet, 2))
        label = self.font.render(wallet_str, 1, (255, 255, 0))
        self.screen.blit(label, (410, 50))

        pygame.display.flip()
