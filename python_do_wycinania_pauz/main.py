import os
from datetime import datetime
from subprocess import check_output
from moviepy.editor import VideoFileClip
import time
import pydub
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.compositing.concatenate import concatenate_videoclips

IMAGEMAGICK_BINARY = r"C:\Users\pkubo\Desktop\ImageMagick-7.1.1-34-portable-Q16-x64\magick.exe"
# pip install ffmpeg-downloader

tmp_file = "tmp_file"
output_file = rf'output_file/result.mp4'

treshold = 3500
samll_treshold = 20000
treshold_step = 100000

main_start_time = time.time()


def rm_tmp():
    for f in os.listdir(os.path.join(os.curdir, tmp_file)):
        os.remove(os.path.join(os.curdir, tmp_file, f))

    for f in os.listdir(os.path.join(os.curdir, output_file.split('/')[0])):
        os.remove(os.path.join(os.curdir, output_file.split('/')[0], f))


def convert_to_mp3(mp4_file: str) -> str:
    out_file_path = os.path.join(os.curdir, tmp_file, mp4_file.split("\\")[-1].replace("mp4", "mp3"))
    video_clip = VideoFileClip(mp4_file)
    audio_clip = video_clip.audio
    audio_clip.write_audiofile(out_file_path, verbose=False, logger=None, )
    audio_clip.close()
    video_clip.close()
    return out_file_path


def get_sound_array(mp3_file: str) -> np.array:
    audio_clip = pydub.AudioSegment.from_mp3(mp3_file)
    return np.array(audio_clip.get_array_of_samples())


def get_extended_domains(ypoints):
    disc_domain = [[x, x + treshold_step] for x in range(0, len(ypoints), treshold_step)]
    finded_domains = [dom for dom in disc_domain if max(ypoints[dom[0]:dom[1]]) > treshold]
    merged_domains = [finded_domains[0]]
    for i in range(1, len(finded_domains)):
        if merged_domains[-1][1] == finded_domains[i][0]:
            merged_domains[-1][1] = finded_domains[i][1]
        else:
            merged_domains.append(finded_domains[i])

    limited_domains = []
    for i in range(len(merged_domains)):
        start_i = merged_domains[i][0]
        end_i = merged_domains[i][1]

        samll_tr = 1
        while ypoints[start_i + samll_tr] < treshold:
            start_i += samll_tr
            if samll_tr + start_i > len(ypoints):
                break
        while ypoints[end_i - samll_tr] < treshold:
            end_i -= samll_tr
        limited_domains.append([start_i, end_i])

    extended_domains = [[dom[0] - samll_treshold, dom[1] + samll_treshold] for dom in limited_domains]
    return extended_domains


def print_sound_chart(ypoints, extended_domains):
    colors = 'grbcmk'
    xpoints = list(range(len(ypoints)))
    plt.rcParams["figure.figsize"] = (30, 15)
    plt.plot(xpoints, ypoints)

    # for i in range(1, len(disc_domain)):
    #     plt.plot([disc_domain[i-1], disc_domain[i]], [treshold, treshold], color=colors[i%len(colors)])
    # steppp = 200
    # for i, word in enumerate(disc_domain):
    #     plt.plot([word[0], word[1]], [treshold+steppp, treshold+steppp], color=colors[i%len(colors)])
    # steppp = 400
    # for i, word in enumerate(merged_domains):
    #     plt.plot([word[0], word[1]], [treshold+steppp, treshold+steppp], color=colors[i%len(colors)])
    # steppp = 600
    # for i, word in enumerate(limited_domains):
    #     plt.plot([word[0], word[1]], [treshold+steppp, treshold+steppp], color=colors[i%len(colors)])
    steppp = 800
    for i, word in enumerate(extended_domains):
        plt.plot([word[0], word[1]], [treshold + steppp, treshold + steppp], color=colors[i % len(colors)])
    plt.show()


def convert_to_s(timee, video_duration, audio_length):
    return video_duration * timee / audio_length


