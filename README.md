# Unikernel-based Deferrable Server Analysis

The repository is used to reproduce the evaluation from

_Unikernel-Based Real-Time Virtualization under Deferrable Servers: Analysis and Realization_

for ECRTS 2022.

This document is organized as follows:
1. [Environment Setup](#environment-setup)
2. [How to run the experiments](#how-to-run-the-experiments)
3. [Overview of the corresponding functions](#overview-of-the-corresponding-functions)
4. [Miscellaneous](#miscellaneous)

## Environment Setup
### Requirements

Some common software should be installed:
```
sudo apt-get install software-properties-common git python3.9
```
If the installation of Python3.9 doesn't work, likely you need to add deadsnakes PPA beforehand as it is not available on universe repo:
```
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
```

To run the experiments Python 3.9 is required (another version of Python 3 might also work). Moreover, the following packages are required:
```
getopt
math
matplotlib
multiprocessing
numpy
os
pickle
random
statistics
sys
```

Assuming that Python 3.9 is installed in the targeted machine, to install the required packages:
```
pip3 install matplotlib numpy
```
or
```
python3.9 -m pip install matplotlib numpy
```
In case there is any dependent package missing, please install them accordingly.

## File Structure
    .
    ├── res                     # Resource packages
    │   ├── benchmark.py        # Server and task creation
    │   ├── our_analysis.py     # Our analysis
    │   ├── plot.py             # Plotting functionality
    │   └── rtc_cb.py           # RTC-based analysis	
    ├── data                    # Evaluation data
    │   ├── 1setup              # Server and task specification
    │   ├── 2results            # Evaluation results
    │   └── 3plots              # Plots to present the results
    ├── main.py                 # Main function of the evaluation
    ├── auto.ssh                # bash-script to automize the evaluation
    └── README.md

Note that the source code of the case study part (Section 6.2) is contributed by the business partner, so it is excluded from this repository.

### Deployment

The following steps explain how to deploy this framework on the machine:

First, clone the git repository or download the [zip file](https://github.com/tu-dortmund-ls12-rt/unikernel-based_deferrable_server_analysis/archive/refs/heads/main.zip):
```
git clone https://github.com/tu-dortmund-ls12-rt/unikernel-based_deferrable_server_analysis.git
```
Move into the extracted/cloned folder, change the permissions of the script to be executable, and execute auto.sh natively:
```
cd unikernel-based_deferrable_server_analysis
chmod 777 auto.sh
./auto.sh
```
## How to run the experiments

- To reproduce Figure 6 and 7 in the paper, ```auto.sh``` should be executed.
- The plotted figures can be found in the folder data/3plots:

Paper figure | Plot in data/3plots
---|---
Fig. 7 | 'plot2_num_servers_combined_util_servers=[0.1, 0.4].pdf'
Fig. 8 | 'plot3_num_servers=[10, 100]_util_servers_combined.pdf'

As a reference, we utilize a machine running Archlinux 5.17.3-arch1-1 x86_64 GNU/Linux,with i7-10610U CPU and 16 GB main memory. 
It takes about 170 seconds with this machine to obtain these two figures, when set ```num_processors = 5``` in ```main.py```

## Overview of the corresponding functions

The following tables describe the mapping between content of our paper and the source code in this repository.

**Section 4.1** (RTC-based analysis):
On Paper | Source code
--- | ---
Theorem 4 | rtc_cb.wcrt_analysis_single()

**Section 4.2** (Our Analysis for Sporadic Tasks):
On Paper | Source code
--- | ---
Theorem 7 | our_analysis.wcrt_analysis_single()

## Miscellaneous

### Authors

* Kuan-Hsun Chen (University of Twente)
* Mario Günzel (TU Dortmund)
* Boguslaw Jablkowski (EMVICORE GmbH)
* Markus Buschhoff (EMVICORE GmbH)
* Jian-Jia Chen (TU Dortmund)

### Acknowledgments

This work has been supported by European Research Council (ERC) Consolidator Award 2019, as part of PropRT (Number 865170), and by Deutsche Forschungsgemeinschaft (DFG), as part of Sus-Aware (Project no. 398602212).

### License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
