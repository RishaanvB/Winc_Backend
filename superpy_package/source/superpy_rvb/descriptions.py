from colorama import Fore

parser_epilog = "epilogue superpy"
parser_epilog = f"""
{Fore.YELLOW}           |
      \    |   /
       \      /
         ,000,           .,
 (')-")_ 00000 ---   ;';'  ';'.
('-  (. ')000'      ';.,;    ,;
 '-.(___)'     \       '.';.'
           |    \ 
           |{Fore.RESET}
 ____                                         ____
/\  _`\                                      /\  _`\ 
\ \,\L\_\    __  __   _____      __    _ __  \ \ \L\ \ __  __
 \/_\__ \   /\ \/\ \ /\ '__`\  /'__`\ /\`'__\ \ \ ,__//\ \/\ \ 
   /\ \L\ \ \ \ \_\ \\ \ \L\ \/\  __/ \ \ \/   \ \ \/ \ \ \_\ \ 
   \ `\____\ \ \____/ \ \ ,__/\ \____\ \ \_\    \ \_\  \/`____ \ 
    \/_____/  \/___/   \ \ \/  \/____/  \/_/     \/_/   `/___/> \ 
                        \ \_\                              /\___/
                         \/_/                              \/__/

{Fore.BLUE}_.~"(_.~"(_.~"(_.~"(_.~"(_.~"(_.~"(_.~"(_.~"(_.~"(_.~"(_.~"(_.~"{Fore.RESET}
                                                            v1.00
"""


subparsers = f"""
Subcommands used for various situations
<buy>           buy product
<sell>          sell product
<list>          update/check list of available products to sell/buy
<inventory>     check inventory 
<report>        report revenue/profit/expiration date
  <revenue>     report subcommand to display revenue
  <profit>      report subcommand to display profit                
<time>          change 'internal' time

{Fore.YELLOW}For more details on the subcommands, check '%(prog)s <subcommand> -h'{Fore.RESET}
"""

subparser_buy = f"""
Subcommand to buy products. 
Bought products will be written to bought.csv file.
Product name and the buy price are mandatory, where product has to be chosen
from a pre-defined list of available products. This list can be changed.
Check '<program> list -h' for more information on this list.
Price can be an integer of float.
{Fore.YELLOW}For 'fake' purposes, products bought are instantly available and there is no transport time.{Fore.RESET}

Optionals include:
  --expirydate    | has to be in format 'YYYY-MM-DD', defaults to 2100-01-01
  --amount        | amount to be purchased, choose between 1-10.
  --date          | set buy date of product, format should be in 'YYYY-MM-DD', defaults to internal current day.  
"""


subparser_sell = """
Subcommand to sell products.
Sold products will be written to sold.csv file.
Product name and the buy price are mandatory, where product has to be chosen
from a pre-determined list of available products. 
To see the product list check '<program> list'.
Price can be an integer of float.


Optionals include:
  --amount        | amount to be sold, choose between 1-10.
"""

subparser_list = """Subcommand to update the list of
available products for purchase/sale. 
The list is already pre-occupied with several items to get you started.
You can expand or remove items from the list with the optional arguments.
When no arguments are chosen, it will print out
an alphabetical list of currently available products.
Duplicates are not allowed. The argument will be converted to all lower case. 


Optionals include:
  --add        | item to be added to the list
  --remove     | item to be removed to the list
  """

subparser_inventory = """Subcommand to display an inventory depending on the arguments used.
The specific inventory will be printed to the console as table form.
Arguments can not be used together, except for the combination:
--short --yesterday.

The --product argument needs a flag, which should be the individual product to be displayed.
For example: '%(prog)s --product orange', will print out the current inventory for the orange product.
The optional --print argument needs no flags and can be used with any other optional.
It will export the printed table to an inventory.txt file.
  """

subparser_report = f"""Subcommand to get a report of various data. 
When only '%(prog)s' is given, will display a table of expired products.

Has two subcommands:
<revenue>
<profit>

Both subcommands accept same optional arguments and print out a table
of revenue/profit over a specific time depending on the optional arguments given.

{Fore.YELLOW}For more details on the optional arguments check '%(prog)s <subcommand> -h'{Fore.RESET} 
"""


subparser_revenue = """
Displays the revenue for a specific time depending on the optional arguments given.
When no optionals are given, prints out an empty table.

Optional arguments include:
--today:        needs no flags, displays revenue for today
--yesterday:    needs no flags, displays revenue for yesterday
--day:          needs a flag in format 'YYYY-MM-DD' and displays revenue for that day
--month:        needs a flag in format 'MMM/YY' where 'MMM'
                is the month's first three characters and 'YY'
                are last 2 digits of the year. Where it will display revenue
                for the month 'MMM' in year '20YY'
                For example:
                '%(prog)s apr/20'
--print         Will export the table printed out to the terminal as a 'report.txt' file

Optional arguments can not be use together, except for --print argument.

"""


subparser_profit = """
Displays the profit for a specific time depending on the optional arguments given.
When no optionals are given, prints out an empty table.

Optional arguments include:
--today:        needs no arguments, displays profit for today
--yesterday:    needs no arguments, displays profit for yesterday
--day:          accepts date in format 'YYYY-MM-DD' and displays profit for that day
--month:        accepts date in format 'MMM/YY' where 'MMM'
                is the month's first three characters and 'YY'
                are last 2 digits of the year. Where it will display profit
                for the month 'MMM' in year '20YY'
                For example:
                '%(prog)s apr/20'
--print         Will export the table printed out to the terminal as a 'report.txt' file

Optional arguments can not be use together, except for --print argument.

"""

subparser_time = """Subcommand used to change the internal date the program has.
Initial date will be the local date and when changed will 'remember' the date set.
Accepts positive and negative integer values,
where the integer determines how the date will be changed.
Positive values will set time in days to the 'future'. 
Negative values will set time in days to the 'past'.
"""