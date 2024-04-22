from youtube_transcript_api import YouTubeTranscriptApi
import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
import chromedriver_autoinstaller
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def accept_cookies(driver_loc: WebDriver) -> None:
    yt_url = "https://youtube.com"
    x_path = "//*[@id=\"content\"]/div[2]/div[6]/div[1]/ytd-button-renderer[2]/yt-button-shape/button/yt-touch-feedback-shape/div/div[2]"
    driver_loc.get(yt_url)
    driver_loc.find_element(By.XPATH, x_path).click()


def scroll_to_bottom(driver: WebDriver):
    for i in range(1, 50, 1):
        driver.execute_script(f"window.scrollTo(0, {i * 1000})")
        time.sleep(0.5)


def get_init_driver() -> WebDriver:
    chromedriver_autoinstaller.install()
    driver = webdriver.Chrome()
    accept_cookies(driver)
    return driver


def get_title(url: str) -> str:
    r = requests.get(url)
    soup = BeautifulSoup(r.text)

    link = soup.find_all(name="title")[0]
    title = str(link)
    title = title.replace("<title>", "")
    title = title.replace("</title>", "")

    return title


def get_url_from_home_page(url: str) -> list:
    driver = get_init_driver()
    time.sleep(0.5)
    driver.get(url)
    time.sleep(0.5)

    prev_url_list_len = 0
    for i in range(1, 150, 1):
        url_list = []
        for j in range(1, 5, 1):
            driver.execute_script(f"window.scrollTo(0, {((i * 10) + j) * 1000})")
            time.sleep(0.5)
        r_text = driver.page_source

        try:
            for a in BeautifulSoup(r_text).find_all('a', class_='yt-simple-endpoint'):
                if "href" in str(a):
                    url_list.append(a.get('href'))
        except:
            pass

        url_list = list(set(url_list))
        if len(url_list) == prev_url_list_len:
            return url_list

        prev_url_list_len = len(url_list)
    raise Exception("No a_href in page --- pk")


def get_subtitles(url: str) -> str:
    video_id = url.split("v=")[1]
    res = YouTubeTranscriptApi.get_transcript(video_id)

    res_text = [x['text'] for x in res]
    text = '\n'.join(res_text)

    return text
