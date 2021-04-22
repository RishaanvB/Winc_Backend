from datetime import date, timedelta
import os
import csv
import argparse
import sys
import datetime as dt
from colorama import Fore, Back

from helper_var import (
    log_dir,
    log_txt_file,
    csv_bought,
    fieldnames_bought,
    csv_sold,
    fieldnames_sold,
    product_list_csv,
    date_file,
)


# Helper functions


def create_log_dir():
    """
    If it doesn't exists, creates a new folder with necessary files
    in the current working directory.
    If the folder already exist,
    checks if there is a specific .txt file in the folder.
    If the .txt file can't be found, program will terminate with error message.
    """

    if log_dir in os.listdir():
        if log_txt_file not in os.listdir(log_dir):
            raise FileExistsError(
                f"""
{Back.RED}!!!WARNING!!!{Back.RESET}{Back.RED}!!!WARNING!!!{Back.RESET}{Back.RED}!!!WARNING!!!{Back.RESET}


Directory '{log_dir}' already exist,
but could not find necessary {log_txt_file} file,
Either you already have an existing '{log_dir}' directory, 
or you may have deleted the necessary {log_txt_file} file!!!
You can try the following:

{Fore.YELLOW}1. Remove '{log_dir}' folder in current directory.
2.Create a new {log_txt_file} file inside the {log_dir} folder. {Fore.RESET}

The program will quit now. Bye!!!


{Back.RED}!!!WARNING!!!{Back.RESET}{Back.RED}!!!WARNING!!!{Back.RESET}{Back.RED}!!!WARNING!!!{Back.RESET}
"""
            )
            sys.exit()

    if log_dir not in os.listdir():
        os.mkdir(log_dir)

        # creates text file with current date
        with open(os.path.join(log_dir, date_file), "w") as date_txt:
            date_txt.write(f"{dt.date.today()}")

        # creates 'check' file.
        with open(os.path.join(log_dir, log_txt_file), "w") as file_log:
            file_log.write(
                f"""created file for first time at {dt.datetime.now()}
            WARNING!!! Do NOT remove this file."""
            )

        # creates bought.csv file
        with open(os.path.join(log_dir, csv_bought), "w", newline="") as bought:
            writer = csv.DictWriter(bought, fieldnames=fieldnames_bought)
            writer.writeheader()

        # creates sold.csv file
        with open(os.path.join(log_dir, csv_sold), "w", newline="") as sold:
            writer = csv.DictWriter(sold, fieldnames=fieldnames_sold)
            writer.writeheader()

        # creates product list file (can buy/sell product if in this list)
        """
        reden voor deze was eigenlijk dat je niet zomaar elk product wat je wilt hebben kunt
        'bestellen' als supermarkt van de 'leverancier'
        """
        with open(product_list_csv, "w", newline="") as p_lst:
            writer = csv.writer(p_lst)
            # volgende writerows om alvast producten te hebben om te kopen/verkopen,
            # zodat je geen producten hoeft aan te maken
            writer.writerow(["eggs"])
            writer.writerow(["milk"])
            writer.writerow(["bread"])
            writer.writerow(["water"])
            writer.writerow(["orange"])


def date_input_checker(date_string):
    return date.fromisoformat(date_string)


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
    and returns it as a string.
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
    Will always print the current and the new date.
    """
    print("Previous date was-->", read_fake_date())
    date_file_location = os.path.join(log_dir, date_file)
    time_days = int(args.time)
    advance_days = timedelta(days=time_days)
    current_date = date.fromisoformat(read_fake_date())
    new_date = current_date + advance_days
    new_date = date.isoformat(new_date)
    with open(date_file_location, "w") as new_date_file:
        new_date_file.write(new_date)
    print("Current date is-->", read_fake_date())


def range_checker(num):
    """
    converts num to int and if num not in range 0-10,
    ArgumentTypeError will be raised.
    Only use for this function is to return a replacement error
    for the builtin error message for the add_argument() method in argparse
    for the kwarg choices.
    """
    num = int(num)
    if num not in list(range(1, 11)):
        raise argparse.ArgumentTypeError("should be between 1 and (including) 10")
    return num


def convert_to_timestr(time_str):
    """
    converts string into a datetime object if argument passed to function corresponds to
    format 'string-num' where string is month in 3 characters and num is a 2 digit num.
    example: jan/20 will be converted to datetime obj: datetime.date(2020, 1, 1)
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