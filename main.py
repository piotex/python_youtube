from pytube import YouTube

def main():
    path = "urls.txt"
    urls = []

    with open(path) as reader:
        urls = [x.strip() for x in reader.readlines() if x.strip() != ""]

    for url in urls:
        yt = YouTube(url)
        yt.streams.filter(type="audio").filter(file_extension="mp4").order_by("abr").asc().first().download()


if __name__ == '__main__':
    main()
