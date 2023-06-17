from terminal_typing_tutor.tutor import print_lines
from terminal_typing_tutor.constants import (
    TERM,
    TSeries,
)

# global variables, used in many functions, all should point to the same variable
# only one series, lesson, and segment can be active at any time
series: TSeries
lesson: int
segment = 0


def inkey_test():
    with TERM.cbreak(), TERM.fullscreen(), TERM.raw():
        print(f"{TERM.home}{TERM.black_on_skyblue}{TERM.clear}")
        print("press 'q' to quit.")
        val = ''
        while val.lower() != 'q':
            val = TERM.inkey(timeout=3)
            tar = '\n'
            if val.name == 'KEY_ENTER' and tar == '\n':
                print('You hit enter')
            if not val:
               print("It sure is quiet in here ...")
            elif val.is_sequence:
               print("got sequence: {0}.".format((str(val), val.name, val.code)))
            elif val:
               print("got {0}.".format(val))
        print(f'bye!{TERM.normal}')

pl_test = """Dear Sirs:

I have just purchased a Heathkit H89 computer system and would
like to order two boxes of diskettes for it.  This system uses
5 1/4 inch, hard-sectored, ten-sector, single-sided, single-
density diskettes.

Enclosed is my check for $45.00.  Please rush this order, as I
can not use my system before they arrive.

Sincerely,

Mr. Smith"""

# print_lines(pl_test)
# key = TERM.inkey()
inkey_test()
