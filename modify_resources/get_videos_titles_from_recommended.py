
def main():
    path_in = "../00_data/text_from_recommended.txt"
    lines = []
    with open(path_in) as reader:
        lines = [x.strip() for x in reader.readlines() if x.strip() != ""]

    res = []
    text_before_title = "Teraz odtwarzane"
    for i, line in enumerate(lines):
        if text_before_title in line and i + 1 < len(lines):
            res.append(lines[i + 1] + "\n")

    with open(f"../00_data/from_recommended-titles.txt", 'w') as writer:
        writer.writelines(res)


if __name__ == '__main__':
    main()
