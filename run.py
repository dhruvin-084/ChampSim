from urllib.request import urlretrieve
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
        subprocess.call(bin_name+" --warmup-instructions "+str(warmup)+" --simulation-instructions "+str(simulation)+" "+benchmarks_dir+"/"+b+" > "+"logs/"+bname+logstr+".txt", shell=True)

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
    run(bin_name,"_"+predictor_name+prefix,10000000, 5000000)
    


gshare(14, 2, 16384*32)