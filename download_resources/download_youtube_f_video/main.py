from download_resources.download_youtube_f_video.create_init_dirs import create_directory_if_missing
from download_resources.download_youtube_f_video.download_func import download_video
from datetime import datetime
import time


def chose_func_to_run(url, path_out):
    # download_video_for_running(url, path_out, True)         # for youtube
    download_video(url, path_out, True)  # for running


def main():
    init_paths = ["input_data", "output_data"]
    for init_path in init_paths:
        create_directory_if_missing(init_path)

    path_in = "input_data/urls.txt"
    path_out = "output_data"

    with open(path_in) as reader:
        urls = [x.strip() for x in reader.readlines() if x.strip() != ""]
    for url in urls:
        start_time = time.time()
        print(f"Start: {datetime.now()}")
        chose_func_to_run(url, path_out)
        print(f"End:   {datetime.now()}")
        end_time = time.time()
        elapsed_time = end_time - start_time
        elapsed_time_str = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
        print(f"Time taken: {elapsed_time_str}")


if __name__ == '__main__':
    main()
