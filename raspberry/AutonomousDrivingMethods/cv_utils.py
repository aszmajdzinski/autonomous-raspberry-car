from numpy import interp


def crop_image(image, crop_height=0.8):
    return image[int(image.shape[0] * crop_height):image.shape[0], 0:image.shape[1]]


def get_steer_value_from_image_center(position: int, image_width: int) -> int:
    if position == 0:
        return 0
    elif image_width / 2 + position < 0:
        return -128
    elif image_width / 2 + position > image_width:
        return 128
    else:
        return int(interp(position, [-image_width/2, image_width/2], [-128, 128]))

