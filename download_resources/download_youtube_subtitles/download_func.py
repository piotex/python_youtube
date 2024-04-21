from youtube_transcript_api import YouTubeTranscriptApi
import requests
from bs4 import BeautifulSoup


def get_title(url: str) -> str:
    r = requests.get(url)
    soup = BeautifulSoup(r.text)

    link = soup.find_all(name="title")[0]
    title = str(link)
    title = title.replace("<title>", "")
    title = title.replace("</title>", "")

    return title


def get_subtitles(url: str) -> str:
    video_id = url.split("v=")[1]
    res = YouTubeTranscriptApi.get_transcript(video_id)

    res_text = [x['text'] for x in res]
    text = '\n'.join(res_text)

    return text
