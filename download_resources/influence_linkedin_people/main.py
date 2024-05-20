import time
from selenium import webdriver
import chromedriver_autoinstaller
from selenium.webdriver.common.by import By
from passwords import *
import json
from dataclasses import dataclass


@dataclass
class LPeople:
    url: str = ""
    count: int = 0

names_list = [
    "Adam", "Adrian", "Agata", "Agnieszka", "Alicja", "Amelia", "Anastazja", "Andrzej", "Angelika", "Anna",
    "Antoni", "Apolonia", "Aurelia", "Barbara", "Bartłomiej", "Beata", "Błażej", "Bogdan", "Bogumił", "Bożena",
    "Bruno", "Cezary", "Dagmara", "Damian", "Daniel", "Danuta", "Dariusz", "Dawid", "Dominik", "Dorota",
    "Edyta", "Eliza", "Elżbieta", "Emilia", "Eryk", "Ewa", "Fabian", "Filip", "Franciszek", "Gabriel",
    "Gabriela", "Grzegorz", "Halina", "Hanna", "Henryk", "Hubert", "Iga", "Igor", "Ilona", "Irena",
    "Iwona", "Izabela", "Jacek", "Jakub", "Jan", "Janina", "Joanna", "Jolanta", "Jonasz", "Józef",
    "Juliusz", "Justyna", "Kacper", "Kamil", "Karina", "Karolina", "Kazimierz", "Kinga", "Konrad", "Kornelia",
    "Krzysztof", "Laura", "Lech", "Leon", "Leszek", "Lidia", "Liliana", "Lucyna", "Łucja", "Maciej",
    "Magdalena", "Maja", "Malwina", "Marek", "Maria", "Marian", "Mariusz", "Marta", "Martyna", "Marzena",
    "Mateusz", "Małgorzata", "Michał", "Milena", "Mirosław", "Monika", "Natalia", "Nikodem", "Norbert", "Olaf",
    "Olga", "Oliwia", "Patrycja", "Paweł", "Piotr", "Przemysław", "Radosław", "Rafał", "Renata", "Robert",
    "Roksana", "Roman", "Ryszard", "Sebastian", "Seweryn", "Sławomir", "Stanisław", "Stefan", "Szymon", "Tadeusz",
    "Tamara", "Tomasz", "Urszula", "Waldemar", "Wanda", "Weronika", "Wiesław", "Wiktor", "Wiktoria", "Wioletta",
    "Witold", "Władysław", "Włodzimierz", "Zbigniew", "Zdzisław", "Zofia", "Zuzanna", "Łukasz", "Świętosław", "Żaneta"
]


def get_user_list_from_linkedin(driver) -> list[LPeople]:
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
    chromedriver_autoinstaller.install()
    driver = webdriver.Chrome()
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
        for j in range(1,11,1):
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
