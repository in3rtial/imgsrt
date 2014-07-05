# -*- coding: utf-8 -*-
"""sort them images"""

from PIL import Image
from colorsys import rgb_to_hsv


# IMAGE TRANSFORMATIONS
def map_vectors(vectors, fun):
    """map function over vectors of image information"""
    new_vectors = []
    for vector in vectors:
        new_vector = []
        for elem in vector:
            new_vector.append(fun(elem))
    return(new_vectors)


def to_vectors(rgb_image, extract_rows=True):
    """rgb image -> list of lists of RGB tuples
    either the rows, or the columns"""
    assert(rgb_image.mode == 'RGB'), "must be a RGB image"""
    vectors = []
    x_size, y_size = rgb_image.size

    if(extract_rows is True):
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


def sort_by_hue(image, extract_rows=True):
    """sort image by line/column by hue"""
    image = image if image.mode == 'RGB' else image.convert(mode='RGB')

    rgb_vectors = to_vectors(image, extract_rows)
    sorted_vectors = []
    for vector in rgb_vectors:
        sorted_vectors.append(sorted(vector, key=lambda x:
                                     rgb_to_hsv(x[0], x[1], x[2])[0]))
    rgb_bytes = []
    if(extract_rows is True):
        for vector in sorted_vectors:
            for(red, green, blue) in vector:
                rgb_bytes.append(int(red))
                rgb_bytes.append(int(green))
                rgb_bytes.append(int(blue))
    else:
        for i in range(0, image.size[1]):
            for vector in sorted_vectors:
                (red, green, blue) = vector[i]
                rgb_bytes.append(int(red))
                rgb_bytes.append(int(green))
                rgb_bytes.append(int(blue))
    return(Image.fromstring('RGB', image.size, bytes(rgb_bytes)))
