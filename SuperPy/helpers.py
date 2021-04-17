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
# product amount kan mss weggelaten worden in fieldnames. is alleen van belang voor aantal writerow()
log_dir = "superpy_logs"
log_txt_file = "log_id_superpy.txt"


products_file = "products_list.csv"
csv_bought = "bought.csv"
csv_sold = "sold.csv"
bought_file = os.path.join(log_dir, csv_bought)
sold_file = os.path.join(log_dir, csv_sold)
product_list_csv = os.path.join(log_dir, products_file)
product_list_lst = [
    "orange",
    "bread",
    "milk",
    "eggs",
    "water",
    "apple",
    "candy",
]  # placeholder product list

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


def create_log_dir():  # meeste is niet nodig, maar vond het leuk om te doen :)
    """
    If it doesn't exists, creates a new folder with .csv files in the current working directory.
    If folder already exist, checks if there is a specific .txt file in the folder.
    If specific .txt file can't be found, program will terminate with error message.
    """

    if log_dir in os.listdir():
        if log_txt_file not in os.listdir(log_dir):
            raise FileExistsError(
                f"""      
{Back.RED}!!!WARNING!!!{Back.RESET}{Back.RED}!!!WARNING!!!{Back.RESET}{Back.RED}!!!WARNING!!!{Back.RESET}


Directory '{log_dir}' already exist, but could not find necessary {log_txt_file} file,
Either you already have an existing '{log_dir}' directory which was not created by this program, 
or you may have deleted the necessary {log_txt_file} file!!! 
You can try the following:

{Fore.YELLOW}1. Remove '{log_dir}' folder in current directory.
2. Manually Create a new {log_txt_file} file inside the {log_dir} folder. {Fore.RESET}

The program will quit now. Bye!!!


{Back.RED}!!!WARNING!!!{Back.RESET}{Back.RED}!!!WARNING!!!{Back.RESET}{Back.RED}!!!WARNING!!!{Back.RESET}
"""
            )
            sys.exit()

    if log_dir not in os.listdir():
        os.mkdir(log_dir)
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
        with open(product_list_csv, "w", newline="") as p_lst:
            writer = csv.writer(p_lst)
            [writer.writerow([p]) for p in product_list_lst]


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
        for i in range(args.amount):
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

        # raises exception if productname is not in bought.csv or amount is not satisfied
        if len(dirty_rows) < args.amount:
            raise ValueError(
                f"""Tried to sell {args.amount} items of {args.product_name}. There are only {len(dirty_rows)} left in stock."""
            )

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
                    "product_amount": row["product_amount"],
                    "expiration_date": row["expiration_date"],
                }
            )
    print(f"product {args.product_name} sold {args.amount} time(s) for {args.price}")


def handle_list(args):
    """Takes in attribute for args and adds or removes product
    from the list of available products"""
    with open(product_list_csv) as lst:
        reader = csv.reader(lst)
        flat_list = [product for sublist in list(reader) for product in sublist]
        print(args.add)
        print(args.remove)
        # add product to list
        if args.add:
            if args.add in flat_list:
                raise ValueError(f"{args.add} already exist")

            if args.add not in flat_list:
                with open(product_list_csv, "a", newline="") as lst:
                    writer = csv.writer(lst)
                    writer.writerow([args.add])

        # remove product to list
        if args.remove:
            if args.remove not in flat_list:
                raise ValueError(f"{args.remove} does not exist")

            if args.remove in flat_list:
                flat_list.remove(args.remove)
                with open(product_list_csv, "w", newline="") as lst:
                    writer = csv.writer(lst)
                    [writer.writerow([product]) for product in flat_list]

        if args.add is None and args.remove is None:
            print(flat_list)


def handle_inventory(args):
    print("handling inventory function")
    # handling simple inventory: product, amount,
    # handling product inventory: amount, buyprice, expdate
    # handling all inventory: product:
    # amount, buyprice, expdate

    with open(bought_file) as bought_r, open(product_list_csv) as lst:
        reader_lst = csv.reader(lst)
        flat_list = [product for sublist in list(reader_lst) for product in sublist]
        simple_inventory = {flat_list: 0 for flat_list in flat_list}
        reader_bought = csv.DictReader(bought_r)
        for row in reader_bought:
            for product, count in simple_inventory.items():
                if product == row["product_name"]:
                    simple_inventory[product] += 1
    print(simple_inventory)

    if args.short:
        print("short inventory")

    # if args.inventory == "product"
    #     print("short inventory")
    # if args.inventory == "all"
    #     print("short inventory")
    # if args.
    if args.long:
        print("long invetory")
