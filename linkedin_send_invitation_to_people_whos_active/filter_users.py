import json

from linkedin_send_invitation_to_people_whos_active.main import LPeople
import datetime

def main():
    max_followers_threshold = 3001

    data_file_path = r"C:\devops_sandbox\git\python_youtube\list_of_users_that_liked_some_publications_in_last_24h.json"

    dict_countries = {}
    with open(data_file_path, "r") as f:
        list_of_users = json.load(f)
        list_of_users = [LPeople(**item) for item in list_of_users]

    with open(data_file_path+f".backup.{datetime.date.today()}.json", "w") as f:
        json.dump([item.__dict__ for item in list_of_users], f, indent=4)

    tmp = []
    banned_last_activity = ["mies.", "mies", "t"]
    for user in list_of_users:
        is_active_user = True
        for activity in banned_last_activity:
            if activity in user.last_activity:
                is_active_user = False
                break

        if is_active_user:
            tmp.append(user)
    list_of_users = tmp

    tmp = []
    banned_countries = ["Ukraina", ""]
    for user in list_of_users:
        if user.country != "" and user.country not in banned_countries:
            tmp.append(user)
    list_of_users = tmp

    tmp = []
    for user in list_of_users:
        if int(user.number_of_folowers) < max_followers_threshold:
            tmp.append(user)
    list_of_users = tmp

    print(len(list_of_users))

    # tmp = []
    # for user in list_of_users:
    #     if user.country != "":
    #         tmp.append(user)
    # list_of_users = tmp

    with open(data_file_path, "w") as f:
        json.dump([item.__dict__ for item in list_of_users], f, indent=4)



if __name__ == '__main__':
    main()