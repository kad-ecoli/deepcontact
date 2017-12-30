#!/usr/bin/env python
import os,sys
rootdir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

default_config=dict(
gen_feature_with_jackhmmer=False, # if Yes, jackhmmer_result will be used to generate feature

path=dict(
    #output_base="/data/work/qing/DeepContact/test",
    ),

# run hhblits and reformat output to aln file
# see hhblits_runner.py
hhblits=dict(
    command=os.path.join(rootdir,"hhsuite-2.0.16-linux-x86_64/bin/hhblits"),
    uniprot_db=os.path.join(rootdir,"uniprot20_2016_02/uniprot20_2016_02"),
    n_threads=1,
    n_iters=3,
    e_value=0.001,
    maxfilt=500000,
    diff="inf",
    id="99",
    cov=50,
    ),

# run jackhmmer
# see jackhmmer_runner.py
jackhmmer=dict(
    command=os.path.join(rootdir,"hmmer/binaries/jackhmmer"),
    uniref_db=os.path.join(rootdir,"uniref90/uniref90.fasta"),
    n_threads=1,
    inc_E=10.0,
    n_iter=3,
    ),

# run hhfilter after jackhmmer
# see jackhmmer_runner.py
hhfilter=dict(
    command=os.path.join(rootdir,"hhsuite-2.0.16-linux-x86_64/bin/hhfilter"),
    ),

# run ccmpred
# see ccmpred_runner.py
ccmpred=dict(
    command=os.path.join(rootdir,"bin/ccmpred"),
    n_threads=1,
    # optional:
    #cuda_dev=6,   # (do not include if use default cuda device)
    ),

# run freecontact in evfold mode
# see freecontact_runner.py
freecontact=dict(
    command=os.path.join(rootdir,"bin/freecontact"),
    n_threads=1,
    ),

# run alnstats
# see alnstats_runner.py
alnstats=dict(
    command=os.path.join(rootdir,"metapsicov/bin/alnstats"),
    n_processes=1,
    ),

# run blastpgp
# see ss_runner.py
blast=dict(
    command=os.path.join(rootdir,"blast/bin/blastpgp"),
    n_processes=1,
    n_threads=1,
    n_iters=3,
    e_value=0.001,
    database="/nfs/amino-library/uniref90/uniref90.fasta",
    ),

# run makemat
# see ss_runner.py
makemat=dict(
    command=os.path.join(rootdir,"blast/bin/makemat"),
    n_processes=1,
    ),
        
# run psipred
# see ss_runner.py
psipred=dict(
    command=os.path.join(rootdir,"psipred/bin/psipred"),
    data=os.path.join(rootdir,"psipred/data"),
    n_processes=1,
    ),

# run psipred_pass2
# see ss_runner.py
psipred_pass2=dict(
    command=os.path.join(rootdir,"psipred/bin/psipass2"),
    n_processes=1,
    n_iters=1,
    DCA=1.0,
    DCB=1.0,
    ),

# run solvpred
# see ss_runner.py
solvpred=dict(
    command=os.path.join(rootdir,"metapsicov/bin/solvpred"),
    data=os.path.join(rootdir,"metapsicov/data/weights_solv.dat"),
    n_processes=1,
    ),

# run hhmake (includes neff)
# see hhmake_runner
hhmake=dict(
    command=os.path.join(rootdir,"hhsuite-2.0.16-linux-x86_64/bin/hhmake"),
    n_processes=1,
    ),
)

def set_HHLIB(config):
    ''' set HHLIB environment variable according to config["hhmake"]["command"]
    '''
    HHLIB=os.path.basename(os.path.dirname(os.path.dirname(
        config["hhmake"]["command"])))
    os.environ["HHLIB"]=HHLIB
    return HHLIB

def parse(default_config, input_sequence, output_dir):
    default_config["path"]["input"] = input_sequence
    default_config["path"]["output"] = output_dir
    output_name = os.path.basename(input_sequence)
    if output_name.endswith('.fasta'):
        output_name = output_name[:-6]
    default_config["id"] = output_name
    return default_config
