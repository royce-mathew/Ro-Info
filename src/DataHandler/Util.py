import csv
import json
import math
from typing import Callable
import threading


"""
    Splits work for worker threads
"""
def split_work(values: list, function: Callable, thread_count: int=25, *args):
    threads = [];

    # Split proxy list for threads
    amount = int(math.ceil(len(values) / thread_count))
    main_threader = [
        values[x : x + amount] for x in range(0, len(values), amount)
    ]
    if len(values) % thread_count > 0.0:
        main_threader[-1].append(values[len(values) - 1])

    for sub_list in main_threader:
        threads.append(threading.Thread(target=function, args=([sub_list, *args])))
        threads[-1].start() 

    for thread in threads: # Wait until all threads finish terminating
        thread.join()

"""
    Save Data to a json file
"""
def save_json(json_data: dict, file_name: str) -> None:
    # Save Modified Data
    with open(file_name, "w") as json_file:
        json.dump(json_data, json_file, indent=4);
        print(f"Wrote to {file_name}")

def save_csv(json_data: dict, file_name: str) -> None:
    with open(file_name, "a") as csv_file:
        writer = csv.writer(csv_file)
        for key, value in json_data.items(): # Loops through each user
            followers = value["followers"][-1][1]
            visits = value["place_visits"][-1][1]

            # Get Followers, Place Visits
            writer.writerow([key, followers, visits])


def write_csv(json_data: dict, file_name: str) -> None:
    with open(file_name, "w") as csv_file:
        writer = csv.writer(csv_file)
        for key, value in json_data.items():
            writer.writerow([key, *value])

"""
    Save Data to a text file
"""
def write_file(json_data: dict, file_name: str) -> None:
    with open(file_name, "w") as file:
        for key in json_data.keys():
            file.write(f"{key}\n")
        print(f"Wrote to {file_name}")

"""
    save List to text file
"""
def write_list(main_list: list, file_name: str) -> None:
    with open(file_name, "w") as file:
        file.writelines(value + "\n" for value in main_list);


"""
    Read file and convert lines to a list
"""
def read_file_list(file_name: str):
    with open(file_name) as file:
        return file.read().splitlines()

"""
    Convert json data to a dictionary
"""
def json_to_dict(file_name: str):
    json_data: dict;
    try:
        with open(file_name, "r") as json_file:
            json_data: dict = json.load(json_file)
    except (json.JSONDecodeError, FileNotFoundError):
        json_data: dict = {}
    return json_data;
