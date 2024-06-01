import time

from pytube import YouTube
from selenium import webdriver
import chromedriver_autoinstaller
from selenium.webdriver.common.by import By
import json
from dataclasses import dataclass, field
import random
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


# =========== strategy =====================
# 1) go to https://www.youtube.com/ and click Reject all
# 2) go to shorts
# 3) 5 scrolls 0.5-1s
#
#
# 4) views from main channel:
# search for Piotr Kubon DevOps channel in youtube search
# go into channel with @piotr.kubon.devops
#
# 5) views from search (a)
# search for Piotr Kubon DevOps channel in youtube search
# click short
#
# 5) views from search (b)
# paste short title
#
#
# ===========================================


@dataclass
class MVideo:
    url: str = ""
    number_of_views: int = 0


def wait_for_x_path_elem(driver: webdriver.Chrome, x_path: str) -> 1:
    max_wait_time_in_s = 5
    number_of_tries = 10
    for i in range(0, number_of_tries, 1):
        try:
            driver.find_element(By.XPATH, x_path)
            return 0
        except:
            time.sleep(max_wait_time_in_s / number_of_tries)
    raise Exception("=== X_Path element not found ===")


def scroll_main_shorts_page(driver: webdriver.Chrome, shorts_to_scroll: int):
    x_path = "/html/body/ytd-app/div[1]/ytd-mini-guide-renderer/div/ytd-mini-guide-entry-renderer[2]/a"
    driver.find_element(By.XPATH, x_path).click()
    time.sleep(0.5)

    x_path = "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-shorts/div[3]/div[2]/ytd-reel-video-renderer[1]/div[3]/div[1]/div[1]/div[1]/ytd-shorts-player-controls/yt-button-shape/button"
    wait_for_x_path_elem(driver, x_path)
    driver.find_element(By.XPATH, x_path).send_keys("M")
    time.sleep(1)

    x_path = "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-shorts/div[5]/div[2]/ytd-button-renderer/yt-button-shape/button"
    for j in range(1, shorts_to_scroll, 1):
        driver.find_element(By.XPATH, x_path).click()
        time.sleep(random.uniform(1.0, 3.0))


def try_click_on_my_channel_in_search_view(driver: webdriver.Chrome, channel_id: str):
    for i_1 in range(1, 3, 1):
        for i_2 in range(1, 11, 1):
            try:
                x_path_list = [
                    f"/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer[{i_1}]/div[3]/ytd-channel-renderer[{i_2}]/div/div[2]/a",
                    f"/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer[{i_1}]/div[3]/ytd-channel-renderer/div/div[2]/a"
                ]
                for x_path in x_path_list:
                    in_channel_id = driver.find_element(By.XPATH, x_path + "/div[1]/div/yt-formatted-string").text
                    if in_channel_id == channel_id:
                        driver.find_element(By.XPATH, x_path).click()
                        time.sleep(1)
                        break
            except:
                if i_1 == 3 and i_2 == 10:
                    raise Exception("=== Channel not found in search window ===")
    time.sleep(1)


def go_to_my_channel(driver: webdriver.Chrome):
    partial_short_title = "How to set up Centos 9 in "

    channel_id = "@piotr.kubon.devops"
    channel_name = "Piotr Kubon DevOps"
    x_path = "/html/body/ytd-app/div[1]/div/ytd-masthead/div[4]/div[2]/ytd-searchbox/form/div[1]/div[1]/input"
    driver.find_element(By.XPATH, x_path).click()
    driver.find_element(By.XPATH, x_path).send_keys(channel_name)
    x_path = "/html/body/ytd-app/div[1]/div/ytd-masthead/div[4]/div[2]/ytd-searchbox/button"
    driver.find_element(By.XPATH, x_path).click()
    time.sleep(1)
    try_click_on_my_channel_in_search_view(driver, channel_id)


def go_to_shorts_in_my_channel(driver: webdriver.Chrome):
    x_path = "//*[@id=\"tabsContent\"]/yt-tab-group-shape/div[1]/yt-tab-shape[2]/div[1]"
    driver.find_element(By.XPATH, x_path).click()
    time.sleep(1)


def get_row_column(idx: int):
    max_in_row = 4
    x_row = int((idx - 0.01) / max_in_row) + 1
    x_column = int(idx % max_in_row)
    if x_column == 0:
        x_column = max_in_row
    return (x_row, x_column)


