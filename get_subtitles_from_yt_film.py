from youtube_transcript_api import YouTubeTranscriptApi

def split_text(text, chunk_size):
    chunks = []
    current_chunk = ''
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
    path_in = "urls.txt"
    urls = []
    res = []
    with open(path_in) as reader:
        urls = [x.strip() for x in reader.readlines() if x.strip() != ""]
    for url in urls:
        video_id = url.split("v=")[1]
        res = YouTubeTranscriptApi.get_transcript(video_id)

    res_text = [x['text'] for x in res]
    text = '\n'.join(res_text)
    chunks = split_text(text, 4500)

    for i, elem in enumerate(chunks):
        with open(f"subtitles_{i}.txt", 'w') as writer:
            elem_1 = elem.replace('. ', '.\n')
            writer.writelines(elem_1)


def main():
    download_subtitles()


if __name__ == '__main__':
    main()