def create_sub_video(sub_path, dom, main_video, ypoints):
    video_duration = main_video.duration
    start_i = dom[0]
    end_i = dom[1]
    start_i = convert_to_s(start_i, video_duration, len(ypoints))
    end_i = convert_to_s(end_i, video_duration, len(ypoints))
    vid_sub = main_video.subclip(start_i, end_i)
    # aud_sub = aud_clip.subclip(start_i, end_i)
    # video = CompositeVideoClip([vid_sub, aud_sub])
    # video = CompositeVideoClip([vid_sub])
    # ===========================================
    # vid_sub.write_videofile(
    #     sub_path,
    #     # fps=vid_clip.fps,
    #     # threads=16,
    #     verbose=False,
    #     logger=None,
    #     # codec="rawvideo",
    #     # preset="veryslow",
    #     audio=True,
    #     audio_bitrate="3000k",
    #     # audio_codec="libmp3lame"
    # )
    # ===========================================
    return vid_sub


def main():
    input_dir = r'input_file'
    rm_tmp()
    for f_mp4 in os.listdir(input_dir):
        f_mp4 = os.path.join(os.curdir, input_dir, f_mp4)
        start_time = time.time()
        f_mp3 = convert_to_mp3(f_mp4)
        print(f"MP4 to MP3: {str(round(time.time() - start_time, 2))}s")

        start_time = time.time()
        ypoints = get_sound_array(f_mp3)
        print(f"Load MP3 file to np array: {str(round(time.time() - start_time, 2))}s")
        start_time = time.time()

        extended_domains = get_extended_domains(ypoints)
        print(f"Get extended domains: {str(round(time.time() - start_time, 2))}s")
        start_time = time.time()
        # # ========================================================
        # print_sound_chart(ypoints, extended_domains)
        # # ========================================================

        part_video_list = []
        vid_clip = VideoFileClip(f_mp4)
        # aud_clip = VideoFileClip(mp4_file)
        for i, dom in enumerate(extended_domains):
            start_time_2 = time.time()
            sub_path = os.path.join(os.curdir, tmp_file, f"{i}.mp4")
            vid = create_sub_video(sub_path, dom, vid_clip, ypoints)
            part_video_list.append(vid)
            print(f"Time: {str(round(time.time() - start_time_2, 2))}s | Partial: {i}/{len(extended_domains)}")
        print(f"Partial video: {str(round(time.time() - start_time, 2))}s")
        start_time = time.time()

        max_len = 100
        for i in range(1 + int(len(part_video_list) / max_len)):
            tmp_output_file = rf'{tmp_file}/{i}.mp4'
            video_clips = part_video_list[i * max_len:(i + 1) * max_len]
            tmp_clip = concatenate_videoclips(video_clips)
            tmp_clip.to_videofile(tmp_output_file, verbose=False, logger=None)
            print(f"Concatenate video {i+1}: {str(round(time.time() - start_time, 2))}s")
            start_time = time.time()

            # check_output(f"ffmpeg -i {tmp_output_file} -f mov {tmp_output_file.replace('mp4', 'mov')}", shell=True)
            # print(f"Write video {i+1}: {str(round(time.time() - start_time, 2))}s")
            # start_time = time.time()

        files = [int(file.split(".")[0]) for file in os.listdir(os.path.join(os.curdir, tmp_file)) if file.endswith("mp4")]
        files = sorted(files)
        files = [f"{f}.mp4" for f in files]

        video_clips = [VideoFileClip(os.path.join(os.curdir, tmp_file, file)) for file in files]
        final_clip = concatenate_videoclips(video_clips)
        final_clip.to_videofile(output_file, verbose=False, logger=None)

        print(f"Write video: {str(round(time.time() - start_time, 2))}s")
        start_time = time.time()

        check_output(f"ffmpeg -i {output_file} -f mov {output_file.replace('mp4', 'mov')}", shell=True)

        main_time = time.time() - main_start_time
        print(f"=== Total time:  {int(main_time / 60)}min {int(main_time - int(main_time / 60) * 60)}s ===")


main()
