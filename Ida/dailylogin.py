from datetime import date


class DailyLogin:

    def __init__(self, player_records):
        self.player_records = player_records
        self.reward = 10

    def claim(self, player_name):

        player = self.player_records.get_player(player_name)

        if player is None:
            return False, 0

        today = str(date.today())

        if player.get("last_claim", "") == today:
            return False, player.get("coins", 0)

        player["coins"] = player.get("coins", 0) + self.reward
        player["last_claim"] = today

        self.player_records.save_data()

        return True, player["coins"]