import json
import re
import time
from datetime import datetime
import schedule
import telebot
import requests
from bs4 import BeautifulSoup
import pandas as pd
from flask import Flask
import hashlib


TOKEN = "bot5334404508:AAFD-Vkaghr_BLOkC5n1Sy_XwFzKl3_4DSo"
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)


with open("event.json", 'r', encoding='utf-8') as e:

    persian = json.load(e)


def connection(url):
    """get html of website with request and parse it with soup"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}

    data = requests.get(url, headers=headers).content
    soup = BeautifulSoup(data, "html.parser")
    table = soup.find("table", id="economicCalendarData")
    return table


def find_time(element):
    """ find the time of each id """
    time_ = element.find("td", class_="first left time js-time").string
    return time_


def find_flag(element):
    """ find the flag of each id """
    flag_name = element.find("td", class_="left flagCur noWrap").text.strip()
    return flag_name


def find_number_star(element):
    """ evaluating value of each news by number of stars """
    imp = element.find("td", class_="left textNum sentiment noWrap").attrs["data-img_key"]
    imp_list = []
    pattern = re.compile("bull([0-3])")
    len_star = pattern.findall(imp)
    for i in range(int(len_star[0])):
        imp_list.append("*")
    imp_star = "".join(imp_list)
    return imp_star


def find_event(element):
    """ the name of event find with this function """
    Event = element.find("a", href=True).text.strip()
    return Event


def find_value(id, element):
    """find the value of each rows of Actual Forecast and Previous"""
    actual = element.find("td", id=f"eventActual_{id}").text
    forecast = element.find("td", id=f"eventForecast_{id}").text
    previous = element.find("td", id=f"eventPrevious_{id}").text

    return actual, forecast, previous


def find_table(table):
    """find the main table """

    main_df = pd.DataFrame(columns=["Time", "Flag", "Imp", "Event", "Actual", "Forecast", "Previous"])
    for element in table.find_all("tr", class_="js-event-item"):
        element_dict = element.attrs
        id = element_dict["id"].split("_")[1]
        time_ = find_time(element)
        flag = find_flag(element)
        imp_star = find_number_star(element)
        event = find_event(element)
        actual, forecast, previous = find_value(id=id, element=element)
        id_df = pd.DataFrame({
            "Time": time_,
            "Flag": flag,
            "Imp": [imp_star],
            "Event": event,
            "Actual": actual,
            "Forecast": forecast,
            "Previous": previous,
        })
        main_df = main_df.append(id_df, ignore_index=True)

    return main_df


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


def clean_df(table):
    """
    table was clean from \xa0 decoded and clean and nothing wasn't shown
    """
    table['Actual'] = table['Actual'].apply(lambda x: str(x).replace(u'\xa0', u''))
    table['Forecast'] = table['Forecast'].apply(lambda x: str(x).replace(u'\xa0', u''))
    table['Previous'] = table['Previous'].apply(lambda x: str(x).replace(u'\xa0', u''))
    return table


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url="https://sheltered-sierra-85399.herokuapp.com/" + TOKEN)
    return "!", 200


def send_massage(loc):
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
        "chat_id": "@ZeroHedge2",
        "text": f"""
✅{persian_name} 
 
{event}

✔️ واقعی---->{actual} 
✔️ پیش بینی---->{forecast} 
✔️ قبلی---->{previous} 



📍@Amiramidiyan📍
"""
    }
    print(parameters["text"])
    resp = requests.get(url=base_url, data=parameters)
    return resp


def main(loc):
    """all of the steps was here"""
    check_list = []
    table = connection(url="https://www.investing.com/economic-calendar")
    table_inf = find_table(table)
    index = find_index(table_inf)
    loc = table_inf.loc[index]
    loc = clean_df(table=loc)
    print(loc)
    try:
        for name in loc.values:
            if not name[1] == "USD":
                continue
            if not name[4] == "":
                resp = send_massage(name)
                hash_massage = hashlib.sha256(resp.text.encode("utf-8")).hexdigest()
                check_list.append(hash_massage)
                print("the massage was sended to bot")
    except Exception:
        time.sleep(20)
    return check_list


def final_table(url="https://www.investing.com/economic-calendar"):
    """get table from investing.com"""
    table = connection(url=url)
    table_inf = find_table(table)
    index = find_index(table_inf)
    loc = table_inf.loc[index]
    loc = clean_df(table=loc)
    print(loc)
    return loc





if __name__ == "__main__":
    schedule.every().day.at("01:00").do(final_table)
    while True:
        schedule.run_pending()
        time.sleep(2)

