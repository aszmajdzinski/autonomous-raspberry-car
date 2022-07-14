def crop_image(image, crop_height=0.8):
    return image[int(image.shape[0] * crop_height):image.shape[0], 0:image.shape[1]]