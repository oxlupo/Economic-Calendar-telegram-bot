import requests
import hashlib
import json
from termcolor import colored


with open("event.json", 'r', encoding='utf-8') as e:
    persian = json.load(e)


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