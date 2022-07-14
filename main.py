import json
import re
import time
import schedule
import requests
from bs4 import BeautifulSoup
import pandas as pd
import hashlib
from termcolor import colored

with open("event.json", 'r', encoding='utf-8') as e:
    persian = json.load(e)


def find_index(main_df):
    """find text of each data for replace new data in it"""
    index_ = []
    main_event = persian.keys()
    for ev in range(int(main_df.shape[0])):
        event = main_df.Event[ev]
        for k in main_event:
            search = re.search(pattern=f"{k}", string=event, flags=0)
            if not search == None:
                index_.append(ev)
    return index_



def send_massage(loc, checklist):
    """send a massage to channel by telegram bot"""
    for pr in persian:
        if pr in loc[3]:
            persian_name = persian[pr]
            break
    event = loc[3]
    actual = loc[4]
    forecast = loc[5]
    previous = loc[6]
    base_url = "https://api.telegram.org/bot5334404508:AAFD-Vkaghr_BLOkC5n1Sy_XwFzKl3_4DSo/sendMessage"
    parameters = {
        "chat_id": "@Amiramidiyan",
        "text": f"""
✅{persian_name} 

{event}

✔️ واقعی---->{actual} 
✔️ پیش بینی---->{forecast} 
✔️ قبلی---->{previous} 



📍@Amiramidiyan📍
"""
    }
    hash_massage = hashlib.sha256(parameters["text"].encode("utf-8")).hexdigest()
    if not hash_massage in checklist:
        try:
            resp = requests.get(url=base_url, data=parameters)
            print(parameters["text"])
            print(colored("the massage was sent to bot", "green"))
        except Exception as e:
            print(e)
    return hash_massage




def main():
    """all of the steps was here"""
    loc = final_table()
    if not isinstance(loc, str):
        try:
            for name in loc.values:
                if not name[4] == "":
                    hash_massage = send_massage(name, check_list)
                    check_list.append(hash_massage)
        except Exception:
            print(Exception)
            time.sleep(20)
    return check_list


if __name__ == "__main__":
    print(colored("the program was started to work", "green"))
    check_list = []
    while True:
        time.sleep(2)
        main()
        time.sleep(2)