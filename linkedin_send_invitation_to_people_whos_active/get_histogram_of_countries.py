import json

from linkedin_send_invitation_to_people_whos_active.main import LPeople


def main():
    dict_countries = {}
    with open(r"C:\devops_sandbox\git\python_youtube\list_of_users_that_liked_some_publications_in_last_24h.json", "r") as f:
        list_of_users = json.load(f)
        list_of_users = [LPeople(**item) for item in list_of_users]

    for user in list_of_users:
        if user.country != "":
            if user.country not in dict_countries:
                dict_countries[user.country] = 0
            dict_countries[user.country] += 1

    sorted_data = sorted(dict_countries.items(), key=lambda x: x[1], reverse=True)

    counter = 0
    for k_v in sorted_data:
        counter += k_v[1]

    print(f"Total: {counter}")
    for k_v in sorted_data:
        print(k_v)

    # with open("list_of_users_that_liked_some_publications_in_last_24h.json", "w") as f:
    #     json.dump([item.__dict__ for item in list_of_users], f, indent=4)



if __name__ == '__main__':
    main()