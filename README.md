# Terminal Typing Tutor

A port of GNU Typist (GTypist)



https://github.com/justinsgithub/terminal-typing-tutor/assets/74565194/c299740b-a2f2-47f5-b244-1ca41fa48295





## Project Goals

GTypist is by far the best program I have used to learn how to type faster. 
However it is pretty outdated and has many potential features that can be added. 
I was initially going to just add to the C code, but decided to switch to Python for faster implementation.
It is a tradeoff for speed, but so far the difference has not taken away from the program.

I tried to stick with the original program layout and how it did things as much as possible, both out of simplicity and respect to the original.

I also think this could be a good starting open-source project for new developers to contribute to.

## Install

in your terminal:

```
$ pip install --user terminal-typing-tutor
---> 100%
Successfully installed terminal-typing-tutor

$ ttt
```

upgrade:

```
$ pip install --user --upgrade terminal-typing-tutor
```

## Features

### New

- Tracking all time WPM, and saving scores to ~/.config/terminal-typing-tutor directory
    - This allows for saving typing scores long-term and between machines. 
    - I add terminal-typing-tutor to my dotfiles managed by stow so that they are saved to github

- Small UI improvements, such as centering the text on the screen, having it up in top left was especially annoying on a large monitor

### Lacking

- There are features and also lessons missing from the original GTypist that I don't use.
- If there is anything you want added, feel free to create and issue or make a pull request, contributions are welcome and encouraged

### Requirements


This project is built with:

- Python 3.6+

- [Typer](https://typer.tiangolo.com) for command line functionality (not really doing much at the moment, but future features will incorporate it more)

- [Blessed](https://github.com/jquast/blessed) for the terminal interface, a wrapper around the curses module

## Contributing

I think this project would be an awesome first open source project for new developers looking to contribute.

There are plenty of things to be improved or added to this package, such as:

- refactoring the code, since it has just been me, I did not worry too much about making it super pretty.
    - there are places where code is repeated and can be extracted into a reusable function

- adding theme options
- tracking the date of users personal bests to display progress over time
- adding new lessons for programming, such as an html, python, and javascript lesson

Some of the new features will need to implement [Typer](https://typer.tiangolo.com), the docs are awesome, so are the [Blessed](https://github.com/jquast/blessed) docs

## License

I stuck with the original license of the project, this is my first real open source project, so please let me know if there are any standards or anything I should do better.

