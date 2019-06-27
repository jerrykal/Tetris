"""
A simple Tetris game written in Python.
"""

import pygame

from src.config import config
from src.game import Game


def main():
    # Initialize pygame
    pygame.init()

    # Initialize display
    display = pygame.display.set_mode(config["display"]["size"])
    pygame.display.set_caption(config["display"]["caption"])

    # Start the game
    game = Game(display)
    game.loop()


if __name__ == "__main__":
    main()
