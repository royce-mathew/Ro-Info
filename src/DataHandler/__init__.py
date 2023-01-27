from Roblox import RobloxGroup, RobloxUser
from DataHandler import Util
from datetime import datetime

DEFAULT_GROUP_OUTPUT="data/group_output.json"
DEFAULT_GROUP_INPUT="data/groups.txt"
DEFAULT_USER_OUTPUT="data/user_output.json"
DEFAULT_USER_INPUT="data/users.txt"


class GroupData:
    def __init__(self, file_name: str=DEFAULT_GROUP_INPUT, json_fname: str=DEFAULT_GROUP_OUTPUT) -> None:
        group_list: list = Util.read_file_list(file_name)
        json_data: dict = Util.json_to_dict(json_fname)

        Util.split_work(group_list, GroupData.__group_main, 25, json_data)

        self.group_list = group_list;
        self.json_data = json_data;


    @staticmethod
    def __group_main(group_list: list, json_data: dict):
        current_time = datetime.now().ctime()

        for group_name in group_list:
            print(f"Group: {group_name}")
            group = RobloxGroup(group_name)
            total_members: int = group.get_group_members()
            members_tuple = (current_time, total_members);

            group_full_name = group.__str__()

            if total_members == 0:
                print(f"Skipping {group_full_name}\n")
                continue;

            try:
                # Append to json dict
                json_data[group]["members"].append(members_tuple)            
            except:
                # There are no previous entries
                print(f"New Entry: {group_full_name}\n")

                # Append data
                json_data[group_full_name] = {
                    "members": [members_tuple],
                }

    def get_data(self) -> dict:
        return self.json_data;

    def save_data(self, file_name: str=DEFAULT_GROUP_OUTPUT):
        Util.save_json(self.json_data, file_name)

class UserData:
    def __init__(self, file_name: str=DEFAULT_USER_INPUT, json_fname: str=DEFAULT_USER_OUTPUT) -> None:
        user_list: list = Util.read_file_list(file_name)
        json_data: dict = Util.json_to_dict(json_fname)

        Util.split_work(user_list, UserData.__user_main, 25, json_data)
        
        self.user_list = user_list;
        self.json_data = json_data;


    @staticmethod
    def __user_main(user_list: list, json_data: dict):
        current_time = datetime.now().ctime()
        # Read user list
        for username in user_list:
            print(f"Username: {username}")
            user = RobloxUser(username)
            
            # Skip to next iteration
            if user.user_id is None:
                user_list.remove(username)
                continue;

            total_visits: int = user.get_total_visits()
            total_followers: int = user.get_followers()

            visit_tuple = (current_time, total_visits);
            followers_tuple = (current_time, total_visits);
            
            if total_visits == 0 or total_followers == 0:
                print(f"Skipped: {username}; visits: {total_visits}; followers: {total_followers}")
                user_list.remove(username)
                continue;

            try:
                # Append to json dict
                json_data[username]["place_visits"].append(visit_tuple)
                json_data[username]["followers"].append(followers_tuple)
            
            except:
                # There are no previous entries
                print(f"New Entry: {username}")

                # Append data
                json_data[username] = {
                    "place_visits": [visit_tuple],
                    "followers": [followers_tuple]
                }

    def get_data(self) -> dict:
        return self.json_data;

    def save_data(self, file_name: str=DEFAULT_USER_OUTPUT):
        Util.save_json(self.json_data, file_name)

    def write_file(self, file_name: str=DEFAULT_USER_INPUT):
        Util.write_file(self.json_data, file_name)

    def store_unchecked(self):
        current_list = self.json_data.keys()
        full_list = self.user_list;
        return [x for x in full_list if x not in current_list]