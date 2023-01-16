import json
from Roblox import RobloxGroup

class GroupData:
    def __init__(self, file_name: str, json_fname: str="group_data") -> None:
        with open(file_name) as file:
            group_list = file.read().splitlines()

        try:
            with open(f"{json_fname}.json", "r") as json_file:
                json_data: dict = json.load(json_file)
        except (json.JSONDecodeError, FileNotFoundError):
            json_data: dict = {}

        for group_name in group_list:
            print(f"Group: {group_name}")
            group = RobloxGroup(group_name)    
            total_members: int = group.get_group_members()
            group_full_name = group.__str__()

            if total_members == 0:
                print(f"Skipping {group_full_name}\n")
                continue;

            try:
                # Append to json dict
                json_data[group]["members"].append(total_members)            
            except:
                # There are no previous entries
                print(f"New Entry: {group_full_name}\n")

                # Append data
                json_data[group_full_name] = {
                    "members": [total_members],
                }

        self.json_data = json_data;


    def save_data(self, save_as: str="group_output") -> None:
        # Save Modified Data
        with open(f"data/{save_as}.json", "w") as json_file:
            json.dump(self.json_data, json_file, indent=4);
            print(f"Wrote to {save_as}.json")
