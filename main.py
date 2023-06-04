#!/usr/bin/env python3

from typing import List, Literal
from blessed.keyboard import Keystroke
import yaml
import json
import time
from constants import MAIN_MENU, MAIN_MENU_TITLE, TERM, HOME, HEIGHT, WIDTH, CLEAR, CENTER, DOWN, UP, XY, X, LEFT

TSeries = Literal["M", "Q", "R", "S", "T", "U", "V"]


def file_content(file: str, parse: Literal["yaml", "json", "text"] = "text"):
    with open(file, "r") as f:
        if parse == "yaml":
            return yaml.unsafe_load(f)
        if parse == "json":
            return json.load(f)
        return f.read()


def end_drill(start_time: float, test_string: str, incorrect_pressed_keys: List[str]):
    confirming_exit = False
    if not start_time == 0.0: # only print stats if drill was started
        time_elapsed = max(time.time() - start_time, 1)
        wpm = round((len(test_string) / (time_elapsed / 60)) / 5)
        wpm_string = TERM.cyan_on_black(str(wpm)) + TERM.white_on_black(" words per minute")
        total_characters = len(test_string)
        mistyped_characters = len(incorrect_pressed_keys)
        correct_characters = total_characters - mistyped_characters
        accuracy = round(correct_characters / total_characters * 100, 2)
        accuracy_string = TERM.cyan_on_black(str(accuracy) + "%") + TERM.white_on_black(" Accuracy")
        print(XY(0, round(HEIGHT // 2)))
        print(CENTER(accuracy_string))
        print(CENTER(wpm_string))

    print(HOME + XY(0, HEIGHT), end="", flush=True)
    print(TERM.black_on_white(" Press R to repeat, N for next exercise or E to exit "), end="", flush=True)

    while True:
        # exit program if user hits ctrl + c
        keystroke = TERM.inkey()
        if keystroke == "\x03":
            exit()
        if keystroke.lower() == "r":
            return "repeat"
        if keystroke.lower() == "n" and not confirming_exit:
            return "next"
        if keystroke.lower() == "e":
            print(HOME + XY(0, HEIGHT), end="", flush=True)
            print(TERM.black_on_white(" Are you sure you want to exit this lesson? [Y/N]     "), end="", flush=True)
            confirming_exit = True
        if keystroke.lower() == "y" and confirming_exit:
            return "menu"
        if keystroke.lower() == "n" and confirming_exit:
            print(HOME + XY(0, HEIGHT), end="", flush=True)
            print(TERM.black_on_white(" Press R to repeat, N for next exercise or E to exit "), end="", flush=True)
            confirming_exit = False


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


def run_drill(content: str):
    drill_started = False
    pressed_wrong_key = False
    start_time = 0.0
    test_string = content
    print(HOME + CLEAR)
    with TERM.location():
        print(HOME + XY(0, HEIGHT), end="", flush=True)
        info_str = "   Drill   "
        print(LEFT(WIDTH - (len(info_str))) + TERM.black_on_white(info_str), end="", flush=True)
    # TODO: fix down/move_up with end=''
    print(TERM.cyan(CENTER("QUICK TEST")) + DOWN(1))
    print(TERM.white(CENTER("(1)")) + DOWN(2))
    print(test_string + UP(2))
    for _ in test_string.split("\n"):
        print(UP(2))
    print(DOWN(1))
    correct_pressed_keys = []
    incorrect_pressed_keys = []

    with TERM.raw():
        while True:
            # first check to see if all characters typed, end drill
            if len(correct_pressed_keys) == len(test_string):
                action = end_drill(start_time, test_string, incorrect_pressed_keys)
                return action

            keystroke = TERM.inkey()

            if keystroke.name == "KEY_ESCAPE":
                # start test over if in middle of test, else confirm exit
                if drill_started:
                    return "repeat"
                else:
                    action = end_drill(start_time, test_string, incorrect_pressed_keys)
                    return action


            _pressed_key = pressed_key(keystroke, test_string, correct_pressed_keys)

            # Set the start time on first key press
            if drill_started == False:
                start_time = time.time()
                drill_started = True

            if _pressed_key["hit_target"]:
                if pressed_wrong_key == False:
                    if not _pressed_key["pressed_enter"]:
                        print(TERM.green(keystroke), end="", flush=True)
                    else:
                        print(TERM.green(keystroke))

                if pressed_wrong_key == True:
                    if _pressed_key["pressed_space"]:
                        print(TERM.red_on_red("x"), end="", flush=True)
                    elif _pressed_key["pressed_enter"]:
                        # may not want down here
                        print(TERM.red_on_red("x"))
                    else:
                        print(TERM.red(keystroke), end="", flush=True)

                correct_pressed_keys.append(keystroke)
                pressed_wrong_key = False

            else:
                pressed_wrong_key = True
                incorrect_pressed_keys.append(keystroke)


def display_menu_screen(menu_title, selection, menu):
    print(HOME + CLEAR)
    print(TERM.cyan(CENTER(menu_title)) + TERM.move_y(HEIGHT // 2))

    for index, menu_item in enumerate(menu):
        if index == selection:
            print(TERM.black_on_cyan(CENTER(menu_item["title"])))
        else:
            print(CENTER(menu_item["title"]))


def menu_selection(menu_title, menu) -> int:
    selection = 0
    # draws menu screen the first time
    display_menu_screen(menu_title, selection, menu)
    selection_inprogress = True
    while selection_inprogress:
        key = TERM.inkey()
        if key.name == "KEY_ESCAPE":
            return -1
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
    selection = menu_selection(MAIN_MENU_TITLE, MAIN_MENU)
    if selection == -1:
        exit()
    series_selected = MAIN_MENU[selection]["series"]
    return series_selected


def display_info_screen(banner_title: str, intro: str, content: str):
    display_info = True
    action = "next"
    print(HOME + CLEAR)
    print(TERM.black_on_cyan(CENTER(banner_title)) + DOWN(1))
    for line in intro.split("\n"):
        print(CENTER(line))
    for line in content.split("\n"):
        even_line = line
        while len(even_line) < 80:
            even_line += " "
        print(CENTER(even_line))
    print(HOME + XY(0, HEIGHT), end="", flush=True)
    print(
        TERM.black_on_white(" Press RETURN or SPACE to continue, ESC to return to the menu ") + X(0), end="", flush=True
    )
    info_str = " Info "
    print(LEFT(WIDTH - len(info_str)) + TERM.black_on_white(info_str), end="", flush=True)
    while display_info:
        key = TERM.inkey()
        if key.name == "KEY_ESCAPE":
            action = "menu"
            display_info = False
        if key.name == "KEY_ENTER" or key == " ":
            display_info = False

    return action


def run_lesson(series_selected: TSeries):
    lesson_selected = run_lesson_menu(series_selected)
    if lesson_selected == 0:
        return 0
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
        action = ""

        if type == "info":
            action = display_info_screen(title, intro, content)
        else:
            action = run_drill(content)

        if action == "next":
            current += 1  # if next go to next segment
        if action == "repeat":
            continue  # if repeat run_drill again with same segment
        if action == "menu":
            show_menu = True
            break

    if show_menu == False:
        return 1

    return 2


def main():
    # with TERM.fullscreen(), TERM.hidden_cursor():
    with TERM.fullscreen(), TERM.cbreak():  # hidden cursor off during development
        num = 0
        series_selected = 0
        while True:
            if num == 0:
                series_selected = run_series_menu()
                num = run_lesson(series_selected)
            if num == 1:
                exit()
            if num == 2:
                num = run_lesson(series_selected)

main()
