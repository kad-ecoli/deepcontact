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
hhblits=dict( # from hhsuite 2.0.16
    command=os.path.join(rootdir,"bin/hhblits"),
    uniprot_db="/nfs/amino-library/local/hhsuite/uniprot20_2016_02/uniprot20_2016_02",
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
jackhmmer=dict( # from hmmer 3.1b2
    command=os.path.join(rootdir,"bin/jackhmmer"),
    uniref_db="/scratch/aminoproject_fluxoe/zcx/uniref90/uniref90.fasta",
    n_threads=1,
    inc_E=10.0,
    n_iter=3,
    ),

# run hhfilter after jackhmmer
# see jackhmmer_runner.py
hhfilter=dict( # from hhsuite 2.0.16
    command=os.path.join(rootdir,"bin/hhfilter"),
    ),

# run ccmpred
# see ccmpred_runner.py
ccmpred=dict( # from ccmpred 0.3.2
    command=os.path.join(rootdir,"bin/ccmpred"),
    n_threads=1,
    # optional:
    #cuda_dev=6,   # (do not include if use default cuda device)
    ),

# run freecontact in evfold mode
# see freecontact_runner.py
freecontact=dict( # from freecontact 1.0.21
    command=os.path.join(rootdir,"bin/freecontact"),
    n_threads=1,
    ),

# run alnstats
# see alnstats_runner.py
alnstats=dict( # from metapsicov 1.04
    command=os.path.join(rootdir,"bin/alnstats"),
    n_processes=1,
    ),

# run blastpgp
# see ss_runner.py
blast=dict( # from legacy blast 2.2.26
    command=os.path.join(rootdir,"bin/blastpgp"),
    n_processes=1,
    n_threads=1,
    n_iters=3,
    e_value=0.001,
    # this database must be in blast's formatdb/makeblastdb format
    database="/nfs/amino-library/uniref90/uniref90.fasta",
    ),

# run makemat
# see ss_runner.py
makemat=dict( # from legacy blast 2.2.26
    command=os.path.join(rootdir,"bin/makemat"),
    n_processes=1,
    ),
        
# run psipred
# see ss_runner.py
psipred=dict( # from psipred4.0
    command=os.path.join(rootdir,"bin/psipred"),
    data=os.path.join(rootdir,"data"),
    n_processes=1,
    ),

# run psipred_pass2
# see ss_runner.py
psipred_pass2=dict( # from psipred4.0
    command=os.path.join(rootdir,"bin/psipass2"),
    n_processes=1,
    n_iters=1,
    DCA=1.0,
    DCB=1.0,
    ),

# run solvpred
# see ss_runner.py
solvpred=dict( # from metapsicov 1.04
    command=os.path.join(rootdir,"bin/solvpred"),
    data=os.path.join(rootdir,"data/weights_solv.dat"),
    n_processes=1,
    ),

# run hhmake (includes neff)
# see hhmake_runner
hhmake=dict( # from hhsuite 2.0.16
    command=os.path.join(rootdir,"bin/hhmake"),
    n_processes=1,
    ),
)

def set_HHLIB(config):
    ''' set HHLIB environment variable according to config["hhmake"]["command"]
    '''
    HHLIB=os.path.dirname(os.path.dirname(config["hhmake"]["command"]))
    os.environ["HHLIB"]=HHLIB
    sys.stdout.write("HHLIB=%s\n"%(os.environ["HHLIB"]))
    return HHLIB

def parse(default_config, input_sequence, output_dir):
    default_config["path"]["input"] = input_sequence
    default_config["path"]["output"] = output_dir
    output_name = os.path.basename(input_sequence)
    if output_name.endswith('.fasta'):
        output_name = output_name[:-6]
    default_config["id"] = output_name
    return default_config
