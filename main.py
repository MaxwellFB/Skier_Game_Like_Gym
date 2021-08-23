"""Start game"""

from Skier import Game

def main():
    game = Game()
    # if "keyboard_game=False", need to use "step(action)" to play
    game.start(keyboard_game=True, increase_speed=1, low_speed=6, max_speed=15)


if __name__ == '__main__':
    main()
