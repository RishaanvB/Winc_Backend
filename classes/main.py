# Do not modify these lines
__winc_id__ = "04da020dedb24d42adf41382a231b1ed"
__human_name__ = "classes"

# Add your code after this line

# part 1
import math


class Player:
    def __init__(self, name, speed, endurance, accuracy):
        self.name = name
        self.speed = speed
        self.endurance = endurance
        self.accuracy = accuracy
        if not 0 < self.speed <= 1:
            raise ValueError("1st argument: 'speed' needs to be between 0 and 1")
        if not 0 < self.endurance <= 1:
            raise ValueError("2nd argument: 'endurance' needs to be between 0 and 1")
        if not 0 < self.accuracy <= 1:
            raise ValueError("3d argument: 'accuracy' needs to be between 0 and 1")

    def introduce(self):
        return f"Hello everyone, my name is {self.name}."

    def strength(self):
        def get_2nd_el(el):
            return el[1]

        return max(
            ("speed", self.speed),
            ("endurance", self.endurance),
            ("accuracy", self.accuracy),
            key=get_2nd_el,
        )


# part 2


class Commentator:
    def __init__(self, name):
        self.name = name

    def sum_player(self, player):
        sum = math.fsum([player.speed, player.endurance, player.accuracy])
        return sum

    def compare_players(self, player_1, player_2, attr):
        def get_2nd_el(el):
            return el[1]

        player_1_stat = getattr(player1, attr)
        player_2_stat = getattr(player2, attr)
        player_1_name = getattr(player1, "name")
        player_2_name = getattr(player2, "name")
        if player_1_stat != player_2_stat:

            max_stat = max(
                (player_1_name, player_1_stat),
                (player_2_name, player_2_stat),
                key=get_2nd_el,
            )
            return max_stat

        elif getattr(player_1, "speed") > getattr(player_2, "speed"):
            return player_1.name
        elif getattr(player_1, "speed") < getattr(player_2, "speed"):
            return player_2.name
        else:
            player_1_sum = (player_1.name, self.sum_player(player_1))
            player_2_sum = (player_2.name, self.sum_player(player_2))
            if player_1_sum[1] == player_2_sum[1]:
                return "These two players might as well be twins!"
            else:
                player_with_most_points = max(
                    player_1_sum, player_2_sum, key=get_2nd_el
                )
                return player_with_most_points[0]


player1 = Player("player1", 0.5, 0.5, 0.7)
player2 = Player("player2", 0.5, 0.3, 0.7)
print(player1.strength(), "strength")
comment = Commentator("John")
print(comment.compare_players(player1, player2, "speed"))