import numpy as np
#import matplotlib.pyplot as plt
#from mpl_toolkits.mplot3d import Axes3D
#import matplotlib as mpl
#from pylab import *
import struct

def CreateVertexList(file_name, initial_part_number, xsize, ysize, zsize, rho_cut, eta_cut):

    initial_part_number = int(initial_part_number)
    SNo = 50400002

    colbd = 'black'
    colfc = 'red'

    A = []
    B = []
    D = []
    set = [file_name] # change this number (original data was coming from set = [5]) -- y is zero right now... 0.05 set as 5000 right now, 0.95 set at 95000
    set2 = [1]

    # for loop only runs once -- left in for added flexibility later
    for ai in set:

            #bnf = open("fullT%dSN%d.dat" %(ai,SNo),"rb")
            bnf = open(ai, "rb")
            fcont = bnf.read()
            fullsize = int(len(fcont)/8)
            Vdfull = struct.unpack('d'*fullsize,fcont[:fullsize*8]) #contains float information for the data file


            #xsize = 60 #58 for original 1-10, 50 for the next set of 20
            #ysize = 104 # 50, 96, 96
            #zsize = 104

            pCut = 1
            etaCut = eta_cut # 0.005 (before April 25, 2020 # 0.07 (before Feb 26, 2020)

            noparts = initial_part_number
            print(noparts)
            print(type(noparts))
            size = xsize*ysize*zsize

            Xd = [0 for x in range(size)]
            Yd = [0 for x in range(size)]
            Zd = [0 for x in range(size)]
            Vd = [0 for x in range(size)]
            Ed = [[0 for y in range(noparts)] for x in range(size)]


            vd = np.zeros(size)

            ysizep = ysize;

            counti = 0
            for z in range(zsize):
                for y in range(ysize):
                    for x in range(xsize):
                        Zd[counti] = x
                        Yd[counti] = y
                        Xd[counti] = z

                        countv = counti*(noparts+1)
                        Vd[counti] = Vdfull[countv]

                        for p in range(noparts):
                            Ed[counti][p] = Vdfull[countv+p+1]

                        counti = counti+1

            lim = rho_cut # we used .2 for everything before this (christmas 2019)


            for pCut in range(noparts):
                countl = 0
                ad =[]
                bd =[]
                cd =[]
                bool = False
                for i in range(0,size):
                    if Vd[i] > lim and Ed[i][pCut] >= etaCut:
                        ad.append(Xd[i])
                        bd.append(Yd[i])
                        cd.append(Zd[i])
                        vd[i] = Vd[i]
                        countl = countl+1
                        bool = True
                    else:
                        ad.append(1000.0)
                        bd.append(1000.0)
                        cd.append(1000.0)
                        vd[i] = 1000.0

                if bool == True:
                    B.append([ad, bd, cd])

                    countth = np.count_nonzero(vd==1000.0)

                    val = np.array([1000.0])

                    x = np.setdiff1d(ad,val,assume_unique = True)
                    y = np.setdiff1d(bd,val,assume_unique = True)
                    z = np.setdiff1d(cd,val,assume_unique = True)
                    v = np.setdiff1d(vd,val,assume_unique = True)


                    A.append([x, y, z])
                    D.append([min(x), min(y), max(x), max(y)])


    C = [xsize, ysize, zsize]


    return B,C,D








