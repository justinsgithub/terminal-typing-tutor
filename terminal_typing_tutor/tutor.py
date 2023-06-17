from typing import List, Literal, cast
from pathlib import Path
from datetime import date
from blessed.keyboard import Keystroke
from urllib import request
import yaml
import json
import time
import os
from terminal_typing_tutor.constants import (
    MAIN_MENU,
    MAIN_MENU_TITLE,
    RIGHT,
    STATS_DICT,
    TERM,
    HOME,
    HEIGHT,
    WIDTH,
    CLEAR,
    CENTER,
    DOWN,
    UP,
    XY,
    X,
    LEFT,
    PB_DICT,
    MIN_PB_CHARS,
    TSeries,
    TStats,
    TStatsFile,
    CURRENT_VERSION
)

# global variables, used in many functions, all should point to the same variable
# only one series, lesson, and segment can be active at any time
series: TSeries
lesson: int
segment = 0

"""
TODOS: 
- track total time spent practicing typing
- track dates to monitor progress over time 
  - implement by creating a directory for pbs and each drill instead of a file
  - create a new file each time a new record is achieved, the file name will be some format of date and time
"""

# stats for current drill
# want to track best words per minute, chars per minute, accuracy, most characters and words typed in a drill
current_wpm: int
current_cpm: int
current_acc: float
current_chars: int
current_words: int

# wrapper for TERM.inkey, so that anytime user hits Ctrl + C, exits app
# TERM.raw so that no ugly error is thrown on screen
def get_key():
    with TERM.raw():
        key = TERM.inkey()
        if key == "\x03":
            exit()
        return key


def file_content(file: Path, parse: Literal["yaml", "json", "text"] = "text") -> str | TStatsFile:
    with open(file, "r") as f:
        if parse == "yaml":
            return yaml.unsafe_load(f)
        if parse == "json":
            return json.load(f)
        return f.read()


def get_stats():
    # make sure stats files exist, create them if not
    home_dir = os.path.expanduser("~")
    pb_dir = f"{home_dir}/.config/terminal-typing-tutor/pb/{series}/{lesson}"
    pb_fp = f"{pb_dir}/{segment}.yaml"
    all_time_fp = f"{home_dir}/.config/terminal-typing-tutor/pb.yaml"
    pb_file = Path(pb_fp)
    all_time_file = Path(all_time_fp)
    if not os.path.exists(pb_dir):
        os.makedirs(pb_dir)
    if not os.path.exists(pb_file):
        with open(pb_file, "w") as file:
            file.write(yaml.safe_dump(STATS_DICT))
    if not os.path.exists(all_time_file):
        with open(all_time_file, "w") as file:
            file.write(yaml.safe_dump(PB_DICT))

    # get stats from files
    all_time_pbs: TStatsFile = cast(TStatsFile, file_content(all_time_file, "yaml"))
    at = all_time_pbs["all_time"]
    drill_pbs: TStats = cast(TStats, file_content(pb_file, "yaml"))
    # return personal best wpm for current drill, and all time best accuracy, wpm, etc...
    return {
        "pb_file": pb_file,
        "all_time_file": all_time_file,
        "drill_pbs": drill_pbs,
        "at": at,
    }


# track users personal bests (pb)
def track_pb():
    global current_wpm, current_acc, current_chars, current_words, current_cpm
    stats = get_stats()
    # check if user beat previous wpm for this drill, or any all time pbs, write new stats to file
    prev_drill_pb = stats["drill_pbs"]["wpm"]
    pb_file = stats["pb_file"]
    at_file = stats["all_time_file"]
    at: TStats = cast(TStats, stats["at"])

    new_stats: TStats = {
        "accuracy": current_acc,
        "wpm": current_wpm,
        "cpm": current_cpm,
        "words": current_words,
        "characters": current_chars,
    }
    new_drill_pb = current_wpm > prev_drill_pb
    if new_drill_pb:
        with open(pb_file, "w") as file:
            file.write(yaml.safe_dump(new_stats))

    new_pb: TStatsFile = {
        "all_time": at
    }

    # only track if drill is min length of characters, (new wpm or accuracy pb should have a minimum test length, the longer the test the more impressive)
    new_wpm = current_wpm > at["wpm"] and current_chars > MIN_PB_CHARS

    if new_wpm:
        new_pb["all_time"] = new_stats

    # only write to file if a new record has been achieved
    if new_wpm:
        with open(at_file, "w") as file:
            file.write(yaml.safe_dump(new_pb))

    return {
        "new_drill_pb": new_drill_pb,
        "new_wpm": new_wpm,
    }


