# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from numpy import *
from scipy import ndimage


class RansacModel(object):
    """ Class for testing homography fit with ransac.py from
        http://www.scipy.org/Cookbook/RANSAC"""

    def __init__(self, debug=False):
        self.debug = debug

    def fit(self, data):
        """ Fit homography to four selected correspondences. """

        # transpose to fit H_from_points()
        data = data.T

        # from points
        fp = data[:3, :4]
        # target [pints
        tp = data[3:, :4]

        # fit homography and return
        return H_from_points(fp, tp)

    def get_error(self, data, H):
        """ Apply homography to all correspondences,
            return error for each transformed point. """

        data = data.T

        # from points
        fp = data[:3]
        # target points
        tp = data[3:]

        # transform fp
        fp_transformed = dot(H, fp)

        # normalize hom. coordinates
        fp_transformed = normalize(fp_transformed)

        # return error per point
        return sqrt(sum((tp - fp_transformed)**2, axis=0))

def H_from_ransac(fp, tp, model, maxiter=1000, match_theshold=10):
    """ Robust estimation of homography H from point
        correspondences using RANSAC (ransac.py from
        http://www.scipy.org/Cookbook/RANSAC).

        input: fp,tp (3*n arrays) points in hom. coordinates. """
    import ransac

    # group corresponding points
    data = vstack((fp, tp))

    # compute H and return
    H, ransac_data = ransac.ransac(data.T,
                                   model,
                                   4,
                                   maxiter,
                                   match_theshold,
                                   10,
                                   return_all=True)
    return H, ransac_data["inliers"]


def H_from_points(fp, tp):
    pass


def Haffine_from_points(fp, tp):
    pass


def normalize(points):
    pass


def make_homog(points):
    pass
