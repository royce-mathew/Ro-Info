import requests
import threading
import math
import sys
import os
import random

timeout=3
thread_count = 50;
valid_proxies = []

user_agent_list = [
   #Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    #Firefox
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
]

def delete_last_line():
    "Use this function to delete the last line in the STDOUT"
    sys.stdout.write('\x1b[1A') # Move cursor up one line
    sys.stdout.write('\x1b[2K') # Delete last line

def initialize_proxies():
    response = requests.get("https://raw.githubusercontent.com/saschazesiger/Free-Proxies/master/proxies/http.txt")
    # response = requests.get("https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/http.txt")
    # response = requests.get("https://raw.githubusercontent.com/parserpp/ip_ports/main/proxyinfo.txt")
    response.raise_for_status() # Check if Proxies Work
    return response.text.splitlines();

def read_proxies():
    try:
        with open("clean_proxies.txt", "r") as file:
            valid_proxies.extend(file.read().splitlines())
    except FileNotFoundError:
        print("File does not exist. Please run ProxyHandler.py")
        return;


def check_proxy(proxy):
    try:
        response = requests.get("https://ipecho.net/plain",
            proxies={"http": proxy,
            "https": proxy},
            timeout=timeout
        )
        return (response.status_code == 200);
    except:
        return False;

def check_proxies(proxies):
    for proxy in proxies:
        print(f"Checking {proxy}", end="\t\t")
        if check_proxy(proxy) == True:
            print("✔️")
            valid_proxies.append(proxy)
        else:
            print("☠️")


def clean_proxies(proxy_list):
    threads = [];
    print("Cleaning Proxies")

    # Split proxy list for threads
    amount = int(math.ceil(len(proxy_list) / thread_count))
    proxy_main = [
        proxy_list[x : x + amount] for x in range(0, len(proxy_list), amount)
    ]
    if len(proxy_list) % thread_count > 0.0:
        proxy_main[-1].append(proxy_list[len(proxy_list) - 1])

    for proxy_sublist in proxy_main:
        threads.append(threading.Thread(target=check_proxies, args=([proxy_sublist])))
        threads[-1].start() 

    for thread in threads: # Wait until all threads finish terminating
        thread.join()


def get_proxy():
    return valid_proxies[random.randint(0, len(valid_proxies))];

def internal_get(url: str):
    if len(valid_proxies) == 0: return;
    proxy = valid_proxies[0];

    delete_last_line()
    print(f"Request: {url}; Proxy: {proxy}")
    try:
        response = requests.get(
            url, 
            proxies={"http": proxy, "https": proxy}, 
            headers={"User-Agent": user_agent_list[random.randint(0, len(user_agent_list))]},
            timeout=3
        )
        response.raise_for_status()
        return response;
    except:
        try:
            valid_proxies.pop(0);
        except IndexError:
            return;
        # Bad Proxy
        return internal_get(url)

def request_get(url: str):
    print("Requesting ..")
    return internal_get(url);

def program_exit():
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)

if __name__ == "__main__":
    open_type: str = input("Would you like to append or overwrite? [a/o]: ")
    if open_type not in ["a", "o"]:
        print("Defaulting to Overwrite")
        open_type = "o"
    
    # Try statement for catching keyboard interrupt
    try:
        # Initialize All Proxies
        proxy_list = initialize_proxies()
        clean_proxies(proxy_list)
    except KeyboardInterrupt:
        pass;
    

    with open("clean_proxies.txt", "w" if (open_type == "o") else "a") as file:
        for proxy in valid_proxies:
            file.write(f"{proxy}\n")

    print(f"\n\nWrote {len(valid_proxies)} Proxies")
    program_exit()
    