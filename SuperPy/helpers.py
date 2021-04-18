import csv
import os.path
import os
import colorama
from colorama import Fore, Back, Style
from colorama import init
import sys
import datetime as dt
from rich.console import Console
from rich.table import Table

# is het verstandig om zoveel globals te hebben?
# product amount kan mss weggelaten worden in fieldnames. is alleen van belang voor aantal writerow()
print(dt.date.today())
log_dir = "superpy_logs"
log_txt_file = "log_id_superpy.txt"


products_file = "products_list.csv"
csv_bought = "bought.csv"
csv_sold = "sold.csv"
bought_file = os.path.join(log_dir, csv_bought)
sold_file = os.path.join(log_dir, csv_sold)
product_list_csv = os.path.join(log_dir, products_file)


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
        # product_list_lst = [
        #     "orange",
        #     "bread",
        #     "milk",
        #     "eggs",
        #     "water",
        #     "apple",
        #     "candy",
        # ]  # placeholder product list
        os.mkdir(log_dir)
        with open(os.path.join(log_dir, "time.txt"), "w") as time_txt:
            time_txt.write(f"{dt.date.today()}")
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
    with open(product_list_csv) as p_file:
        reader = csv.reader(p_file)
        product_list = [row[0] for row in reader]
        return product_list


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
    """Takes in attribute for args, which are 'add' or 'remove'
    and adds or removes the argument given from the list of available products
    It will print out a list of products available for purchase/sell if no args are given.
    """
    # product_list_lst is de default list, zodat je zelf geen producten hoeft aan te maken
    with open(product_list_csv) as lst:
        reader = csv.reader(lst)
        flat_list = [product for sublist in list(reader) for product in sublist]
        # add product to list
        if args.add:
            args.add = args.add.lower()
            if args.add in flat_list:
                raise ValueError(f"{args.add} already exist")

            if args.add not in flat_list:
                with open(product_list_csv, "a", newline="") as lst:
                    writer = csv.writer(lst)
                    writer.writerow([args.add])

        # remove product from list
        if args.remove:
            args.remove = args.remove.lower()
            if args.remove not in flat_list:
                raise ValueError(f"{args.remove} does not exist")

            if args.remove in flat_list:
                flat_list.remove(args.remove)
                with open(product_list_csv, "w", newline="") as lst:
                    writer = csv.writer(lst)
                    [writer.writerow([product]) for product in flat_list]

        if args.add is None and args.remove is None:
            print(f"Total unique products in stock: {len(flat_list)}")
            [print(product) for product in sorted(flat_list)]


def handle_inventory(args):
    """
    handles what kind of table and information will be displayed,
    depending on the attribute of args given, will call
    one of 3 functions.
    1) short_inventory()
    2) product_inventory()
    3) long_inventory()
    4) sold_inventory()
    """
    # er zitten wat overlappingen in de functies die hier inzitten, maar ik wilde ze toch
    # apart houden omdat ik dacht dat het dan overzichtelijker zou zijn, vooral als er bv iets mis
    # zou gaan met een bepaalde functie, dan kon ik makkelijker zien waar ik de fout kan vinden.
    
    def write_table_to_file(txt_data):
        """
        Writes the printed out inventory table to inventory.txt
        If the inventory.txt file already exist it will overwrite it.
        """
        with open(
            os.path.join(log_dir, "inventory.txt"), "w", encoding="utf-8"   #encoding anders kon die bepaalde characters niet decoden.
        ) as inventory:
            inventory.write(txt_data)

    def short_inventory():
        """
        Reads through bought.csv and creates a simple inventory list
        of format: {product: count} and prints it in table form to the console.
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
            txt = console.export_text()
            write_table_to_file(txt)

    # print(simple_inventory)
    def product_inventory():
        count = 0
        product = args.product
        table_columns = ["buy_price", "buy_date", "expiration_date"]
        product_table = Table(
            title=f"{Fore.YELLOW}Product Inventory for {product.title()}{Fore.RESET} ",
            show_lines=True,
        )
        # product_table.add_column()
        with open(bought_file) as bought, open(product_list_csv) as product_list:
            reader_product_list = csv.reader(product_list)
            reader = csv.DictReader(bought)
            flat_list = [
                product for sublist in list(reader_product_list) for product in sublist
            ]

            for header in reader.fieldnames:
                if header in table_columns:
                    product_table.add_column(header)
            for row in reader:
                if row["product_name"] == product:
                    count += 1
                    product_table.add_row(
                        row[table_columns[0]],
                        row[table_columns[1]],
                        row[table_columns[2]],
                    )

        if product not in flat_list:
            raise ValueError(
                f"""Can't find {product}. Check your spelling or if the product is in the available products list"""
            )
        console.print(product_table)
        print(f"{Fore.YELLOW}Total items of {product} in stock: {count}{Fore.RESET} ")
        if args.print:
            txt = console.export_text()
            write_table_to_file(txt)

    def long_inventory():
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
            txt = console.export_text()
            write_table_to_file(txt)

    def sold_inventory():
        print("sold inventory")

    # calling functions depending on args command given
    if args.short:
        short_inventory()
    if args.product:
        product_inventory()
    if args.long:
        long_inventory()
    if args.sold:
        sold_inventory()