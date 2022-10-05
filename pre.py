import sys
import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

key      = sys.argv[1]
ptype    = int(sys.argv[2])  
fclass   = sys.argv[3]
fmflr    = sys.argv[4]
simfol   = sys.argv[5]

pr_flag  = int(sys.argv[6])
zi       = int(sys.argv[7])
zf       = int(sys.argv[8])

out_pk   = sys.argv[9]
out_f    = sys.argv[10]

#####################################################################################################

def create_mflr_file(ini_file,muflr_file):
    d = {}
    with open(f"{ini_file}.ini") as f:
        for line in f:
            if "#" in line:
                continue
            if line.startswith('root'):
                break
            d[line.split()[0]] = line.split()[-1]

    h        = d['h']
    Omega_m  = d['Omega_m']
    Omega_b  = d['Omega_b']
    Omega_nu = d['Omega_ncdm']
    sigma8   = d['sigma8']
    n_s      = d['n_s']

    T_cmb_k  = 2.7255
    w0       = -1
    wa       = 0
    cs_1     = 0
    cs_2     = 0
    print_r  = pr_flag
    notu     = 0
    z_i      = zi
    nrs      = 1
    z_f      = zf
    cambf    = '/srv/scratch/cppcnbody/MuFLR/nu05_transfer_z0.dat'
    nu_appr  = 1

    fout = open(f'{muflr_file}.txt','w+')
    fout.write(str(n_s)+" # n_s: scalar spectral index \n")
    fout.write(str(sigma8)+"\n")
    fout.write(str(h)+"\n")
    fout.write(str(Omega_m)+"\n")
    fout.write(str(Omega_b)+"\n")
    fout.write(str(Omega_nu)+"\n")
    fout.write(str(T_cmb_k)+"\n")
    fout.write(str(w0)+"\n")
    fout.write(str(wa)+"\n")
    fout.write(str(cs_1)+"\n")
    fout.write(str(cs_2)+"\n")
    fout.write(str(print_r)+"\n")
    fout.write(str(notu)+"\n")
    fout.write(str(z_i)+"\n")
    fout.write(str(nrs)+"\n")
    fout.write(str(z_f)+"\n")
    fout.write(str(cambf)+"\n")
    fout.write(str(nu_appr)+"\n")
    fout.close()

def scale_back(fclass,fmflr,simfol,f_pk,f_f):
    k,Pk_class = np.loadtxt(f"{fclass}.dat",unpack=True)
    mf_data    = np.loadtxt(f"{fmflr}.txt",skiprows=4)
    Pk_i       = interp1d(k,Pk_class,kind='cubic')
    np.savetxt(str(simfol)+'/'+str(f_pk)+'.txt',np.column_stack((mf_data[:,1],Pk_i(mf_data[:,1])*mf_data[:,2]**2)))
    np.savetxt(str(simfol)+'/'+str(f_f)+'.txt', np.column_stack((mf_data[:,1],mf_data[:,3])))

#def restart_hybrid():

#def plot_check():
#    fig,ax = plt.subplots(1,1,figsize=(8,7))
#    ax.loglog(k,Pk_class,label='raw')
#    ax.loglog(mf_data[:,1],Pk_i(mf_data[:,1])*mf_data[:,2]**2,label='rescaled')
#    ax.legend()

#####################################################################################################

if key == 'MuFLR_file':
    create_mflr_file(fclass,fmflr)

if key == 'pre_sim':
    if ptype == 0: 
        scale_back(fclass,fmflr,simfol,out_pk,out_f)
    if ptype == 1:
        #restart_hybrid()
        raise Exception ("Not implemented yet!")

#if key == 'post_sim':
    # Post processing 
