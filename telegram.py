import requests


def send_massage():
    """send a massage to channel by telegram bot"""

    base_url = "https://api.telegram.org/bot5334404508:AAFD-Vkaghr_BLOkC5n1Sy_XwFzKl3_4DSo/sendMessage"
    parameters = {
        "chat_id": "@ZeroHedge2",
        "text": "This is test API"
    }
    resp = requests.get(url=base_url, data=parameters)
    return resp


