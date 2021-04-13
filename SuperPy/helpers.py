import csv
import os.path
import os
import colorama
from colorama import Fore, Back, Style
from colorama import init
import sys


log_dir = "logs"
log_txt_file = "log_id_superpy.txt"


def create_log_dir():
    """
    If not exists, creates a new logs folder in the current working directory.
    If folder already exist, checks if there is a specific file in the folder and continues.
    If folder already exist, but specific file can't be found, program will terminate.
    """
    if log_dir in os.listdir():
        if log_txt_file not in os.listdir(log_dir):
            print(
                f"""           
    {Back.RED}!!!WARNING!!!{Back.RESET}
    Directory '{log_dir}' already exist, but could not find necessary {log_txt_file} file,
    Either you already have an existing '{log_dir}' directory which was not created by this program, 
    or you may have deleted the necessary {log_txt_file} file!!! 
    You can try the following:

    {Fore.YELLOW}1. Remove '{log_dir}' folder in current directory
    2. Manually Create a new {log_txt_file} file. {Fore.RESET}

    The program will quit now. Bye!!!
    {Back.RED}!!!WARNING!!!{Back.RESET} 
    """
            )
            sys.exit()

    if log_dir not in os.listdir():
        os.mkdir("logs")
        with open(os.path.join(log_dir, log_txt_file), "w") as file:
            file.write(
                """created file for first time at *****time****
            WARNING!!! Do NOT remove this file."""
            )


def write_bought_row(bought_file, has_bought_file, args):
    """
    writes row for args into bought_file.
    If bought_file does not exist, creates header as first line,
    else skips creating header.
    """
    bought_file_location = os.path.join(bought_file)
    fieldnames = [
        "id",
        "product_name",
        "buy_price",
        "product_amount",
        "buy_date",
        "expiration_date",
    ]

    if has_bought_file:  # mss korter maken met has_header()
        with open(bought_file_location) as csv_bought:
            file_length = len(csv_bought.readlines())

        with open(bought_file_location, "a", newline="") as csv_bought:
            writer = csv.DictWriter(csv_bought, fieldnames=fieldnames)
            writer.writerow(
                {
                    "id": file_length,
                    "product_name": args.productname,
                    "buy_price": args.price,
                    "product_amount": args.amount,
                    "buy_date": "empty buy date",
                    "expiration_date": args.expirydate,
                }
            )
    if not has_bought_file:
        with open(bought_file_location, "a", newline="") as csv_bought:
            writer = csv.DictWriter(csv_bought, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow(
                {
                    "id": 1,
                    "product_name": args.productname,
                    "buy_price": args.price,
                    "product_amount": args.amount,
                    "buy_date": "empty buy date",
                    "expiration_date": args.expirydate,
                }
            )


def buy_product(args):
    """
    uses args parameter to access arguments in subparser
    and writes row of arguments into file 'bought.csv'
    """
    bought_file = "bought.csv"
    bought_file_location = os.path.join(log_dir, bought_file)
    if bought_file in os.listdir(log_dir):
        write_bought_row(bought_file_location, True, args)

    if bought_file not in os.listdir(log_dir):
        write_bought_row(bought_file_location, False, args)
    print("Product added!")


def sell_product(args):
    print(
        f"""sold {args.amount} of {args.productname} for €{args.price}
    total sell price: €{args.price * args.amount}"""
    )
    pass