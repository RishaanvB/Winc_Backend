# Do not modify these lines
__winc_id__ = '71dd124b4a6e4d268f5973db521394ee'
__human_name__ = 'strings'

# Add your code after this line

# Part 1
scorer = "Ruud Gullit"
scorer2 = "Marco van Basten"
goal_0 = 32
goal_1 = 54
scorers = scorer + " " + str(goal_0) + ", " + scorer2 + " " + str(goal_1)
# report = f"{scorer} scored in the {goal_0}nd minute\n{scorer2} scored in the {goal_1}th minute"
report = f"{scorer} scored in the {goal_0}th minute\n{scorer2} scored in the {goal_1}th minute"
print(report)
print(type(report))
# Part 2
player = "Frank Rijkaard"
first_name = player[0:player.find(" ")]
last_name_len = len(player[player.find(" "): -1])
name_short = player.replace(player[0:player.find(" ")], player[:1] + ".")
chant = (first_name + "! ") * (len(first_name) - 1) + (first_name + "!")
good_chant = chant[-1] != " "
player = "Marco van Basten "
first_name = player[0:5]

# chant = (len(first_name)) * (player[-1] + first_name + "!")
print(chant)