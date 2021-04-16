import csv
import os.path
import os
import colorama
from colorama import Fore, Back, Style
from colorama import init
import sys
import datetime as dt
from pprint import pprint


# is het verstandig om zoveel globals te hebben?
log_dir = "superpy_logs"
log_txt_file = "log_id_superpy.txt"

csv_bought = "bought.csv"
csv_sold = "sold.csv"
bought_file = os.path.join(log_dir, csv_bought)
sold_file = os.path.join(log_dir, csv_sold)


fieldnames_bought = [
    "id",
    "product_name",
    "buy_price",
    "product_amount",
    "buy_date",
    "expiration_date",
]
fieldnames_sold = [
    "id",
    "product_name",
    "product_amount",
    "buy_price",
    "sell_price",
    "buy_date",
    "sell_date",
    "expiration_date",
]


def create_log_dir():       # meeste is niet nodig, maar vond het leuk om te doen :)
    """
    If it doesn't exists, creates a new folder with .csv files in the current working directory.
    If folder already exist, checks if there is a specific .txt file in the folder.
    If specific .txt file can't be found, program will terminate with error message.
    """
    if log_dir in os.listdir():
        if log_txt_file not in os.listdir(log_dir):
            raise Exception(
                f"""      
{Back.RED}!!!WARNING!!!{Back.RESET}{Back.RED}!!!WARNING!!!{Back.RESET}{Back.RED}!!!WARNING!!!{Back.RESET}
Directory '{log_dir}' already exist, but could not find necessary {log_txt_file} file,
Either you already have an existing '{log_dir}' directory which was not created by this program, 
or you may have deleted the necessary {log_txt_file} file!!! 
You can try the following:

{Fore.YELLOW}1. Remove '{log_dir}' folder in current directory.
2. Manually Create a new {log_txt_file} file. {Fore.RESET}

The program will quit now. Bye!!!
{Back.RED}!!!WARNING!!!{Back.RESET}{Back.RED}!!!WARNING!!!{Back.RESET}{Back.RED}!!!WARNING!!!{Back.RESET}
"""
            )
            sys.exit()

    if log_dir not in os.listdir():
        os.mkdir("logs")
        with open(os.path.join(log_dir, log_txt_file), "w") as file:
            file.write(
                f"""created file for first time at {dt.datetime.now()}
            WARNING!!! Do NOT remove this file."""
            )
        with open(os.path.join(log_dir, csv_bought), "w", newline="") as bought:
            writer = csv.DictWriter(bought, fieldnames=fieldnames_bought)
            writer.writeheader()
        with open(os.path.join(log_dir, csv_sold), "w", newline="") as sold:
            writer = csv.DictWriter(sold, fieldnames=fieldnames_sold)
            writer.writeheader()


def buy_product(args):
    """
    uses args parameter to access product info given in subparser command
    and appends row of arguments into file 'bought.csv'.
    """
# ik doe nu niks met id.. Kan mss weg.
    with open(bought_file) as csv_bought:
        id = len(csv_bought.readlines())

    with open(bought_file, "a", newline="") as csv_bought:
        writer = csv.DictWriter(csv_bought, fieldnames=fieldnames_bought)
        writer.writerow(
            {
                "id": id,
                "product_name": args.product_name,
                "buy_price": args.price,
                "product_amount": args.amount,
                "buy_date": "empty buy date",
                "expiration_date": args.expirydate,
            }
        )
    print("product added")


def sell_product(args):
    """
    Uses args parameter to access product info given in subparser command
    and reads from 'bought.csv' if valid command is given.
    Writes product info to 'sold.csv' and updates 'bought.csv' accordingly.
    """

    # reads from bought.csv if product/product amount exist.
    # appends target product and non-target product to lists.
    dirty_rows = []
    clean_rows = []
    with open(bought_file, "r") as bought_r:
        reader = csv.DictReader(bought_r)
        count = 0
        for row in reader:
            if row["product_name"] == args.product_name:
                if count == args.amount:  # uses args.amount for amount to sell
                    clean_rows.append(row)
                    continue
                else:
                    dirty_rows.append(row)
                    count += 1
            if row["product_name"] != args.product_name:
                clean_rows.append(row)

        # raises exception if productname is not in bought.csv
        if len(dirty_rows) < args.amount:
            raise Exception(f"Product {args.product_name} sold out")

    # re-writes clean rows to bought.csv
    with open(bought_file, "w", newline="") as bought_w:
        writer = csv.DictWriter(bought_w, fieldnames=fieldnames_bought)
        writer.writeheader()
        writer.writerows(clean_rows)

    # writes dirty rows to sold.csv
    with open(sold_file, "a", newline="") as sold:
        writer = csv.DictWriter(sold, fieldnames=fieldnames_sold)
        for row in dirty_rows:

            writer.writerow(
                {
                    "id": row["id"],
                    "product_name": row["product_name"],
                    "buy_price": row["buy_price"],
                    "buy_date": "!!!!!!empty buy date!!!!!!",
                    "sell_price": args.price,
                    "sell_date": "!!!!!empty sell date!!!!!",
                    "product_amount": args.amount,
                    "expiration_date": row["expiration_date"],
                }
            )
    print(f"product {args.product_name} sold {args.amount} time(s) for {args.price}")
