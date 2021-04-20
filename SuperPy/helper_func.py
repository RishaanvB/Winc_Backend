import csv
import argparse

# import os.path
import os
from colorama import Fore, Back
import sys
import datetime as dt
from datetime import date, timedelta, datetime
from rich.console import Console
from rich.table import Table
from helper_var import (
    log_dir,
    log_txt_file,
    # products_file,
    csv_bought,
    csv_sold,
    bought_file,
    sold_file,
    product_list_csv,
    inventory_txt,
    fieldnames_bought,
    fieldnames_sold,
    date_file,
    report_file,
)

# is het verstandig om zoveel globals te hebben?
# product amount kan mss weggelaten worden in fieldnames. is alleen van belang voor aantal writerow()
console = Console(record=True)


def create_log_dir():
    """
    If it doesn't exists, creates a new folder with necessary files in the current working directory.
    If the folder already exist, checks if there is a specific .txt file in the folder.
    If the .txt file can't be found, program will terminate with error message.
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


def set_fake_date(args):
    """
    reads current fake date from date.txt and updates it in days with the integer of
    args.time attribute. If args.time is 1, sets the date.txt to 1 day in the future
    Time will go back if a negative number is given.
    Will always print the current and the date that has been set.
    """
    print("Previous date was-->", read_fake_date())
    date_file_location = os.path.join(log_dir, date_file)
    current_date = read_fake_date()
    time_days = int(args.time)
    advance_days = timedelta(days=time_days)
    current_date = date.fromisoformat(current_date)
    new_date = current_date + advance_days
    new_date = date.isoformat(new_date)
    with open(date_file_location, "w") as new_date_file:
        new_date_file.write(new_date)
    print("Current date is-->", read_fake_date())


def range_checker(num):
    """
    converts num to int and if num not in range 0-10,
    ArgumentTypeError will be raised.
    Only use for this function is to return a replacement error for the builtin error message for the add_argument() method in argparse
    for the kwarg choices.
    """
    num = int(num)
    if num not in list(range(1, 11)):
        raise argparse.ArgumentTypeError("should be between 1 and (including) 10")
    return num


def buy_product(args):
    """
    uses args parameter to access product info given in subparser command
    and appends row of values into file 'bought.csv'.
    """
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
    print(f"product {args.product_name} added")


def sell_product(args):
    """
    Uses args parameter to access product info given in subparser command
    and reads from 'bought.csv' if valid command is given.
    Writes product info to 'sold.csv' and 'updates' 'bought.csv' accordingly.
    With 'updates', meaning it wil delete the row from bought.csv file
    """

    # reads from bought.csv if product/product amount exist.
    # appends target product and non-target product to clean_rows and dirt_rows respectively.
    dirty_rows = []
    clean_rows = []
    with open(bought_file, "r") as bought_r:
        reader = csv.DictReader(bought_r)
        count = 0
        for row in reader:
            if row["product_name"] == args.product_name:
                if count == args.amount:
                    clean_rows.append(row)
                    continue
                else:
                    dirty_rows.append(row)
                    count += 1
            if row["product_name"] != args.product_name:
                clean_rows.append(row)

        # raises error if amount to sell > in stock
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
    """
    Used for updating products_list.csv with custom items.
    List is already pre-occupied with items for quicker use of program.
    Takes in attribute for args, which are 'add' or 'remove'
    and adds or removes the item given from the products_list.csv.
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
        print(f"Total unique products available to buy/sell: {len(flat_list)}")
        [print(product) for product in sorted(flat_list)]


