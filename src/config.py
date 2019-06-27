"""
Configurations for the Tetris game.
"""

config = {
    # Display configuration
    "display": {
        "size": (400, 800),
        "caption": "Tetris"
    },

    # Game configuration
    "game": {
        "fps": 60,
        "drop_delay": 48,
        "soft_drop_delay": 2,
        "das_delay": 16,
        "entry_delay": 14
    },

    # Playfield configuration
    "playfield": {
        "area": (0, 0, 400, 800),
        "vanish_zone": (0, -80, 400, 80),
        "bgd_color": (10, 10, 10),
        "cell_size": (40, 40)
    },

    # Configurations for 7 different tetrominoes
    "tetromino": [
        # I
        {
            "spawn": ((3, 0), (4, 0), (5, 0), (6, 0)),
            "color": (99, 197, 235),
            "rotate_offsets": (((2, -2), (1, -1), (0, 0), (-1, 1)),
                               ((-2, 2), (-1, 1), (0, 0), (1, -1)))
        },
        # O
        {
            "spawn": ((4, 0), (5, 0), (4, 1), (5, 1)),
            "color": (244, 211, 72),
            "rotate_offsets": (((0, 0), (0, 0), (0, 0), (0, 0)),
                               ((0, 0), (0, 0), (0, 0), (0, 0)))
        },
        # T
        {
            "spawn": ((4, 0), (5, 0), (6, 0), (5, 1)),
            "color": (161, 82, 152),
            "rotate_offsets": (((1, -1), (0, 0), (-1, 1), (-1, -1)),
                               ((1, 1), (0, 0), (-1, -1), (1, -1)),
                               ((-1, 1), (0, 0), (1, -1), (1, 1)),
                               ((-1, -1), (0, 0), (1, 1), (-1, 1)))
        },
        # S
        {
            "spawn": ((5, 0), (6, 0), (4, 1), (5, 1)),
            "color": (100, 178, 82),
            "rotate_offsets": (((1, 0), (0, 1), (1, -2), (0, -1)),
                               ((-1, 0), (0, -1), (-1, 2), (0, 1)))
        },
        # Z
        {
            "spawn": ((4, 0), (5, 0), (5, 1), (6, 1)),
            "color": (220, 58, 53),
            "rotate_offsets": (((2, -1), (1, 0), (0, -1), (-1, 0)),
                               ((-2, 1), (-1, 0), (0, 1), (1, 0)))
        },
        # J
        {
            "spawn": ((4, 0), (5, 0), (6, 0), (6, 1)),
            "color": (92, 102, 168),
            "rotate_offsets": (((1, -1), (0, 0), (-1, 1), (-2, 0)),
                               ((1, 1), (0, 0), (-1, -1), (0, -2)),
                               ((-1, 1), (0, 0), (1, -1), (2, 0)),
                               ((-1, -1), (0, 0), (1, 1), (0, 2)))
        },
        # L
        {
            "spawn": ((4, 0), (5, 0), (6, 0), (4, 1)),
            "color": (224, 126, 58),
            "rotate_offsets": (((1, -1), (0, 0), (-1, 1), (0, -2)),
                               ((1, 1), (0, 0), (-1, -1), (2, 0)),
                               ((-1, 1), (0, 0), (1, -1), (0, 2)),
                               ((-1, -1), (0, 0), (1, 1), (-2, 0)))
        },
    ]
}
