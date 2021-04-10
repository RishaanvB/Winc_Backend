
parser_epilog = "epilogue superpy"
# parser_epilog = """
#            |
#      \     |     /
#        \       /
#          ,000,           .,
#  (')-")_ 00000 ---   ;';'  ';'.
# ('-  (. ')000'      ';.,;    ,;
#  '-.(___)'     \       '.';.'
#            |    \ 
#            |
#  ____                                         ____               
# /\  _`\                                      /\  _`\             
# \ \,\L\_\    __  __   _____      __    _ __  \ \ \L\ \ __  __    
#  \/_\__ \   /\ \/\ \ /\ '__`\  /'__`\ /\`'__\ \ \ ,__//\ \/\ \   
#    /\ \L\ \ \ \ \_\ \\ \ \L\ \/\  __/ \ \ \/   \ \ \/ \ \ \_\ \  
#    \ `\____\ \ \____/ \ \ ,__/\ \____\ \ \_\    \ \_\  \/`____ \ 
#     \/_____/  \/___/   \ \ \/  \/____/  \/_/     \/_/   `/___/> \ 
#                         \ \_\                              /\___/
#                          \/_/                              \/__/ 

# _.~"(_.~"(_.~"(_.~"(_.~"(_.~"(_.~"(_.~"(_.~"(_.~"(_.~"(_.~"(_.~"
#                                                             v1.00
#     """

subparser_buy_description = f"""

       
        subcommand to purchase products.
        Mandatory arguments are:
            <productname>
            <price>

        <productname> has to be chosen from specific product list.
        To view the product list, see '-ll' or '-ls'

        <price> can be set as either integer or float.

        Optional arguments include:
            <expirationdate>   -e/-exp/-expirydate
            <amount>            -a/-amount

        <expirationdate> argument should be in format:
        'YYYY-MM-DD'
        If omitted, expiration date will be set as 2100-01-01

        <amount> argument accepts only integers.
        If omitted, amount will be set as 1.
        """