def click_short_with_matching_title(driver: webdriver.Chrome, partial_short_title: str):
    for i_row in range(1, 101):
        for i_column in range(1, 5):
            try:
                x_path = f"/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse[2]/ytd-two-column-browse-results-renderer/div[1]/ytd-rich-grid-renderer/div[6]/ytd-rich-grid-row[{i_row}]/div/ytd-rich-item-renderer[{i_column}]/div/ytd-rich-grid-slim-media/div[1]/div/h3/a"
                in_short_title = driver.find_element(By.XPATH, x_path + "/span").text
                if partial_short_title in in_short_title:
                    driver.find_element(By.XPATH, x_path).click()
                    time.sleep(1)
                    video_url = driver.current_url
                    video_length = YouTube(video_url).length
                    time.sleep(random.uniform(video_length * 0.8, video_length * 1.1))
                    return 0
            except:
                if i_row == 100 and i_column == 4:
                    raise Exception(f"=== Can not find video: {partial_short_title} ===")


def get_max_shorts_count(driver: webdriver.Chrome) -> int:
    old_max_shorts_count = -1
    max_shorts_count = 0
    while old_max_shorts_count != max_shorts_count:
        driver.execute_script(f"window.scrollTo(0, {(max_shorts_count+1) * 1000})")
        time.sleep(1)
        for i_row in range(1, 10+max_shorts_count):
            for i_column in range(1, 5):
                try:
                    x_path = f"/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse[2]/ytd-two-column-browse-results-renderer/div[1]/ytd-rich-grid-renderer/div[6]/ytd-rich-grid-row[{i_row}]/div/ytd-rich-item-renderer[{i_column}]/div/ytd-rich-grid-slim-media/div[1]/div/h3/a"
                    in_short_title = driver.find_element(By.XPATH, x_path + "/span").text
                    max_shorts_count += 1
                except:
                    pass
        if max_shorts_count == old_max_shorts_count:
            return max_shorts_count
        old_max_shorts_count = max_shorts_count
    return max_shorts_count


def click_X_number_short(driver: webdriver.Chrome, x_vid_id: int):
    (x_row, x_column) = get_row_column(x_vid_id)

    try:
        x_path = f"/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse[2]/ytd-two-column-browse-results-renderer/div[1]/ytd-rich-grid-renderer/div[6]/ytd-rich-grid-row[{x_row}]/div/ytd-rich-item-renderer[{x_column}]/div/ytd-rich-grid-slim-media/div[1]/div/h3/a"
        driver.find_element(By.XPATH, x_path).click()
        time.sleep(1)
        video_url = driver.current_url
        video_length = YouTube(video_url).length
        time.sleep(random.uniform(video_length * 0.8, video_length * 1.1))
        return 0
    except:
        raise Exception(f"=== Can not find video X_ID: {x_vid_id} ===")


def reject_cookies(driver: webdriver.Chrome):
    login_url = "https://www.youtube.com/"
    driver.get(login_url)
    time.sleep(1)

    x_path = "/html/body/ytd-app/ytd-consent-bump-v2-lightbox/tp-yt-paper-dialog/div[4]/div[2]/div[6]/div[1]/ytd-button-renderer[1]/yt-button-shape/button"
    driver.find_element(By.XPATH, x_path).click()
    time.sleep(2)


def get_random_video_id(max_id: int) -> int:
    start_id = max_id
    end_id = start_id - 4

    result_list = []
    multiplier = 8

    while end_id > 0:
        for id in range(start_id, end_id, -1):
            for j in range(0, multiplier, 1):
                result_list.append(id)

        if multiplier > 2:
            multiplier -= 2

        start_id -= 4
        end_id = start_id - 4

    if start_id > 0:
        for id in range(start_id, 0, -1):
            for j in range(0, multiplier, 1):
                result_list.append(id)

    random.shuffle(result_list)
    return random.choice(result_list)


def main():
    list_of_videos = []
    driver = None

    chromedriver_autoinstaller.install()
    driver = webdriver.Chrome()
    reject_cookies(driver)
    # scroll_main_shorts_page(driver, 3)
    go_to_my_channel(driver)
    go_to_shorts_in_my_channel(driver)
    max_vid_id = get_max_shorts_count(driver)
    vid_id = get_random_video_id(max_vid_id)
    click_X_number_short(driver, vid_id)
    scroll_main_shorts_page(driver, 5)


if __name__ == '__main__':
    main()
