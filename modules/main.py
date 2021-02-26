# Do not modify these lines
__winc_id__ = "78029e0e504a49e5b16482a7a23af58c"
__human_name__ = "modules"

# Add your code after this line


from time import sleep
from math import sin
from datetime import datetime
from sys import platform as pf
from greet import supergreeting

# 1

# import this


# 2


def wait(seconds):
    sleep(seconds)
    return


# 3


def my_sin(radial):
    return sin(radial)


# 4
def iso_now():
    return datetime.now().strftime("%Y-%m-%dT%H:%M")


# 5


def platform():
    return pf


# 6
def supergreeting_wrapper(name):
    return supergreeting(name)
