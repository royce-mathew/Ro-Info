import json
from Roblox import RobloxUser

class DataHandler:
    def __init__(self, file_name: str) -> None:
        with open(file_name) as file:
            user_list = file.read().splitlines()

        try:
            with open("saved_data.json", "r") as json_file:
                json_data: dict = json.load(json_file)
        except (json.JSONDecodeError, FileNotFoundError):
            json_data: dict = {}

        for username in user_list:
            print(f"Username: {username}")
            user = RobloxUser(username)    
            total_visits: int = user.get_total_visits()
            total_followers: int = user.get_followers()            
            try:
                # Append to json dict
                json_data[username]["place_visits"].append(total_visits)
                json_data[username]["followers"].append(total_followers)
            
            except:
                # There are no previous entries
                print("new entry: ", username)

                # Append data
                json_data[username] = {
                    "place_visits": [total_visits],
                    "followers": [total_followers]
                }

                # Append to json dict
                # json_data[username]["place_visits"].append(total_visits)
                # json_data[username]["followers"].append(total_followers)

        self.json_data = json_data;


    def save_data(self) -> None:
        # Save Modified Data
        with open("saved_data.json", "w") as json_file:
            json.dump(self.json_data, json_file, indent=4);
            print("Wrote the File")
