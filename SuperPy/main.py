# Imports
import argparse
import csv
from datetime import date
from rich.console import Console

import descriptions as d  # mss onduidelijk als d, maar waar ze worden gebruikt, maakt het duidelijk genoeg hoop ik
from helper_func import (
    create_log_dir,
    buy_product,
    sell_product,
    handle_product_list,
    handle_inventory,
    read_productlist_csv,
    handle_report,
    range_checker,
    handle_revenue,
    handle_profit,
    read_fake_date
)

import colorama
from colorama import Fore, Back, Style

# even uitzoeken hoe coloroma precies werkt!!!!!!!!!
# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"


# Your code below this line.
def main():
    create_log_dir()  # creates and/or checks necessary folders
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description=d.parser,
        epilog=d.parser_epilog,
    )
    parser.set_defaults(func=None)

    subparsers = parser.add_subparsers(
        help=f"help message {Fore.RED}for{Fore.RESET} subparsers",  # wijzigen
        dest="subparser_name",
        description=d.subparsers,
    )
    # or use nargs = ? to read/write to external file!!!

    # ======= SUBPARSER commands========
    subparser_buy = subparsers.add_parser(
        "buy",
        formatter_class=argparse.RawTextHelpFormatter,
        description=d.subparser_buy,
    )
    subparser_sell = subparsers.add_parser(
        "sell",
        formatter_class=argparse.RawTextHelpFormatter,
        description=d.subparser_sell,
    )
    subparser_list = subparsers.add_parser(
        "list",
        formatter_class=argparse.RawTextHelpFormatter,
        description=d.subparser_list,
    )
    subparser_inventory = subparsers.add_parser(
        "inventory",
        formatter_class=argparse.RawTextHelpFormatter,
        description=d.subparser_inventory,
    )
    subparser_report = subparsers.add_parser(
        "report",
        formatter_class=argparse.RawTextHelpFormatter,
        description=d.subparser_report,
        add_help=False,
    )
    subparsers_report = subparser_report.add_subparsers()

    # ==========Arguments for BUY subparser===========

    subparser_buy.add_argument(
        "product_name",
        choices=read_productlist_csv(),
        metavar="name [product]",
        help="set product name from list",
    )
    subparser_buy.add_argument(
        "price", type=float, metavar="buy price", help="set product buy price"
    )
    subparser_buy.add_argument(
        "-e",
        "-exp",
        "--expirydate",
        required=False,
        metavar="expiration date",
        default="2100-01-01",
        help="set product expiration date (default: 2100-01-01)",
    )
    subparser_buy.add_argument(
        "-a",
        "--amount",
        default=1,
        type=range_checker,
        metavar="product amount",
        help="set amount of product to be purchased (default: 1)",
    )
    subparser_buy.add_argument(
        "-d",
        "--date",
        default=read_fake_date(),
        # type=range_checker,   # kan ik een functie neerzetten die hem automatisch format
        metavar="product amount",
        help="set amount of product to be purchased (default: 1)",
    )

    # ==========Arguments for SELL subparser===========

    subparser_sell.add_argument(
        "product_name",
        choices=read_productlist_csv(),
        metavar="name [product]",
        help="set product name from list",
    )

    subparser_sell.add_argument(
        "price", type=float, metavar="sell price", help="set product sell price"
    )
    subparser_sell.add_argument(
        "--amount",
        "-a",
        type=range_checker,
        default=1,
        metavar="product amount",
        help="set amount of product to be sold (default: 1)",
    )

    # ==========Arguments for LIST subparser===========

    list_group = subparser_list.add_mutually_exclusive_group()
    list_group.add_argument(
        "--add",
        "-a",
        type=str,
        metavar="list to expand",
        help="expand available list of products",
    )
    list_group.add_argument(
        "--remove",
        "-rm",
        type=str,
        metavar="list to shorten",
        help="shorten available list of products",
    )

    # ==========Arguments for INVENTORY subparser===========
    inventory_group = subparser_inventory.add_mutually_exclusive_group()
    inventory_group.add_argument(
        "--short",
        "-s",
        help="displays short inventory",
        action="store_true",
    )
    inventory_group.add_argument(
        "--long", "-l", help="displays long inventory", action="store_true"
    )
    inventory_group.add_argument(
        "--dumped", "-dump", "-d", help="displays sold products", action="store_true"
    )
    subparser_inventory.add_argument(
        "--product",
        "-p",
        help="displays product inventory",
    )
    subparser_inventory.add_argument(
        "--print", action="store_true", help="prints inventory table to file"
    )
    # ==========Arguments for REPORT subparser===========
    
    # all arguments will be passed to revenue/profit subparsers
    report_group = subparser_report.add_mutually_exclusive_group()
    report_group.add_argument("--today", "-t", action="store_true", help="displays report for today")
    report_group.add_argument("--yesterday", "-y", action="store_true", help="displays report for yesterday")
    report_group.add_argument("--date", help="sets date to display report")

    revenue = subparsers_report.add_parser("revenue", parents=[subparser_report])
    profit = subparsers_report.add_parser("profit", parents=[subparser_report])

    # function defaults for subparser arguments
    subparser_buy.set_defaults(func=buy_product)
    subparser_sell.set_defaults(func=sell_product)
    subparser_list.set_defaults(func=handle_product_list)
    subparser_inventory.set_defaults(func=handle_inventory)
    subparser_report.set_defaults(func=handle_report)
    revenue.set_defaults(func=handle_revenue)
    profit.set_defaults(func=handle_profit)

    args = parser.parse_args()
    # if args.func:     # met errors even kijken of deze weer terug moet, weet niet meer waarom ik de if statement heb neergezet..
    # args.func(args)  # calls appropiate function for subparser args
    args.func(args)
    print(args)


if __name__ == "__main__":
    main()
