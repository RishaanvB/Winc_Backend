# SuperPy

Superpy is a Python script for various usage of maintaining and updating an inventory of custom items that are used for an 'imaginary' supermarket.

With the Superpy script you can add or remove products to/from an inventory, set buy and sell prices for said products.

It also supports advancing or setting back time.
For fake purposes of the program, when items are 'bought', ie. added to the inventory, they will instantly be available in the inventory, ignoring real-life possible transport time between supplier and supermarket.  
Superpy uses the Rich library to print out some tables to the console.

## Compatibility

Superpy has only been tested on Windows 10 on Python v3.9. If it does not work, use the original repo, found here:

https://github.com/RishaanvB/Winc_Backend/tree/main/SuperPy

## Installing

Install with `pip` .

```
pip install -i https://test.pypi.org/simple/ superpy-rvb==0.1.2
```

Run the following code to test Superpy output on your terminal:

```
superpy
```

It should add a folder `superpy_logs` in the directory where you input this code in the terminal.
In `superpy_logs` folder, several files will be created and if, at any time you use the
`--print` command, exported files will be put in this folder.

## Superpy Subcommands

There are several subcommands that you can use with Superpy. We will discuss all of them  
and for each subcommand there will be atleast one example to show how the command works.
To see what is available you can use the `-h` flag after any subcommand to see the available options and what the subcommand does.

## Buy

Handles the buying of products.

## Sell

Handles the selling of products.

## List

Handles the available products from the 'imaginary supplier' of the supermarket you.

## Inventory

Prints out table to the console depending on optional arguments.

## Report

Handles revenue, profit for certain time spans and is able to print out a table of expired products.

### Click the following headings for details on the different subcommands:

<details>
<summary>Buy</summary>

## Superpy Buy

The buy command is used to buy products and add them to your inventory.  
You can also set the expiration date, the amount products you'd like to buy and the date on which you want to buy the product.
The `product name` and the `price` are both mandatory.

The `product name` should be a name available from the list of available products. To get you started the list is already pre-occupied with several items. To update this list, you can use the `list` subcommand. We will discuss this later.
The minimum commands required could look like this:

```python
superpy buy orange 1.5
```

This will 'buy' an orange for the price of 1.5. The `price` can either be a float or an integer.  
If a product is chosen not available in the list, it will produce an error message where you can see the products you must choose from.

Optional commands include:

Setting the expiration can be done with the `-e` flag, where the date should be in the format `yyyy-mm-dd`. It defaults to '2100-01-01' if it's not chosen.  
The product amount can be set with the `-a` flag where the max number of products is 10 per command.  
The `-d` flag sets the date on which you want to buy the product, if you want to buy something not on the current internal date. This defaults to what the program perceives as 'today'. This can be changed with the `time` subcommand. More on this later.

Possible buy commands in combination with optional flags could look like this:

```
superpy buy orange 2 -e 2000-12-04 -a 15
```

or

```
superpy buy milk 5 -a 10 -d 200-04-20
```

</details>

<details>
<summary>Sell</summary>

## Superpy Sell

The `sell` command operates in the same way as the `buy` command, with a few differences.  
The `product name` and the `price` are mandatory, the only optional flag is the `-a`. Which sets the amount you wish to sell.
Possible inputs could look like this:

```
superpy sell orange 3
```

```
superpy sell milk 3 -a 5
```

</details>

<details>
<summary>List</summary>

## SuperPy List

The product list consists of available products you are able to buy and/or sell. If a product is not in this list, using the `buy` or `sell` command will output an error message.  
To get you started the list is already pre-occupied with some items.

To view the list just go to:

```
superpy list
```

This will print an alphabetical list of products available.

This list is not an inventory and should not be consideres as one. Its only function is there to see what kind of products the 'imaginative' supplier has to offer.

### Adding or Removing products from the list

You can either `add` or `remove` items from the list. Inputs will be converted to all lowercase. If trying to `add` a product which is already in the list, it will produce an error. The same goes for trying to `remove` a product which is not in the list.
When removing or adding something the console will print out the newly created list and the product which has been removed/added. Both flags `-a` and `-r` can't be used in the same command.

