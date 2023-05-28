#!/usr/bin/env python3

from typing import Literal
import yaml
import json
import time
from constants import MAIN_MENU, MAIN_MENU_TITLE
from blessed import Terminal

term = Terminal()

TSeries = Literal["M", "Q", "R", "S", "T", "U", "V"]


def file_content(file: str, parse: Literal["yaml", "json", "text"] = "text"):
    with open(file, "r") as f:
        if parse == "yaml":
            return yaml.unsafe_load(f)
        if parse == "json":
            return json.load(f)
        return f.read()


def run_drill(content: str):
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
            pressed_key = term.inkey()
            if test_started == False:
                start_time = time.time()
                test_started = True
            if len(correct_pressed_keys) >= len(test_string):
                time_elapsed = max(time.time() - start_time, 1)
                wpm = round((len(test_string) / (time_elapsed / 60)) / 5)
                wpm_string = str(wpm) + " words per minute\n"
                total_characters = len(test_string)
                mistyped_characters = len(incorrect_pressed_keys)
                correct_characters = total_characters - mistyped_characters
                accuracy = round(correct_characters / total_characters * 100, 2)
                accuracy_string = str(accuracy) + "% Accuracy\n"
                print(term.home + term.clear + term.move_y(term.height // 2))
                print(term.black_on_green(term.center("Test Complete\n")))
                print(term.black_on_green(term.center(accuracy_string)))
                print(term.black_on_green(term.center(wpm_string)))
                return

            if pressed_key == "\x03":
                exit()

            target_character = test_string[len(correct_pressed_keys)]
            if pressed_key == target_character:
                if pressed_wrong_key == False:
                    print(term.green(pressed_key) + term.move_up(1))

                if pressed_wrong_key == True:
                    if pressed_key == " ":
                        print(term.red_on_red("x") + term.move_up(1))
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
    menu = file_content(menu_file, "json")
    menu_title = file_content(title_file)

    # lessons start at 1 not 0
    lesson_selected = menu_selection(menu_title, menu) + 1
    # lesson_selected = menu[selection]['lesson']
    # return lesson_selected
    return lesson_selected

    # display_menu_screen(menu_title, lesson_selection, menu)
    # test()


def run_series_menu() -> TSeries:
    with term.fullscreen(), term.hidden_cursor():
        selection = menu_selection(MAIN_MENU_TITLE, MAIN_MENU)

    series_selected = MAIN_MENU[selection]["series"]
    return series_selected


def display_info_screen(banner_title: str, intro: str, content: str):
    display_info = True
    action = "next"
    print(term.home + term.clear)
    print(term.black_on_cyan(term.center(banner_title)) + term.move_down(1))
    for line in intro.split("\n"):
        print(term.center(line))
    for line in content.split("\n"):
        even_line = line
        while len(even_line) < 80:
            even_line += " "
        print(term.center(even_line))
    print(term.home + term.move_xy(0, term.height - 1))
    print(term.black_on_white(" Press RETURN or SPACE to continue, ESC to return to the menu ") + term.move_up(1))
    info_str = " Info "
    print(term.move_right(term.width - len(info_str)) + term.black_on_white(info_str) + term.move_up(1))
    with term.cbreak():
        while display_info:
            key = term.inkey()
            if key.name == "KEY_ESCAPE":
                action = "menu"
                display_info = False
            if key.name == "KEY_ENTER" or key == " ":
                display_info = False

    return action


def run_lesson(series_selected: TSeries):
    lesson_selected = run_lesson_menu(series_selected)
    lesson_dir = f"lessons/{series_selected}/{str(lesson_selected)}"
    show_menu = False
    data_file = f"{lesson_dir}/data.yaml"
    lesson_data = file_content(data_file, "yaml")
    total_segments = lesson_data["total_segments"]
    segments = lesson_data["segments"]

    current = 0

    while current < total_segments:
        current_seg = segments[current]
        intro = current_seg["intro"]
        content = current_seg["content"]
        title = f"Lesson {series_selected}{str(lesson_selected)}"
        type = current_seg["type"]

        if type == 'info':
            action = display_info_screen(title, intro, content)
        else:
            action == run_drill()

        if action == "next":
            current += 1
        if action == "menu":
            show_menu = True
            break

    return show_menu


def main():
    series_selected = run_series_menu()
    show_menu = True
    while show_menu:
        show_menu = run_lesson(series_selected)
        # test()


main()
