import colorama
from colorama import Fore, Back, Style

colorama.init()


def color():
    print(f"something something")


color()

print(f"\033[31msome red text")