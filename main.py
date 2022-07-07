import json
import re
import tweepy
import requests
from bs4 import BeautifulSoup
import pandas as pd

data = open("retail.txt", "r").read()
soup = BeautifulSoup(data, "html.parser")
table = soup.find("table", id="economicCalendarData")
with open("event.json", 'r', encoding='utf-8') as e:
    pass
    # persian = json.load(e)
text = f"""
#FOREX_FACTORY

🗓️ چهارشنبه ۵  ژوئن ۲۰۲۲

✅شاخص خالص خرده فروشی  (ماهانه) (ژوئن) 
 
Core Retail Sales m/m


✔️ واقعی      
✔️ پیش بینی0.7%
✔️ قبلی        0.6%



✅شاخص خرده فروشی  (ماهانه) (ژوئن)

 Retail Sales m/m


✔️ واقعی       
✔️ پیش بینی 1%
✔️ قبلی          0.9%


 #USD
📍@Amiramidiyan📍"""

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
    for ev in range(int(main_df.shape[0])):
        event = main_df.Event[ev]
        if "Initial Jobless Claims" in event:
            index_.append(ev)
        elif "Manufacturing PMI" in event:
            index_.append(ev)
        elif "Services PMI" in event:
            index_.append(ev)
    return index_


table_inf = find_table(table)
index = find_index(table_inf)
loc = table_inf.loc[index]
print(loc)


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


text = """
CRUDE OIL INVENTORIES

BUSINESS INVENTORIES

CONSUMER CONFIDENCE

CONSUMER CREDIT

CONSUMER SENTIMENT

CPI (CONSUMER PRICE INDEX)

DURABLE GOODS ORDERS

EXISTING HOME SALES

FACTORY ORDERS

GDP

HOUSING STARTS

TRADE BALANCE

ISM(INSTITUTE OF SUPPLY MANAGEMENT)

INITIAL JOBLESS CLAIMS

NEW HOME SALES

NON FRAM – PAYROLLS

AVERAGE HOURLY EARNING

UNEMPLOYMENT RATE

EMPLOYMENT COST INDEX

PPI  ( PRODUCER PRICE INDEX )

RETAIL SALES"""


for name in loc.values:
    send_massage(name)






