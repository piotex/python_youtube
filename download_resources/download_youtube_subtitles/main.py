import os
import re

from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
import requests
from bs4 import BeautifulSoup
import YoutubeTags
from YoutubeTags import videotags


def split_subtitles(subtitles: str, max_text_len: int) -> list:
    chunks = []
    current_chunk = ''
    tmp_sub = subtitles[:]
    words = tmp_sub.replace('\n', '').replace('.', ". ").split()
    for word in words:
        if len(current_chunk) + len(word) <= max_text_len:
            current_chunk += word + ' '
        else:
            chunks.append(current_chunk)
            current_chunk = word + ' '

    if current_chunk:
        chunks.append(current_chunk)
    return chunks


def get_description(url: str) -> str:
    soup = BeautifulSoup(requests.get(url).content, features="html.parser")
    pattern = re.compile('(?<=shortDescription":").*(?=","isCrawlable)')
    description = pattern.findall(str(soup))[0].replace('\\n', '\n')

    # description = YouTube(url).description
    return description


def get_tags(url: str) -> str:
    variable_name = videotags(url)
    return variable_name


def get_title(url: str) -> str:
    r = requests.get(url)
    soup = BeautifulSoup(r.text, features="html.parser")  # Specify html parser
    title = soup.find("title").text.strip()  # Use .text and .strip() for cleaner extraction
    return title


def get_subtitles(url: str) -> str:
    video_id = url.split("v=")[1]
    res = YouTubeTranscriptApi.get_transcript(video_id)

    res_text = [x['text'] for x in res]
    text = '\n'.join(res_text)

    return text


def create_directory_if_missing(directory_path: str):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)


def create_file_if_missing(file_path: str):
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            file.write("")


def main():
    init_paths = ["input_data", "output_data", "output_data/subtitles_for_google", "output_data/subtitles_for_chatgpt", "output_data/main_data"]
    for init_path in init_paths:
        create_directory_if_missing(init_path)

    path_in = "input_data/urls.txt"
    create_file_if_missing(path_in)
    with open(path_in) as reader:
        urls = [x.strip() for x in reader.readlines() if x.strip() != ""]

    for url in urls:
        title = get_title(url)
        subtitles = get_subtitles(url)
        description = get_description(url)
        tags = get_tags(url)

        subtitles_list = split_subtitles(subtitles, 4500)
        for i, elem in enumerate(subtitles_list):
            with open(f"output_data/subtitles_for_google/subtitles_{title[:20]}_{i}.txt", 'w') as writer:
                writer.writelines(elem)

        subtitles_list = split_subtitles(subtitles, 2000)
        for i, elem in enumerate(subtitles_list):
            with open(f"output_data/subtitles_for_chatgpt/subtitles_{title[:20]}_{i}.txt", 'w') as writer:
                writer.writelines(elem)

        with open(f"output_data/main_data/description_{title[:20]}.txt", 'w', encoding="utf-8") as writer:
            writer.writelines(description)
        with open(f"output_data/main_data/tags_{title[:20]}.txt", 'w', encoding="utf-8") as writer:
            writer.writelines(tags)


if __name__ == '__main__':
    main()
