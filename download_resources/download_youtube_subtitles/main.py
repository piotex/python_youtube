from download_resources.download_youtube_subtitles.download_func import get_subtitles, get_title
from download_resources.download_youtube_subtitles.modify_func import split_subtitles


def main():
    path_in = "input_data/urls.txt"
    with open(path_in) as reader:
        urls = [x.strip() for x in reader.readlines() if x.strip() != ""]

    for url in urls:
        title = get_title(url)
        subtitles = get_subtitles(url)

        subtitles_list = split_subtitles(subtitles, 4500)
        for i, elem in enumerate(subtitles_list):
            with open(f"output_data/subtitles_for_google/subtitles_{title}_{i}.txt", 'w') as writer:
                writer.writelines(elem)

        subtitles_list = split_subtitles(subtitles, 2000)
        for i, elem in enumerate(subtitles_list):
            with open(f"output_data/subtitles_for_chatgpt/subtitles_{title}_{i}.txt", 'w') as writer:
                writer.writelines(elem)


if __name__ == '__main__':
    main()
