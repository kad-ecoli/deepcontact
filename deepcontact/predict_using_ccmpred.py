#!/usr/bin/env python
docstring='''
./deepcontact/predict_using_ccmpred.py ./tmp_pickle/feature.pkl ./tmp_output/prediction.pkl
    use ./tmp_pickle/feature.pkl as input feature, generate python pickle
    format contact prediction ./tmp_output/prediction.pkl

./deepcontact/predict_using_ccmpred.py ./tmp_pickle/feature.pkl ./tmp_output/prediction.deepcontact
    use ./tmp_pickle/feature.pkl as input feature, generate gremlin
    format contact prediction ./tmp_output/prediction.deepcontact
'''
#################################################################################
#     File Name           :     predict_using_ccmpred.py
#     Created By          :     yang
#     Creation Date       :     [2018-06-15 20:12]
#     Last Modified       :     [2018-06-15 20:47]
#     Description         :      
#################################################################################

from main import load_model
from model import ModelCCMPRED
import theano.tensor as T
import theano, lasagne, numpy as np
import cPickle, sys, os

def normalize(data):
    mean = np.mean(data)
    std = np.std(data)
    data -= mean
    if std != 0:
        data /= std
    return data

def predict_using_ccmpred(ccmpred_feature,output_filename):
    ccmpred_feature = normalize(ccmpred_feature)
    protein_length = ccmpred_feature.shape[0]

    ccmpred_feature_for_nn = np.array([[ccmpred_feature]]).astype(np.float32)

    model = ModelCCMPRED(max_len = protein_length, feature2d_len = 1)

    feature2d = T.tensor4('feature2d')
    network = model.build_model(feature2d)
    output = lasagne.layers.get_output(network, deterministic = True)
    pred_fn = theano.function([feature2d], output, updates = None)
    load_model(output_layer = network, model_file =os.path.abspath(
        os.path.join(os.path.dirname(__file__), "models/model_ccmpred.npz")))

    prediction = pred_fn(ccmpred_feature_for_nn)[0][0][:protein_length, :protein_length]
    if output_filename.endswith(".pkl"):
        with open(output_filename, "wb") as fout:
            cPickle.dump(prediction, fout)
    else:
        np.savetxt(output_filename, prediction, delimiter='\t')

def main(input_filename,output_filename):
    ccmpred_feature = np.loadtxt(input_filename).astype(np.float32)
    predict_using_ccmpred(ccmpred_feature,output_filename)

if __name__=="__main__":
    if len(sys.argv)<=2:
        sys.stderr.write(docstring)
        exit()
    input_filename  = sys.argv[1]
    output_filename = sys.argv[2]
    main(input_filename,output_filename)
