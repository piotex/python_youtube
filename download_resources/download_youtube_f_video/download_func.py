from pytube import YouTube


def download_video(url: str, path_out: str, high_quality: bool):
    yt = YouTube(url)
    a1 = yt.streams
    a3 = a1.filter(file_extension="mp4")
    a4 = a3.filter(type="video")
    if high_quality:
        a5 = a4.order_by("abr").desc()  # highest first
    else:
        a5 = a4.order_by("abr").asc()   # lowest first
    a6 = a5.first().download(output_path=path_out)
