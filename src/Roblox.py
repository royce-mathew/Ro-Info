import requests
from ProxyHandler import request_get
from typing import Union
from urllib.parse import quote

USERS_ENDPOINT="https://users.roblox.com"
API_ENDPOINT="https://api.roblox.com"
GAMES_ENDPOINT="https://games.roblox.com"
FRIENDS_ENDPOINT="https://friends.roblox.com"


class RobloxUser:
    def __init__(self, user: Union[int, str]):
        if type(user) == str:            
            user = RobloxUser.get_user_id(user);
            #response: requests.Response = requests.get(f"{USERS_ENDPOINT}/v1/users/{user}")
            #response.raise_for_status()
        
        self.user_id = user

    @staticmethod
    def get_user_id(user_name: str) -> int:
        response: requests.Response = request_get(f"{API_ENDPOINT}/users/get-by-username?username={user_name}")
        response_json: dict = response.json()
        try:
            return response_json["Id"]
        except Exception as err:
            print(f"User: {user_name} not found; {err}");
            return None;


    def get_total_visits(self) -> int:
        total_place_visits: int = 0;
        response = request_get(f"{GAMES_ENDPOINT}/v2/users/{self.user_id}/games?limit=50")
        response_json: dict = response.json()
        for game in response_json["data"]:
            total_place_visits += game["placeVisits"]
        return total_place_visits

    def get_followers(self) -> int:
        response: requests.Response = request_get(f"{FRIENDS_ENDPOINT}/v1/users/{self.user_id}/followers/count")
        response_json = response.json()
        try:
            return response_json["count"]
        except:
            raise Exception(response_json["errorMessage"])


class RobloxGroup:
    def __init__(self, group: Union[int, str]):
        if type(group) == str: # Group name was specified
            self.group_data =  RobloxGroup.get_group_data(group);

    @staticmethod
    def get_group_data(group_name: str) -> int:
        response: requests.Response = request_get(f"https://groups.roblox.com/v1/groups/search/lookup?groupName={quote(group_name)}")
        response_json: dict = response.json()
        try:
            return response_json["data"][0]
        except IndexError:
            print(f"Group: {group_name} not found");
            return None;
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            raise


    def get_group_members(self) -> int:
        try:
            return self.group_data["memberCount"]
        except Exception as err:
            print(err)
            return 0;

    def __str__(self) -> str:
        try:
            return self.group_data["name"]
        except Exception as err:
            print(err)
            return ""

    def __repr__(self) -> str:
        try:
            f"{self.group_data['id']} : {self.group_data['name']}"
        except Exception as err:
            print(err)
            return ""