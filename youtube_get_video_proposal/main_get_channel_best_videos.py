import os
import time
from selenium import webdriver
import chromedriver_autoinstaller
from selenium.webdriver.common.by import By
import json
from dataclasses import dataclass, field


@dataclass
class yt_video:
    url: str = ""
    number_of_views: int = -1
    video_title:str = ""

    base_channel:str = ""
    base_channel_number_of_subscriptions: int = -1

@dataclass
class yt_user:
    url: str = ""
    number_of_subscriptions: int = -1
    list_of_videos: list[yt_video] = field(default_factory=list)


def get_user_data(driver: webdriver.Chrome, user: yt_user):
    max_in_column = 3
    max_in_row = 99
    if "http" not in user.url:
        user.url = "https://www.youtube.com/" + user.url
    user.url = user.url + "/videos"
    driver.get(user.url)
    time.sleep(1)

    str_fixer_1 = ""
    for tmp_fixer in ["", "[1]", "[2]"]:
        try:
            x_path = f"/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse{tmp_fixer}/ytd-two-column-browse-results-renderer/div[1]/ytd-rich-grid-renderer/div[1]/ytd-feed-filter-chip-bar-renderer/div/div/div[3]/iron-selector/yt-chip-cloud-chip-renderer[2]/yt-formatted-string"
            tmp_txt = driver.find_element(By.XPATH, x_path).text
            if tmp_txt == 'Popularne':
                str_fixer_1 = tmp_fixer
                break
        except:
            pass

    x_path = f"/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse{str_fixer_1}/ytd-two-column-browse-results-renderer/div[1]/ytd-rich-grid-renderer/div[1]/ytd-feed-filter-chip-bar-renderer/div/div/div[3]/iron-selector/yt-chip-cloud-chip-renderer[2]/yt-formatted-string"
    driver.find_element(By.XPATH, x_path).click()
    time.sleep(1)

    for i_row in range(1, max_in_row + 1, 1):
        driver.execute_script(f"window.scrollTo(0, {i_row * 1000})")
        time.sleep(1)

        for i_column in range(1, max_in_column + 1, 1):
            link = ""
            view_count = -1
            title = ""

            try:
                x_path = f"/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse{str_fixer_1}/ytd-two-column-browse-results-renderer/div[1]/ytd-rich-grid-renderer/div[6]/ytd-rich-grid-row[{i_row}]/div/ytd-rich-item-renderer[{i_column}]/div/ytd-rich-grid-media/div[1]/div[3]/div[1]/ytd-video-meta-block/div[1]/div[2]/span[1]"
                views_count_txt = driver.find_element(By.XPATH, x_path).text.strip()
                x_path = f"/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse{str_fixer_1}/ytd-two-column-browse-results-renderer/div[1]/ytd-rich-grid-renderer/div[6]/ytd-rich-grid-row[{i_row}]/div/ytd-rich-item-renderer[{i_column}]/div/ytd-rich-grid-media/div[1]/div[3]/div[1]/h3/a"
                link = driver.find_element(By.XPATH, x_path).get_attribute('href')
                x_path = f"/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse{str_fixer_1}/ytd-two-column-browse-results-renderer/div[1]/ytd-rich-grid-renderer/div[6]/ytd-rich-grid-row[{i_row}]/div/ytd-rich-item-renderer[{i_column}]/div/ytd-rich-grid-media/div[1]/div[3]/div[1]/h3/a/yt-formatted-string"
                title = driver.find_element(By.XPATH, x_path).text.strip()
                view_count = -1

                tmp_unit_list = [["tys.", 1000, 10], ["mln", 1000000, 10000], ["K", 1000, 10], ["M", 1000000, 10000]]
                for repl_txt in tmp_unit_list:
                    if repl_txt[0] in views_count_txt:
                        view_count = views_count_txt.split()[0]
                        if "," in view_count:
                            fix_number = 1
                            if len(view_count.split(",")[1]) == 1:
                                fix_number = 10
                            view_count = int(view_count.split(",")[0]) * repl_txt[1] + int(
                                view_count.split(",")[1]) * fix_number * repl_txt[2]
                        else:
                            view_count = int(view_count) * repl_txt[1]
                        break
                noting_in = True
                for tmp_unit in tmp_unit_list:
                    if tmp_unit[0] in views_count_txt:
                        noting_in = False
                        break
                if noting_in:
                    view_count = int(views_count_txt)
            except:
                pass
            if view_count < 15000:
                return user.list_of_videos
            user.list_of_videos.append(yt_video(url=link, number_of_views=view_count, video_title=title, base_channel=user.url, base_channel_number_of_subscriptions=user.number_of_subscriptions))
    return user.list_of_videos

def main():
    init_linkedin = True
    get_user_data_f = True
    driver = None
    data_file_path = "output_data/channels.json"

    with open(data_file_path, "r") as f:
        list_of_users = json.load(f)
        list_of_users = [yt_user(**item) for item in list_of_users]

    if init_linkedin:
        chromedriver_autoinstaller.install()
        driver = webdriver.Chrome()
        driver.get("https://www.youtube.com/")
        time.sleep(1)
        x_path = "/html/body/ytd-app/ytd-consent-bump-v2-lightbox/tp-yt-paper-dialog/div[4]/div[2]/div[6]/div[1]/ytd-button-renderer[1]/yt-button-shape/button"
        driver.find_element(By.XPATH, x_path).click()
        time.sleep(1)

    list_of_videos = []
    if get_user_data_f:
        for user in list_of_users:
            list_of_videos += get_user_data(driver, user)
            # to update channels we must parse also video list ...
            # with open("output_data/channels.json", "w") as f:
            #     json.dump([item.__dict__ for item in list_of_users], f, indent=4)
            with open("output_data/list_of_videos.json", "w") as f:
                json.dump([item.__dict__ for item in list_of_videos], f, indent=4)


if __name__ == '__main__':
    main()
