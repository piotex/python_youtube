from pytube import YouTube

path_out = "output_data"
# link of the video to be downloaded
link = "https://www.youtube.com/watch?v=2aoLsF3-2gI"

try:
    # object creation using YouTube
    yt = YouTube(link)
except:
    #to handle exception
    print("Connection Error")

# Get all streams and filter for mp4 files
mp4_streams = yt.streams.filter(file_extension='mp4').all()

# get the video with the highest resolution
d_video = mp4_streams[-1]

try:
    # downloading the video
    d_video.download(output_path=path_out)
    print('Video downloaded successfully!')
except:
    print("Some Error!")