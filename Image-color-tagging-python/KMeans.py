# -*- coding: utf-8 -*-
"""

@author: ramon
"""
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as axes3d
from sklearn.decomposition import PCA
from skimage import color
import ColorNaming as cn

def distance(X,Y):  # NO TOCAR
    dist = 0
    for i in range(0, len(X)):
        dist += float((X[i] - Y[i]) **2)
    return dist
    #return np.linalg.norm(X-Y)

class KMeans():    # NO TOCAR
    def __init__(self, X, K, options=None):     # NO TOCAR
        if options == None:                     # NO TOCAR
            options = {}                        # NO TOCAR
        if not 'km_init' in options:            # NO TOCAR
            options['km_init'] = 'first'        # NO TOCAR
        if not 'verbose' in options:            # NO TOCAR
            options['verbose'] = False          # NO TOCAR
        self.options = options                  # NO TOCAR
        if not 'rthol' in options:
            options['rthol'] = 0.0001
        self.rthol = options['rthol']

        self.K = K                              # NO TOCAR
        self.X = X
        self._init_centroids()                  # NO TOCAR
        self.clusters = np.zeros(len(self.X))
        self.agrupacio = [[] for i in range(self.K)]
        self._iterate()                         # NO TOCAR
    '''
    Segons si l'opció del flag 'km_init', es farà una inicalització o una altra.
    Si el valor de 'km_init' és  first, s'inicialitzaran els K-centroides com els
    K primers píxels de la imatge. Si el valor és random, s'inicialitzaran de
    manera aleatòria, mentre que si és distributed, els centroides quedaran
    distribuits per tot l'espai. Deixem obert a la vostra creativitat noves
    maneres d'inicialitzar els centroides.
    '''
    def _init_centroids(self):  # NO TOCAR
        self.old_centroids = np.zeros((self.K, self.X.shape[1]))
        self.centroids = np.zeros((self.K, self.X.shape[1]))
        if self.options['km_init'] == 'first':
            for i in range(0, self.K):
                self.centroids[i] = self.X[i].copy()
        elif self.options['km_init'] == 'distributed':
            self.centroids = np.zeros((self.K, 3))
            if (self.K > 0):
                self.centroids[0] = [0,255,0] #green
            if (self.K > 1):
                self.centroids[1] = [255,0,0] #red
            if (self.K > 2):
                self.centroids[2] = [0,0,255] #blue
            if (self.K > 3):
                self.centroids[3] = [255,165,0] #orange
            if (self.K > 4):
                self.centroids[4] = [255,255,0] #yellow
            if (self.K > 5):
                self.centroids[5] = [0,0,0] #black
            if (self.K > 6):
                self.centroids[6] = [165,42,42] #brown
            if (self.K > 7):
                self.centroids[7] = [255,255,255] #white
            if (self.K > 8):
                self.centroids[8] = [128,0,128] #purple
            if (self.K > 9):
                self.centroids[9] = [255,192,203] #pink
            if (self.K > 10):
                self.centroids[10] = [84,84,84] #grey
            if (self.K > 11):
              self.centroids[11] = [255,210,0] #orangeyellow
            if (self.K > 12):
              self.centroids[12] = [0,0,128] #blackblue
            if (self.K > 13):
                self.centroids[13] = [210,149,149] #brownwhite
            if (self.K > 14):
                self.centroids[14] = [64,0,192] #bluepurple
            if (self.K > 15):
                self.centroids[15] = [0,128,128] #bluegreen
            #print self.centroids, type(self.centroids)
            if self.options['colorspace'] == 'Lab':
                self.centroids=np.reshape(self.centroids,(-1,1,self.centroids.shape[1]))
                self.centroids = color.rgb2lab(self.centroids)
                self.centroids = np.reshape(self.centroids, (-1, self.centroids.shape[2]))
            if self.options['colorspace'] == 'ColorNaming':
                self.centroids = np.reshape(self.centroids, (-1, self.centroids.shape[1]))
                self.centroids = cn.ImColorNamingTSELabDescriptor(self.centroids)

        elif self.options['km_init'] == 'random':
            #self.centroids = np.zeros((self.K, 3))
            index = []
            for i in range(0, self.K):
                ind = np.random.randint(0, self.X.shape[0])
                if ind not in index:
                    index.append(ind)
                    self.centroids[i] = self.X[ind]
            self.centroids = np.random.uniform(0, 255,(self.centroids.shape))
            if self.options['colorspace'] == 'ColorNaming':
                self.centroids = np.reshape(self.centroids, (-1, self.centroids.shape[1]))
                self.centroids = cn.ImColorNamingTSELabDescriptor(self.centroids)
            if self.options['colorspace'] == 'Lab':
                self.centroids=np.reshape(self.centroids,(-1,1,self.centroids.shape[1]))
                self.centroids = color.rgb2lab(self.centroids)
                self.centroids = np.reshape(self.centroids, (-1, self.centroids.shape[2]))
    '''
    Per tot el conjunt de píxels de la imatge, cal mirar quin dels K
    centroides es més proper. Aleshores obtenim el vector Px1 on guarda
    la relació de quin és el centroide que ha quedat més proper per tots
    els píxels P (P=NxM).
    '''
    def _cluster_points(self):  # NO TOCAR
        aux = [[] for i in range(self.K)]
        self.old_centroids = self.centroids.copy()
        for i in range(0, len(self.X)):
            minim = 10000000, -1
            for j in range(0, len(self.centroids)):
                dist = distance(self.centroids[j], self.X[i])
                if dist < minim[0]:
                    minim = dist, j
            aux[minim[1]].append(self.X[i].tolist())
            self.clusters[i] = minim[1]
        self.agrupacio = aux

    '''
    Un cop classificats tots els punts pel punt (2), es recalculen els
    centroides, posant-los al punt mitjà d'entre tots els píxels que s'han
    categoritzat a la classe que el centroide en qüestió representa.
    '''
    def _get_centroids(self):  # NO TOCAR
        for i in range(0, len(self.agrupacio)): #agrupacions
            for j in range(0, self.X.shape[1]): #punts agrupacio
                aux = [item[j] for item in self.agrupacio[i]] # element i de cada punt de la agrupacio
                if len(aux) == 0: #zero ele al cluster
                    ind = np.random.randint(self.X.shape[0]-1)
                    nou_centr = self.X[ind]
                    self.centroids[i] = nou_centr
                    break
                if sum(aux) !=0 and len(aux) !=0:
                    mean = sum(aux)/len(aux)
                    self.centroids[i][j] = mean
    '''
    Els centroides actuals s'han desplaçat (dins d'una tolerància
    permesa rthol) respecte la iteració anterior? En cas afirmatiu,
    l'algorisme Kmeans ha convergit i ja hem acabat. En cas negatiu,
    tornar al punt (2) i fer una nova iteració.
    '''
    def _converges(self):  # NO TOCAR
        dist = 0
        for i in range(0 , self.K):
            dist += distance(self.old_centroids[i], self.centroids[i])
        if dist <= self.rthol:
            return True
        else:
            return False


    def _iterate(self):                     # NO TOCAR
        self.num_iter = 1                   # NO TOCAR
        self._cluster_points()              # NO TOCAR
        self._get_centroids()               # NO TOCAR
        if self.options['verbose']:         # NO TOCAR
            self.plot()                     # NO TOCAR
        while not self._converges() :       # NO TOCAR
            self._cluster_points()          # NO TOCAR
            self._get_centroids()           # NO TOCAR
            self.num_iter += 1              # NO TOCAR
            if self.options['verbose']:     # NO TOCAR
                self.plot(False)            # NO TOCAR

    '''
    mètode d'avaluació que ens permet saber com de bona ha
    estat l'agrupació que el kmeans ha obtingut un cop ha convergit (FISHER).
    '''
    def fitting(self):  # NO TOCAR
        #numerador fisher
        dist = []
        for x in range(0, len(self.agrupacio)): #cada cluster
            for i in range(0, len(self.agrupacio[x])): #cada punt del cluster
                for j in range(i+1, len(self.agrupacio[x])): #cada punt restant del cluster
                    dist.append(distance(self.agrupacio[x][i], self.agrupacio[x][j]))
        numerador = sum(dist)/ (len(dist) * (len(dist) -1))

        #denominador fisher

        suma = []
        for x in range(0, len(self.agrupacio)): #cada cluster
            for y in range(x + 1, len(self.agrupacio)): #cada cluster restant
                dist = []
                for i in range(0, len(self.agrupacio[x])): #cada punt del cluster x
                    for j in range(0, len(self.agrupacio[y])): #cada punt del cluster y
                        dist.append(distance(self.agrupacio[x][i], self.agrupacio[y][j]))
                suma.append(sum(dist) / (len(self.agrupacio[x]) * len(self.agrupacio[y]))) #distancia x a y
        denominador = float(sum(suma))
        return (numerador / denominador)



    def plot(self, first_time=True): # NO TOCAR res de la funcio

        #markersshape = 'ov^<>1234sp*hH+xDd'
        markerscolor = 'bgrcmybgrcmybgrcmyk'

        if first_time:
            plt.gcf().add_subplot(111, projection='3d')
            plt.ion()
            plt.show()
            if self.X.shape[1]>3:
                self.pca = PCA(n_components=3)
                self.pca.fit(self.X)

        if self.X.shape[1]>3:
            Xt = self.pca.transform(self.X)
            Ct = self.pca.transform(self.centroids)
        else:
            Xt=self.X
            Ct=self.centroids

        for k in range(self.K):
            plt.gca().plot(Xt[self.clusters==k,0], Xt[self.clusters==k,1], Xt[self.clusters==k,2], '.'+markerscolor[k])
            plt.gca().plot(Ct[k,0:1], Ct[k,1:2], Ct[k,2:3], 'o'+'k',markersize=12)
        plt.draw()
        plt.pause(0.01)
