def split_subtitles(subtitles: str, max_text_len: int) -> list:
    chunks = []
    current_chunk = ''
    tmp_sub = subtitles[:]
    words = tmp_sub.replace('\n', '').replace('.', ". ").split()
    for word in words:
        if len(current_chunk) + len(word) <= max_text_len:
            current_chunk += word + ' '
        else:
            chunks.append(current_chunk)
            current_chunk = word + ' '

    if current_chunk:
        chunks.append(current_chunk)
    return chunks
