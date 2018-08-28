#!/usr/bin/env python
docstring='''
./deepcontact/main_only_ccmpred.py ./tmp_pickle/feature.pkl ./tmp_output/prediction.pkl
    use ./tmp_pickle/feature.pkl as input feature, generate python pickle
    format contact prediction ./tmp_output/prediction.pkl

./deepcontact/main_only_ccmpred.py ./tmp_pickle/feature.pkl ./tmp_output/prediction.deepcontact
    use ./tmp_pickle/feature.pkl as input feature, generate gremlin
    format contact prediction ./tmp_output/prediction.deepcontact
'''
#################################################################################
#     File Name           :     ./main_only_ccmpred.py
#     Created By          :     yang
#     Creation Date       :     [2018-06-12 08:50]
#     Last Modified       :     [2018-06-12 09:03]
#     Description         :      
#################################################################################

from main import load_model
from model import ModelCCMPRED
import theano.tensor as T
import theano, lasagne, numpy as np
import cPickle, sys, os

def main_only_ccmpred(feature_2d = None, output_filename = None, feature_pickle_filename = None):
    if feature_2d is None:
        with open(feature_pickle_filename, "rb") as fin:
            feature2d_value, _, protein_length = cPickle.load(fin)
    else:
        feature2d_value = feature_2d

    m = ModelCCMPRED(max_len = feature2d_value.shape[-1],
                     feature2d_len = feature2d_value.shape[0])

    feature2d = T.tensor4("feature2d")
    network = m.build_model(feature2d)
    output = lasagne.layers.get_output(network, deterministic = True)
    pred_fn = theano.function([feature2d], output, updates = None)
    load_model(output_layer = network, model_file =os.path.abspath(
        os.path.join(os.path.dirname(__file__), "models/model_ccmpred.npz")))
    prediction = pred_fn([feature2d_value])[0][0][:protein_length, : protein_length]
    if output_filename is None:
        output_filename = './tmp_output/prediction.pkl'

    if output_filename.endswith(".pkl"):
        with open(output_filename, "wb") as fout:
            cPickle.dump(prediction, fout)
    else:
        np.savetxt(output_filename, prediction, delimiter='\t')

if __name__=="__main__":
    if len(sys.argv)<=2:
        sys.stderr.write(docstring)
        exit()
    feature_pickle_filename = sys.argv[1]
    output_filename = sys.argv[2]
    main_only_ccmpred(feature_pickle_filename = feature_pickle_filename, output_filename = output_filename)
