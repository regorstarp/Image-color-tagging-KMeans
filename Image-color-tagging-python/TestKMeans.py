# -*- coding: utf-8 -*-
"""

@author: Ramon
"""

from skimage import io
from skimage.transform import rescale
import numpy as np
import matplotlib.pyplot as plt

import KMeans as km
import ColorNaming as cn
from skimage import color

plt.close("all")
if __name__ == "__main__":

    c = 'RGB'
    options = {'colorspace':c, 'K':6}


    im = io.imread('Images/0000.jpg')
    im = rescale(im, 0.25, preserve_range=True)

    if options['colorspace'] == 'ColorNaming':  # NO TOCAR
        im = np.reshape(im, (-1, im.shape[2]))
        im = cn.ImColorNamingTSELabDescriptor(im)
    elif options['colorspace'] == 'RGB':        # NO TOCAR
        im = np.reshape(im, (-1, im.shape[2]))
    elif options['colorspace'] == 'Lab':        # NO TOCAR
        im = color.rgb2lab(im)
        im = np.reshape(im, (-1, im.shape[2]))
    k_m = km.KMeans(im, options['K'], {'verbose':True, 'km_init':'random', 'rthol':0.0001, 'colorspace':c,})


    print k_m.centroids
    print "discriminant fisher: " , k_m.fitting()
    k_m.plot()
    raw_input("press Enter")
    print options
