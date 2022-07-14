import requests
from bs4 import BeautifulSoup
import re

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


def usa_table(table):
    """only show USA event"""
    for index, flag in enumerate(table.values):
        if not flag[1] == "USD":
            table = table.drop(index)
    table = table.reset_index(drop=True)
    return table


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