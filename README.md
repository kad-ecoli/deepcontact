# DeepContact

## Installation
1. Install the following dependencies
  - HHBlits 2.0.16
  - Jackhmmer 3.1b2
  - HHFilter 2.0.16
  - CCMPred
  - FreeContact 1.0.21
  - MetaPsicov 1.02
  - Blast legacy 2.2.26
  - Psipred 4.0
2. Modify default_config dictionary in data-processing/default.py
   with path to the above programs
3. Install python dependencies with

 ```bash
 conda env create -f environment.yml
 source activate deepcontact-env
 pip install --upgrade https://github.com/Lasagne/Lasagne/archive/master.zip
 ```

 (alternatively, see DeepCov document for installing theano & lasagne)

## Usage Example

```bash
data-processing/run_pipeline.py test.fasta ./tmp_feature
deepcontact/feature_gen.py test.fasta ./tmp_feature ./tmp_pickle/feature.pkl
deepcontact/main.py ./tmp_pickle/feature.pkl ./tmp_output/prediction.deepcontact
```

Here, ./tmp_output/prediction.deepcontact is final contact map in 
gremlin/ccmpred format.
