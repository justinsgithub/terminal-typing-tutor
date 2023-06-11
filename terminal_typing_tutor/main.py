import typer
from terminal_typing_tutor.tutor import tutor

def main():
    tutor()

# typer is not really being used yet, adding now for future features
if __name__ == "__main__":
    typer.run(main)
