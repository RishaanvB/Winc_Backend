# Imports
import argparse
import csv
from datetime import date
from rich.console import Console

import descriptions as d  # mss onduidelijk als d, maar waar ze worden gebruikt, maakt het duidelijk genoeg hoop ik
from helpers import create_log_dir, buy_product, sell_product

import colorama
from colorama import Fore, Back, Style

# even uitzoeken hoe coloroma precies werkt!!!!!!!!!
# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"


# Your code below this line.
def main():
    create_log_dir()
    console = Console()
    product_list = ["orange", "bread", "milk", "eggs", "water", "apple", "candy"]

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description=d.parser,
        epilog=d.parser_epilog,
    )
    parser.set_defaults(func=None)
    # show list of available products
    parser.add_argument(
        "-ls", "--list", action="store_true", help="show list of products"
    )

    subparsers = parser.add_subparsers(
        help=f"help message {Fore.RED}for{Fore.RESET} subparsers",
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
        description=d.subparser_sell
    )

    # function defaults for subparser arguments
    subparser_buy.set_defaults(func=buy_product)
    subparser_sell.set_defaults(func=sell_product)

    # ==========Arguments for BUY subparser===========

    subparser_buy.add_argument(
        "product_name",
        choices=product_list,
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
    subparser_buy.add_argument(  # set limiet op aantal zodat je niet 1000X iets kan kopen. met lambda functie??? kijken wat dat is.
        "-a",
        "--amount",
        default=1,
        type=int,
        metavar="product amount",
        help="set amount of product to be purchased (default: 1)",
    )
    # ==========Arguments for SELL subparser===========

    subparser_sell.add_argument(
        "product_name",
        choices=product_list,
        metavar="name [product]",
        help="set product name from list",
    )

    subparser_sell.add_argument(
        "price", type=float, metavar="sell price", help="set product sell price"
    )
    subparser_sell.add_argument(
        "--amount",
        "-a",
        type=int,
        default=1,
        metavar="product amount",
        help="set amount of product to be sold (default: 1)",
    )

    # add report group
    # add revenue group
    # add profit group
    args = parser.parse_args()
    # print(args)

    if args.func:
        args.func(args)         # calls appropiate function for subparser args
    if args.list:
        print(f"There are {len(product_list)} available products for purchase:")
        [print("\t", i, p) for i, p in (enumerate(sorted(product_list), start=1))]


if __name__ == "__main__":
    main()
