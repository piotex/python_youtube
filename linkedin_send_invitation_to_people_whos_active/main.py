import time
from selenium import webdriver
import chromedriver_autoinstaller
from selenium.webdriver.common.by import By
import json
from dataclasses import dataclass


@dataclass
class LPeople:
    url: str = ""
    number_of_contacts: int = 0

    processed_count: int = 0


def login_to_linkedin(driver: webdriver.Chrome):
    login_url = "https://www.linkedin.com/uas/login"
    driver.get(login_url)
    time.sleep(1)

    x_path = "/html/body/div/main/div[1]/div/section/div/div[2]/button[2]"
    driver.find_element(By.XPATH, x_path).click()
    time.sleep(1)

    secrets_path = r"C:\devops_sandbox\git\secrets\linkedin.pwd"
    with open(secrets_path) as reader:
        x_path = "/html/body/div/main/div[2]/div[1]/form/div[1]/input"
        driver.find_element(By.XPATH, x_path).send_keys(reader.readlines()[0].strip())
    with open(secrets_path) as reader:
        x_path = "/html/body/div/main/div[2]/div[1]/form/div[2]/input"
        driver.find_element(By.XPATH, x_path).send_keys(reader.readlines()[1].strip())
    x_path = "/html/body/div/main/div[2]/div[1]/form/div[3]/button"
    driver.find_element(By.XPATH, x_path).click()
    time.sleep(1)


def get_users_that_liked_some_publications_in_last_24h(driver: webdriver.Chrome) -> list[LPeople]:
    number_of_scrolls = 3
    keywords_list = [
        # "aws",
        "devops"
    ]
    return_list = []
    return_list_tmp_urls = []
    for keyword in keywords_list:
        url_main_search_page = f"https://www.linkedin.com/search/results/content/?datePosted=%22past-24h%22&keywords={keyword}&sid=S6p"
        driver.get(url_main_search_page)
        time.sleep(3)
        for j in range(1, number_of_scrolls, 1):
            driver.execute_script(f"window.scrollTo(0, {j * 1000})")
            time.sleep(1)
        driver.execute_script(f"window.scrollTo(0, {0})")
        time.sleep(1)
        for i1 in range(5, 7):
            for i2 in range(3, 4):
                for i3 in range(2, 3):
                    for i4 in range(1, 2):
                        for i5 in range(1, 2):
                            for i6 in range(1, 9):
                                for i7 in range(1, 9):
                                    for i8 in range(1, 9):
                                        x_path_list = [
                                            f"/html/body/div[{i1}]/div[{i2}]/div[{i3}]/div/div[{i4}]/main/div/div/div/div[{i5}]/div[{i6}]/div/ul/li[{i7}]/div/div/div/div/div/div[{i8}]/div[1]/div/div/ul/li[1]/button",
                                            # f"/html/body/div[{i1}]/div[{i2}]/div[{i3}]/div/div[{i4}]/main/div/div/div/div[{i5}]/div[{i6}]/div/ul/li[{i7}]/div/div/div/div/div/div[{i8}]/div[1]/div/div/ul/li/button",
                                        ]
                                        for x_path in x_path_list:
                                            try:
                                                text = driver.find_element(By.XPATH, x_path+"/span").text
                                                if text.isdigit():
                                                    driver.find_element(By.XPATH, x_path).click()
                                                    time.sleep(2)

                                                    if int(text) > 5:
                                                        for ii3 in range(1, int(text), 3):
                                                            x_path = f"/html/body/div[3]/div/div/div[2]"
                                                            pop_up_window = driver.find_element(By.XPATH, x_path)
                                                            driver.execute_script(f"arguments[0].scrollTo(0, {ii3 * 1000})", pop_up_window)
                                                            time.sleep(0.5)

                                                    for ii4 in range(1,int(text)+1):
                                                        x_path = f"/html/body/div[3]/div/div/div[2]/div/div/div[1]/ul/li[{ii4}]/div/div/a"
                                                        try:
                                                            url_to_person_site = driver.find_element(By.XPATH, x_path).get_attribute('href')
                                                            return_list_tmp_urls.append(LPeople(url=url_to_person_site))
                                                        except:
                                                            pass

                                                    x_path = "/html/body/div[3]/div/div/button"
                                                    driver.find_element(By.XPATH, x_path).click()
                                                    time.sleep(1)
                                            except Exception as excepppption:
                                                pass
    # ############################
    # TODO:
    # return unique list of LPeople based on url
    # ############################

    return return_list_tmp_urls


def send_invitation_to_linkedin_user(driver: webdriver.Chrome, url: str):
    number_of_contacts = 0
    last_activity = 0

    driver.get(url)
    time.sleep(3)

    for i1 in range(4,7):
        x_path = f"/html/body/div[{i1}]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/ul/li[2]/span"
        try:
            inner_text = driver.find_element(By.XPATH, x_path).text
            number_of_contacts = inner_text.split(" ")[0]                                                                                         # 499     500+
            a = 0
        except:
            pass

    for i1 in range(4,7):
        x_path = f"/html/body/div[{i}]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/ul/li[1]/span"
        try:
            inner_text = driver.find_element(By.XPATH, x_path).text
            number_of_folowers = inner_text.split(" ")[0]                                                                                         # 499     500+
            a = 0
        except:
            pass


    for i1 in range(4,7):
        for i2 in range(1, 6):
            for i3 in range(3, 0, -1):
                x_path = f"/html/body/div[{i1}]/div[3]/div/div/div[2]/div/div/main/section[{i2}]/div[4]/div/div/div[1]/ul/li[{i3}]/div/div/a/div/span/span[1]"
                try:
                    inner_text = driver.find_element(By.XPATH, x_path).text
                    last_activity = driver.find_element(By.XPATH, x_path).text                  #  • 1 mies.  • 8h    11h   1d
                    a = 0
                except:
                    pass


    aa = 0



