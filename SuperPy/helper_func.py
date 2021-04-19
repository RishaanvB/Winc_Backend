import csv
import argparse

# import os.path
import os
from colorama import Fore, Back
import sys
import datetime as dt
from datetime import date, timedelta
from rich.console import Console
from rich.table import Table
from helper_var import (
    log_dir,
    log_txt_file,
    products_file,
    csv_bought,
    csv_sold,
    bought_file,
    sold_file,
    product_list_csv,
    inventory_txt,
    fieldnames_bought,
    fieldnames_sold,
    date_file,
)

# is het verstandig om zoveel globals te hebben?
# product amount kan mss weggelaten worden in fieldnames. is alleen van belang voor aantal writerow()
console = Console(record=True)


def create_log_dir():
    f"""
    If it doesn't exists, creates a new folder {log_dir} with necessary files in the current working directory.
    If folder already exist, checks if there is a {log_txt_file} file in the folder.
    If {log_txt_file} file can't be found, program will terminate with error message.
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
        with open(os.path.join(log_dir, date_file), "w") as date_txt:
            date_txt.write(f"{dt.date.today()}")
        with open(os.path.join(log_dir, log_txt_file), "w") as file_log:
            file_log.write(
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
            # volgende writerows om alvast producten te kunnen kopen/verkopen, zodat je geen producten hoeft aan te maken
            writer.writerow(["eggs"])
            writer.writerow(["milk"])
            writer.writerow(["bread"])
            writer.writerow(["water"])
            writer.writerow(["orange"])


def read_productlist_csv():
    """
    reads available list of products from products_list file
    and returns them as a list of strings
    """
    with open(product_list_csv) as p_file:
        reader = csv.reader(p_file)
        product_list = [row[0] for row in reader]
        return product_list


def read_fake_date():
    """
    reads current 'fake' date from date.txt
    and prints the first line, which should be the 'internal' fake date as string
    """
    date_file_location = os.path.join(log_dir, date_file)
    with open(date_file_location) as date:
        current_date = date.readline()
    return current_date


def set_fake_date():
    pass


def range_checker(num):
    """
    converts num to int and if num not in range 0-10,
    ArgumentTypeError will be raised.
    Only use for this function is to return a replacement error for the builtin error message for the add_argument() method in argparse
    for the choices kwarg.
    """
    num = int(num)
    if num not in list(range(1, 11)):
        raise argparse.ArgumentTypeError("should be between 1 and (including) 10")
    return num


def buy_product(args):
    """
    uses args parameter to access product info given in subparser command
    and appends row of arguments into file 'bought.csv'.
    """

    # ik doe nu niks met id.. Kan mss weg.
    # with open(bought_file) as csv_bought:
    #     id = len(csv_bought.readlines())

    with open(bought_file, "a", newline="") as csv_bought:
        writer = csv.DictWriter(csv_bought, fieldnames=fieldnames_bought)
        for i in range(args.amount):
            writer.writerow(
                {
                    "product_name": args.product_name,
                    "buy_price": args.price,
                    "product_amount": 1,
                    "buy_date": args.date,
                    "expiration_date": args.expirydate,
                }
            )
    print("product added")


def sell_product(args):
    """
    Uses args parameter to access product info given in subparser command
    and reads from 'bought.csv' if valid command is given.
    Writes product info to 'sold.csv' and 'updates' 'bought.csv' accordingly.
    With 'updates', meaning it wil delete the row from bought.csv.
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

        # raises exception if amount to sell > in stock
        if len(dirty_rows) < args.amount:
            raise ValueError(
                f"""Tried to sell {args.amount} items of {args.product_name}. There are only {len(dirty_rows)} left in stock."""
            )

    # re-writes clean rows to bought.csv
    with open(bought_file, "w", newline="") as bought_w:
        writer = csv.DictWriter(bought_w, fieldnames=fieldnames_bought)
        writer.writeheader()
        writer.writerows(clean_rows)

    # appends dirty rows to sold.csv
    with open(sold_file, "a", newline="") as sold:
        writer = csv.DictWriter(sold, fieldnames=fieldnames_sold)
        for row in dirty_rows:

            writer.writerow(
                {
                    # "id": row["id"],
                    "product_name": row["product_name"],
                    "buy_price": row["buy_price"],
                    "buy_date": row["buy_date"],
                    "sell_price": args.price,
                    "sell_date": read_fake_date(),
                    "product_amount": row["product_amount"],
                    "expiration_date": row["expiration_date"],
                }
            )
    print(f"product {args.product_name} sold {args.amount} time(s) for {args.price}")


