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

    roi: int = -1


@dataclass
class yt_user:
    url: str = ""
    number_of_subscriptions: int = -1
    list_of_videos: list[yt_video] = field(default_factory=list)


if __name__ == "__main__":
    input_file = "output_data/list_of_videos.json"
    output_file = "output_data/channels.txt"

    res_lines = []
    with open(input_file, "r") as f:
        videos_list = json.load(f)
        videos_list = [yt_video(**item) for item in videos_list]


    for i, video in enumerate(videos_list):
        video.roi = video.number_of_views / video.base_channel_number_of_subscriptions

    sorted_videos = sorted(videos_list, key=lambda obj: obj.roi, reverse=True)

    for i in range(0,5,1):
        print(sorted_videos[i])

    with open("output_data/list_of_videos_ROI.json", "w") as f:
        json.dump([item.__dict__ for item in sorted_videos], f, indent=4)

    # with open("output_data/channels.json", "w") as f:
    #     json.dump([item.__dict__ for item in res_lines], f, indent=4)