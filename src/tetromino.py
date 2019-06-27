"""
A group of four square block that moved as an unit.
https://tetris.wiki/Tetromino
"""

import pygame

from src.config import config as src_config


class Piece(pygame.sprite.OrderedUpdates):
    """A group of blocks that moved as an unit

    https://tetris.wiki/Piece
    """

    def __init__(self, playfield, *sprites):
        """Initialize an instance of Piece

        Every sprite in the group must be an instance of Block.
        """
        super().__init__(*sprites)

        self.playfield = playfield

    def add_internal(self, sprite):
        """Do not use this method directly

        It is used by the group to add a sprite internally.
        """
        if isinstance(sprite, Block):
            super().add_internal(sprite)

    def draw(self):
        """Draw the piece onto the display

        Returns a list of Rectangular areas on the display that have
        been changed.
        """
        dirty = super().draw(self.playfield.surface)
        offset = self.playfield.surface.get_offset()
        return [rect.move(offset) for rect in dirty]

    def clear(self):
        """Draw the background of the playfield over the sprites"""
        super().clear(self.playfield.surface, self.playfield.clear_callback)

    def move(self, col, row):
        """Move the piece in place by the given offset

        Returns True if the piece moved successfully, otherwise returns False.
        """
        # Move the piece by the given offset
        for block in self.sprites():
            block.move(col, row)

        # Ensure the moved piece is in the valid space of the playfield
        if not self.playfield.valid_space(self):
            # Undo the movement
            for block in self.sprites():
                block.move(-col, -row)
            return False

        return True


class Tetromino(Piece):
    """A group of four blocks that moved as an unit"""

    config = src_config["tetromino"]

    def __init__(self, playfield, id_):
        """Initialize an instance of Tetromino"""
        spawn = self.config[id_]["spawn"]
        color = self.config[id_]["color"]
        sprites = (
            Block(playfield, cell[0], cell[1], color) for cell in spawn
        )
        super().__init__(playfield, *sprites)

        self.id = id_

        self.rotate_offsets = self.config[id_]["rotate_offsets"]
        self.curr_rotate_offset = 0

    def rotate(self, counterclockwise=False):
        """Rotate the tetromino in place clockwise or counterclockwise

        Returns True if the tetromino rotated successfully, otherwise returns
        False.
        """
        if not self.rotate_offsets:
            return False

        # Get the rotate_offset in order to rotate the tetromino
        rotate_offset = self.rotate_offsets[self.curr_rotate_offset]
        if counterclockwise:
            rotate_offset = tuple(
                (-offset[0], -offset[1])
                for offset in self.rotate_offsets[self.prev_rotate_offset]
            )

        # Rotate the tetromino
        for block, offset in zip(self.sprites(), rotate_offset):
            block.move(offset[0], offset[1])

        # Ensure the rotated tetromino is in the valid space of the playfield
        if not self.playfield.valid_space(self):
            # Undo the rotate
            for block, offset in zip(self.sprites(), rotate_offset):
                block.move(-offset[0], -offset[1])
            return False

        # Update self.curr_rotate_offset
        if counterclockwise:
            self.curr_rotate_offset = self.prev_rotate_offset
        else:
            self.curr_rotate_offset = self.next_rotate_offset

        return True

    @property
    def next_rotate_offset(self):
        """Get the next rotate offset"""
        return (self.curr_rotate_offset + 1) % len(self.rotate_offsets)

    @property
    def prev_rotate_offset(self):
        """Get the previous rotate offset"""
        ro_len = len(self.rotate_offsets)
        return ((self.curr_rotate_offset - 1) + ro_len) % ro_len


class Block(pygame.sprite.Sprite):
    """Square block that moves in playfield"""

    def __init__(self, playfield, col, row, color):
        """Initialize an instance of Block"""
        super().__init__()

        self.playfield = playfield
        self._col, self._row = None, None

        self.image = pygame.Surface(self.playfield.config["cell_size"])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.col, self.row = col, row

    @property
    def col(self):
        """Get the current column of the block"""
        return self._col

    @col.setter
    def col(self, value):
        """Set the current column of the block"""
        self._col = value
        self.rect.x = self.playfield.get_x(self._col)

    @property
    def row(self):
        """Get the current row of the block"""
        return self._row

    @row.setter
    def row(self, value):
        """Set the current row of the block"""
        self._row = value
        self.rect.y = self.playfield.get_y(self._row)

    def move(self, col, row):
        """Move the block in place by the given offset"""
        self.col += col
        self.row += row