def handle_product_list(args):
    """Takes in attribute for args, which are 'add' or 'remove'
    and adds or removes the argument given from the products_list.csv
    It will always print out a list of products available from products_list.csv.
    """
    with open(product_list_csv) as lst:
        reader = csv.reader(lst)
        flat_list = [product for sublist in list(reader) for product in sublist]

    def add_product():
        args.add = args.add.lower()
        if args.add in flat_list:
            raise ValueError(f"{args.add} already exist")

        if args.add not in flat_list:
            with open(product_list_csv, "a", newline="") as lst:
                writer = csv.writer(lst)
                writer.writerow([args.add])

    def remove_product():
        args.remove = args.remove.lower()
        if args.remove not in flat_list:
            raise ValueError(f"{args.remove} does not exist")

        if args.remove in flat_list:
            flat_list.remove(args.remove)
            with open(product_list_csv, "w", newline="") as lst:
                writer = csv.writer(lst)
                [writer.writerow([product]) for product in flat_list]

    if args.add:
        add_product()
    if args.remove:
        remove_product()
    if args:
        print(f"Total unique products in stock: {len(flat_list)}")
        [print(product) for product in sorted(flat_list)]


def handle_inventory(args):
    """
    handles what kind of table and information will be displayed,
    depending on the attribute of args given, calls
    one or a combination of 4 functions.
    1) short_inventory()    prints succinct inventory to terminal
    2) product_inventory()  prints specified product inventory to terminal
    3) long_inventory()     prints detailed inventory to terminal
    4) sold_inventory()     prints detailed sold products to terminal

    *If args.print is True, the printed out inventory table will also be exported to a .txt file.
    """

    def short_inventory():
        """
        Reads through bought.csv and creates a simple inventory list
        with tablecolumns: [product, count] and prints it in table form to the console.
        If count is 0(zero), the row will be colored red.
        """
        with open(bought_file) as bought_r, open(product_list_csv) as lst:
            reader_lst = csv.reader(lst)
            flat_list = [product for sublist in list(reader_lst) for product in sublist]
            simple_inventory = {flat_list: 0 for flat_list in flat_list}
            reader_bought = csv.DictReader(bought_r)

            for row in reader_bought:
                for product, count in simple_inventory.items():
                    if product == row["product_name"]:
                        simple_inventory[product] += 1
        short_table = Table(title="Short Inventory", show_lines=True)
        short_table.add_column("Product")
        short_table.add_column("Count", justify="right")
        total_items = 0

        for product, count in simple_inventory.items():
            total_items += count
            if count == 0:
                short_table.add_row(product, str(count), style="red")
            else:
                short_table.add_row(product, str(count))

        console.print(short_table)
        print(
            f"{Fore.YELLOW}There are a total of {total_items} items in stock{Fore.RESET}"
        )
        # writers/re-writes inventory.txt with inventory table
        if args.print:
            console.save_text(os.path.join(log_dir, inventory_txt))
            # write_table_to_file(txt)

    def product_inventory(file_to_open=bought_file):
        """
        Reads through bought.csv and creates an inventory list for specified product
        with table columns: [buy_price, buy_date, expiration_date]
        and prints it in table form to the console.
        Output depends on input of kwarg file_to_open. Default kwarg is bought_file
        """
        count = 0
        product = args.product

        # product_table.add_column()
        with open(file_to_open) as csv_read, open(product_list_csv) as product_list:
            reader_product_list = csv.reader(product_list)
            reader = csv.DictReader(csv_read)
            flat_list = [
                product for sublist in list(reader_product_list) for product in sublist
            ]
            if file_to_open == bought_file:
                product_table = Table(
                    title=f"{Fore.YELLOW}Product Inventory for {product.title()}{Fore.RESET} ",
                    show_lines=True,
                )
                table_columns = ["buy_price", "buy_date", "expiration_date"]

                # for header in reader.fieldnames:
                #     if header in table_columns:
                #         product_table.add_column(header)
                for header in table_columns:
                    product_table.add_column(header)
                for row in reader:
                    if row["product_name"] == product:
                        count += 1
                        product_table.add_row(
                            row[table_columns[0]],
                            row[table_columns[1]],
                            row[table_columns[2]],
                        )

            if file_to_open == sold_file:
                product_table = Table(
                    title=f"{Fore.YELLOW}Product {product.title()} Sold{Fore.RESET} ",
                    show_lines=True,
                )
                table_columns = [
                    "id",
                    "product_name",
                    "product_amount",
                    "buy_price",
                    "sell_price",
                    "buy_date",
                    "sell_date",
                    "expiration_date",
                ]
                for header in reader.fieldnames:
                    product_table.add_column(header)
                for row in reader:
                    if row["product_name"] == product:
                        count += 1
                        product_table.add_row(
                            row[table_columns[0]],
                            row[table_columns[1]],
                            row[table_columns[2]],
                            row[table_columns[3]],
                            row[table_columns[4]],
                            row[table_columns[5]],
                            row[table_columns[6]],
                            row[table_columns[7]],
                        )

        if product not in flat_list:
            raise ValueError(
                f"""Can't find {product}. Check your spelling or if the product is in the available products list"""
            )
        console.print(product_table)

        if file_to_open == bought_file:
            print(
                f"{Fore.YELLOW}Total items of {product} in stock: {count}{Fore.RESET} "
            )
        if file_to_open == sold_file:
            print(f"{Fore.YELLOW}Total items of {product} sold: {count}{Fore.RESET} ")

        if args.print:
            console.save_text(os.path.join(log_dir, inventory_txt))

    def long_inventory():
        """
        Reads through bought.csv and creates an inventory list of all items currently in stock
        with table columns: ["product_name", "buy_price", "buy_date", "expiration_date"]
        and prints it in table form to the console.
        """
        long_table = Table(
            title=f"{Fore.YELLOW}Total Inventory{Fore.RESET} ",
            show_lines=False,
        )
        table_columns = ["product_name", "buy_price", "buy_date", "expiration_date"]
        with open(bought_file) as bought:
            reader = csv.DictReader(bought)

            for header in reader.fieldnames:
                if header in table_columns:
                    long_table.add_column(header)
            for row in reader:
                long_table.add_row(
                    row[table_columns[0]],
                    row[table_columns[1]],
                    row[table_columns[2]],
                    row[table_columns[3]],
                )
        console.print(long_table)
        if args.print:
            console.save_text(os.path.join(log_dir, inventory_txt))

    def sold_inventory():
        """
        Reads through sold.csv and creates a list of all items sold
        and prints it in table form to the console.
        """
        dump_table = Table(
            title=f"{Fore.YELLOW}Total Sold{Fore.RESET}", show_lines=False
        )
        table_columns = [
            "product_name",
            "product_amount",
            "buy_price",
            "sell_price",
            "buy_date",
            "sell_date",
            "expiration_date",
        ]
        with open(sold_file) as sold:
            reader = csv.DictReader(sold)
            for header in reader.fieldnames:
                if header in table_columns:
                    dump_table.add_column(header)
            for row in reader:
                dump_table.add_row(
                    row[table_columns[0]],
                    row[table_columns[1]],
                    row[table_columns[2]],
                    row[table_columns[3]],
                    row[table_columns[4]],
                    row[table_columns[5]],
                    row[table_columns[6]],
                )
        console.print(dump_table)
        if args.print:
            console.save_text(os.path.join(log_dir, inventory_txt))

    # calling functions depending on args command given
    if args.short:
        short_inventory()
    if args.product and not args.dumped:
        product_inventory()
    if args.long:
        long_inventory()
    if args.dumped and not args.product:
        sold_inventory()
    if args.dumped and args.product:
        product_inventory(sold_file)


