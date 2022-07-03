import argparse
import cv2
import numpy


def get_n_chars(text: str, n: int):
    text_slice = str()
    for i in range(n):
        try:
            text_slice += text[i]
        except IndexError:            text_slice += ' '
    return text_slice


def show_image(name: str, image: numpy.ndarray):
    cv2.imshow(name, image)
    cv2.waitKey(1)


def get_cmd_line_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-nohardware', help='doesn\'t use serial. Use it to run on a PC.', action='store_true')
    parser.add_argument('-datapath', help='use images from that path instead of camera. Use it when you don\'t have a '
                                          'PiCamera', default=None)
    parser.add_argument('-controller', help='specifies controller to be used. Currently acceptable: \n'
                                            '\'PG9076\' - iPega PG-9076'
                                            '\'keyboard\' - standard keyboard', default='PG9076')
    return parser.parse_args()
