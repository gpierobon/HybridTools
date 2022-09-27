#!/bin/bash

########################################################################################################
# Module PreGadget for Nbody simulations of Neutrinos/Axions                                           #
########################################################################################################


ptype=2                                              # 1: SuperEasy
                                                     # 2: MultiFluid LR
                                                     # 3: Hybrid      


ClassPath='/Users/z5278074/gpierobon/class_public'   # Path to class 
SePath='/Users/z5278074/gpierobon/nu_flr'            # Path to mf module 
MfPath='/Users/z5278074/gpierobon/nu_mflr'           # Path to mf module 
SimFolder='./outp'                                 # Path to simulation folder 

ClassStart='ax'                                      # .ini file that runs class
MfOut='raw_files/mf_out'                                       # Output of mfluid result
Nk=16                                                # Number of modes for multifluid/supereasy
zi=49                                                # Initial simulation time

PkOut='Pk_ini'                                       # Create the rescaled Pk,   .txt file
GFOut='GrFact_ini'                                   # Create the growth factor, .txt file

#######################################################################################################

mkdir -p $SimFolder  
ClassOut=raw_files/$ClassStart'_pk'              
cdir=$(pwd)
#export $OMP_NUM_THREADS=4
case $ptype in
    1) 
    echo 'Prepare SuperEasy simulation' 
    export PATH=$ClassPath:$PATH; export PATH=$SePath:$PATH 
    python3 pre.py $ptype $ClassOut $MfOut $SimFolder $file3 $file4
    ;;    
    
    2) 
    echo 'Prepare MultiFluid simulation'
    export PATH=$ClassPath:$PATH; export PATH=$MfPath:$PATH
    echo 'Running Class ...' ;            class          $ClassStart.ini
    echo 'Running MFLR ...' ;             nu_mflr        $MfOut $Nk $zi
    echo 'Setting files for Gadget ...' ; python3 pre.py $ptype $ClassOut $MfOut $SimFolder $PkOut $GFOut
    ;;
    
    3) 
    echo 'Prepare Hybrid simulation'
     
    export PATH=$ClassPath:$PATH
    export PATH=$MfPath:$PATH
    ;;
esac

