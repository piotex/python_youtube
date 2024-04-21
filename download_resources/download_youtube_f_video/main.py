from pytube import YouTube

from download_resources.download_youtube_f_video.create_init_dirs import create_directory_if_missing


def download_video_for_running():
    path_in = "input_data/urls.txt"
    path_out = "output_data"
    urls = []
    with open(path_in) as reader:
        urls = [x.strip() for x in reader.readlines() if x.strip() != ""]
    for url in urls:
        yt = YouTube(url)
        a1 = yt.streams
        a3 = a1.filter(file_extension="mp4")
        a4 = a3.filter(type="video")
        a5 = a4.order_by("abr").asc()  # lowest first
        a6 = a5.first().download(output_path=path_out)


def download_video_for_yt():
    path = "input_data/urls.txt"
    urls = []
    with open(path) as reader:
        urls = [x.strip() for x in reader.readlines() if x.strip() != ""]
    for url in urls:
        yt = YouTube(url)
        a1 = yt.streams
        a3 = a1.filter(file_extension="mp4")
        a4 = a3.filter(type="video")
        a5 = a4.order_by("abr").desc()  # lowest first
        a6 = a5.first().download()


def main():
    init_paths = ["input_data", "output_data"]
    for init_path in init_paths:
        create_directory_if_missing(init_path)

    download_video_for_running()
    # download_video_for_yt()


if __name__ == '__main__':
    main()
