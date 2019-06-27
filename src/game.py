"""
Game engine for the Tetris game.
"""

from random import randint

import pygame

from src.config import config as src_config
from src.playfield import Playfield
from src.tetromino import Tetromino


class Game:
    """Game engine for the Tetris game"""

    config = src_config["game"]

    def __init__(self, display):
        """Initialize the game engine"""
        self.display = display
        self.quit = False

        self.changed_areas = []

        self.hud = GameHUD(self)
        self.hud.level = 0
        self.hud.score = 0
        self.hud.line_cleared = 0

        self.playfield = Playfield(self.display)
        self.tetromino = None
        self.next_tetromino = None
        self.new_tetromino()

        self.move_keydowns = set()

        self.drop_delay = {
            "delay": self.config["drop_delay"][min(self.hud.level, 29)],
            "counter": 0,
            "soft_drop": False
        }

        self.shift_offset = None
        self.shift_delay = {
            "delay": self.config["das_delay"],
            "counter": 0,
            "delayed_auto_shift": False
        }

        self.entry_delay = {
            "delay": self.config["entry_delay"],
            "counter": 0,
        }

    def reinit(self):
        """Reinitialize the game"""
        self.__init__(self.display)

    def loop(self):
        """Main game loop of the game engine"""
        # Initialize clock, which is used to cap the framerate
        clock = pygame.time.Clock()

        # Draw everything first before entering the game loop
        pygame.display.flip()

        while not self.quit:
            self.handle_events()

            if self.tetromino:
                self.handle_tetromino_shift()
                self.handle_tetromino_drop()
            else:
                self.handle_tetromino_entry()

            # Update changed portion of the display
            pygame.display.update(self.changed_areas)
            self.changed_areas = []

            # Cap the framerate
            clock.tick(self.config["fps"])

    def handle_events(self):
        """Handle inpute events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit = True

            elif event.type in (pygame.KEYDOWN, pygame.KEYUP):
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_LEFT, pygame.K_RIGHT,
                                     pygame.K_DOWN):
                        self.move_keydowns.add(event.key)

                    # Rotate the tetromino when the player presses x or z key
                    elif self.tetromino and event.key == pygame.K_x:
                        self.rotate_tetromino()
                    elif self.tetromino and event.key == pygame.K_z:
                        self.rotate_tetromino(counterclockwise=True)
                else:
                    if event.key in (pygame.K_LEFT, pygame.K_RIGHT,
                                     pygame.K_DOWN):
                        self.move_keydowns.discard(event.key)

                # Prepare to move the tetromino if only one of the movement
                # key is pressed.
                if len(self.move_keydowns) == 1:
                    if self.tetromino and pygame.K_DOWN in self.move_keydowns:
                        self.drop_delay["soft_drop"] = True
                    elif pygame.K_LEFT in self.move_keydowns:
                        self.shift_offset = -1
                    elif pygame.K_RIGHT in self.move_keydowns:
                        self.shift_offset = 1
                else:
                    self.shift_offset = None
                    if self.tetromino:
                        self.shift_delay["delayed_auto_shift"] = False
                    self.drop_delay["soft_drop"] = False

    def handle_tetromino_shift(self):
        """Handle the shift movement of the tetromino"""
        # Try to shift self.tetromino if self.shift_offset is set
        if self.shift_offset:
            # Implement delayed auto shift(https://tetris.wiki/DAS)
            if not self.shift_delay["delayed_auto_shift"]:
                if self.move_tetromino(self.shift_offset, 0):
                    self.shift_delay["counter"] = 0
                else:
                    # Instantly set the delay counter to its max value if a tap
                    # shift is blocked.
                    self.shift_delay["counter"] = self.shift_delay["delay"]
                self.shift_delay["delayed_auto_shift"] = True
            else:
                if self.shift_delay["counter"] >= self.shift_delay["delay"]:
                    if self.move_tetromino(self.shift_offset, 0):
                        self.shift_delay["counter"] -= 6
                else:
                    self.shift_delay["counter"] += 1

    def handle_tetromino_drop(self):
        """Handle the drop movement of the tetromino"""
        delay = self.drop_delay["delay"]
        if self.drop_delay["soft_drop"] and\
                delay > self.config["soft_drop_delay"]:
            delay = self.config["soft_drop_delay"]

        if self.drop_delay["counter"] >= delay:
            # Lock the tetromino if it cannot drop
            if not self.move_tetromino(0, 1):
                self.handle_tetromino_lock()
                self.drop_delay["soft_drop"] = False

            self.drop_delay["counter"] = 0
        else:
            self.drop_delay["counter"] += 1

    def handle_tetromino_entry(self):
        """Handle the entry of the next tetromino"""
        if self.entry_delay["counter"] >= self.entry_delay["delay"]:
            self.new_tetromino()
            self.entry_delay["counter"] = 0
        else:
            self.entry_delay["counter"] += 1

    def handle_tetromino_lock(self):
        """Lock the tetromino onto the playfield

        Also calls self.game_over if the tetromino is overlapping with locked
        blocks.
        """
        if self.playfield.locked_collide(self.tetromino):
            self.handle_game_over()
            return

        self.lock_tetromino()

    def handle_game_over(self):
        """Game Over

        Quit or restart the game based on the player's input.
        """
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit = True
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.restart()
                        return

    def new_tetromino(self):
        """Generating new tetromino"""
        if self.next_tetromino:
            self.tetromino = self.next_tetromino
        else:
            self.tetromino = Tetromino(self.playfield, randint(0, 6))

        self.tetromino.clear()
        self.changed_areas = self.tetromino.draw()

        id_ = randint(0, 7)
        if id_ == 7 or id_ == self.tetromino.id:
            id_ = randint(0, 6)
        self.next_tetromino = Tetromino(self.playfield, id_)

    def rotate_tetromino(self, *args, **kwargs):
        """Rotate the tetromino and update it onto the display"""
        if self.tetromino.rotate(*args, **kwargs):
            self.tetromino.clear()
            self.changed_areas += self.tetromino.draw()

    def move_tetromino(self, *args, **kwargs):
        """Move the tetromino and update it onto the display"""
        if self.tetromino.move(*args, **kwargs):
            self.tetromino.clear()
            self.changed_areas += self.tetromino.draw()
            return True
        return False

    def lock_tetromino(self, *args, **kwargs):
        """Lock the tetromino and update it onto the display"""
        line_cleared = self.playfield.lock_piece(self.tetromino)
        self.tetromino.clear()
        self.playfield.locked_blocks.clear()
        self.changed_areas += self.playfield.locked_blocks.draw()

        if line_cleared:
            self.hud.line_cleared += line_cleared

            if line_cleared == 1:
                self.hud.score += 30 * (self.hud.level + 1)
            elif line_cleared == 2:
                self.hud.score += 100 * (self.hud.level + 1)
            elif line_cleared == 3:
                self.hud.score += 300 * (self.hud.level + 1)
            elif line_cleared == 4:
                self.hud.score += 1200 * (self.hud.level + 1)

            if self.hud.level != self.hud.line_cleared // 10:
                self.hud.level = self.hud.line_cleared // 10
                self.drop_delay["delay"] =\
                    self.config["drop_delay"][min(self.hud.level, 29)]

    def restart(self):
        """Restart the game"""
        # Reinitialize the game
        self.reinit()

        # Draw everything
        pygame.display.flip()


class GameHUD:
    """Heads-up display that shows useful in-game informations"""

    config = src_config["game"]["hud"]

    def __init__(self, game):
        """Initialize and instance of GameHUD"""
        self.game = game
        self.font = pygame.font.Font(self.config["font"]["face"],
                                     self.config["font"]["size"])

        self._level = None
        self._score = None
        self._line_cleared = None

    @property
    def level(self):
        """Get the current level of the game session"""
        return self._level

    @level.setter
    def level(self, value):
        """Set the current level of the game session"""
        self._level = value
        text = f"{self._level:02}" if self._level < 100 else "99+"
        self.draw_text(text, topleft=self.config["level_topleft"])

    @property
    def score(self):
        """Get the current score of the game session"""
        return self._score

    @score.setter
    def score(self, value):
        """Set the current score of the game session"""
        self._score = value
        text = f"{self._score:06}" if self._score < 1000000 else "999999+"
        self.draw_text(text, midtop=self.config["score_midtop"])

    @property
    def line_cleared(self):
        """Get the total line cleared of the game session"""
        return self._line_cleared

    @line_cleared.setter
    def line_cleared(self, value):
        """Set the total line cleared of the game session"""
        self._line_cleared = value
        text =\
            f"{self._line_cleared:03}" if self._line_cleared < 1000 else "999+"
        self.draw_text(text, topright=self.config["line_cleared_topright"])

    def draw_text(self, text, **kwargs):
        """Draw the given text onto the display

        The keyword arguments will be applied to the attribute of the rectangle
        of the text.
        """
        surf = self.font.render(text, 1, self.config["font"]["color"],
                                self.config["font"]["bgd_color"])
        rect = surf.get_rect(**kwargs)
        self.game.display.blit(surf, rect)
        self.game.changed_areas.append(rect)
