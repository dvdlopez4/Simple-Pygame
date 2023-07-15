import os


ASSET_FILE_PATH = os.path.join(os.path.dirname(__file__), '../assets/')
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
ROOMS = {
    "hall": [
        ["       w",
         "   www w",
         "       w",
         "  www  w",
         " wwww   ",
         " wwww   ",
         " w      ",
         "wwwwwwww"],
        ["        ",
         "   w w  ",
         "    w   ",
         "    w   ",
         "        ",
         "    ww  ",
         " w wwwww",
         "wwwwwwww"],
        ["    w   ",
         "   www  ",
         "        ",
         "www     ",
         "     w  ",
         "    ww  ",
         " www w  ",
         "wwwwwwww"],
        ["       w",
         "  w     ",
         "  w     ",
         "www    w",
         "w       ",
         "w       ",
         "w       ",
         "wwwwwwww"],
        ["      ww",
         "w     ww",
         "        ",
         "        ",
         "        ",
         "wwwww   ",
         "        ",
         "wwwwwwww"],
        ["ww      ",
         "    w   ",
         "        ",
         "w ww    ",
         "     w  ",
         "     w  ",
         "     w  ",
         "wwwwwwww"],
        ["        ",
         "        ",
         "     www",
         "ww      ",
         "   w    ",
         "        ",
         " w    w ",
         "wwwwwwww"],
    ],
    "drop": [
        ["        ",
         "        ",
         "        ",
         "        ",
         "     b  ",
         "        ",
         "        ",
         "        "],
        ["        ",
         "        ",
         "        ",
         "    w   ",
         "        ",
         "  w    w",
         "        ",
         "   www  "],
        ["     b  ",
         "   w w   ",
         "    w   ",
         "    w   ",
         "   w w  ",
         "  w   w ",
         "        ",
         "        "]
    ],
    0: [
        ["wwwwwwww", "wwwww   ", "wwwww   ", "wwwww   ",
            "wwwww   ", "wwwww   ", "wwwww   ", "wwwwwwww"],
        ["    wwww", "w   w   ", "  www   ", "        ",
         "        ", "        ", "        ", "wwwwwwww"],
        ["wwwwwwww", "wwwwwwww", "wwwwwwww", "wwwwwwww",
         "wwwwwwww", "wwwwwwww", "wwwwwwww", "wwwwwwww"],
    ],
    "start": [["        ", "        ", "        ", "        ", "        ", " ^      ", "(e)     ", "wwwwwwww"]],
    "end": [["        ", "        ", "        ", "        ", "        ", " ^      ", "(s)     ", "wwwwwwww"]]
}
