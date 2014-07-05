"""transliteration of Kim Asendorf's pixel sorting script"""

from copy import copy
from random import random, gauss
from PIL import Image
from numpy import int32


# PROGRAM CONSTANTS
# rgb(103, 105, 128)
BLACK_VALUE = int32(-10000000)
# rgb(164, 114, 128)
WHITE_VALUE = int32((255 << 24) + (230 << 16) + (230 << 8) + 230)
BRIGHTNESS_VALUE = int32(30)


# PIXEL CONVERSION FUNCTIONS
def get_pixel_value(pixel):
    """rgb pixel to int32 processing representation"""
    return(int32((((255 << 8) | pixel[0]) << 8 | pixel[1]) << 8 | pixel[2]))


def get_pixel_brightness(pixel):
    """rgb pixel to brightness value"""
    return(max((pixel[0], pixel[1], pixel[2])) / 255 * 100)


# PIXEL FINDING FUNCTIONS
def get_next_satisfying(vector, starting_position, condition_fun):
    """find next pixel in the vector after starting position
    that satisfies the condition (boolean)
    return -1 if not found"""
    position = starting_position
    while(position < len(vector) and
          not(condition_fun(vector[position]))):
        position += 1
    if(position == (len(vector) - 1) and
       not(condition_fun(vector[position]))):
        position = - 1
    return(position)


# black mode
def get_next_black(vector, starting_position):
    """next black pixel"""
    condition = lambda x: int32(get_pixel_value(x)) > BLACK_VALUE
    return get_next_satisfying(vector, starting_position, condition)


def get_next_not_black(vector, starting_position):
    """next non black pixel"""
    condition = lambda x: int32(get_pixel_value(x)) < BLACK_VALUE
    return get_next_satisfying(vector, starting_position, condition)


# bright mode
def get_next_bright(vector, starting_position):
    """next bright pixel"""
    condition = lambda x: int32(get_pixel_brightness(x)) < BRIGHTNESS_VALUE
    return get_next_satisfying(vector, starting_position, condition)


def get_next_dark(vector, starting_position):
    """next dark pixel"""
    condition = lambda x: int32(get_pixel_brightness(x)) > BRIGHTNESS_VALUE
    return get_next_satisfying(vector, starting_position, condition)


# white mode
def get_next_white(vector, starting_position):
    """next white pixel"""
    condition = lambda x: int32(get_pixel_value(x)) < WHITE_VALUE
    return get_next_satisfying(vector, starting_position, condition)


def get_next_not_white(vector, starting_position):
    """next not white pixel"""
    condition = lambda x: int32(get_pixel_value(x)) > WHITE_VALUE
    return get_next_satisfying(vector, starting_position, condition)


FIND_FUNCTIONS = ((get_next_black, get_next_not_black),  # black
                  (get_next_bright, get_next_dark),      # bright
                  (get_next_white, get_next_not_white))  # white


# PIXEL SORTING FUNCTIONS
def sort_pixels(vector, mode=0, find=FIND_FUNCTIONS):
    """sort pixel in the given vector"""
    assert(mode in (0, 1, 2)), "invalid use case"
    vector = copy(vector)
    position = 0
    pos_end = None
    while(position < len(vector)):
        if((position == -1) or (pos_end == -1)):
            break
        position = find[mode][0](vector, position)
        pos_end = find[mode][1](vector, position)
        vector[position:pos_end] = sorted(vector[position:pos_end],
                                          key=lambda x: get_pixel_value(x))
        position = pos_end + 1
    return(vector)


# IMAGE TRANSFORMATIONS
def to_vectors(rgb_image, row_or_col):
    """rgb image -> list of lists of RGB tuples"""
    assert(rgb_image.mode == "RGB"), "must be a RGB image"""
    assert(row_or_col in (0, 1)), "row = 0, col = 1"
    vectors = []
    x_size, y_size = rgb_image.size

    if(row_or_col == 0):
        for y_coord in range(0, y_size):
            row = []
            for x_coord in range(0, x_size):
                row.append(rgb_image.getpixel((x_coord, y_coord)))
            vectors.append(row)
    else:
        for x_coord in range(0, x_size):
            col = []
            for y_coord in range(0, y_size):
                col.append(rgb_image.getpixel((x_coord, y_coord)))
            vectors.append(col)
    return(vectors)


# COMPLETE FUNCTIONS
def sort_image(image, row_or_col, mode=0, prob=1, avg_band_size=1):
    """input: (rgb image, row or column, sort mode, probability of sorting,
    average band size for sorting)
    output: sorted out image)"""
    x_size, y_size = image.size
    sigma = avg_band_size / 4

    vectors = to_vectors(image, row_or_col)

    new_vectors = []
    position = 0

    while(position < len(vectors)):
        if(random() < prob):
            # calculate the indices of the rows to sort
            to_sort = []
            coarseness = int(gauss(avg_band_size, sigma))
            for index in range(position, position + coarseness):
                if(index >= len(vectors)):
                    break
                else:
                    to_sort.append(index)
            for index in to_sort:
                new_vectors.append(sort_pixels(vectors[index], mode))
            position += coarseness

        else:
            new_vectors.append(vectors[position])
            position += 1

    new_image = []
    if(row_or_col == 0):
        for vector in new_vectors:
            for (red, green, blue) in vector:
                new_image.append(int(red))
                new_image.append(int(green))
                new_image.append(int(blue))
    else:
        for i in range(0, y_size):
            for vector in new_vectors:
                (red, green, blue) = vector[i]
                new_image.append(int(red))
                new_image.append(int(green))
                new_image.append(int(blue))
    return(Image.fromstring('RGB', (x_size, y_size), bytes(new_image)))


__all__ = ["Image", "sort_image"]
