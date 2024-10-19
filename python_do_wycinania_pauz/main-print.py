import pydub
import numpy as np

IMAGEMAGICK_BINARY=r"C:\Users\pkubo\Desktop\ImageMagick-7.1.1-34-portable-Q16-x64\magick.exe"
# pip install ffmpeg-downloader


import matplotlib.pyplot as plt
import numpy as np

def read(f):
    """MP3 to numpy array"""
    a = pydub.AudioSegment.from_mp3(f)
    y = np.array(a.get_array_of_samples())
    return a.frame_rate, y

in_path = r'C:\devops_sandbox\git\python_do_wycinania_pauz\test-video.mp3'
sr, x = read(in_path)

sr = sr*2
x = x
time = len(x)/sr
time_s = f"{int(time/60)}min {int(time-(int(time/60)*60))}s"
print(x)


treshold = 3500
treshold_step = 200000

ypoints = x
disc_domain = [[x, x+treshold_step] for x in range(0, len(ypoints), treshold_step)]
finded_domains = [dom for dom in disc_domain if max(ypoints[dom[0]:dom[1]]) > treshold]
merged_domains = [finded_domains[0]]
for i in range(len(finded_domains)):
    if merged_domains[-1][1] == finded_domains[i][0]:
        merged_domains[-1][1] = finded_domains[i][1]
    else:
        merged_domains.append(finded_domains[i])

limited_domains = []
for i in range(len(merged_domains)):
    start_i = merged_domains[i][0]
    end_i = merged_domains[i][1]

    samll_treshold = 1
    while ypoints[start_i+samll_treshold] < treshold:
        start_i += samll_treshold
        if samll_treshold+start_i > len(ypoints):
            break
    while ypoints[end_i-samll_treshold] < treshold:
        end_i -= samll_treshold
    limited_domains.append([start_i, end_i])

samll_treshold = 50000
extended_domains = [[dom[0]-samll_treshold, dom[1]+samll_treshold] for dom in limited_domains]

# colors = 'grbcmk'
#
# xpoints = list(range(len(ypoints)))
# plt.rcParams["figure.figsize"] = (30,15)
# plt.plot(xpoints, ypoints)
#
# for i in range(1, len(disc_domain)):
#     plt.plot([disc_domain[i-1], disc_domain[i]], [treshold, treshold], color=colors[i%len(colors)])
#
# steppp = 200
# for i, word in enumerate(disc_domain):
#     plt.plot([word[0], word[1]], [treshold+steppp, treshold+steppp], color=colors[i%len(colors)])
# steppp = 400
# for i, word in enumerate(merged_domains):
#     plt.plot([word[0], word[1]], [treshold+steppp, treshold+steppp], color=colors[i%len(colors)])
# steppp = 600
# for i, word in enumerate(limited_domains):
#     plt.plot([word[0], word[1]], [treshold+steppp, treshold+steppp], color=colors[i%len(colors)])
# steppp = 800
# for i, word in enumerate(extended_domains):
#     plt.plot([word[0], word[1]], [treshold+steppp, treshold+steppp], color=colors[i%len(colors)])
# plt.show()

# ==========================================================================


from moviepy.editor import *
clip = VideoFileClip("test-video.mp4")
clips = []
for dom in extended_domains:
    start_i = dom[0]
    end_i = dom[0]
    clips.append(clip.subclip(start_i, end_i))

video = CompositeVideoClip(clips)
video.write_videofile("test-video-2.mp4")


