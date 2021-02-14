# Do not modify these lines
__winc_id__ = '49bce82ef9cc475ca3146ee15b0259d0'
__human_name__ = 'functions'

# Add your code after this line

# 1


def greet(name):
    return print(f"Hello, {name}!")

# 2


def add(x, y, z):
    return x + y + z

# 3


def scottish_greet(name, isChild):
    if isChild == False:
        return print(f"Hello, {name}")
    else:
        return print(f"Hello, wee {name}")
# 4


def positive(num):
    if num > 0:
        return print(True)
    else:
        return print(False)

# 5

def negative(num):
    if num < 0:
        return print(True)
    else:
        return print(False)

# 6
def sign(num):
    if type(num) == str:
        return print("This doesn't have a sign")
    if num > 0:
        return print(1)
    if num < 0:
        return print(-1)
# 7

def nag(name, item, int):
    sentence = f"{name}{int * '.'} Why can't I have a {item}?!\n"
    return print((sentence * int))

nag("John", "cookie", 6)