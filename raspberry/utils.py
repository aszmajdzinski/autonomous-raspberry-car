import cv2
import numpy


def get_n_chars(text: str, n: int):
    text_slice = str()
    for i in range(n):
        try:
            text_slice += text[i]
        except IndexError:
            text_slice += ' '
    return text_slice


def show_image(name: str, image: numpy.ndarray):
    cv2.imshow(name, image)
    cv2.waitKey(1)
