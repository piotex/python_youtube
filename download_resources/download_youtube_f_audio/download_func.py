from pytube import YouTube


def download_audio(url: str, path_out: str):
    yt = YouTube(url)
    a1 = yt.streams
    a3 = a1.filter(file_extension="mp4")
    a4 = a3.filter(type="audio")
    a5 = a4.order_by("abr").asc()  # lowest first
    a6 = a5.first().download(output_path=path_out)




