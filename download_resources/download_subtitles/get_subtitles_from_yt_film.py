from youtube_transcript_api import YouTubeTranscriptApi


def split_text_old(lines, chunk_size):
    chunks = []
    current_chunk = ''
    for line in lines:
        line_1 = line.replace('\n', '.')
        words = line_1.split()
        for word in words:
            if len(current_chunk) + len(word) <= chunk_size:
                current_chunk += word + ' '
            else:
                chunks.append(current_chunk)
                current_chunk = word + ' '
    if current_chunk:
        chunks.append(current_chunk)
    return chunks


def split_text(lines, chunk_size):
    chunks = []
    current_chunk = ''
    text = ' '.join(lines)
    words = text.split()
    for word in words:
        if len(current_chunk) + len(word) <= chunk_size:
            current_chunk += word + ' '
        else:
            chunks.append(current_chunk)
            current_chunk = word + ' '

    if current_chunk:
        chunks.append(current_chunk)
    return chunks


def download_subtitles():
    path_in = "../../00_data/urls.txt"
    urls = []
    res = []
    with open(path_in) as reader:
        urls = [x.strip() for x in reader.readlines() if x.strip() != ""]
    for url in urls:
        video_id = url.split("v=")[1]
        res = YouTubeTranscriptApi.get_transcript(video_id)

    res_text = [x['text'] for x in res]
    # text = '\n'.join(res_text)

    str_in = '.'
    str_ou = '\n'
    chunks = split_text(res_text, 4500)
    for i, elem in enumerate(chunks):
        with open(f"00_data/subtitles_for_google/subtitles_{i}.txt", 'w') as writer:
            elem_1 = elem.replace(str_in, str_ou)
            writer.writelines(elem_1)

    chunks = split_text(res_text, 2000)
    for i, elem in enumerate(chunks):
        with open(f"00_data/subtitles_for_chatgpt/subtitles_{i}.txt", 'w') as writer:
            elem_1 = elem.replace(str_in, str_ou)
            writer.writelines(elem_1)


def main():
    download_subtitles()


if __name__ == '__main__':
    main()
