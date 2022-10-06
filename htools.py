import sys
import h5py as  h5
import numpy as np
import cmasher as cmr
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
from parse import *

args = parser.parse_args()

#####################################################################################################

def create_mflr_file(ini_file,muflr_file,pr_flag,zi,zf):
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

def load_powerspec(powerspecfile):
    header_length = 5
    with open(powerspecfile) as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]
    
    numlines = int(lines[1])
    boxlength = float(lines[2])
    
    datalines = lines[header_length:header_length+numlines]
    data = np.zeros([numlines,5])

    for i, line in enumerate(datalines):
        data[i,:] = np.fromstring(line, dtype=float, sep=' ')
    
    k = data[:,0]
    pk = data[:,2]*boxlength**3 
    datarray = np.array([k,pk])

    return datarray.transpose()

def restart_hybrid(simfol,out_pk,out_gr,out_cb,input_delta,input_theta,input_pcb,streamno,Nstreams):
    # Prepare PowerSpectrumFile
    delta_nu_dat = np.loadtxt(input_delta,delimiter=',',usecols=range(0,Nstreams+1))
    k_delta = delta_nu_dat[:,0]
    delta = delta_nu_dat[:,streamno]**2
    data_delta = np.array([k_delta,delta])
    np.savetxt(simfol+'/'+f'{out_pk}.txt',data_delta.transpose())
    # Prepare GrowthRateFile
    theta_nu_dat = np.loadtxt(input_theta,delimiter=',',usecols=range(0,Nstreams+1))
    growthrate = theta_nu_dat[:,streamno]/delta_nu_dat[:,streamno]
    data_growthrate = np.array([k_delta,growthrate])
    np.savetxt(simfol+'/'+f'{out_gr}.txt',data_growthrate.transpose())
    # Prepare CBPowerSpectrumFile
    pcbdat = load_powerspec(input_pcb)
    np.savetxt(simfol+'/'+f'{out_cb}.txt',pcbdat)

def restart_hybrid_multi(simfol,out_pk,out_gr,out_cb,input_delta,input_theta,input_pcb,streamno,Nstreams):
    # Prepare PowerSpectrumFile
    delta_nu_dat = np.loadtxt(input_delta,delimiter=',',usecols=range(0,51)) # To fix number
    k_delta = delta_nu_dat[:,0]
    delta = np.sum(delta_nu_dat[:,streamno:streamno+Nstreams],axis=1)/Nstreams
    delta_sq = delta**2
    data_delta = np.array([k_delta,delta_sq])
    np.savetxt(simfol+'/'+f'{out_pk}.txt',data_delta.transpose())
    # Prepare GrowthRateFile
    theta_nu_dat = np.loadtxt(input_theta,delimiter=',',usecols=range(0,51)) # To fix number
    theta = np.sum(theta_nu_dat[:,streamno:streamno+Nstreams],axis=1)/Nstreams
    growthrate = theta/delta
    data_growthrate = np.array([k_delta,growthrate])
    np.savetxt(simfol+'/'+f'{out_gr}.txt',data_growthrate.transpose())
    # Prepare CBPowerSpectrumFile
    pcbdat = load_powerspec(input_pcb)
    np.savetxt(simfol+'/'+f'{out_cb}.txt',pcbdat)


def projection(simfol,snap_num,patype,axis,mtype):
    snapshot  = str(simfol)+'/snapshot_%3d'%snap_num
    f = h5.File(str(snapshot)+'.hdf5','r')
    z = f['Header'].attrs['Redshift']
    L = f['Header'].attrs['BoxSize']
    grid  = f['Parameters'].attrs['GridSize']
    BoxSize = L
    ptypes  = patype                   
    MAS       = 'CIC'               
    verbose   = True
    threads   = 4
    delta     = MASL.density_field_gadget(snapshot, ptypes, grid, MAS, do_RSD=False, axis=0, verbose=verbose)
    fig,ax = plt.subplots(1,1,figsize=(13,12))
    im = ax.imshow(np.log10(np.mean(delta,axis=axis)),cmap='cmr.%s'%mtype,origin='lower',extent=[-L/2,L/2,-L/2,L/2])
    plt.colorbar(im)
    ax.set_xlabel(r'$x~({\rm Mpc}/h)$')
    ax.set_ylabel(r'$y~({\rm Mpc}/h)$')
    print('Saving plot in %s'%(str(simfol)+'/plots'))
    if len(ptype) > 1:
        fig.savefig(str(simfol)+'/plots/'+'ptype_%d-%d_z%.1f.pdf'%(ptype[0],ptype[-1],z),bbox_inches='tight')
    else:
        fig.savefig(str(simfol)+'/plots/'+'ptype_%d_z%.1f.pdf'%(ptype[0],z),bbox_inches='tight')

#def plot_check():
#    fig,ax = plt.subplots(1,1,figsize=(8,7))
#    ax.loglog(k,Pk_class,label='raw')
#    ax.loglog(mf_data[:,1],Pk_i(mf_data[:,1])*mf_data[:,2]**2,label='rescaled')
#    ax.legend()

#####################################################################################################

if args.key == 'MuFLR_file':
    create_mflr_file(args.fclass,args.fmflr,args.pr_flag,args.zi,args.zf)

if args.key == 'pre_sim':
    if args.otype == 0: 
        scale_back(args.fclass,args.fmflr,args.simfol,args.out_pk,args.out_gr)
    if args.otype == 1:
        if args.Nstreams > 1:
            restart_hybrid_multi(args.simfol,args.out_pk,args.out_gr,args.out_cb,args.in_de,args.in_th,args.in_cb,args.stream,args.Nstreams)
        else:
            restart_hybrid(args.simfol,args.out_pk,args.out_gr,args.out_cb,args.in_de,args.in_th,args.in_cb,args.stream,args.Nstreams)

if args.otype == 2:
    import MAS_library as MASL
    
    axis = 0
    cmap = 'amber'
    
    if args.pp_index < 3:
        print('Creating projection plot')
        if args.pp_index == 0:
            patype = [1,2,3,4,5] 
        
        elif args.pp_index == 1:
            patype = [1]  

        elif args.pp_index > 1:
            patype = [args.pp_index] 

        projection(args.simfol,args.snap_num,patype,axis,cmap)
    
    if args.pp_index == 3:
        print('Creating power spectrum')

