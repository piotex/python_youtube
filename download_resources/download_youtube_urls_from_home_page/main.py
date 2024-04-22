from download_func import get_subtitles, get_title, get_url_from_home_page
from common_func.create_init_dirs import create_directory_if_missing, create_file_if_missing


def main():
    init_paths = ["input_data", "output_data"]
    for init_path in init_paths:
        create_directory_if_missing(init_path)

    path_in = "input_data/urls.txt"
    create_file_if_missing(path_in)
    with open(path_in) as reader:
        urls = [x.strip() for x in reader.readlines() if x.strip() != ""]

    for url in urls:
        title = get_title(url)
        url_list = get_url_from_home_page(url)
        url_list = [x for x in url_list if "/shorts/" in x]
        with open(f"output_data/urls_{title}.txt", 'w') as writer:
            for elem in url_list:
                writer.write(f"{elem}\n")



if __name__ == '__main__':
    main()
