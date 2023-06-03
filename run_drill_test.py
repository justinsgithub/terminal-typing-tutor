#!/usr/bin/env python3

from typing import Literal
import yaml
import json
import time

# from constants import MAIN_MENU, MAIN_MENU_TITLE
from blessed import Terminal

term = Terminal()


def file_content(file: str, parse: Literal["yaml", "json", "text"] = "text"):
    with open(file, "r") as f:
        if parse == "yaml":
            return yaml.unsafe_load(f)
        if parse == "json":
            return json.load(f)
        return f.read()


lesson_dir = f"./lessons/Q/1"
data_file = f"{lesson_dir}/data.yaml"
lesson_data = file_content(data_file, "yaml")
segments = lesson_data["segments"]
content = segments[11]["content"]


def end_drill(start_time, test_string, incorrect_pressed_keys):
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


def run_drill():
    drill_started = False
    pressed_wrong_key = False
    start_time = 0.0
    time_elapsed = 0.0
    test_string = content
    # test_string2 = "the cat over there just took a pee in the plant my aunt gave me\n"
    # test_strings = [test_string, test_string2]
    print(term.home + term.clear)
    with term.location():
        print(term.home + term.move_xy(0, term.height))
        info_str = "   Drill   "
        print(term.move_right(term.width - (len(info_str))) + term.black_on_white(info_str))
    print(term.cyan(term.center("QUICK TEST")) + term.move_down(1))
    print(term.white(term.center("(1)")) + term.move_down(2))
    print(test_string + term.move_up(2))
    for _ in test_string.split('\n'):
        print(term.move_up(2))
    print(term.move_down(1))
    correct_pressed_keys = []
    incorrect_pressed_keys = []
    drill_over = False

    # with term.raw(), term.hidden_cursor(): HIDDEN CURSOR OFF DURING DEBUGGING
    with term.raw():
        while not drill_over:
            pressed_key = term.inkey()
            # we want to start the timer after user starts test (after first key is pressed)
            if drill_started == False:
                start_time = time.time()
                drill_started = True
            # end drill after all characters are typed
            if len(correct_pressed_keys) == len(test_string) - 1:
                time_elapsed = max(time.time() - start_time, 1)
                wpm = round((len(test_string) / (time_elapsed / 60)) / 5)
                wpm_string = str(wpm) + " words per minute"
                total_characters = len(test_string)
                mistyped_characters = len(incorrect_pressed_keys)
                correct_characters = total_characters - mistyped_characters
                accuracy = round(correct_characters / total_characters * 100, 2)
                accuracy_string = str(accuracy) + "% Accuracy"
                # print(term.home + term.clear + term.move_y(term.height // 2))
                print(term.move_xy(0, round(term.height // 2)))
                # print(term.green_on_black(term.center("Drill Complete")))
                print(term.green_on_black(term.center(accuracy_string)))
                print(term.green_on_black(term.center(wpm_string)))
                print(term.home + term.move_xy(0, term.height - 1))
                print(term.black_on_white(" Press R to repeat, N for next exercise or E to exit "))
                # info_str = "   Stats   "
                # print(term.move_right(term.width - (len(info_str))) + term.black_on_white(info_str))
                return

            if pressed_key == "\x03":
                exit()

            target_character = test_string[len(correct_pressed_keys)]
            line_break = target_character == "\n"
            pressed_enter = pressed_key.name == "KEY_ENTER"
            pressed_space = pressed_key == " "
            hit_target1 = pressed_key == target_character
            hit_target2 = line_break and pressed_enter

            if hit_target1 or hit_target2:
                if pressed_wrong_key == False:
                    if pressed_enter:
                        # go to beginning of next line after line break
                        print(term.move_x(0))
                    else:
                        print(term.green(pressed_key) + term.move_up(1))

                if pressed_wrong_key == True:
                    if pressed_space:
                        print(term.red_on_red("x") + term.move_up(1))
                    elif pressed_enter:
                        # may not want term.move_down here
                        print(term.red_on_red("x") + term.move_down(1) + term.move_x(0))
                    else:
                        print(term.red(pressed_key) + term.move_up(1))

                correct_pressed_keys.append(pressed_key)
                pressed_wrong_key = False

            else:
                pressed_wrong_key = True
                incorrect_pressed_keys.append(pressed_key)


run_drill()