# -today, timedelta 0
# -yesterday, timedelta 0
# -date 12-28-10 timedelta = 0
# -delta 2020-12 timedelta = 30


def revenue(
    args, price="sell_price", file=sold_file, delta_days=5, target_date=read_fake_date()
):
    # delta_days = 1
    # print(delta.days, "print delta.days")
    # print(args, "print in revenue")
    total_price = 0
    with open(file) as opened_file:
        reader = csv.DictReader(opened_file)
        for row in reader:
            sell_date = date.fromisoformat(row[price])
            sell_price = float(row[price])
            current_date = date.fromisoformat(read_fake_date())
            # print(type(target_date))
            format_target_date = date.fromisoformat(target_date)
            # print(current_date.weekday())
            # print(sell_date, sell_price, current_date)
            diff = sell_date - current_date
            # print(target_date, current_date, "same")
            # print(type(current_date))
            if diff.days <= delta_days and format_target_date == current_date:
                # print(row["sell_price"], "sold today")
                # print("yes")
                total_price += sell_price
        print(total_price, "total price")
        return total_price


def handle_report(args):
    print("handling report")
    revenue(args)
    print("finished handling report")
    # if row[""]
    # door sold heen loopen
    # check if sold date = date to look for
    # check current !!fake!!date
    # check sold price and sum
    # check date!!!!!


def expenses():
    pass


def profit():
    total_profit = revenue() - expenses()
    return total_profit


# profit = revenue - expenses


#    parser.add_argument("--foo",choices=range(10))
def handle_revenue(args):
    print("handling revenue")


def handle_profit(args):
    print("handloing profit")