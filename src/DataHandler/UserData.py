import json
from Roblox import RobloxUser

class UserData:
    def __init__(self, file_name: str, json_fname: str="user_data") -> None:
        with open(file_name) as file:
            user_list = file.read().splitlines()

        try:
            with open(f"{json_fname}.json", "r") as json_file:
                json_data: dict = json.load(json_file)
        except (json.JSONDecodeError, FileNotFoundError):
            json_data: dict = {}

        for username in user_list:
            print(f"Username: {username}")
            user = RobloxUser(username)    
            total_visits: int = user.get_total_visits()
            total_followers: int = user.get_followers()
            
            if total_visits == 0 or total_followers == 0:
                print(f"Skipped: {username}; visits: {total_visits} : followers: {total_followers}")
                continue;

            try:
                # Append to json dict
                json_data[username]["place_visits"].append(total_visits)
                json_data[username]["followers"].append(total_followers)
            
            except:
                # There are no previous entries
                print(f"New Entry: {username}")

                # Append data
                json_data[username] = {
                    "place_visits": [total_visits],
                    "followers": [total_followers]
                }

        self.json_data = json_data;


    def save_data(self, save_as: str="user_output") -> None:
        # Save Modified Data
        with open(f"data/{save_as}.json", "w") as json_file:
            json.dump(self.json_data, json_file, indent=4);
            print(f"Wrote to {save_as}.json")
