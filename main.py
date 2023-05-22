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
    test_started = False
    pressed_wrong_key = False
    start_time = 0.0
    time_elapsed = 0.0
    test_string = "the quick brown fox jumped over the lazy dog"
    # test_string2 = "the cat over there just took a pee in the plant my aunt gave me\n"
    # test_strings = [test_string, test_string2]
    print(term.home + term.clear)
    print(term.cyan(term.center("QUICK TEST")) + term.move_down(1))
    print(term.white_on_black("(1)") + term.move_down(2))
    print(term.white_on_black(test_string) + term.move_up(1))
    correct_pressed_keys = []
    incorrect_pressed_keys = []

    with term.raw(), term.hidden_cursor():
        while True:
        # for index in range(len(test_string)):
            if test_started == False:
                start_time = time.time()
                test_started = True
            pressed_key = term.inkey()
            if len(correct_pressed_keys) >= len(test_string):
                time_elapsed = max(time.time() - start_time, 1)
                wpm = round((len(test_string) / (time_elapsed / 60)) / 5)
                wpm_string = str(wpm) + ' words per minute\n'
                total_characters = len(test_string)
                mistyped_characters = len(incorrect_pressed_keys)
                correct_characters = total_characters - mistyped_characters
                accuracy = round(correct_characters / total_characters * 100, 2)
                accuracy_string = str(accuracy) + '% Accuracy\n'
                print(term.home + term.clear + term.move_y(term.height // 2))
                print(term.black_on_green(term.center('Test Complete\n')))
                print(term.black_on_green(term.center(accuracy_string)))
                print(term.black_on_green(term.center(wpm_string)))
                return

            if pressed_key == '\x03':
                exit()

            target_character = test_string[len(correct_pressed_keys)]
            if pressed_key == target_character:

                if pressed_wrong_key == False:
                    print(term.green(pressed_key) + term.move_up(1))

                if pressed_wrong_key == True:
                    if pressed_key == ' ':
                        print(term.red_on_red('x') + term.move_up(1))
                    else:
                        print(term.red(pressed_key) + term.move_up(1))

                correct_pressed_keys.append(pressed_key)
                pressed_wrong_key = False


            else:
                pressed_wrong_key = True
                incorrect_pressed_keys.append(pressed_key)


def run_selection(selection, menu):
    dir = f"lessons/{menu[selection]['directory']}"
    title_file = f"{dir}/title"
    with open(title_file, 'r') as f:
        banner_title = f.read()
        display_menu_screen(banner_title, selection, menu)
        time.sleep(1)
        test()


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