# ---------comments over de handle_inventory()
"""
ik zag pas nadat ik 99% klaar was dat je de inventory moest kunnen zien van bepaalde dagen.
Dus heb daar geen rekening mee gehouden toen ik met de handle_inventory() begon.
Heb later de mogelijkheid erin gezet om alleen de short_inventory() van 'gisteren' te kunnen zien.
Hoop dat dat genoeg is.
Ook was het, denk ik, niet echt handig om zoveel functies in een functie te nestelen, 
maar ik vond het zelf handig om ze bij elkaar te houden.
Heb er zelf niet zoveel last van gehad, maar ik denk dat als er bugs in zitten, dat die traceback
waarschijnlijk steeds langer wordt en lastiger wordt om te ontcijferen.
"""
# comments over de handle_inventory()----------


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
            current_fake_date = date.fromisoformat(read_fake_date())

            for row in reader_bought:
                buy_date = date.fromisoformat(row["buy_date"])
                for product, count in simple_inventory.items():

                    # if-block laat alleen inventory van gisteren zien
                    if args.yesterday:
                        buy_date = date.fromisoformat(row["buy_date"])
                        buy_date_delta = buy_date - current_fake_date

                        if product == row["product_name"] and buy_date_delta.days == -1:
                            simple_inventory[product] += 1

                    elif (
                        product == row["product_name"] and buy_date <= current_fake_date
                    ):
                        simple_inventory[product] += 1

        # prints table to console
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

    def product_inventory(file_to_open=bought_file):
        """
        Reads through bought.csv and creates an inventory list for specified product
        with table columns: [buy_price, buy_date, expiration_date]
        and prints it in table form to the console.
        Output depends on input of kwarg file_to_open. Default kwarg is bought_file
        """
        count = 0
        product = args.product
        with open(file_to_open) as csv_read, open(product_list_csv) as product_list:
            reader_product_list = csv.reader(product_list)
            reader = csv.DictReader(csv_read)
            flat_list = [
                product for sublist in list(reader_product_list) for product in sublist
            ]
            current_fake_date = date.fromisoformat(read_fake_date())
            # prints table for current inventory for specified product
            if file_to_open == bought_file:
                product_table = Table(
                    title=f"{Fore.YELLOW}Product Inventory for {product.title()}{Fore.RESET} ",
                    show_lines=True,
                )
                table_columns = ["buy_price", "buy_date", "expiration_date"]

                for header in table_columns:
                    product_table.add_column(header)
                for row in reader:
                    buy_date = date.fromisoformat(row["buy_date"])
                    if row["product_name"] == product and buy_date <= current_fake_date:
                        count += 1
                        product_table.add_row(
                            row[table_columns[0]],
                            row[table_columns[1]],
                            row[table_columns[2]],
                        )

            # prints sold table for specified product
            if file_to_open == sold_file:
                product_table = Table(
                    title=f"{Fore.YELLOW}Product {product.title()} Sold{Fore.RESET} ",
                    show_lines=True,
                )

                product_table.add_column("product name")
                product_table.add_column("buy price")
                product_table.add_column("sell price")
                product_table.add_column("sell date")
                product_table.add_column("expiration date")
                for row in reader:
                    if row["product_name"] == product:
                        count += 1
                        product_table.add_row(
                            row["product_name"],
                            row["buy_price"],
                            row["sell_price"],
                            row["sell_date"],
                            row["expiration_date"],
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
        current_fake_date = date.fromisoformat(read_fake_date())
        with open(bought_file) as bought:
            reader = csv.DictReader(bought)

            for header in reader.fieldnames:
                if header in table_columns:
                    long_table.add_column(header)
            for row in reader:
                buy_date = date.fromisoformat(row["buy_date"])
                if buy_date <= current_fake_date:
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
        sold_table = Table(
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
        current_fake_date = date.fromisoformat(read_fake_date())
        with open(sold_file) as sold:
            reader = csv.DictReader(sold)
            for header in reader.fieldnames:
                if header in table_columns:
                    sold_table.add_column(header)
            for row in reader:
                sell_date = date.fromisoformat(row["sell_date"])
                if sell_date <= current_fake_date:
                    sold_table.add_row(
                        row[table_columns[0]],
                        row[table_columns[1]],
                        row[table_columns[2]],
                        row[table_columns[3]],
                        row[table_columns[4]],
                        row[table_columns[5]],
                        row[table_columns[6]],
                    )
        console.print(sold_table)
        if args.print:
            console.save_text(os.path.join(log_dir, inventory_txt))

    # calling nested functions depending on args command given
    if args.short:
        short_inventory()
    if args.product and not args.sold:
        product_inventory()
    if args.long:
        long_inventory()
    if args.sold and not args.product:
        sold_inventory()
    if args.sold and args.product:
        product_inventory(sold_file)


def convert_to_timestr(time_str):
    """
    converts string into a datetime object if argument passed to function corresponds to
    format 'string-num' where string is month in 3 characters and num is a 2 digit num.
    example: jan-20 will be converted to datetime obj: datetime.date(2020, 1, 1)
    Only use is as a typechecker in report parser to return datetime obj from passed  '--month' argument
    ** needs to be updated every 100 years... :)**
    """
    month_str, year_int = time_str.split("/")
    months = [
        "jan",
        "feb",
        "mar",
        "apr",
        "may",
        "jun",
        "jul",
        "aug",
        "sep",
        "oct",
        "nov",
        "dec",
    ]
    try:
        for i, month in enumerate(months, start=1):
            if month_str == month:
                month_int = i
        year_int = f"20{year_int}"  # is pas over 80 jaar een probleem.. :)
        date_time = date(int(year_int), int(month_int), 1)
        return date_time
    except Exception:
        print(
            """something went wrong with your input. Check if input is of format 'aaa/bb', 
        where 'aaa' is a three length string of the month and 'bb' is the year.
        Acceptable examples:
        jan/20
        mar/22
        jul/18
        """
        )


def get_total_price(args, price, file, type_report):

    """
    Reads through file(.csv) parameter and calculates the total
    for all the rows in the file with the attribute price parameter.
    Depending on the args attribute will calculate and return total price.
    Also prints the product.  Functie doet een beetje te veel..
    """

    total_price = 0
    table = Table(
        title=f"{Fore.YELLOW}Total {type_report}{Fore.RESET}", show_lines=False
    )
    with open(file) as opened_file:
        reader = csv.DictReader(opened_file)
        table.add_column("product_name")
        table.add_column("sell_price")

        for row in reader:

            sell_date = date.fromisoformat(row["sell_date"])
            sell_price = float(row[price])
            current_fake_date = date.fromisoformat(read_fake_date())

            if args.today:
                if current_fake_date == sell_date:
                    total_price += sell_price
                    table.add_row(
                        row["product_name"],
                        row["sell_price"],
                    )
            if args.yesterday:
                sell_date_delta = sell_date - current_fake_date
                if sell_date_delta.days == -1:
                    total_price += sell_price
                    table.add_row(
                        row["product_name"],
                        row["sell_price"],
                    )
            if args.day:
                target_date_string = date.fromisoformat(args.day)
                if target_date_string == sell_date:
                    total_price += sell_price
                    table.add_row(
                        row["product_name"],
                        row["sell_price"],
                    )
            if args.month:
                sell_year = sell_date.year
                target_year = args.month.year
                sell_month = sell_date.month
                target_month = args.month.month
                if sell_year == target_year and sell_month == target_month:
                    table.add_row(
                        row["product_name"],
                        row["sell_price"],
                    )
                    total_price += sell_price
    if type_report == "revenue":
        console.print(table)
        if args.today:
            print(f"The {type_report} for today is €{total_price}")
        if args.yesterday:
            print(f"The {type_report} for yesterday is €{total_price}")
        if args.day:
            print(f"The {type_report} for {args.day} is €{total_price}")
        if args.month:
            print(
                f"The {type_report} for {args.month.strftime('%B')}, {args.month.strftime('%Y')} is €{total_price}"
            )
    if args.print:
        console.save_text(os.path.join(log_dir, report_file))

    return total_price


def get_revenue(args):
    revenue = get_total_price(args, "sell_price", sold_file, "revenue")
    return revenue


def get_expenses(args):
    expenses = get_total_price(args, "buy_price", sold_file, "expenses")
    return expenses


def get_profit(args):
    # niet get_revenue - get_expenses gebruikt, omdat er dan dubbel wordt geprint naar de console
    total_profit = get_total_price(
        args, "sell_price", sold_file, "profit"
    ) - get_total_price(args, "buy_price", sold_file, "profit")

    if args.today:
        print(f"The profit for today is €{total_profit}")
    if args.yesterday:
        print(f"The profit for yesterday is €{total_profit}")
    if args.day:
        print(f"The profit for {args.day} is €{total_profit}")
    if args.month:
        print(
            f"The profit for {args.month.strftime('%B')}, {args.month.strftime('%Y')} is €{total_profit}"
        )


def display_expired(args):
    """
    prints a table of expired products to the console.
    expired means in this case, if the expiration date is less than the current 'fake date'
    from the date.txt file.
    If args.print is True, exports the printed table to expired_items.txt
    """
    table = Table(title=f"{Fore.YELLOW}Expired Products{Fore.RESET}", show_lines=False)

    with open(bought_file) as bought_csv:

        reader = csv.DictReader(bought_csv)
        current_date = date.fromisoformat(read_fake_date())

        table.add_column("product name")
        table.add_column("buy price")
        table.add_column("buy date")
        table.add_column("expiration date")

        for row in reader:
            exp_date = date.fromisoformat(row["expiration_date"])

            if current_date > exp_date:
                table.add_row(
                    row["product_name"],
                    row["buy_price"],
                    row["buy_date"],
                    row["expiration_date"],
                )
        console.print(table)
        if args.print:
            console.save_text(os.path.join(log_dir, "expired_items.txt"))
