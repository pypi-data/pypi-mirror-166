'''Module to generate random Boggle boards for testing'''
from sys import argv
from random import randint, shuffle
from math import sqrt

def read_dice_file(path):
    # TODO: Factor in 'qu' die face
    '''Return list of die strings from file ignoring all comments (#)'''
    with open(path, 'r+', encoding="utf-8") as file:
        return [line.rstrip().split(',') for line in file.readlines() if line[0] != "#"]

def roll_die(die: str):
    '''Return a face of the given die string to simulate rolling a die'''
    return str(die[randint(0, len(die) - 1)])

def roll_dice(dice: list[str]):
    '''Return a random roll for each die'''
    return [ roll_die(die) for die in dice ]

if __name__ == '__main__':
    if len(argv) != 2:
        print('Usage: python3 board_randomizer.py <dice_file>')
    else:
        dice_strings = read_dice_file(argv[1])
        shuffle(dice_strings)
        rolls = roll_dice(dice_strings)

        # Format dice rolls for boards file
        board_size = int(sqrt(len(rolls)))
        for i in range(0, len(dice_strings), board_size):
            print(",".join(rolls[i:i+board_size]))
