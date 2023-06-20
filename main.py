from pytube import YouTube

def main():
    path = "urls.txt"
    urls = []

    with open(path) as reader:
        urls = [x.strip() for x in reader.readlines() if x.strip() != ""]

    for url in urls:
        yt = YouTube(url)
        a1 = yt.streams
        # a2 = a1.filter(type="audio")
        a3 = a1.filter(file_extension="mp4")
        a4 = a3.order_by("abr").asc().first().download()
        # yt.streams.filter(type="audio").filter(file_extension="mp4").order_by("abr").asc().first().download()


if __name__ == '__main__':
    main()
