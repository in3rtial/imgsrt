"""transliteration of Kim Asendorf's pixel sorting script"""

from numpy import int32
from copy import copy
from random import random, gauss
from PIL import Image


# PROGRAM CONSTANTS
black_value = int32(-10000000)  # rgb(103, 105, 128)
white_value = int32(-6000000)  # rgb(164, 114, 128)
brightness_value = 30  # 255 << 24) + (32<< 16) + (32 << 8) + 32
white_value = int32((255 << 24) + (230<< 16) + (230 << 8) + 230)



#PIXEL CONVERSION FUNCTIONS
def get_pixel_value(pixel):
    """rgb pixel to int32 processing representation"""
    return(int32(( ((255 << 8) | pixel[0]) << 8 | pixel[1]) << 8 | pixel[2]))


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
        position = -1
    return(position)


# black
def get_next_black(vector, starting_position):
    """next black pixel"""
    condition = lambda x: get_pixel_value(x) > black_value
    return get_next_satisfying(vector, starting_position, condition)


def get_next_not_black(vector, starting_position):
    """next non black pixel"""
    condition = lambda x: get_pixel_value(x) < black_value
    return get_next_satisfying(vector, starting_position, condition)


# bright
def get_next_bright(vector, starting_position):
    """next bright pixel"""
    condition = lambda x: get_pixel_brightness(x) < brightness_value
    return get_next_satisfying(vector, starting_position, condition)


def get_next_dark(vector, starting_position):
    """next dark pixel"""
    condition = lambda x: get_pixel_brightness(x) > brightness_value
    return get_next_satisfying(vector, starting_position, condition)


#white
def get_next_white(vector, starting_position):
    """next white pixel"""
    condition = lambda x: get_pixel_value(x) < white_value
    return get_next_satisfying(vector, starting_position, condition)


def get_next_not_white(vector, starting_position):
    """next not white pixel"""
    condition = lambda x: get_pixel_value(x) > white_value
    return get_next_satisfying(vector, starting_position, condition)


finding_functions = ((get_next_black, get_next_not_black),  # black
                     (get_next_bright, get_next_dark),      # bright
                     (get_next_white, get_next_not_white))  # white



# PIXEL SORTING FUNCTIONS
def sort_pixels(vector, mode=0, finding_functions=finding_functions):
    """sort pixel in the given vector"""
    assert(mode in (0, 1, 2)), "invalid use case"
    vector = copy(vector)
    position = 0
    position_end = None
    while(position < len(vector)):
        if((position == -1) or (position_end == -1)):
            break
        position = finding_functions[mode][0](vector, position)
        position_end = finding_functions[mode][1](vector, position)
        vector[position:position_end] = sorted(vector[position:position_end], key=lambda x: get_pixel_value(x))
        position = position_end + 1
    return(vector)


# IMAGE TRANSFORMATIONS
def to_vectors(rgb_image, row_or_col):
    """rgb image -> list of lists of RGB tuples"""
    assert(rgb_image.mode == "RGB"), "must be a RGB image"""
    assert(row_or_col in (0,1)), "row = 0, col = 1"
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
def sort_image(image, row_or_col, mode=0, prob=1, mu=1):
    """ """
    x_size, y_size = image.size
    sigma = mu / 4

    vectors = to_vectors(image, row_or_col)

    new_vectors = []
    position = 0

    while(position < len(vectors)):
        if(random() < prob):
            # calculate the indices of the rows to sort
            to_sort = []
            coarseness = int(gauss(mu, sigma))
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
            for (R,G,B) in vector:
                new_image.append(int(R))
                new_image.append(int(G))
                new_image.append(int(B))
    else:
        for i in range(0, y_size):
            for vector in new_vectors:
                (R, G, B) = vector[i]
                new_image.append(int(R))
                new_image.append(int(G))
                new_image.append(int(B))
    return(Image.fromstring('RGB', (x_size, y_size), bytes(new_image)))



__all__ = ["sort_image"]