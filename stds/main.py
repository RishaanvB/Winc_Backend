# Leave these lines untouched
__winc_id__ = "8c2e6882503c4baa9ce2e050497c3f2f"
__human_name__ = "stds"

# Your code here
import sys


def main():
    text = sys.stdin.read()
    remove_char = sys.argv[1]
    sys.stdout.write(text.replace(remove_char, "-"))
    sys.stdout.write("\n")
    sys.stdout.write(f"Replaced '{sys.argv[1]}' {text.count(remove_char)} times")


if __name__ == "__main__":
    main()
