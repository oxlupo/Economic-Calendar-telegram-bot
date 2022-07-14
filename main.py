import time
from termcolor import colored
from table import final_table
from telegram import send_massage


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
    print(colored("the bot was started to work", "green"))
    check_list = []
    while True:
        time.sleep(2)
        main()
        time.sleep(2)