def get_user_list_from_linkedin(driver: webdriver.Chrome) -> list[LPeople]:
    tmp_url = "https://www.linkedin.com/mynetwork/invite-connect/connections/"
    driver.get(tmp_url)
    time.sleep(5)

    # aaa = input()

    user_list = []
    old_j = 0
    for j in range(1, 550, 1):
        driver.execute_script(f"window.scrollTo(0, {j * 1000})")
        try:
            x_path = "/html/body/div[6]/div[3]/div/div/div/div/div[2]/div/div/main/div/section/div[2]/div[2]/div/button"
            driver.find_element(By.XPATH, x_path).click()
        except:
            pass

        for k in range(1, 3, 1):
            try:
                x_path = f"/html/body/div[6]/div[3]/div/div/div/div/div[2]/div/div/main/div/section/div[2]/div[1]/ul/li[{j}]/div/div/div[{k}]/a"
                tmp_url = driver.find_element(By.XPATH, x_path).get_attribute('href')
                user_list.append(LPeople(tmp_url, 0))
                break
            except:
                pass
        if len(user_list) == old_j:
            break
        old_j = j
    return user_list


def get_user_list_from_file() -> list[LPeople]:
    with open("user_list.json", "r") as f:
        data = json.load(f)
    items = [LPeople(**item) for item in data]
    return items


def sort_by_count_descending(obj_list):
    def get_count(obj):
        return obj.count

    sorted_list = sorted(obj_list, key=get_count, reverse=False)
    return sorted_list


def main():
    list_of_users = []
    driver = None
    init_linkedin = True
    get_users_from_linkedin = False
    get_users_from_file = True
    send_invitation = True

    if init_linkedin:
        chromedriver_autoinstaller.install()
        driver = webdriver.Chrome()
        login_to_linkedin(driver)
        print("Waiting for confirmation {ENTER} that logged in successfully...")
        input()

    if get_users_from_linkedin:
        list_of_users = get_users_that_liked_some_publications_in_last_24h(driver)
        with open("list_of_users_that_liked_some_publications_in_last_24h.json", "w") as f:
            json.dump([item.__dict__ for item in list_of_users], f, indent=4)

    if get_users_from_file:
        with open("list_of_users_that_liked_some_publications_in_last_24h.json", "r") as f:
            list_of_users = json.load(f)
            list_of_users = [LPeople(**item) for item in list_of_users]

    if send_invitation:
        for user in list_of_users:
            send_invitation_to_linkedin_user(driver, url=user.url)










    l_usr_list = get_user_list_from_linkedin(driver)
    f_usr_list = get_user_list_from_file()

    for i in range(len(l_usr_list)):
        for j in range(len(f_usr_list)):
            if l_usr_list[i].url == f_usr_list[j].url:
                l_usr_list[i] = f_usr_list[j]

    l_usr_list = sort_by_count_descending(l_usr_list)
    new_people = 0
    for i, item in enumerate(l_usr_list):
        if new_people >= 30:
            break
        driver.get(item.url)
        time.sleep(5)
        x_path = "/html/body/div[6]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/ul/li/a"
        driver.find_element(By.XPATH, x_path).click()
        time.sleep(10)
        for j in range(1, 11, 1):
            try:
                x_path = f"/html/body/div[6]/div[3]/div[2]/div/div[1]/main/div/div/div[1]/div/ul/li[{j}]/div/div/div/div[3]/div/button/span"
                tmp_button = driver.find_element(By.XPATH, x_path).text
                x_path = f"/html/body/div[6]/div[3]/div[2]/div/div[1]/main/div/div/div[1]/div/ul/li[{j}]/div/div/div/div[2]/div[1]/div[1]/div/span[1]/span/a/span/span[1]"
                tmp_name = driver.find_element(By.XPATH, x_path).text
                time.sleep(1)

                if "kontakt" not in tmp_button:
                    continue
                for name in names_list:
                    if name in tmp_name:
                        raise Exception("polish name")

                x_path = f"/html/body/div[6]/div[3]/div[2]/div/div[1]/main/div/div/div[1]/div/ul/li[{j}]/div/div/div/div[3]/div/button"
                driver.find_element(By.XPATH, x_path).click()
                time.sleep(1)
                x_path = "/html/body/div[3]/div/div/div[3]/button[2]"
                driver.find_element(By.XPATH, x_path).click()
                time.sleep(1)
                l_usr_list[i].count += 1
                new_people += 1
            except:
                pass
            a = 0

    data = [item.__dict__ for item in l_usr_list]
    with open("user_list.json", "w") as f:
        json.dump(data, f, indent=4)


if __name__ == '__main__':
    main()
