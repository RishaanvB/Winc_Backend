1.  Ik vond het gebruik van de range_checker wel interessant om te doen. Ik wilde eigenlijk de built-in error message van argparse met het gebruik van de keyword argument 'choices' vervangen door iets anders. De normale built-in message weergeeft alle mogelijke opties waaruit je kunt kiezen. Als je bv uit 1000 dingen kan kiezen, zou die die allemaal uitprinten in de error message en zoiets wilde ik voorkomen.

```
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
```

2.  Om te voorkomen dat je mss 'duplicates' kunt kopen/verkopen heb ik een lijst van producten gemaakt, waar je uit kunt kiezen. Dat leek me logisch, aangezien je als supermarkt niet alles zomaar kunt bestellen, je bent afhankelijk van de leverancier voor wat voor producten je kunt inkopen.

Ingekorte versie:

```
def handle_product_list(args):
    """
    Used for updating products_list.csv with custom items.
    List is already pre-occupied with items for quicker use of program.
    Takes in attribute for args, which are 'add' or 'remove'
    and adds or removes the item given from the products_list.csv.
    It will always print out a list of products available from products_list.csv.
    """

    product_list = read_productlist_csv()

    def add_product():
        product = args.add.lower()
        if product in product_list:
            raise ValueError(f"{product} already exist")

        with open(product_list_csv, "a", newline="") as lst:
            writer = csv.writer(lst)
            writer.writerow([product])

    def remove_product():
        product = args.remove.lower()
        if product not in product_list:
            raise ValueError(f"{product} does not exist")

        product_list.remove(product)
        with open(product_list_csv, "w", newline="") as lst:
            writer = csv.writer(lst)
            [writer.writerow([product]) for product in product_list]
```

3.  Voor de inventory vond ik het zelf belangrijk om tenminste een optie te hebben om de inventaris van 1 specifiek product te kunnen laten zien. Een supermarkt heeft veel producten en een 'normale' inventaris van de producten is mss onoverzichtelijk om te lezen.(ben nooit supermarkt manager geweest , dus weet ook niet of dit iets is wat handig zou zijn in het echt :) )
    Vandaar dat ik de optie heb gegeven om van 1 specifiek product de inventaris te laten zien.
    Ingekorte versie van de functie:

```
def product_inventory(file_to_open=bought_file):
        """
        Reads through bought.csv and creates an inventory list for specified product
        with table columns: [buy_price, buy_date, expiration_date]
        and prints it in table form to the console.
        Output depends on input of kwarg file_to_open. Default kwarg is bought_file
        """
        count = 0
        product = args.product
        with open(file_to_open) as csv_read:
            reader = csv.DictReader(csv_read)
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
```
