# Do not modify these lines
__winc_id__ = '49bce82ef9cc475ca3146ee15b0259d0'
__human_name__ = 'functions'

# Add your code after this line

# 1


def greet(name):
    return (f"Hello, {name}!")

# 2


def add(x, y, z):
    return x + y + z

# 3


def scottish_greet(name, isChild):
    if isChild == False:
        return (f"Hello, {name}!")
    else:
        return (f"Hello, wee {name}!")


print(scottish_greet('Ian', True))

# 4


def positive(num):
    return num > 0

# 5


def negative(num):
    if num < 0:
        return (True)
    else:
        return (False)

# 6


def sign(num):
    if type(num) is not int and type(num) is not float:
        return ("This doesn't have a sign!")
    if num > 0:
        return print(1)
    if num < 0:
         print(-1)
         return print(0)
# 7


def nag(name, item, int):
    sentence = f"{name}{int * '.'} Why can't I have a {item}?!\n"
    return print((sentence * int))


sign(0.9)
def main():
    print("do things")


main()