To add an item to the list:

```
superpy list -a chocolate
```

To remove an item from the list:

```
superpy list -r chocolate
```

</details>

<details>
<summary>Inventory</summary>

## Superpy Inventory

With the `inventory` command you can check your inventory of items in various ways,
but in essence all commands should be given like:

```
superpy inventory '-flag'
```

Depending on the `flag` being used it will print out a different table to the console.
All flags are mutually exclusive and can't be used together, except for the `--print` flag.
There are four different ways to get an overview of your inventory:
`--short, --long, --sold and --product.`

```
superpy inventory --short
```

Will print out a table with minimum details. If there are zero items in stock, the row will be colored red.

```
superpy inventory --long
```

Will print out a more detailed table of all the products in stock.

```
superpy inventory --sold
```

Prints out a table of sold products on that day.

```
superpy inventory --product orange
```

Prints out a table of the inventory ofa single product specified as argument for the `--product` flag. In the example above, it will print out the specifics for the 'orange' product.

It is possible to check the inventory of what the program perceives as 'yesterday' by using `--yesterday` with the `--short` argument.

```
superpy --yesterday --short
```

Note: The `--yesterday` argument will not work in combination with any other argument except for the `--short` argument.

### Exporting inventory

You can export the printed out table to a `.txt` file by adding the `--print` to the command line. The result will be exported to a `inventory.txt` file, that can be found in the `superpy_logs` folder. It will not create new files for each report, but instead will overwrite it, if the `inventory.txt` already exists

</details>

<details>
<summary>Report</summary>

## Report

Using only the `report` subcommand will result in a printed out table to the console of expired products.

```
superpy report
```

Both the profit and revenue commands work in the exact same way. The only difference is the result.
They are used in combination with a flag corresponding with a specific time period.
Revenue will print the revenue and profit will print out the profit.

Both revenue and profit have to be used in combination with one of the following flags. If no flags are given, it will just print out an empty table with no information.

--today  
--yesterday  
--day  
--month

Both `--today` and `--yesterday` don't need any other flags or arguments, and will print out the desired information for today or yesterday.  
 Example uses of these two are:

```
superpy report revenue --today
```

or

```
superpy report profit --yesterday
```

The `--day` flag needs a date as an argument in the format: 'yyyy-mm-dd' and prints the revenue or profit for that specific day

```
superpy report profit --day 2020-04-27
```

The `--month` flag needs a date as an argument in the format: 'mmm/yy'.

Where 'mmm' is the month's first three characters and 'yy'
are the last 2 digits of the year. Where it will display revenue
for the month 'MMM' in year '20YY'.

Example uses:

```
superpy report profit --month jun/21
```

Will display the profit for the month June in the year 2021.

### Exporting report

You can export the printed out table to a `.txt` file by adding the `--print` to the command line. The result will be exported to a `report.txt` file, that can be found in the `superpy_logs` folder. It will not create new files for each report, but instead will overwrite it, if the `report.txt` already exists

</details>

<details>
<summary>Time</summary>

## Superpy Time

Superpy has a command where you can set the time the program perceives as the current time.
It will be saved in a file, located in the `superpy_logs` folder. On program exit the `time` last changed settings will be saved and used. So keep in mind when previously changing the time, it will not reset the 'internal' time to the real current date.

For example:  
If you have set the time to be a tuesday when it is in reality a monday, restart the console, it will still think the day is tuesday.

Changin the 'internal' time can be done with the subcommand `time` and an integer an argument, where the integer is how many `days` you want to change the 'internal' time. Negative values will mean the program goes back in time. If you specify `0` as the argument, the program will only display the current 'internal' time.

The following example sets the time forward 7 days:

```
superpy time 7
```

</details>  
  
### Note:    
  
Most, if not all, arguments have a shorter version of the flags. These are not displayed here, but can be viewed when checking out the `--help` section of each subcommand.
