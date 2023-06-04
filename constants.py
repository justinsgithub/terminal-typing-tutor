from blessed import Terminal

MAIN_MENU_TITLE = 'Series selection menu'

MAIN_MENU = [
    {
        "title": "Series Q    Quick QWERTY course  (Q1 - Q5) ",
        "series": "Q",
    },
    {
        "title": "Series R    Long QWERTY course  (R1 - R14) ",
        "series": "R",
    },
    {
        "title": "Series T    QWERTY touch typing  (T1 - T16)",
        "series": "T",
    },
    {
        "title": "Series V    Yet more QWERTY  (V1 - V19)    ",
        "series": "V",
    },
    {
        "title": "Series U    QWERTY Review  (U1 - U13)      ",
        "series": "U",
    },
    {
        "title": "Series M    Typing drills  (M1 - M11)      ",
        "series": "M",
    },
    {
        "title": "Series S    Speed drills  (S1 - S4)        ",
        "series": "S",
    },
]

TERM = Terminal()
HOME = TERM.home
HEIGHT = TERM.height
WIDTH = TERM.width
CLEAR = TERM.clear
CENTER = TERM.center
DOWN = TERM.move_down
UP = TERM.move_up
XY = TERM.move_xy
X = TERM.move_x
LEFT = TERM.move_right
