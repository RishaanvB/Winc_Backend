import colorama
from colorama import Fore, Back, Style


# parser_epilog = "epilogue superpy"
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

subparser_buy = f"""

<================================================================================>
        
        Subcommand to purchase products.
        Positional arguments are:
            {Fore.YELLOW}<productname>
            <price>{Fore.RESET}

        Optional arguments include:
            {Fore.YELLOW}<expirationdate>{Fore.RESET}    -e/-exp/--expdate
            {Fore.YELLOW}<amount>{Fore.RESET}            -a/-amount
        
<================================================================================>
        
        Where {Fore.YELLOW}<productname>{Fore.RESET} has to be chosen from specific product list.
        To view the product list, see {Fore.BLUE}'%(prog)s -ll' or '%(prog)s -ls'{Fore.RESET}
        
        {Fore.YELLOW}<price>{Fore.RESET} can be set as either integer or float.
        
        {Fore.YELLOW}<expirationdate>{Fore.RESET} argument should be in format: {Fore.BLUE}'YYYY-MM-DD'{Fore.RESET}
        
        Set {Fore.YELLOW}<amount>{Fore.RESET} in integers, 
        where {Fore.YELLOW}<amount>{Fore.RESET} is the amount of products to buy.

<================================================================================>

        {Fore.GREEN}Valid inputs include, but are not restricted to:

        %(prog)s orange 
        %(prog)s orange 2
        %(prog)s orange -e 2012-12-01
        %(prog)s orange -a 30 -e 2012-12-01{Fore.RESET}
               
        {Fore.WHITE}{Back.RED}!!!ATTENTION!!!{Style.RESET_ALL}
        {Fore.RED}If omitted, {Fore.YELLOW}<expirationdate>{Fore.RESET} {Fore.RED}will be set as {Fore.BLUE}2100-01-01{Fore.RESET}
        {Fore.RED}If omitted, {Fore.YELLOW}<amount>{Fore.RESET} {Fore.RED}will be set as {Fore.BLUE}1{Fore.RESET}
  
<================================================================================>
  
        """
parser = f"""
        {Fore.RED}
        Program for keeping {Fore.RESET} track of inventory.
        Possible usages are buying and selling of products,
        advancing time to check inventory at specific dates,
        and checking revenue and profit over certain period of time.
        """

subparsers = """description for all subparsers buy/sell/report etc """ 

subparser_sell = """
description for the sell subparser argument. 
Moet ik nog aan werken 
"""

subparser_list = """subparser description for the list argument""" 
subparser_report = """subparser description for the report argument""" 
subparser_inventory = """subparser description for the inventory argument""" 

