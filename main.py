#!/usr/bin/env python3

import time
from blessed import Terminal


term = Terminal()

MAIN_MENU = [
    {
        "title": "Series Q    Quick QWERTY course  (Q1 - Q5) ",
        "directory": "q",
    },
    {
        "title": "Series R    Long QWERTY course  (R1 - R14) ",
        "directory": "r",
    },
    {
        "title": "Series T    QWERTY touch typing  (T1 - T16)",
        "directory": "t",
    },
    {
        "title": "Series V    Yet more QWERTY  (V1 - V19)    ",
        "directory": "v",
    },
    {
        "title": "Series U    QWERTY Review  (U1 - U13)      ",
        "directory": "u",
    },
    {
        "title": "Series M    Typing drills  (M1 - M11)      ",
        "directory": "m",
    },
    {
        "title": "Series S    Speed drills  (S1 - S4)        ",
        "directory": "s",
    },
]


def display_menu_screen(menu_title, selection, menu):
    print(term.home + term.clear)
    print(term.cyan(term.center(menu_title)) + term.move_y(term.height // 2))

    for index, menu_item in enumerate(menu):
        if index == selection:
            print(term.black_on_cyan(term.center(menu_item["title"])))
            # print('{t.bold_red_reverse}{title}'.format(t=term, title=m[0]))
        else:
            print(term.center(menu_item["title"]))
            # print('{t.normal}{title}'.format(t=term, title=m[0]))

def test():
    test_string = "the quick brown fox jumped over the lazy dog"
    test_string2 = "the cat over there just took a pee in the plant my aunt gave me\n"
    test_strings = [test_string, test_string2]
    print(term.home + term.clear)
    print(term.cyan(term.center("QUICK TEST")) + term.move_down(1))
    print(term.white_on_black("(1)") + term.move_down(3))
    print(term.white_on_black(test_string) + term.move_up(2))
    keys_pressed = []
    with term.raw():
        for index in range(len(test_string)):
            pressed_key = term.inkey()
            if pressed_key == '\x03':
                exit()
            if pressed_key == test_string[index]:
                print(term.green(pressed_key) + term.move_up(1))
            else:
                print(term.red(pressed_key) + term.move_up(1))

        # print(term.cyan("b"))



def run_selection(selection, menu):
    dir = f"lessons/{menu[selection]['directory']}"
    title_file = f"{dir}/title"
    with open(title_file, 'r') as f:
        banner_title = f.read()
        display_menu_screen(banner_title, selection, menu)
        time.sleep(1)
        test()


# with term.cbreak(), term.hidden_cursor():
#     while True:
#         inp = term.inkey()
#         print(term.move_down(1) + 'You pressed ' + term.bold(repr(inp)))


def make_selection(menu):
    selection = 0
    # draws menu screen the first time
    display_menu_screen("Series selection menu", selection, menu)
    selection_inprogress = True
    with term.cbreak():
        while selection_inprogress:
            key = term.inkey()
            down_keys = ["KEY_DOWN", "KEY_TAB"]
            if key.name in down_keys or key == "j":
                selection += 1
            if key.name == "KEY_UP" or key == "k":
                selection -= 1
            if key.name == "KEY_ENTER":
                selection_inprogress = False

            selection = selection % len(menu)

            # needs to redraw menu screen every time selection is changed to highlight new selection
            display_menu_screen("Series selection menu", selection, menu)
    return selection


def main():
    with term.fullscreen():
        selection = make_selection(MAIN_MENU)

    run_selection(selection, MAIN_MENU)


main()
