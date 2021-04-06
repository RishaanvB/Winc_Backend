
# display all prodcucts
# display product
    # display amount of product
    # display buy price
    # display sell price
    # display expiry date
        # display if expiry date true/false

# All data must be saved in CSV files

# implement internal naive date
    # advance time with command:
        # --advance-time 2


""""
$ python super.py buy --product-name orange --price 0.8 --expiration-date 2020-01-01
$ python super.py sell --product-name orange --price 2
$ python super.py --advance-time 2
$ python super.py report revenue --today
$ python super.py report profit --today
""""


# adding clear descriptions to each argument
# adding documentation .txt file with examples


# The application must support:
# Setting and advancing the date that the application perceives as 'today';
# Recording the buying and selling of products on certain dates;
# Reporting revenue and profit over specified time periods;
# Exporting selections of data to CSV files;
# Two other additional non-trivial features of your choice, for example:
# The use of an external module Rich to improve the application.
# The ability to import/export reports from/to formats other than CSV (in addition to CSV)
# The ability to visualize some statistics using Matplotlib
# Another feature that you thought of.