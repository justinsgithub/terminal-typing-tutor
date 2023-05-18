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
        print('KEY ' +  str(key))
        print('KEY NAME' +  str(key.name))
        print('KEY CODE' +  str(key.code))
        print('\x03' == repr(key))
        print(key == '\x03')
        print(key.lower())
        print(term.move_down(1) + 'You pressed ' + term.bold(repr(key)))

