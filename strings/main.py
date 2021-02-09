# Do not modify these lines
__winc_id__ = '71dd124b4a6e4d268f5973db521394ee'
__human_name__ = 'strings'

# Add your code after this line

# Part 1
name_scorer = "Ruud Gullit"
name_scorer2 = "Marco van Basten"
goal_0 = 32
goal_1 = 54
scorers = name_scorer + " " + str(goal_0) + ", " + name_scorer2 + " " + str(goal_1)
report = F"{name_scorer} scored in the {goal_0}nd minute \n{name_scorer2} scored in the {goal_1}th minute"

print(report)
print(type(report))
# Part 2
player = "Frank Rijkaard"
first_name = player[0:player.find(" ")]
last_name_len = len(player[player.find(" "): -1])
name_short = player.replace(player[0:player.find(" ")], player[:1] + ".")
chant = (first_name + "! ") * (len(first_name) - 1) + (first_name + "!")
good_chant = chant[-1] != " "
