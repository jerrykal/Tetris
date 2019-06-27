"""
The surface into which tetrominoes fall.
https://tetris.wiki/Playfield
"""

import pygame

from src.config import config as src_config
from src.tetromino import Block


class Playfield:
    """The surface into which tetrominoes fall"""

    config = src_config["playfield"]

    def __init__(self, display):
        """Initialize an instance of Playfield"""
        self.display = display

        self.surface = self.display.subsurface(self.config["area"])
        self.surface.fill(self.config["bgd_color"])

        self.locked_blocks = LockedBlocked(self)

    def get_x(self, col):
        """Get the x coordinate of the given column in the playfield"""
        return col * self.config["cell_size"][0]

    def get_y(self, row):
        """Get the y coordinate of the given row in the playfield"""
        return row * self.config["cell_size"][1]

    def valid_space(self, piece):
        """Check if the given piece is in the valid space of the playfield

        Returns True if the given piece is contained withing the playfield and
        its not colliding with locked blocks, otherwise returns False.
        """
        return self.contains(piece) and (not self.locked_collide(piece))

    def contains(self, piece):
        """Check if the given piece is contained within the playfield

        Returns True if the given piece is contained within the playfield,
        otherwise returnns False.
        """
        vanish_zone = pygame.Rect(self.config["vanish_zone"])
        rect = self.surface.get_rect().union(vanish_zone)
        for block in piece.sprites():
            if not rect.contains(block.rect):
                return False
        return True

    def locked_collide(self, piece):
        """Check if the given piece is colliding with locked blocks

        Returns True if the given piece is colliding with locked blocks,
        otherwise returns False.
        """
        return bool(pygame.sprite.groupcollide(piece, self.locked_blocks,
                                               dokilla=False, dokillb=False))

    def lock_piece(self, piece):
        """Lock the given piece onto the playfield"""
        # Add all block in the given piece to self.locked_blocks
        self.locked_blocks.add(piece)

        # Remove all block from the given piece, so the player can no longer
        # control the piece.
        piece.empty()

        # Clear complete line and return the amount of line cleared
        return self.locked_blocks.line_clear()

    def clear_callback(self, surf, rect):
        """Callback function for pygame.sprite.AbstractGroup.clear"""
        surf.fill(self.config["bgd_color"], rect)


class LockedBlocked(pygame.sprite.RenderUpdates):
    """A group of blocks that's been locked onto the playfield"""

    def __init__(self, playfield, *sprites):
        """Initialize an instance of LockedBlocked

        Every sprite in the group must be an instance of Block.
        """
        super().__init__(*sprites)

        self.playfield = playfield
        self.sprite_groups = tuple(pygame.sprite.Group() for i in range(0, 22))

    def add_internal(self, sprite):
        """Do not use this method directly

        It is used by the group to add a sprite internally.
        """
        if isinstance(sprite, Block):
            super().add_internal(sprite)
            self.sprite_groups[21 - (sprite.row + 2)].add(sprite)

    def remove_internal(self, sprite):
        """Do not use this method directly

        It is used by the group to remove a sprite internally.
        """
        if isinstance(sprite, Block):
            super().remove_internal(sprite)
            self.sprite_groups[21 - (sprite.row + 2)].remove(sprite)

    def draw(self):
        """Draw the lock blocks onto the display

        Returns a list of Rectangular areas on the display that have
        been changed.
        """
        dirty = super().draw(self.playfield.surface)
        offset = self.playfield.surface.get_offset()
        return [rect.move(offset) for rect in dirty]

    def clear(self):
        """Draw the background of the playfield over the sprites"""
        super().clear(self.playfield.surface, self.playfield.clear_callback)

    def line_clear(self):
        """Clear complete row of blocks, and moves blocks above it downward

        Returns the total amount rows been cleared.
        """
        line_cleared = 0

        for i, group in enumerate(self.sprite_groups):
            if len(group) == 0:
                break
            elif len(group) == 10:
                self.remove(group)
                line_cleared += 1
            elif line_cleared:
                for block in group.sprites():
                    block.move(0, line_cleared)
                self.sprite_groups[i - line_cleared].add(group)
                group.empty()

        return line_cleared
