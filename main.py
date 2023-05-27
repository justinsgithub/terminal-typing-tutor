#!/usr/bin/env python3

import json
import time
from blessed import Terminal

term = Terminal()

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

def display_menu_screen(menu_title, selection, menu):
    print(term.home + term.clear)
    print(term.cyan(term.center(menu_title)) + term.move_y(term.height // 2))

    for index, menu_item in enumerate(menu):
        if index == selection:
            print(term.black_on_cyan(term.center(menu_item["title"])))
        else:
            print(term.center(menu_item["title"]))

# def get_lesson_selection(selection, menu):
#     dir = f"lessons/{menu[selection]['directory']}"
#     title_file = f"{dir}/title"
#     with open(title_file, 'r') as f:
#         banner_title = f.read()
#         display_menu_screen(banner_title, selection, menu)
#         test()

def menu_selection(menu_title, menu) -> int:
    selection = 0
    # draws menu screen the first time
    display_menu_screen(menu_title, selection, menu)
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
            display_menu_screen(menu_title, selection, menu)
    return selection

def run_lesson_menu(series_name) -> int:
    dir = f"lessons/{series_name}"
    title_file = f"{dir}/title"
    menu_file = f"{dir}/menu.json"
    print(menu_file)
    with open(menu_file, 'r') as f:
        menu = json.load(f)
        # print(menu)
        # print(json.dumps(menu))
    with open(title_file, 'r') as f:
        menu_title = f.read()

    # lessons start at 1 not 0
    lesson_selected = menu_selection(menu_title, menu) + 1
    # lesson_selected = menu[selection]['lesson']
    # return lesson_selected
    return lesson_selected

    # display_menu_screen(menu_title, lesson_selection, menu)
    # test()

def run_series_menu() -> int:
    with term.fullscreen(), term.hidden_cursor():
        selection = menu_selection(MAIN_MENU_TITLE, MAIN_MENU)

    return selection

def display_info_screen(banner_title, content):
    display_info = True
    action = 'next'
    print(term.home + term.clear)
    print(term.black_on_cyan(term.center(banner_title)))
    for line in content.split('\n'):
        even_line = line
        while len(even_line) < 80:
            even_line += ' '
        print(term.center(even_line))
    print(term.home + term.move_xy(0, term.height - 1))
    print(term.black_on_white(" Press RETURN or SPACE to continue, ESC to return to the menu ") + term.move_up(1))
    info_str = ' Info '
    print(term.move_right(term.width - len(info_str)) + term.black_on_white(info_str) + term.move_up(1))
    with term.cbreak():
        while display_info:
            key = term.inkey()
            if key.name == "KEY_ESCAPE":
                action = 'menu'
                display_info = False
            if key.name == "KEY_ENTER" or key == ' ':
                display_info = False

    return action


def run_lesson(lesson_dir):
    show_menu = False
    data_file = f"{lesson_dir}/data.json"
    with open(data_file, 'r') as f:
        lesson_data = json.load(f)

    current = 0

    # while True:
    while current < len(lesson_data):
        data = lesson_data[current]
        filename = str(current + 1)
        file = f"{lesson_dir}/{filename}"
        with open(file, 'r') as f:
            content = f.read()

        action = display_info_screen('blah', content)
        if action == 'next':
            current += 1
        if action == 'menu':
            show_menu = True
            break

    return show_menu

def main():
    series_selected = run_series_menu()
    series_name = MAIN_MENU[series_selected]['series']
    show_menu = True
    while show_menu:
        lesson_selected = run_lesson_menu(series_name)
        lesson_dir = f"lessons/{series_name}/{str(lesson_selected)}"
        show_menu = run_lesson(lesson_dir)
        # test()

main()
