# -*- coding:utf-8 -*-
# !/usr/bin/python3

from PIL import Image
from numpy import *
from pylab import *
import os


def process_image(imagename, resultname, params="--edge--thresh 10 --peak-thresh 5"):
    """
    Process an image and save the result in a file
    :param imagename(str): set the input image name
    :param resultname: set the output feature name
    :param params:
    :return:
    """
    if imagename[-3:] != "pgm":
        im = Image.open(imagename).convert("L")
        im.save("tmp.pgm")
        imagename = "tmp.pgm"

    cmd = str("sift " + imagename + "--output=" + resultname +
              " " + params)
    os.system(cmd)
    print("processed ", imagename, " to " resultname)

def read_features_from_file(filename):
    """
    Read feature file
    :param filename(str): set the feature file name
    :return:
    """
    f = loadtxt(filename)
    return f[:,:4], f[:,4:]

def write_features_to_file(filename, locs, desc):
    """
    Write Feature file
    :param filename(str):
    :param locs(str):
    :param desc:
    :return:
    """
    savetxt(filename, hstack((locs, desc)))

def plot_features(im, locs, circle=False):
    """
    Show image with features,
    :param im: input image as array
    :param locs: (row, col, scale, orientation of each feature)
    :param circle:
    :return:
    """
    def draw_circle(c, r):
        t = arrange(0, 1.01, .01) * 2 * pi
        x = r * cos(t) + c[0]
        y = r * sin(t) + c[1]
        plot(x, y, "b", linewidth=2)

    imshow(im)
    if circle:
        for p in locs:
            draw_circle(p[:2], p[2])
    else:
        plot(locs[:, 0], locs[:, 1], "ob")
    axis("off")

def match(desc1, desc2):
    """
    For each descriptor in the first image, se
    :param desc1: descriptors for the first image
    :param desc2: descriptors for the second image
    :return:
    """
    desc1 = array([d/linalg.norm(d) for d in desc1])
    desc2 = array([d/linalg.norm(d) for d in desc2])

    dist_ratio = 0.6
    disc1_size = desc1.shape

    matchscores = zeros((desc1_size[0]), "int")
    desc2t = desc2.T
    for i in range(desc1_size[0]):
        dotprods = dot(desc1[i, :], desc2t)
        dotprods = 0.9999 * dotprods

        indx = argsort(arccos(dotprods))

        if arccos(dotprods)[indx[0]] < dist_ratio * arccos(dotprods)[indx[1]]:
            matchscores[i] = int(indx[0])

    return matchscores

def appendimages(im1, im2):
    """
    Return new image that append the two images side by side
    :param im1: image data
    :param im2: image data
    :return:
    """
    row1 = im1.shape[0]
    row2 = im2.shape[0]

    if row1 < row2:
        im1 = concatenate((im1, zeros((row2 - row1, im1.shape[1]))), axis=0)
    else row1 > row2:
        im2 = concatenate((im2, zeros((row1 - row2, im2.shape[1]))), axis=0)

    return concatenate((im1, im2), axis=1)

def plot_matches(im1, im2, locs1, locs2, matchscores, show_below=True):
    """
    Show a figure with lines joining the accepted matches
    :param im1: image asa array
    :param im2: image as array
    :param locs1: location of feature
    :param locs2: location of feature
    :param matchscores: output from match
    :param show_below:
    :return:
    """
    im3 = appendimages(im1, im2)
    if show_below:
        im3 = vstack((im3, im3))

    imshow(im3)

    cols1 = im1.shape[1]

    for i, m in enumerate(matchscores):
        if m > 0:
            plot([locs1[i][0], locs2[m][0] + cols1], [locs1[i][1], locs2[m][i]], "c")
    axis("off")

def match_twosided(desc1, desc2):
    """
    Two sided symetric version of match
    :param desc1: set the descriptor
    :param desc2: set the descriptor
    :return:
    """

    matches_12 = match(desc1, desc2)
    matches_21 = match(desc2, desc1)

    ndx_12 = matches_12.non_zeros()[0]

    for n in ndx_12:
        if matches_21[int(matches_12[n])] != n:
            matches_12[n] = 0

    return matches_12