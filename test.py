#!/usr/bin/env python3

from blessed import Terminal
import os
term = Terminal()

with term.cbreak(), term.hidden_cursor(), term.raw():
    print(os.listdir('lessons'))
    while True:
        key = term.inkey()
        if key == '\x03':
            exit()
        if key == '\n':
            print(term.red('KEY IS KEY_ENTER'))
        if key.is_sequence:
            print(term.green('KEY IS SEQUENCE'))
        if key.name == 'KEY_BACKSPACE':
            print(term.green('KEY IS KEY_BACKSPACE'))
        if key.name == 'KEY_ENTER':
            print(term.green('KEY IS KEY_ENTER'))
        print(term.green('term.inkey() = ' +  key))
        print(term.green('KEY NAME' +  str(key.name)))
        print(term.green('KEY CODE' +  str(key.code)))
        print(term.green(str('\x03' == repr(key))))
        print(term.green(str(key == '\x03')))
        print(term.green(key.lower()))
        print(term.move_down(1) + 'You pressed ' + term.bold(repr(key)))

