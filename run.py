from urllib.request import urlretrieve
import shlex
import os
import json
import re
import subprocess

benchmarks = [
    "603.bwaves_s-1080B.champsimtrace.xz",
    "607.cactuBSSN_s-3477B.champsimtrace.xz",
    "600.perlbench_s-210B.champsimtrace.xz"
]

benchmarks_url = "https://dpc3.compas.cs.stonybrook.edu/champsim-traces/speccpu/"

benchmarks_dir = "traces"
log_dir = "logs"

if not os.path.isdir(benchmarks_dir):
    os.mkdir(benchmarks_dir)

if not os.path.isdir(log_dir):
    os.mkdir(log_dir)

for b in benchmarks:
    if not os.path.isfile(benchmarks_dir+"/"+b):
        print("Downloading "+b+".....")
        urlretrieve(benchmarks_url+b, benchmarks_dir+"/"+b)


config_file = "champsim_config.json"



def change_config(predictor_name, prefix):
    with open(config_file, 'r+') as f:
        config = json.load(f)
        config['executable_name'] = "champsim_" + predictor_name+prefix
        config['ooo_cpu'][0]['branch_predictor'] = predictor_name
        f.seek(0)
        json.dump(config, f, indent=4)
        f.truncate()
        os.system("./config.sh "+config_file)

def compile():
    os.system("make -j6")

def add_defines(options):
    with open("_configuration.mk", 'r+') as f:
        content = f.read()
        for o in options:
            content += "CPPFLAGS += -D"+o+"="+str(options[o])+"\n" 
        f.seek(0)
        f.write(content)

def run(bin_name, logstr, warmup, simulation):
    for b in benchmarks:
        bname = re.findall("\.[a-zA-Z]*_", b)[0][1:-1]
        print("running "+bin_name+" for "+b)
        cmd = bin_name+" --warmup-instructions "+str(warmup)+" --simulation-instructions "+str(simulation)+" "+benchmarks_dir+"/"+b+" > "+"logs/"+bname+logstr+".txt"
        cmds = shlex.split(cmd)
        subprocess.Popen(cmd, shell=True)


def gshare(history_length=14, counter_bits=2, table_size=16384):
    predictor_name = "gshare"
    prefix = "_"+str(history_length)+"_"+str(counter_bits)+"_"+str(table_size)
    bin_name = "bin/champsim_"+predictor_name+prefix

    change_config(predictor_name, prefix)

    options = {
        "GSHARE_HISTORY_LENGTH": history_length,
        "GSHARE_COUNTER_BITS": counter_bits,
        "GSHARE_TABLE_SIZE": table_size
    }
    add_defines(options)

    compile()
    # run(bin_name,"_"+predictor_name+prefix,1000000000, 500000000)

def Perceptron(phistory = 24, pbits = 8, pnum = 163):
    predictor_name = "perceptron"
    prefix = "_"+str(phistory)+"_"+str(pbits)+"_"+str(pnum)
    bin_name = "bin/champsim_"+predictor_name+prefix

    change_config(predictor_name, prefix)

    options = {
        "PHISTORY": phistory,
        "PBITS": pbits,
        "PNUM": pnum
    }

    add_defines(options)

    compile()
    # run(bin_name,"_"+predictor_name+prefix,1000000000, 500000000)
    return bin_name

def tage(lenGlobal = 14, lenTag = 11,minHistory=5, maxHistory = 131):
    predictor_name = "tage"
    prefix = "_his_"+str(minHistory)+"_"+str(maxHistory)
    bin_name = "bin/champsim_"+predictor_name+prefix

    change_config(predictor_name, prefix)

    options = {
        "LEN_GLOBAL": lenGlobal,
        "LEN_TAG": lenTag,
        "MIN_HISTORY_LEN": minHistory,
        "MAX_HISTORY_LEN": maxHistory
    }

    add_defines(options)

    compile()
    return bin_name


def Hybrid(phistory = 24, pbits = 8, pnum = 163, tglobalLen = 13, ttagLen = 11, prefix = "5050"):
    predictor_name = "hybrid"
    
    bin_name = "bin/champsim_"+predictor_name+prefix

    change_config(predictor_name, prefix)

    options = {
        "PHISTORY": phistory,
        "PBITS": pbits,
        "PNUM": pnum,
        "LEN_GLOBAL": tglobalLen,
        "LEN_TAG": ttagLen
    }

    add_defines(options)

    compile()
    return bin_name



