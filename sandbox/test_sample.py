import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    "-s", "--square", help="display a square of a given number", type=int
)
parser.add_argument(
    "-q", "--q", help="display a square of a given number", type=int
)
args = parser.parse_args()
print(args)
