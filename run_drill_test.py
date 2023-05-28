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
total_segments = lesson_data["total_segments"]
segments = lesson_data["segments"]
content = segments[5]["content"]


def run_drill():
    test_started = False
    pressed_wrong_key = False
    start_time = 0.0
    time_elapsed = 0.0
    test_string = content
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



run_drill()
