import numpy as np
#import matplotlib.pyplot as plt
#from mpl_toolkits.mplot3d import Axes3D
#import matplotlib as mpl
#from pylab import *
import struct


def limits(filename, initial_part_number, xsize, ysize, zsize, shifts, rho_cut, eta_cut):

    # lower bound shifts
    z_shift = shifts[4] #2.7 #1.3 # change for different contacts with the glass block
    y_shift_l = shifts[3]  #4.0 #2.7 #1.1 #2.3 # these values will be changed based on  model parameters -- maximum overlap between two particles? -- Same overall porosity -- georgina's iterative idea?
    x_shift_l = shifts[1]  #4.0 #2.7 #1.1 #2.3 #1.1
    # upper bound shifts
    y_shift_h = shifts[2]  #4.0 #2.7 #1.1 #2.3
    x_shift_h = shifts[0]  #4.0 #2.7 #1.1 #2.3 # 1.1# what should this shift be??

    A_temp = []
    A = []
    B = []

    x_mins = []
    y_mins = []
    z_mins = []

    x_maxs = []
    y_maxs = []
    z_maxs = []

    set = [filename] # change this number (original data was coming from set = [5])

    # for loop only executes once
    for ai in set:

            bnf = open(ai,"rb")
            fcont = bnf.read()
            fullsize = int(len(fcont)/8)
            Vdfull = struct.unpack('d'*fullsize,fcont[:fullsize*8]) #contains float information for the data file


            pCut = 1
            etaCut = eta_cut

            noparts = int(initial_part_number)

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

            lim = rho_cut

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
                        bool=True
                    else:
                        ad.append(1000.0)
                        bd.append(1000.0)
                        cd.append(1000.0)
                        vd[i] = 1000.0

                if bool==True:
                    countth = np.count_nonzero(vd==1000.0)

                    val = np.array([1000.0])

                    x = np.setdiff1d(ad,val,assume_unique = True)
                    y = np.setdiff1d(bd,val,assume_unique = True)
                    z = np.setdiff1d(cd,val,assume_unique = True)
                    v = np.setdiff1d(vd,val,assume_unique = True)

                    x_mins.append(min(x))
                    y_mins.append(min(y))
                    z_mins.append(min(z))

                    x_maxs.append(max(x))
                    y_maxs.append(max(y))
                    z_maxs.append(max(z))


            x_mint = min(x_mins) # mins of the mins
            y_mint = min(y_mins)
            z_mint = min(z_mins)

            x_maxt = max(x_maxs) # maxs of the maxs
            y_maxt = max(y_maxs)
            z_maxt = max(z_maxs)

            bottom = z_mint + z_shift
            x_bound_high = x_maxt - x_shift_h
            y_bound_high = y_maxt - y_shift_h
            z_bound_high = z_maxt # - z_shift

            x_bound_low = x_mint + x_shift_l
            y_bound_low = y_mint + y_shift_l

    # scale information
    scale = .01058
    bottom = bottom*scale
    x_bound_high = x_bound_high*scale 
    y_bound_high = y_bound_high*scale
    z_bound_high = z_bound_high*scale

    x_bound_low = x_bound_low*scale
    y_bound_low = y_bound_low*scale

    return bottom, x_bound_low, x_bound_high, y_bound_low, y_bound_high, z_bound_high
