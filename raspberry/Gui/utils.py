def get_n_chars(text: str, n: int):
    text_slice = str()
    for i in range(n):
        try:
            text_slice += text[i]
        except IndexError:
            text_slice += ' '
    return text_slice