# gshare(19, 2, 2**19)
# gshare(18, 2, 2**18)
# gshare(17, 2, 2**17)
# gshare(16, 2, 2**16)
# gshare(15, 2, 2**15)
# run("bin/champsim_gshare_15_2_"+str(2**15), "_gshare_8KB", 1000000000, 500000000)
# run("bin/champsim_gshare_16_2_"+str(2**16), "_gshare_16KB", 1000000000, 500000000)
# run("bin/champsim_gshare_17_2_"+str(2**17), "_gshare_32KB", 1000000000, 500000000)
# run("bin/champsim_gshare_18_2_"+str(2**18), "_gshare_64KB", 1000000000, 500000000)

# Perceptron(24, 8, 163)
# Perceptron(24*2, 8*2, 163*8)
# Hybrid(24*2, 8*2, 163*4, 13, 11, "5050")
# Hybrid(48, 16, 1304, 12, 13, "3070")
# Hybrid(47, 10, 652, 13, 17, "7030")
# run("bin/champsim_hybrid5050", "_hybrid_5050", 1000000000, 500000000)
# run("bin/champsim_hybrid3070", "_hybrid_3070", 1000000000, 500000000)
# run("bin/champsim_hybrid7030", "_hybrid_7030", 1000000000, 500000000)


def calculate_tage_size(num_banks, bimodal_size, len_bimodal, len_global, len_tag, len_counts, min_history_len, max_history_len):
    # bimodal table size
    a1 = bimodal_size * len_bimodal

    # table sizes
    com_his_size = 48
    bank_entry_size = len_counts + len_tag + 2
    a2 = num_banks * (com_his_size + bank_entry_size + 2**len_global * bank_entry_size)

    # bank global index
    a3 = len_global*num_banks

    # tag result
    a4 = len_tag*num_banks

    return a1 + a2 + a3 + a4 + max_history_len

# print(calculate_tage_size(4, 4099, 2, 14, 11, 3, 5, 131)/8/(2**10))
# print(calculate_tage_size(4, 4099, 2, 13, 11, 3, 5, 131)/8/(2**10))
# print(calculate_tage_size(4, 4099, 2, 12, 11, 3, 5, 131)/8/(2**10))
# print(calculate_tage_size(4, 4099, 2, 11, 10, 3, 5, 131)/8/(2**10))
# print(calculate_tage_size(4, 4099, 2, 10, 10, 3, 5, 131)/8/(2**10))

# tage(14, 11, 131)
# tage(13, 11, 131)
# tage(12, 11, 131)
# tage(11, 10, 131)
# tage(10, 10, 131)
# run("bin/champsim_tage_10_10_131", "_tage_8KB", 1000000000, 500000000)
# run("bin/champsim_tage_13_13_131", "_tage_64KB", 1000000000, 500000000)
# run("bin/champsim_tage_14_14_131", "_tage_128B", 1000000000, 500000000)
def perceptron_size(phistory, pbits, pnum):
    return (phistory+1)*pbits*pnum


#Perceptron(96, 16, 678)
#Perceptron(80, 12, 538)
#Perceptron(60, 10, 422)
#Perceptron(48, 8, 335)
#Perceptron(38, 6, 268)

# run("bin/champsim_perceptron_48_8_335", "_perceptron_16KB", 1000000000, 500000000)
# run("bin/champsim_perceptron_48_8_335", "_perceptron_64KB", 1000000000, 500000000)
# run("bin/champsim_perceptron_96_16_678", "_perceptron_128KB", 1000000000, 500000000)

# tage(14, 11, 5, 73)
# tage(14, 11, 5, 96)
# tage(14, 11, 10, 131)
# tage(14, 11, 15, 180)
# tage(14, 11, 25, 240)

# run("bin/champsim_tage_his_5_73", "_tage_his_5_73", 1000000000, 500000000)
# run("bin/champsim_tage_his_15_180", "_tage_his_15_180", 1000000000, 500000000)
# run("bin/champsim_tage_his_25_240", "_tage_his_25_240", 1000000000, 500000000)