def end_drill(start_time: float, test_string: str, incorrect_pressed_keys: List[str]):
    confirming_exit = False
    failed_drill = False
    end_msg = " Press R to repeat, N for next exercise or E to exit " 
    global current_wpm, current_acc, current_chars, current_words, current_cpm
    if not start_time == 0.0:  # only print stats if drill was started
        time_elapsed = max(time.time() - start_time, 1)
        minutes = time_elapsed / 60
        current_chars = len(test_string)
        mistyped_characters = len(incorrect_pressed_keys)
        correct_characters = current_chars - mistyped_characters
        current_words = round(current_chars / 5)
        current_cpm = round(current_chars / minutes)
        current_wpm = round(current_words / minutes)
        current_acc = round(correct_characters / current_chars * 100, 2)
        wpm_string = f" {TERM.cyan_on_black(str(current_wpm)) + TERM.white_on_black( ' Words Per Minute ')}"
        accuracy_string = f" {TERM.cyan_on_black( str(current_acc) + '%') + TERM.white_on_black(' Accuracy ')}"
        words_string = f" {TERM.cyan_on_black(str(current_words)) + TERM.white_on_black( ' Words Typed ')}"
        if current_acc < 97.00:
            failed_drill = True
            end_msg = " Accuracy not high enough, must hit at least 97% "
        else:
            pbs = track_pb()
            if pbs["new_wpm"]:
                wpm_string += TERM.red_on_black("NEW ALL TIME PB ")
            elif pbs["new_drill_pb"]:
                wpm_string += TERM.red_on_black("NEW DRILL PB ")

        print(XY(0, round(HEIGHT // 3)))
        print(f"{CENTER(wpm_string)}\n")
        print(f"{CENTER(accuracy_string)}\n")
        print(CENTER(words_string))

    # reset stats after they are tracked and displayed
    current_wpm = 0
    current_cpm = 0
    current_acc = 0
    current_words = 0
    current_chars = 0

    print(HOME + XY(0, HEIGHT), end="", flush=True)
    print(TERM.black_on_white(end_msg), end="", flush=True)

    while True:
        # exit program if user hits ctrl + c
        key = get_key()
        if failed_drill:
            if key.name in ["KEY_ESCAPE", "KEY_ENTER"] or key == " ":
                return "repeat"
        else:
            if key.lower() == "r":
                return "repeat"
            if key.lower() == "n" and not confirming_exit:
                return "next"
            if key.lower() == "e":
                print(HOME + XY(0, HEIGHT), end="", flush=True)
                print( TERM.black_on_white( " Are you sure you want to exit this lesson? [Y/N]     "), end="", flush=True,)
                confirming_exit = True
            if key.lower() == "y" and confirming_exit:
                return "menu"
            if key.lower() == "n" and confirming_exit:
                print(HOME + XY(0, HEIGHT), end="", flush=True)
                print( TERM.black_on_white( " Press R to repeat, N for next exercise or E to exit "), end="", flush=True,)
                confirming_exit = False


def pressed_info(key: Keystroke, target_char: str):
    pressed_space = key == ' '
    pressed_enter = key.name == 'KEY_ENTER' 
    hit_target = key == target_char or (pressed_enter and target_char == '\n') 

    return {
            "pressed_enter": pressed_enter,
            "pressed_space": pressed_space,
            "hit_target": hit_target,
            }

def print_lines(test_string: str) -> int:
    lines = test_string.split("\n")
    line_count = len(lines)
    longest_line = lines[0]
    for line in lines:
        if len(line) > len(longest_line):
            longest_line = line
    extra_width = WIDTH - len(longest_line)
    left_padding = extra_width // 2
    for index, line in enumerate(lines):
        if index == line_count - 1:
            print(f"{RIGHT(left_padding)}{line}", end="", flush=True)
        else:
            print(f"{RIGHT(left_padding)}{line}\n", end="", flush=True)
    if line_count > 1:
        print(UP(line_count))
    print(X(left_padding), end="", flush=True)
    
    return left_padding

def run_drill(title: str, intro: str, content: str):
    drill_started = False
    pressed_wrong_key = False
    start_time = 0.0
    test_string = content.rstrip()
    print(HOME + CLEAR, end="", flush=True)
    with TERM.location():
        print(HOME + XY(0, HEIGHT), end="", flush=True)
        info_str = "   Drill   "
        print(RIGHT(WIDTH - (len(info_str))) + TERM.black_on_white(info_str), end="", flush=True)
    # TODO: fix down/move_up with end=''
    print(TERM.black_on_cyan(CENTER(title)) + DOWN(1))
    print(TERM.white(CENTER(intro)) + DOWN(2))
    left_padding = print_lines(test_string)
    correct_pressed_keys = []
    incorrect_pressed_keys = []

    while True:
        # first check to see if all characters typed, end drill
        if len(correct_pressed_keys) == len(test_string):
            action = end_drill(start_time, test_string, incorrect_pressed_keys)
            return action

        target_character = test_string[len(correct_pressed_keys)]
        if target_character == '\n':
            print(f"{TERM.white_on_white('x')}{LEFT(1)}", end="", flush=True)
        else:
            print(f"{TERM.black_on_white(target_character)}{LEFT(1)}", end="", flush=True)
        key = get_key()

        if key.name == "KEY_ESCAPE":
            # start test over if in middle of test, else confirm exit
            if drill_started:
                return "repeat"
            else:
                action = end_drill(0.0, test_string, incorrect_pressed_keys)
                return action

        pressed_key = pressed_info(key, target_character)

        # Set the start time on first key press
        if drill_started == False:
            start_time = time.time()
            drill_started = True

        if pressed_key["hit_target"]:
            if pressed_wrong_key == False:
                if pressed_key["pressed_enter"]:
                    print(f" \n{X(left_padding)}", end="", flush=True)
                else:
                    print(TERM.green(key), end="", flush=True)

            if pressed_wrong_key == True:
                if pressed_key["pressed_space"]:
                    print(TERM.red_on_red("x"), end="", flush=True)
                elif pressed_key["pressed_enter"]:
                    # may not want down here
                    print(f"{TERM.red_on_red('x')}\n{X(left_padding)}", end="", flush=True)
                else:
                    print(TERM.red(key), end="", flush=True)

            correct_pressed_keys.append(key)
            pressed_wrong_key = False

        else:
            # if user mistypes A, we only want to track it first time, do not penalize for missing same character twice
            if pressed_wrong_key == False:
                incorrect_pressed_keys.append(key)
            # if they did not hit target, we want to set True
            pressed_wrong_key = True


def display_menu_screen(menu_title: str, selection, menu):
    print(HOME + CLEAR, end="", flush=True)
    print(TERM.black_on_cyan(CENTER(menu_title.strip())) + DOWN(1))
    print(TERM.move_y(HEIGHT // 3))

    for index, menu_item in enumerate(menu):
        if index == selection:
            print(TERM.black_on_white(CENTER(menu_item["title"])))
        else:
            print(CENTER(menu_item["title"]))


def menu_selection(menu_title, menu) -> int:
    selection = 0
    # draws menu screen the first time
    display_menu_screen(menu_title, selection, menu)
    selection_inprogress = True
    while selection_inprogress:
        key = get_key()
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


def run_lesson_menu():
    global lesson
    dir = f"series/{series}"
    title_fp = f"{dir}/title"
    menu_fp = f"{dir}/menu.json"
    title_file = Path(__file__).parent.joinpath(title_fp)
    menu_file = Path(__file__).parent.joinpath(menu_fp)
    menu = file_content(menu_file, "json")
    menu_title = file_content(title_file)

    # lessons start at 1 not 0
    lesson = menu_selection(menu_title, menu) + 1


def run_series_menu():
    global series
    selection = menu_selection(MAIN_MENU_TITLE, MAIN_MENU)
    if selection == -1:
        exit()
    series = cast(TSeries ,MAIN_MENU[selection]["series"])


def display_info_screen(banner_title: str, intro: str, content: str):
    display_info = True
    action = "next"
    print(HOME + CLEAR, end="", flush=True)
    print(TERM.black_on_cyan(CENTER(banner_title)) + DOWN(1))
    for line in intro.split("\n"):
        print(CENTER(line))
    for line in content.split("\n"):
        even_line = line
        while len(even_line) < 80:
            even_line += " "
        print(CENTER(even_line))
    print(HOME + XY(0, HEIGHT), end="", flush=True)
    message = " Press RETURN or SPACE to continue, ESC to return to the menu "
    print(TERM.black_on_white(message) + X(0), end="", flush=True)
    info_str = " Info "
    print(
        RIGHT(WIDTH - len(info_str)) + TERM.black_on_white(info_str), end="", flush=True
    )
    while display_info:
        key = get_key()
        if key.name == "KEY_ESCAPE":
            action = "menu"
            display_info = False
        if key.name == "KEY_ENTER" or key == " ":
            display_info = False

    return action


def prompt_next_lesson():
    print(HOME + XY(0, HEIGHT), end="", flush=True)
    message = f" Do you want to continue to lesson {series}{str(lesson + 1)} [Y/N] ? "
    print(TERM.black_on_white(message) + "      ", end="", flush=True)
    while True:
        key = get_key()
        if key.lower() == "y":
            return "next"
        if key.lower() == "n":
            return "menu"


def get_lesson_data() -> dict:
    lesson_dir = f"series/{series}/{str(lesson)}"
    data_fp = f"{lesson_dir}/data.yaml"
    data_file = Path(__file__).parent.joinpath(data_fp)
    lesson_data = cast(dict, file_content(data_file, "yaml"))
    return lesson_data


def run_lesson():
    global lesson
    global segment
    run_lesson_menu()
    if lesson == 0:
        return 0
    show_menu = False
    lesson_data = get_lesson_data()
    lc_fp = f"series/{series}/lesson_count"
    lc_file = Path(__file__).parent.joinpath(lc_fp)
    lesson_count = int(cast(str,file_content(lc_file)))

    while segment <= lesson_data["total_segments"]:
        is_last_segment = segment == lesson_data["total_segments"]
        if is_last_segment:
            segment = 0
            # check if user is on last lesson, return to menu
            if lesson == lesson_count:
                show_menu = True
                break
            else:
                answer = prompt_next_lesson()
                if answer == "menu":
                    show_menu = True
                    break
                else:
                    lesson += 1
                    lesson_data = get_lesson_data()
                    continue

        current_seg = lesson_data["segments"][segment]
        intro = current_seg["intro"]
        content = current_seg["content"]
        title = f"Lesson {series}{str(lesson)}"
        type = current_seg["type"]
        action = ""

        if type == "info":
            action = display_info_screen(title, intro, content)
        else:
            action = run_drill(title, intro, content)
        if action == "next":
            segment += 1  # if next go to next segment
        if action == "repeat":
            continue  # if repeat run_drill again with same segment
        if action == "menu":
            segment = 0
            show_menu = True
            break

    if show_menu == False:
        return 1

    return 2

def days_difference(day1,day2):
    if day1 == day2:
        return 0
    else:
        return int(str(date.fromisoformat(day2)-date.fromisoformat(day1)).split(' ')[0])

def update_check():
    today=str(date.today())
    package_name='terminal_typing_tutor'
    update_data = Path(__file__).parent.joinpath("update.json").read_text()
    update = json.loads(update_data)
    latest_version = CURRENT_VERSION
    if update["check_date"] == "" or (days_difference(update["check_date"],today) > 7 and not update["available"]):
        try:
            url = f"https://pypi.org/pypi/{package_name}/json"
            data = json.load(request.urlopen(url))
            versions = sorted(list(data["releases"].keys()))
            latest_version = versions[-1]
        except Exception as _:
            print("Failed getting latest version information to check for update")

        if latest_version > CURRENT_VERSION:
             update["available"] = True
             update["number"] = latest_version
        update["check_date"] = today
    update_data_to_dump = json.dumps(update)
    Path(__file__).parent.joinpath("update.json").write_text(update_data_to_dump)
    if update["available"] and (update["last_shown"] == "" or days_difference(update["last_shown"],today) >= 2):
        update["last_shown"] = today
        update_data_to_dump = json.dumps(update)
        Path(__file__).parent.joinpath("update.json").write_text(update_data_to_dump)
        print(f"\n\n{TERM.green('Upgrade available!')} To upgrade run:\n")
        print(f"pip install --user --upgrade terminal-typing-tutor\n\n")

def tutor():
    """
    runs typing tutor program
    """
    update_check()
    with TERM.fullscreen(), TERM.cbreak():  # hidden cursor off during development
    # with TERM.fullscreen(), TERM.cbreak(), TERM.hidden_cursor():
        num = 0
        while True:
            if num == 0:
                run_series_menu()
                num = run_lesson()
            if num == 1:
                exit()
            if num == 2:
                num = run_lesson()
