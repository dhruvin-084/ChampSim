# CA Assignment 1 P1

This is part of Assignment 1 P1 of coures E0 243 Computer architecture offered at CSA department at Indian Institute of Science.

In this assignment we eavluate different branch predictors with ChampSim simulator

ChampSim installation guilde can be found in [ChampSim_README.md](ChampSim_README.md) file


## Building and running champsim for different predictors

We have written python script for building and running the simulation for different predictors and different 

[run.py](run.py) script contains functions to compile and run siumation for different configuration of branch pridcitors.

run.py contains functions:

### ```gshare(history_length, counter_bits, table_size)```
This function will compile ChampSim with gshare predictor. It will store the executable file in bin folder
#### Parameters:
- history_length: length of the BHR register
- counter_bits: number of bits for saturating counter per table entry
- table_size: number of entry in pattern history table

### ```Perceptron(phistory, pbits, pnum)```
This functions will compile ChampSim with Perceptron preditor. It will store the executable file in bin folder.

#### Parameters:
- phisotry: perceptron history length
- pbits: number of bits per weight
- pnum: number of perceptron

### ```tage(lenGlobal, lenTag, minHistory, maxHistory)```
This functions will compile ChampSim with tage preditor. It will store the executable file in bin folder.

#### parameters:
- lenGlobal: bits of the global history
- lenTag: bits per tag
- minHisotry: minimum bits in geometric history
- maxHistory: maximum bits in geometric history



### ```Hybrid(phistory, pbits, pnum, tglobalLen, ttagLen, postfix)```
This functions will compile ChampSim with hybrid preditor. It will store the executable file in bin folder.

#### Parameters:
- phisotry: perceptron history length
- pbits: number of bits per weight in perceptron
- pnum: number of perceptron
- tlenGlobal: bits of the global history for tage
- tlenTag: bits per tag for tage
- tminHisotry: minimum bits in geometric history for tage
- tmaxHistory: maximum bits in geometric history for tage
- postfix: postfix for name of executable file. e.g. "5050", "3070" or "7030"

### ```run(bin_name, logstr, warmup, simulation)```
This function will run the simulation. It will also store the log file in log folder.

#### Parameters:
- bin_name: name binary executable file
- logstr: postfix string for the log file
- warmup: number of warmup instructions
- simulation: number of simulation instructions


We have commented functions in run.py file. Just uncomment the functions for any configuration of the branch predictor and run the python script. It will generate the binary exectuable in bin folder.

You can run this executable manually or using run fucntion provided in the script. 