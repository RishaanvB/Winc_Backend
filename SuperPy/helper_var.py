
import os


log_dir = "superpy_logs"
log_txt_file = "log_id_superpy.txt"

report_file = "report.txt"
products_file = "products_list.csv"
csv_bought = "bought.csv"
csv_sold = "sold.csv"
bought_file = os.path.join(log_dir, csv_bought)
sold_file = os.path.join(log_dir, csv_sold)
product_list_csv = os.path.join(log_dir, products_file)
inventory_txt = "inventory.txt"
date_file = "date.txt"
fieldnames_bought = [
    "product_name",
    "buy_price",
    "product_amount",
    "buy_date",
    "expiration_date",
]
fieldnames_sold = [
    "product_name",
    "product_amount",
    "buy_price",
    "sell_price",
    "buy_date",
    "sell_date",
    "expiration_date",
]