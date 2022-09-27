import sys
import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt


ptype  = int(sys.argv[1])  
fclass = sys.argv[2]
fmflr  = sys.argv[3]
simfol = sys.argv[4]
f_pk   = sys.argv[5]
f_f    = sys.argv[6] 

if ptype == 1: raise Exception('Not implemented!')

if ptype == 2:
    k,Pk_class = np.loadtxt(f"{fclass}.dat",unpack=True)
    mf_data    = np.loadtxt(f"{fmflr}.txt")
    Pk_i       = interp1d(k,Pk_class,kind='cubic')
    np.savetxt(str(simfol)+'/'+str(f_pk)+'.txt',np.column_stack((mf_data[:,1],Pk_i(mf_data[:,1])*mf_data[:,2]**2)))
    np.savetxt(str(simfol)+'/'+str(f_f)+'.txt', np.column_stack((mf_data[:,1],mf_data[:,3])))


print('\n')
