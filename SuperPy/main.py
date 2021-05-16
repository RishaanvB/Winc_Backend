"""
This script can be used to keep track of various data within
an inventory system of items. 
Possible usages are buying and selling of items,
advancing time,checking revenue and profit over certain period of time.
Also able to print out and export various data.
"""
# Imports
import argparse
import descriptions as d
from core_func import (
    buy_product,
    sell_product,
    handle_product_list,
    handle_inventory,
    get_revenue,
    get_profit,
    display_expired,
)
from helper_func import (
    create_log_dir,
    date_input_checker,
    read_productlist_csv,
    read_fake_date,
    set_fake_date,
    range_checker,
    convert_to_timestr,
)


# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"

# Your code below this line.


def main():
    create_log_dir()  # creates and/or checks necessary folders
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description=__doc__,
        epilog=d.parser_epilog,
    )
    parser.set_defaults(func=None)

    subparsers = parser.add_subparsers(
        dest="subparser_name",
        description=d.subparsers,
    )

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
        conflict_handler="resolve",
    )
    subparser_time = subparsers.add_parser(
        "time",
        formatter_class=argparse.RawTextHelpFormatter,
        description=d.subparser_time,
    )
    subparsers_report = subparser_report.add_subparsers()

    # ==========Arguments for BUY subparser===========

    subparser_buy.add_argument(
        "product_name",
        choices=read_productlist_csv(),
        metavar="name [products]",
        help="set product name",
    )
    subparser_buy.add_argument(
        "price", type=float, metavar="buy price", help="set product buy price"
    )
    subparser_buy.add_argument(
        "-e",
        "-exp",
        "--expirydate",
        metavar="expiration date",
        default="2100-01-01",
        type=date_input_checker,
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
        type=date_input_checker,
        metavar="product buy date",
        help="set buy date. (default: 'today')",
    )

    # ==========Arguments for SELL subparser===========

    subparser_sell.add_argument(
        "product_name",
        choices=read_productlist_csv(),
        metavar="name [product]",
        help="set product name",
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
        metavar="expand product list",
        help="expand available list of products",
    )
    list_group.add_argument(
        "--remove",
        "-rm",
        type=str,
        metavar="subtract product list",
        help="subtract from available list of products",
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
        "--sold", "-sld", "-sl", help="displays sold products", action="store_true"
    )
    inventory_group.add_argument(
        "--product",
        "-p",
        help="displays single product inventory",
    )
    subparser_inventory.add_argument(
        "--print", action="store_true", help="prints inventory table to file"
    )
    subparser_inventory.add_argument(
        "--export", "-x", action="store_true", help="exports inventory to .csv file"
    )

    subparser_inventory.add_argument(
        "--yesterday", "-y", action="store_true", help="get yesterday inventory"
    )

    # ==========Arguments for REPORT subparser===========

    report_group = subparser_report.add_mutually_exclusive_group()
    report_group.add_argument(
        "--today", "-t", action="store_true", help="displays report for today"
    )
    report_group.add_argument(
        "--yesterday", "-y", action="store_true", help="displays report for yesterday"
    )
    report_group.add_argument("--day", "-d", help="displays report for date")
    report_group.add_argument(
        "--month",
        "-m",
        type=convert_to_timestr,
        help="displays report for entire month",
    )
    subparser_report.add_argument(
        "--print", action="store_true", help="exports table to .txt file"
    )

    revenue = subparsers_report.add_parser(
        "revenue",
        parents=[subparser_report],
        conflict_handler="resolve",
        description=d.subparser_revenue,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    profit = subparsers_report.add_parser(
        "profit",
        parents=[subparser_report],
        conflict_handler="resolve",
        description=d.subparser_profit,
        formatter_class=argparse.RawTextHelpFormatter,
    )

    # ==========Arguments for ADVANCE TIME parser===========
    subparser_time.add_argument("time", help="change time in days", type=int)

    # function defaults for subparser arguments
    subparser_buy.set_defaults(func=buy_product)
    subparser_sell.set_defaults(func=sell_product)
    subparser_list.set_defaults(func=handle_product_list)
    subparser_inventory.set_defaults(func=handle_inventory)
    subparser_time.set_defaults(func=set_fake_date)
    subparser_report.set_defaults(func=display_expired)
    revenue.set_defaults(func=get_revenue)
    profit.set_defaults(func=get_profit)

    args = parser.parse_args()
    print(args)
    if args.func:
        args.func(args)  # calls appropiate function for subparser args


if __name__ == "__main__":
    main()
