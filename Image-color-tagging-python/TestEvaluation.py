# -*- coding: utf-8 -*-
"""

@author: ramon
"""
from skimage import io
import matplotlib.pyplot as plt


import labels as lb


plt.close("all")
if __name__ == "__main__":

    #'colorspace': 'RGB', 'Lab' o 'ColorNaming'
    options = {'colorspace':'ColorNaming', 'K':12, 'synonyms':False, 'single_thr':0.6, 'verbose':False, 'km_init':'distributed', 'metric':'basic'}

    ImageFolder ='/Users/rogerprats/Dropbox/UAB/2nQ/IA/Practiques/Tagging/projecte2/Images' #mac
    #ImageFolder = '/home/roger/Dropbox/UAB/2nQ/IA/Practiques/Tagging/projecte2/Images' #ubuntu
    #ImageFolder = '../Images'
    GTFile = 'LABELSlarge.txt' #LABELSlarge

    GTFile = ImageFolder + '/' + GTFile
    GT = lb.loadGT(GTFile)

    DBcolors = []
    for gt in GT:
        print gt[0]
        im = io.imread(ImageFolder+"/"+gt[0])
        colors,_,_ = lb.processImage(im, options)
        DBcolors.append(colors)
        #lb.similarityMetric(colors, gt, options)
    encert,_ = lb.evaluate(DBcolors, GT, options)
    print "Encert promig: "+ '%.2f' % (encert*100) + '%'
    print options
    print "\n"
