#!/bin/bash

####################################################################################################################################

OPT=0                                                # 0: Start           (MFLR/Hybrid)
                                                     # 1: Restart         (Hybrid only)
                                                     # 2: Postprocess     (SuperEasyLR/MFLR/Hybrid)

# Paths
SimFolder='./simdir'                                 # Path to simulation folder                                  All OPT

Class_Path='/srv/scratch/cppcnbody/class_public'     # Path to class      (Set in cppc shared folder)             OPT=0 only
MuFLR_Path='/srv/scratch/cppcnbody/MuFLR'            # Path to mf module  (Set in cppc shared folder)             OPT=0 only
Hybrid_Path='/srv/scratch/cppcnbody/gadget4-hybrid'  # Path to hybrid     (Set in cppc shared folder)             OPT=0,1
   
# Class file
ClassFile='nu'                                       # .ini file for class, from folder inifiles,                 OPT=0 only 
 
# MuFLR options
MfIn='params_MuFLR'                                  # Generates MuFLR input file, placed in inifiles,            OPT=0 only
MfOut='MuFLR_out'                                    # Output of MuFLR result, will go in raw_files,              OPT=0 only
PrintOpt=0                                           # Print options. 0: D_cb, f, neutrino density,               OPT=0 only  
zi=200.0                                             # Initial redshift for MuFLR,                                OPT=0 only
zf=49.0                                              # Output redshift (gadget4 initial redshift),                OPT=0 only

# Opts for preprocessing
PkOut='P_k'                                          # Filename for PowerSpectrumFile in param.txt,               OPT=0,1
GFOut='GrFact'                                       # Filename for GrowthRateFile in param.txt,                  OPT=0,1
CBOut='P_m'                                          # Filename for CBPowerSpectrumFile in param.txt,             OPT=1 only       

aRes=0.198                                           # Scale factor for Hybrid restart, .3f format!               OPT=1 only
snap_number=1                                        # Select a snapshot to restart from or postprocess           OPT=1,2
Stream=0                                             
NumStreams=10                                         
mass=0.3                                             # Neutrino mass in eV                                        OPT=1

# Opts for postprocessing
pindex=0                                             # 0: Projection plot all                                     OPT=2 only
                                                     # 1: Projection plot cdm only                                OPT=2 only
                                                     # 2: Projection plot neutrinos only                          OPT=2 only
                                                     # 3: Power Spectrum particles + neutrino fluids              OPT=2 only

####################################################################################################################################

mkdir -p $SimFolder  
cdir=$(pwd)

case $OPT in

    0) 
    echo 'Prepart start of simulation in folder' $SimFolder
    export PATH=$ClassPath:$PATH
    export PATH=$MfPath:$PATH
    ClassOut=raw_files/$ClassFile'_pk'              

    echo 'Checking the N_tau and N_mu parameters ...'
    Ntau1=$(awk -F " |;" '{if ($3 == "N_tau") print $5}' $MuFLR_Path/AU_cosmofunc.h)
    Nmu1=$(awk -F " |;" '{if ($3 == "N_mu") print $5}'   $MuFLR_Path/AU_cosmofunc.h)
    Ntau2=$(sed -n '13p' $Hybrid_Path/src/neutrinos/neutrinomflr.h | awk -F " |;" '{print $10}')
    Nmu2=$(sed -n '14p' $Hybrid_Path/src/neutrinos/neutrinomflr.h | awk -F " |;" '{print $10}')
    
    if [[ $Ntau1 != $Ntau2 ]]; 
    then echo 'MuFLR has N_tau =' $Ntau1 ', while gadget-4 has N_tau =' $Ntau2
         echo 'Set the parameters equally and recompile!'
    fi
    if [[ $Nmu1 != $Nmu2 ]]; 
    then echo 'MuFLR has N_mu =' $Nmu1 ', while gadget-4 has N_mu =' $Nmu2
         echo 'Set the parameters equally and recompile!'
    fi
    
    echo 'Running Class in' $Class_Path '...'            
    $Class_Path/class       inifiles/$ClassFile.ini

    echo 'Compiling MuFLR in' $MuFLR_Path '...'
    cd $MuFLR_Path; make; cd $cdir
    
    echo 'Creating MuFLR input file' $MfIn '...'
    python3 htools.py -k MuFLR_file -ot $OPT -c inifiles/$ClassFile -m inifiles/$MfIn 
    
    echo 'Running MuFLR ...'
    $MuFLR_Path/MuFLR          inifiles/$MfIn.txt > raw_files/$MfOut.txt
    
    echo 'Setting files for Gadget ...'
    python3 htools.py -k pre_sim -ot $OPT -c $ClassOut -m $SimFolder/$MfOut -sf $SimFolder -pf $PrintOpt -zi $zi -zf $zf -pk $PkOut -gr $GFOut 
    echo 'Files' $PkOut 'and' $GFOut 'are ready in' $SimFolder
    ;;
    
    1) 
    echo 'Restart Hybrid simulation in folder' $SimFolder
    #echo 'Converting' 'streams in' 'batch(es)'

    NuDelta=$SimFolder/neutrino_stream_data/neutrino_delta_stream_$aRes.csv
    NuTheta=$SimFolder/neutrino_stream_data/neutrino_theta_stream_$aRes.csv
    PowerSpectrum=$SimFolder/powerspecs/powerspec_00$snap_number.txt
    
    python3 htools.py -k pre_sim -ot $OPT -sf $SimFolder -pk $PkOut -gr $GFOut -cb $CBOut -id $NuDelta -it $NuTheta -icb $PowerSpectrum -str $Stream -Ns $NumStreams
    
    c=299792458
    tau=$(sed -n '1p' $SimFolder/$MfOut.txt | awk '{print $4}')
    Stream_Vel=$(echo "$tau/$mass*$c/1000 " | bc -l)
    echo 'Set stream velocity in the param.txt file as '$Stream_Vel '(km/s)'
    
    ;;

    2)
    mkdir -p $SimFolder/plots
    echo 'Post-processing simulation from folder' $SimFolder
    python3 htools.py -k post_sim -ot $OPT -sf $SimFolder -pp $pindex -sa $snap_number 
    ;;
esac

