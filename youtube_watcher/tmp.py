import random

from pytube import YouTube


# video = "https://www.youtube.com/shorts/MTc-EHwR4Fg"
# yt = YouTube(video)  ## this creates a YOUTUBE OBJECT
# video_length = yt.length   ## this wil
#
# aa = 0

def get_random_video_id(max_id: int):
    # max = 10
    # 10 - 7    x8
    # 6 - 3     x6
    # 2 - 1     x4

    start_id = max_id
    end_id = start_id-4

    result_list = []
    multiplier = 8

    while end_id > 0:
        for id in range(start_id, end_id, -1):
            for j in range(0,multiplier,1):
                result_list.append(id)

        if multiplier > 2:
            multiplier -= 2

        start_id -= 4
        end_id = start_id-4

    if start_id > 0:
        for id in range(start_id, 0, -1):
            for j in range(0,multiplier,1):
                result_list.append(id)
    return result_list


def get_histogram(list_of_int):
    dict_countries = {}
    for user in list_of_int:
        if user not in dict_countries:
            dict_countries[user] = 0
        dict_countries[user] += 1

    sorted_data = sorted(dict_countries.items(), key=lambda x: x[1], reverse=True)

    counter = 0
    for k_v in sorted_data:
        counter += k_v[1]

    return sorted_data
    # print(f"raw: {sorted_data}")
    # for k_v in sorted_data:
    #     print(k_v)


# res_list = [0,0,
#             1,1,1,
#             2,2,2,2,
#             3,3,3,3,
#             4,4,4,4,
#             5,5,5,5,5,5,5]
# get_histogram(res_list)
#
# res_list = get_random_video_id(22)
# result = get_histogram(res_list)
# print(f"raw: {result}")
# for k_v in result:
#     print(k_v)


res_list_of_int = []
for i in range(0,10000,1):
    res_list_tmp = get_random_video_id(22)
    random.shuffle(res_list_tmp)
    res_int = random.choice(res_list_tmp)
    res_list_of_int.append(res_int)

result = get_histogram(res_list_of_int)
for k_v in result:
    print(k_v)



result = get_histogram(get_random_video_id(22))
expected = [(22, 8), (21, 8), (20, 8), (19, 8), (18, 6), (17, 6), (16, 6), (15, 6), (14, 4), (13, 4), (12, 4), (11, 4), (10, 2), (9, 2), (8, 2), (7, 2), (6, 2), (5, 2), (4, 2), (3, 2), (2, 2), (1, 2)]
for i in range(0, len(result), 1):
    if result[i] != expected[i]:
        raise Exception("aa0")
result = get_histogram(get_random_video_id(10))
expected = [(10, 8), (9, 8), (8, 8), (7, 8), (6, 6), (5, 6), (4, 6), (3, 6), (2, 4), (1, 4)]
for i in range(0, len(result), 1):
    if result[i] != expected[i]:
        raise Exception("aa1")
result = get_histogram(get_random_video_id(4))
expected = [(4, 8), (3, 8), (2, 8), (1, 8)]
for i in range(0, len(result), 1):
    if result[i] != expected[i]:
        raise Exception("aa2")
result = get_histogram(get_random_video_id(2))
expected = [(2, 8), (1, 8)]
for i in range(0, len(result), 1):
    if result[i] != expected[i]:
        raise Exception("aa3")
result = get_histogram(get_random_video_id(1))
expected = [(1, 8)]
for i in range(0, len(result), 1):
    if result[i] != expected[i]:
        raise Exception("aa4")
result = get_histogram(get_random_video_id(0))
expected = []
for i in range(0, len(result), 1):
    if result[i] != expected[i]:
        raise Exception("aa5")


def get_row_column(idx: int):
    max_in_row = 4
    x_row = int((idx - 0.01) / max_in_row) + 1
    x_column = int(idx % max_in_row)
    if x_column == 0:
        x_column = max_in_row
    return (x_row, x_column)


if get_row_column(10) != (3, 2):
    raise Exception("ss1")
if get_row_column(2) != (1, 2):
    raise Exception("ss")
if get_row_column(3) != (1, 3):
    raise Exception("ss")
if get_row_column(4) != (1, 4):
    raise Exception("ss")
if get_row_column(5) != (2, 1):
    raise Exception("ss")
if get_row_column(6) != (2, 2):
    raise Exception("ss")
if get_row_column(7) != (2, 3):
    raise Exception("ss")
if get_row_column(8) != (2, 4):
    raise Exception("ss")
