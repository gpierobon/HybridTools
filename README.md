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
 
