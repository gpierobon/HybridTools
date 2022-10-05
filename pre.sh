#!/bin/bash

####################################################################################################################################
ptype=2                                              # 0: Start           (SuperEasyLR/MFLR/Hybrid)
                                                     # 1: Restart         (Hybrid only)
                                                     # 2: Postprocessing  (SuperEasyLR/MFLR/Hybrid)

# Paths
SimFolder='./simdir'                                 # Path to simulation folder
Class_Path='/srv/scratch/cppcnbody/class_public'     # Path to class      (Set in our shared folder)
MuFLR_Path='/srv/scratch/cppcnbody/MuFLR'            # Path to mf module  (Set in our shared folder)
Hybrid_Path='/srv/scratch/cppcnbody/gadget4-hybrid'  # Path to hybrid     (Set in our shared folder)

# Class file
ClassFile='nu'                                       # .ini file for class, from folder inifiles

# MuFLR options
MfIn='params_MuFLR'                                  # Generates MuFLR input file, placed in inifiles
MfOut='MuFLR_out'                                    # Output of MuFLR result, will go in raw_files
Opt=0                                                # Print options. 0: D_cb, f, neutrino density  
zi=200                                               # Initial redshift for MuFLR
zf=49                                                # Output redshift (gadget4 initial redshift)

# Opts for preprocessing
PkOut='P_k_ini'                                      # PowerSpectrumFile in param, .txt file found in SimFolder
GFOut='GrFact_ini'                                   # GrowthRateFile in param, .txt file found in SimFolder
CBOut='P_m_ini'                                      # CBPowerSpectrumFile in param, .txt file (hybrid_only)       
Stream=0                                             
NumStreams=0                                         

# Opts for postprocessing
pindex=0                                             # 0: Projection plot all
                                                     # 1: Projection plot cdm only
                                                     # 2: Projection plot neutrinos only
                                                     # 3: Power Spectrum particles + neutrino fluids 
snap_base=snapshot
snap_number=1

####################################################################################################################################

mkdir -p $SimFolder  
ClassOut=raw_files/$ClassFile'_pk'              
cdir=$(pwd)

case $ptype in

    0) 
    echo 'Prepart start of simulation in folder' $SimFolder
    export PATH=$ClassPath:$PATH
    export PATH=$MfPath:$PATH

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
    python3 pre.py MuFLR_file  $ptype inifiles/$ClassFile inifiles/$MfIn $SimFolder $Opt $zi $zf $PkOut $GFOut
    
    echo 'Running MuFLR ...'
    $MuFLR_Path/MuFLR          inifiles/$MfIn.txt > raw_files/$MfOut.txt
    
    echo 'Setting files for Gadget ...'
    python3 pre.py pre_sim     $ptype $ClassOut raw_files/$MfOut $SimFolder $Opt $zi $zf $PkOut $GFOut 
    echo 'Files' $PkOut 'and' $GFOut 'are ready in' $SimFolder
    ;;
    
    1) 
    echo 'Restart Hybrid simulation in folder' $SimFolder
    #echo 'Converting' 'streams in' 'batch(es)'
    m=0.31
    c=299792458
    tau=$(sed -n '1p' raw_files/$MfOut.txt | awk '{print $4}')
    Stream_Vel=$(echo "$tau/$m*$c/1000 " | bc -l)
    echo 'The stream velocity is '$Stream_Vel 'km/s'
    
    ;;

    2)
    mkdir -p $SimFolder/plots
    echo 'Post-processing simulation from folder' $SimFolder
    python3 pre.py post_sim $ptype $ClassOut raw_files/$MfOut $SimFolder $Opt $zi $zf $PkOut $GFOut $pindex $snap_base $snap_number 
    ;;
esac

