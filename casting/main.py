# Do not modify these lines
__winc_id__ = '62311a1767294e058dc13c953e8690a4'
__human_name__ = 'casting'

# Add your code after this line

# 1
leek_price = 2
leek_string = str(leek_price)
print("Leek is " + leek_string + " euro per kilo."  )

# 2
leek_order = "leek 4"
price = int(leek_order[leek_order.find("4"):])
sum_total  = price * leek_price
print(sum_total)

# 3
broccoli_price = 2.34
broccoli_order = "broccoli 1.6"
broccoli_order_kg = float(broccoli_order[broccoli_order.find(" "):])
broccoli_total_price = broccoli_price * broccoli_order_kg
# print(broccoli_total_price)
rounded_total_price = round(broccoli_total_price, 2)
# print(rounded_total_price)
stringified_order = str(broccoli_order_kg) + "kg broccoli costs " + str(rounded_total_price) + "e."
print(stringified_order)
print("something")
print("something")
print("something")
print("something")