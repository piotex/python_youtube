import time

import win32clipboard
from selenium import webdriver
import chromedriver_autoinstaller
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from common_func.create_init_dirs import create_directory_if_missing, create_file_if_missing
import win32com.client
from passwords import *

def main():

    chromedriver_autoinstaller.install()
    driver = webdriver.Chrome()

    tmp_url = "https://www.linkedin.com/uas/login"
    driver.get(tmp_url)
    time.sleep(1)

    x_path = "/html/body/div/main/div[1]/div/section/div/div[2]/button[2]"
    driver.find_element(By.XPATH, x_path).click()
    time.sleep(1)

    x_path = "/html/body/div/main/div[2]/div[1]/form/div[1]/input"
    driver.find_element(By.XPATH, x_path).send_keys(usr)
    x_path = "/html/body/div/main/div[2]/div[1]/form/div[2]/input"
    driver.find_element(By.XPATH, x_path).send_keys(pwd)
    x_path = "/html/body/div/main/div[2]/div[1]/form/div[3]/button"
    driver.find_element(By.XPATH, x_path).click()

    aaa = input()

    tmp_url = "https://www.linkedin.com/in/piotr-kubo%C5%84-b6b081232/overlay/create-post"
    driver.get(tmp_url)
    time.sleep(5)

    x_path = "/html/body/div[3]/div/div/div/div[2]/div/div[2]/div[1]/div/div/div/div/div/div/div[1]"
    driver.find_element(By.XPATH, x_path).click()
    time.sleep(0.5)

    x_path = "/html/body/div[3]/div/div/div/div[2]/div/div[2]/div[1]/div/div/div/div/div/div/div[1]/p"
    text = "ala test \n kota \n piesssss"
    driver.find_element(By.XPATH, x_path).send_keys(text)
    time.sleep(1)

    x_path = "/html/body/div[3]/div/div/div/div[2]/div/div[2]/div[2]/div[1]/div/section/div[2]/ul/li[1]/div/div/span/button"
    driver.find_element(By.XPATH, x_path).click()
    time.sleep(0.5)

    tmp_path = r"C:\Users\pkubo\Pictures\Screenshots\Zrzut ekranu 2024-05-20 181619.png"
    x_path = "/html/body/div[3]/div/div/div/div[2]/div/div/div[1]/div/div[2]/input"
    driver.find_element(By.XPATH, x_path).send_keys(tmp_path)

    x_path = "/html/body/div[3]/div/div/div/div[2]/div/div/div[2]/div/button[2]"
    driver.find_element(By.XPATH, x_path).click()
    time.sleep(1)

    x_path = "/html/body/div[3]/div/div/div/div[2]/div/div/div[2]/div[3]/div/div[2]/button"
    driver.find_element(By.XPATH, x_path).click()

    a = 9


    # init_paths = ["input_data", "output_data"]
    # for init_path in init_paths:
    #     create_directory_if_missing(init_path)
    #
    # path_in = "input_data/urls.txt"
    # create_file_if_missing(path_in)
    # with open(path_in) as reader:
    #     urls = [x.strip() for x in reader.readlines() if x.strip() != ""]
    #
    # for url in urls:
    #     title = get_title(url)
    #     url_list = get_url_from_home_page(url)
    #     url_list = [x for x in url_list if "/shorts/" in x]
    #     with open(f"output_data/urls_{title}.txt", 'w') as writer:
    #         for elem in url_list:
    #             writer.write(f"{elem}\n")



if __name__ == '__main__':
    main()
