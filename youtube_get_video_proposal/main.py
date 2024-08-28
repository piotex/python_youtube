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


def create_if_missing(f_d_path: str):
    if not os.path.exists(f_d_path) and "." not in f_d_path:
        os.makedirs(f_d_path)
    if not os.path.exists(f_d_path) and "." in f_d_path:
        with open(f_d_path, 'w') as file:
            file.write("")

def get_channels_links(driver: webdriver.Chrome, max_scroll_number: int) -> list[yt_user]:
    result_list = []
    driver.get("https://www.youtube.com/results?search_query=devops&sp=EgIQAg%253D%253D")
    time.sleep(2)
    x_path = "/html/body/ytd-app/ytd-consent-bump-v2-lightbox/tp-yt-paper-dialog/div[4]/div[2]/div[6]/div[1]/ytd-button-renderer[1]/yt-button-shape/button"
    driver.find_element(By.XPATH, x_path).click()
    time.sleep(1)
    for i1 in range(1, max_scroll_number, 1):
        driver.execute_script(f"window.scrollTo(0, {i1 * 1000})")
        time.sleep(5)
        for i2 in range(1, 21, 1):
            x_path = f"/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer[{i1}]/div[3]/ytd-channel-renderer[{i2}]/div/div[2]/a"
            try:
                link = driver.find_element(By.XPATH, x_path).get_attribute('href')
                x_path += f"/div[1]/div/span[2]"
                sub_numb = driver.find_element(By.XPATH, x_path).text.split("•")[-1].replace("subskrybentów", "")   # 7,36 tys. subskrybentów

                repl_txt = "tys."
                if repl_txt in sub_numb:
                    sub_numb = sub_numb.split()[0]
                    sub_numb = int(sub_numb.split(",")[0]) * 1000 + int(sub_numb.split(",")[1]) * 10
                repl_txt = "mln"
                if repl_txt in sub_numb:
                    sub_numb = sub_numb.split()[0]
                    sub_numb = int(sub_numb.split(",")[0]) * 1000000 + int(sub_numb.split(",")[1]) * 10000

                a_obj = yt_user(url=link, number_of_subscriptions=sub_numb)
                result_list.append(a_obj)

                with open("output_data/channels.json", "w") as f:
                    json.dump([item.__dict__ for item in result_list], f, indent=4)
            except:
                pass
    return result_list

def main():
    init_linkedin = True
    get_init_channels_urls = True

    driver = None
    init_paths = ["input_data", "output_data", "output_data/channels.json"]
    for init_path in init_paths:
        create_if_missing(init_path)

    if init_linkedin:
        chromedriver_autoinstaller.install()
        driver = webdriver.Chrome()

    if get_init_channels_urls:
        get_channels_links(driver, 100)


    with open(init_paths[2], "r") as f:
        list_of_users = json.load(f)
        list_of_users = [yt_user(**item) for item in list_of_users]

    issss1 = "piotr" in list_of_users
    issss2 = "Piotr" in list_of_users

    a = 0


    #
    # with open(init_paths[2], "w") as f:
    #     json.dump([item.__dict__ for item in list_of_users], f, indent=4)
    #
    # a = 0

    # for i, elem in enumerate(subtitles_list):
    #     with open(f"output_data/subtitles_for_google/subtitles_{title[:20]}_{i}.txt", 'w') as writer:
    #         writer.writelines(elem)
    #
    # subtitles_list = split_subtitles(subtitles, 2000)
    # for i, elem in enumerate(subtitles_list):
    #     with open(f"output_data/subtitles_for_chatgpt/subtitles_{title[:20]}_{i}.txt", 'w') as writer:
    #         writer.writelines(elem)
    #
    # with open(f"output_data/main_data/description_{title[:20]}.txt", 'w', encoding="utf-8") as writer:
    #     writer.writelines(description)
    # with open(f"output_data/main_data/tags_{title[:20]}.txt", 'w', encoding="utf-8") as writer:
    #     writer.writelines(tags)


if __name__ == '__main__':
    main()
