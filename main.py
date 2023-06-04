#!/usr/bin/env python3

from typing import List, Literal
from blessed.keyboard import Keystroke
import yaml
import json
import time
from constants import MAIN_MENU, MAIN_MENU_TITLE
from blessed import Terminal

term = Terminal()
home = term.home
height = term.height
width = term.width
clear = term.clear
center = term.center
down = term.move_down
up = term.move_up
xy = term.move_xy
x = term.move_x
y = term.move_y
right = term.move_right

TSeries = Literal["M", "Q", "R", "S", "T", "U", "V"]

def file_content(file: str, parse: Literal["yaml", "json", "text"] = "text"):
    with open(file, "r") as f:
        if parse == "yaml":
            return yaml.unsafe_load(f)
        if parse == "json":
            return json.load(f)
        return f.read()


def end_drill(start_time: float, test_string: str, incorrect_pressed_keys: List[str]):
    action = ''
    confirm_exit = False
    time_elapsed = max(time.time() - start_time, 1)
    wpm = round((len(test_string) / (time_elapsed / 60)) / 5)
    wpm_string = str(wpm) + " words per minute"
    total_characters = len(test_string)
    mistyped_characters = len(incorrect_pressed_keys)
    correct_characters = total_characters - mistyped_characters
    accuracy = round(correct_characters / total_characters * 100, 2)
    accuracy_string = str(accuracy) + "% Accuracy"
    # print(home + clear + term.move_y(height // 2))
    print(xy(0, round(height // 2)))
    # print(term.green_on_black(center("Drill Complete")))
    print(term.green_on_black(center(accuracy_string)))
    print(term.green_on_black(center(wpm_string)))
    print(home + xy(0, height), end='', flush=True)
    print(term.black_on_white(" Press R to repeat, N for next exercise or E to exit "))

    while action == '':
        # exit program if user hits ctrl + c
        keystroke = term.inkey()
        if keystroke == "\x03":
            exit()
        if keystroke.lower() == 'r':
            action = 'repeat'
        if keystroke.lower() == 'n':
            action = 'next'
        if keystroke.lower() == 'e':
            print(home + xy(0, height), end='', flush=True)
            print(term.black_on_white(" Are you sure you want to exit this lesson? [Y/N] "))
            action = 'menu'

    return action
        # info_str = "   Stats   "
        # print(right(width - (len(info_str))) + term.black_on_white(info_str))


def pressed_key(keystroke: Keystroke, test_string: str, correct_pressed_keys: List[str]):
    # exit program if user hits ctrl + c
    if keystroke == "\x03":
        exit()
    target_character = test_string[len(correct_pressed_keys)]
    line_break = target_character == "\n"
    pressed_enter = keystroke.name == "KEY_ENTER"
    pressed_space = keystroke == " "
    if (keystroke == target_character) or (line_break and pressed_enter):
        return {"pressed_enter": pressed_enter, "pressed_space": pressed_space, "hit_target": True}
    return {"pressed_enter": pressed_enter, "pressed_space": pressed_space, "hit_target": False}


def run_drill(content: str) -> Literal['next', 'repeat', 'menu']:
    action = 'next'
    drill_started = False
    pressed_wrong_key = False
    start_time = 0.0
    test_string = content
    print(home + clear)
    with term.location():
        print(home + xy(0, height), end='', flush=True)
        info_str = "   Drill   "
        print(right(width - (len(info_str))) + term.black_on_white(info_str), end='', flush=True)
    # TODO: fix down/move_up with end=''
    print(term.cyan(center("QUICK TEST")) + down(1))
    print(term.white(center("(1)")) + down(2))
    print(test_string + up(2))
    for _ in test_string.split("\n"):
        print(up(2))
    print(down(1))
    correct_pressed_keys = []
    incorrect_pressed_keys = []
    drill_over = False

    # with term.raw(), term.hidden_cursor(): HIDDEN CURSOR OFF DURING DEVELOPMENT
    with term.raw():
        while not drill_over:
            # first check to see if all characters typed, end drill
            if len(correct_pressed_keys) == len(test_string) - 1:
                action = end_drill(start_time, test_string, incorrect_pressed_keys)
                drill_over = True

            keystroke = term.inkey()

            # Set the start time on first key press
            if drill_started == False:
                start_time = time.time()
                drill_started = True

            if keystroke.name == 'KEY_ESCAPE':
                return 'repeat' # start test over

            _pressed_key = pressed_key(keystroke, test_string, correct_pressed_keys)

            if _pressed_key["hit_target"]:
                if pressed_wrong_key == False:
                    if not _pressed_key["pressed_enter"]:
                         print(term.green(keystroke), end='', flush=True)
                    # if _pressed_key["pressed_enter"]:
                    #     # go to beginning of next line after line break
                    #     print(x(0))
                    # else:
                    #     print(term.green(keystroke))

                if pressed_wrong_key == True:
                    if _pressed_key["pressed_space"]:
                        print(term.red_on_red("x"), end='', flush=True)
                    elif _pressed_key["pressed_enter"]:
                        # may not want down here
                        print(term.red_on_red("x"))
                    else:
                        print(term.red(keystroke), end='', flush=True)

                correct_pressed_keys.append(keystroke)
                pressed_wrong_key = False

            else:
                pressed_wrong_key = True
                incorrect_pressed_keys.append(keystroke)
    return action


def display_menu_screen(menu_title, selection, menu):
    print(home + clear)
    print(term.cyan(center(menu_title)) + term.move_y(height // 2))

    for index, menu_item in enumerate(menu):
        if index == selection:
            print(term.black_on_cyan(center(menu_item["title"])))
        else:
            print(center(menu_item["title"]))


def menu_selection(menu_title, menu) -> int:
    selection = 0
    # draws menu screen the first time
    display_menu_screen(menu_title, selection, menu)
    selection_inprogress = True
    with term.cbreak():
        while selection_inprogress:
            key = term.inkey()
            if key.name == 'KEY_ESCAPE':
                pass
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
    return lesson_selected


def run_series_menu() -> TSeries:
    with term.fullscreen(), term.hidden_cursor():
        selection = menu_selection(MAIN_MENU_TITLE, MAIN_MENU)

    series_selected = MAIN_MENU[selection]["series"]
    return series_selected


def display_info_screen(banner_title: str, intro: str, content: str):
    display_info = True
    action = "next"
    print(home + clear)
    print(term.black_on_cyan(center(banner_title)) + down(1))
    for line in intro.split("\n"):
        print(center(line))
    for line in content.split("\n"):
        even_line = line
        while len(even_line) < 80:
            even_line += " "
        print(center(even_line))
    print(home + xy(0, height), end='', flush=True)
    print(term.black_on_white(" Press RETURN or SPACE to continue, ESC to return to the menu ") + x(0), end='', flush=True)
    info_str = " Info "
    print(right(width - len(info_str)) + term.black_on_white(info_str), end='', flush=True)
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
        action = ''

        if type == "info":
            action = display_info_screen(title, intro, content)
        else:
            action == run_drill(content)

        if action == "next":
            current += 1 # if next go to next segment
        if action == "repeat":
            continue # if repeat run_drill again with same segment
        if action == "menu":
            show_menu = True
            break


    return show_menu


def main():
    series_selected = run_series_menu()
    show_menu = True
    while show_menu:
        show_menu = run_lesson(series_selected)

main()
