import numpy as np
import math
import struct
import generate_verticies_3 as vertex # should normally be 3 # generate_verticies_subset


def CreateSurfacePoints(file_name, initial_part_number, xsize, ysize, zsize, rho_cut, eta_cut):

    # pass point information from data processing script
    point_list, xyz_totals, boundary = vertex.CreateVertexList(file_name, initial_part_number, xsize, ysize, zsize, rho_cut, eta_cut)
    V = []
    verticies = []
    points = []

    # loop through the different particles (determined by their eta variables) and extract the surface
    for r in range(len(point_list)):

        points = point_list[r]

        x_min = boundary[r][0]
        y_min = boundary[r][1]
        x_max = boundary[r][2]
        y_max = boundary[r][3]

        xp = points[0]
        yp = points[1]
        zp = points[2]

        xtot = xyz_totals[0]
        ytot = xyz_totals[1]
        ztot = xyz_totals[2]

        # building the C matrix to index (indexing in the "6 directions" around the chosen point)
        C = []
        C =  np.arange(int(len(xp)))

        n=0
        for i in range(len(C)):
            if xp[i] < 900:
                n += 1
                C[i] = n
            else:
                C[i] = -1000 # something outside the possible range 

        C_split = C.reshape(ztot,ytot,xtot) # this split must match up with the loop ### flip x and z when needed

        xpnp = np.array(xp)
        ypnp = np.array(yp)
        zpnp = np.array(zp)

        xp_split = xpnp.reshape(ztot,ytot,xtot)
        yp_split = ypnp.reshape(ztot,ytot,xtot)
        zp_split = zpnp.reshape(ztot,ytot,xtot)

        Vo = []
        Vox = []
        Voy = []

        # remove the points that make up the surface of the point cloud
        for k in range(0, xtot-1):
            for j in range(0, ytot-1):
                for i in range(0, ztot-1):

                    if C_split[i][j][k] >= 0:
                        if C_split[i][j+1][k] < 0 or C_split[i][j][k+1] < 0 or C_split[i-1][j][k] < 0 or C_split[i][j-1][k] < 0 or C_split[i][j][k-1] < 0 or C_split[i+1][j][k] < 0:
                            Vo.append([xp_split[i][j][k], yp_split[i][j][k], zp_split[i][j][k]])
                            Vox.append(xp_split[i][j][k])
                            Voy.append(yp_split[i][j][k])

        # ensure that the edge points are filled in -- prevent holes from ruining stl generation
        x_min, y_min, x_max, y_max = min(Vox), min(Voy), max(Vox), max(Voy)

        for k in range(0, xtot):
            for j in range(0, ytot):
                for i in range(0, ztot):
                    if int(xp_split[i][j][k]) == int(x_min) or int(xp_split[i][j][k]) == int(x_max) or int(yp_split[i][j][k]) == int(y_min) or int(yp_split[i][j][k]) == int(y_max):
                        if [xp_split[i][j][k], yp_split[i][j][k], zp_split[i][j][k]] not in Vo:
                            Vo.append([xp_split[i][j][k], yp_split[i][j][k], zp_split[i][j][k]])

        #remove duplicates
        V.append(Vo)

    return(V)




