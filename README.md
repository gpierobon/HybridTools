# HybridTools

Bash+Python scripts for neutrino simulations based on [gadget4-hybrid](https://github.com/joechenUNSW/gadget4-hybrid_public) and multi-fluid linear response [MuFLR](https://github.com/upadhye/MuFLR). 
Options include: 
  
  - Starting a neutrino simulations (LinearResponse or Hybrid )
  - Restarting hybrid simulations, converting streams into particles 
  - General post-processing

J.Z. Chen is the author of the [gadget4-hybrid](https://github.com/joechenUNSW/gadget4-hybrid_public) code.<br />
A. Upadhye is the author of the [MuFLR](https://github.com/upadhye/MuFLR) code.<br />
  
 ## Usage
 
```
git clone https://github.com/gpierobon/HybridTools; cd HybridTools
```
Adjust parameters in the htools.sh file and then run:
```
bash htools.sh
```

## Requirements

- Numpy,h5py
- OpenMP


## HPC jobs

For HPC runs a typical script (running with the PBS job scheduler) can be found in job.pbs. A typical simulation will have the following setup.
Create a folder in your HPC system:
```
mkdir /path/to/sim_folder
```
Copy the data in the simfiles
```
cp simfiles/* /path/to/sim_folder
```
Go in the simulation you just created, adjust your parameters in the Config.sh or Config_restart.sh files and the options in the htools.sh module. The latter  will run the configuration file based on OPT (0 for Start,1 for Restart), and in the simulation folder you will find the right executable file. For a starting run type 
```
mpirun -np <n_processes> ./gadget4-hybrid param.txt
```
For a hybrid restart run type
```
mpirun -np <n_processes> ./gadget4-hybrid_restart param_restart.txt
```


