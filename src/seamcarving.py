import sys

import numba
import numpy as np
from imageio import imread, imwrite
import os
from scipy.ndimage.filters import convolve
from tqdm import trange
'''
The implementation of the algorithm is adapted from
https://karthikkaranth.me/blog/implementing-seam-carving-with-python/
'''

def energy_mapping(img):
    sobel_du = np.array([
        [1.0,2.0,1.0],
        [0.0,0.0, 0.0],
        [-1.0, -2.0, -1.0],
    ])
    sobel_dv = np.array([
        [1.0,0.0,-1.0],
        [2.0, 0.0, -2.0],
        [1.0, 0.0, -1.0],
    ])
    sobel_du = np.stack([sobel_du]* 3, axis=2)
    sobel_dv = np.stack([sobel_dv]*3, axis=2)

    img = img.astype('float32')
    convolved = np.absolute(convolve(img, sobel_du)) + np.absolute(convolve(img, sobel_dv))
    energy_map = convolved.sum(axis=2)
    return energy_map

@numba.jit
def seam(img):
    width, height, _ = img.shape
    energy_map = energy_mapping(img)
    map = energy_map.copy()
    dp = np.zeros_like(map, dtype=np.int)
    for i in range(1,width):
        for j in range(0, height):
            if j == 0:
                idx = np.argmin(map[i-1, j:j+2])
                dp[i,j] = idx + j
                min = map[i-1, idx+j]
            else:
                idx = np.argmin(map[i-1, j-1:j+2])
                dp[i,j] = idx + j -1
                min = map[i-1, idx+j-1]

            map[i,j] = map[i,j] + min

    return map, dp
@numba.jit
def carve_column(img):
    width, height, _ = img.shape
    map, dp = seam(img)
    mask = np.ones((width,height), dtype=np.bool)
    j = np.argmin(map[-1])
    for i in reversed(range(width)):
        mask[i,j] = False
        j = dp[i,j]
    mask = np.stack([mask] * 3, axis=2)
    img = img[mask].reshape((width, height -1, 3))
    return img

def crop_c(img, scale):
    width, height, _ = img.shape
    new_height = int(scale * height)
    for i in trange(height- new_height):
        img = carve_column(img)
    return img



