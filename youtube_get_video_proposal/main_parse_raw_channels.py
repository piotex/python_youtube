import os
import time
from selenium import webdriver
import chromedriver_autoinstaller
from selenium.webdriver.common.by import By
import json
from dataclasses import dataclass, field


@dataclass
class yt_user:
    url: str = ""
    number_of_subscriptions: int = 0


if __name__ == "__main__":
    input_file = "input_data/raw_channels.txt"
    output_file = "output_data/channels.txt"

    res_lines = []
    with open(input_file, "r", encoding="utf-8") as input_f:
        input_list = input_f.readlines()

    for line in input_list:
        if "@" not in line:
            continue

        url = line.split("•")[0]
        sub_numb = -1
        try:
            sub_numb_txt = line.split("•")[1].replace("subskrybentów", "").strip()
            for repl_txt in [["tys.", 1000, 10], ["mln", 1000000, 10000]]:
                if repl_txt[0] in sub_numb_txt:
                    sub_numb = sub_numb_txt.split()[0]
                    if "," in sub_numb:
                        fix_number = 1
                        if len(sub_numb.split(",")[1]) == 1:
                            fix_number = 10
                        sub_numb = int(sub_numb.split(",")[0]) * repl_txt[1] + int(sub_numb.split(",")[1]) * fix_number * repl_txt[2]
                    else:
                        sub_numb = int(sub_numb) * repl_txt[1]
                    break
            if "tys." not in sub_numb_txt and "mln" not in sub_numb_txt:
                sub_numb = int(sub_numb_txt)
        except:
            pass

        if sub_numb < 10000:
            continue
        if sub_numb > 200000:
            continue
        user = yt_user(url=url, number_of_subscriptions=sub_numb)
        res_lines.append(user)

    with open("output_data/channels.json", "w") as f:
        json.dump([item.__dict__ for item in res_lines], f, indent=4)