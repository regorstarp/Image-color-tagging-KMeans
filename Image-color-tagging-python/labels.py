# -*- coding: utf-8 -*-
"""

@author: ramon
"""
import re
import numpy as np
import ColorNaming as cn
from skimage import color
import KMeans as km
import re
from skimage.transform import rescale


def loadGT(filename):    # NO TOCAR tota la funcio
	# GT is a list of tuples (Name, [list-of-labels])
    GT = []
    fd = open(filename, 'r')
    for line in fd:
        splitLine = line.split(' ')[:-1]
        labels = [''.join(sorted(filter(None,re.split('([A-Z][^A-Z]*)',l)))) for l in splitLine[1:]]
        GT.append( (splitLine[0], labels) )

    return GT

'''
per avaluar el rendiment genèric d'entre tot el conjunt d'imatges.
'''
def evaluate(description, GT, options): # NO TOCAR
    scores = np.zeros(len(description))
    for i in range(0, len(description)):
        scores[i] = similarityMetric(description[i], GT[i], options)
    print np.mean(scores), scores.tolist()
    return np.mean(scores), scores.tolist()

'''
Funcions que ens permetran obtenir el rendiment de la vostra aplicació.
Per avaluar una imatge en concret. Segons el valor del flag 'metric',
si té el valor 'basic' utilitzaran la mesura de similitud que us vàrem
definir. Queda obert a la vostra creativitat provar d'altres mètriques.
'''
def similarityMetric(Est, GT, options):# NO TOCAR
    if options['metric'] == 'basic':
        matches = set(Est) & set(GT[1])
        if options['synonyms'] == True:
            pass
        res = float(len(matches)) / float(len(GT[1]))
        print res
        return res
    elif options['metric'] == 'pro':
        matches = set(Est) & set(GT[1])
        missed = set(GT[1]) - set(Est)
        exceed = set(Est) - set(GT[1])
        if len(missed) != 0 and len(exceed) !=0:
            aux = []
            for ele in missed:
                for a in re.split(r'([A-Z][a-z]*)', ele):
                     if a and a not in aux:
                         aux.append(a)
            aux1 = []
            for ele in exceed:
                for a in re.split(r'([A-Z][a-z]*)', ele):
                     if a and a not in aux1:
                         aux1.append(a)
            match = set(aux) & set(aux1)
            encert = (float(len(match)) * 0.5) + float(len(matches))
            res = encert / float(len(GT[1]))
        else:
            res = float(len(matches)) / float(len(GT[1]))
        return res
    elif options['metric'] == 'pro1':
        matches = set(Est) & set(GT[1])
        missed = set(GT[1]) - set(Est)
        exceed = set(Est) - set(GT[1])
        match_pes = 5
        miss_pes = -2
        exc_pes = -1
        punts_max = len(GT[1]) * 4
        res = len(matches) * match_pes + len(missed) * miss_pes + len(exceed) * exc_pes
        res = float(res) / float(punts_max)
        print res
        return res
'''
Donada la matriu dels Kx3 centroides, cal fer la crida a la funció
de colorNaming per obtenir el vector de probabilitats que, aquell centroide,
sigui anomenat d'un color entre els 11 colors bàsics. ATENCIÓ: Si aquest
vector que us retorna no està normalitzat (és a dir, que la suma de tots els seus
valors sigui diferent de 1, cal normalitzar-ho). Aleshores, segons el
paràmetre 'single_thr', a cada un dels centroides s'assignarà un nom de
color simple (1 dels colors bàsics) o bé compost (2 colors bàsics ajuntats).
Exemple return:
['color0', 'color1', 'color2', 'color3', 'color4', 'color5']
[[0], [1], [2], [3], [4], [5]]
'''
def getLabels(kmeans, options):    # NO TOCAR
    colors = {}
    for i in range (0,kmeans.K):
        num1 = 0
        num2 = 0
        id1 = 0
        id2 = 0
        trobat = 0
        if np.sum(kmeans.centroids[i]) > 1:
            for x in np.nditer(kmeans.centroids[i], op_flags=['readwrite']):
                if x != 0:
                    x /= np.sum(kmeans.centroids[i])


        for j in range(0, len(kmeans.centroids[0])):
            if kmeans.centroids[i][j] >= kmeans.options['single_thr']:
                idAux = j
                trobat = 1
                break
            if kmeans.centroids[i][j] > num1:
                id1 = j
                num1 = kmeans.centroids[i][j]
            elif kmeans.centroids[i][j] > num2:
                id2 = j
                num2 = kmeans.centroids[i][j]
        if (trobat == 0):
            idAux = id1,id2
        if idAux not in colors.keys():
            colors[idAux] = [] #nem trobat un
            colors[idAux].append(i)
        else:
            colors[idAux].append(i)
    colors_trobats = []
    for key in colors:
        if isinstance(key, tuple):
            l = []

            l.append(cn.colors[key[0]])
            l.append(cn.colors[key[1]])
            l = sorted(l)
            colors_trobats.append(l[0] + l[1])
        else:
            colors_trobats.append(cn.colors[key])
    #retornar colors i num de centroide del color
    return colors_trobats, colors.values()







def processImage(im, options): # NO TOCAR
    im = rescale(im, 0.25, preserve_range=True)

    if options['colorspace'] == 'ColorNaming':  # NO TOCAR
        im = np.reshape(im, (-1, im.shape[2]))
        im = cn.ImColorNamingTSELabDescriptor(im)
    elif options['colorspace'] == 'RGB':        # NO TOCAR
        im = np.reshape(im, (-1, im.shape[2]))
    elif options['colorspace'] == 'Lab':        # NO TOCAR
        im = cn.RGB2Lab(im)
        im = np.reshape(im, (-1, im.shape[2]))


    if options['K']<2: # trobar la millor K
        i = 2
        fitting = []
        for i in range(2,15):
            kmeans = km.KMeans(im, i, options)
            fitting.append(kmeans.fitting())
        print "k optima = ",fitting.index(min(fitting)) + 3
        kmeans = km.KMeans(im, fitting.index(min(fitting)) + 3, options)
    else:
        kmeans = km.KMeans(im, options['K'], options)  # NO TOCAR

    if options['colorspace'] == 'RGB':
        kmeans.centroids = cn.ImColorNamingTSELabDescriptor(kmeans.centroids) #centroides a cn
    elif options['colorspace'] == 'Lab':
        kmeans.centroids = np.reshape(kmeans.centroids, (-1, 1, kmeans.centroids.shape[1]))
        kmeans.centroids = color.lab2rgb(kmeans.centroids)*255
        kmeans.centroids = cn.ImColorNamingTSELabDescriptor(kmeans.centroids) #centroides a cn
        kmeans.centroids = np.reshape(kmeans.centroids, (-1, kmeans.centroids.shape[2]))

    #obtenir una representacio dels kmeans.centroids en funcio del 11 colors basics
    #normalitzar: obtenir una representacio dels kmeans.centroids que sumi 1 per fila


    colors, which = getLabels(kmeans, options)   # NO TOCAR
    return colors, which, kmeans                 # NO TOCAR
