import requests
from ProxyHandler import request_get
from typing import Union
from itertools import cycle
import time

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
        # response.raise_for_status()
        # print(get_proxy())
        if response.status_code == 429:
            time.sleep(2)
            print(f"Retrying: {time.time()}")
            return RobloxUser.get_user_id(user_name)

        response_json: dict = response.json()
        try:
            return response_json["Id"]
        except:
            raise Exception(response_json["errorMessage"])


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


