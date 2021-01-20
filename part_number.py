import numpy as np
#import matplotlib.pyplot as plt
#from mpl_toolkits.mplot3d import Axes3D
#import matplotlib as mpl
#from pylab import *
import struct
import sys
#import filter

file_name = str(sys.argv[1]) # input parameters
noparts = sys.argv[2]
xsize = sys.argv[3]
ysize = sys.argv[4]
zsize = sys.argv[5]
rho_cut	= sys.argv[6]
eta_cut	= sys.argv[7]


noparts = int(noparts)
initial_part_number = noparts

xsize = int(xsize)
ysize = int(ysize)
zsize = int(zsize)
rho_cut = float(rho_cut)
eta_cut = float(eta_cut)

#shift = .20

SNo = 50400002

colbd = 'black'
colfc = 'red'

#U_limit, L_limit = filter.extrema(file_name, initial_part_number, xsize, ysize, zsize)

A = []
B = []
D = []
set = [file_name] # change this number (original data was coming from set = [5]) -- y is zero right now... 0.05 set as 5000 right now, 0.95 set at 95000
set2 = [1]

for ai in set:
                #bnf = open("fullT%dSN%d.dat" %(ai,SNo),"rb")
    bnf = open(ai, "rb")
    fcont = bnf.read()
    fullsize = int(len(fcont)/8)
    Vdfull = struct.unpack('d'*fullsize,fcont[:fullsize*8]) #contains float information for the data file

    pCut = 1
    etaCut = eta_cut # 0.07 (before christmas 2019)

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

    particles =[]
    for pCut in range(noparts):
        countl = 0
        bool = False
        #include = False
        for i in range(0,size):
            if Vd[i] > lim and Ed[i][pCut] >= etaCut: # and Xd[i] > shift*xsize and Yd[i] > shift*ysize: # and Zd[i] > shift*zsize and Xd[i] < (xsize - shift*xsize) and Yd[i] < (ysize - shift*ysize) and Zd[i] < (zsize - shift*zsize):
                bool = True
        #        if Xd[i] > L_limit[0] and Yd[i] > L_limit[1] and Zd[i] > L_limit[2] and Xd[i] < U_limit[0] and Yd[i] < U_limit[1] and Zd[i] < U_limit[2]:
        #            include = True

        if bool == True: # and include == True:
            particles.append(pCut)

    num_of_particles = len(particles)
    print(num_of_particles)







