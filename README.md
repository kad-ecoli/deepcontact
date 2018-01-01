# DeepContact

## Installation
1. The following dependencies have already been pre-installed for 64bit Linux.
   You need to update respective executables only if you are using other
   operating system.
  - HHBlits 2.0.16
  - HHFilter 2.0.16
  - CCMPred
  - FreeContact 1.0.21
  - Jackhmmer 3.1b2
  - Blast legacy 2.2.26
  - MetaPsicov 1.02
  - Psipred 4.0

2. In the "default_config" dictionary in data-processing/default.py,
   update the following variables to point to respective paths:

   uniprot_db - hhsuite's "uniprot20_2016_02" or "uniclust30"  
   
   uniref_db  - (optional) FASTA format uniref90 or uniref100  
   
   database   - uniref90 in blast's formatdb/makeblastdb format. This is
                used for secondary structure and solvent accessibility
                prediction, and does not need to be most recent version.

   By default, deepcontact uses hhblits + uniprot_db. You can optionally
   switch to use jackhmmer + uniref_db by changing

   ```python
   gen_feature_with_jackhmmer=False,
   ```

   in data-processing/default.py, to

   ```python
   gen_feature_with_jackhmmer=True,
   ```

3. deepcontact uses the same python environment as DeepCov. Please ignore
   this section if DeepCov has already been installed and configured. 
   Otherwise, install python dependencies with

 ```bash
 conda env create -f environment.yml
 source activate deepcontact-env
 pip install --upgrade https://github.com/Lasagne/Lasagne/archive/master.zip
 ```

 (alternatively, see DeepCov document for installing theano & lasagne)

## Usage Example

```bash
data-processing/run_pipeline.py test.fasta ./tmp_feature
deepcontact/make_pred.py test.fasta ./tmp_feature test.deepcontact
```

Here, test.deepcontact is final contact map in gremlin/ccmpred format.
