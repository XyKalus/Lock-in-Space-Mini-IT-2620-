import os
import json


class PlayerRecords:

    def __init__(self, base_dir):

        self.save_path = os.path.join(
            base_dir,
            "player_data.json"
        )

        self.data = self.load_data()

    def load_data(self):

        if not os.path.exists(self.save_path):
            return {"players": []}

        try:
            with open(self.save_path, "r") as file:
                return json.load(file)

        except (json.JSONDecodeError, FileNotFoundError):
            return {"players": []}


    def save_data(self):

        with open(self.save_path, "w") as file:
            json.dump(
                self.data,
                file,
                indent=4
            )


    def create_player(self, name, gender):

        player = {
            "name": name,
            "gender": gender,
            "coins": 0,
            "study_time": 0,
            "wallpaper": "White and Wood",
            "inventory": []
        }

        self.data["players"].append(player)

        self.save_data()