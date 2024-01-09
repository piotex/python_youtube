from pytube import YouTube


def download_video_for_running():
    path = "urls.txt"
    urls = []
    with open(path) as reader:
        urls = [x.strip() for x in reader.readlines() if x.strip() != ""]
    for url in urls:
        yt = YouTube(url)
        a1 = yt.streams
        a3 = a1.filter(file_extension="mp4")
        a4 = a3.filter(type="video")
        a5 = a4.order_by("abr").asc()  # lowest first
        a6 = a5.first().download()


def download_audio():
    path = "urls.txt"
    urls = []
    with open(path) as reader:
        urls = [x.strip() for x in reader.readlines() if x.strip() != ""]
    for url in urls:
        yt = YouTube(url)
        a1 = yt.streams
        a4 = a1.filter(type="audio")
        a5 = a4.order_by("abr").asc()  # lowest first
        a6 = a5.first().download()


def main():
    download_video_for_running()
    # download_audio()


if __name__ == '__main__':
    main()
