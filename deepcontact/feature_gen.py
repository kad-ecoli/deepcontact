#!/usr/bin/env python
docstring='''
./deepcontact/feature_gen.py ./deepcontact/feature.yaml ./tmp_feature ./tmp_pickle/feature.pkl
    Generate features listed by ./deepcontact/feature.yaml, using input
    files under ./tmp_feature. Output the feature files, in python pickle
    format, to ./tmp_pickle/feature.pkl

./deepcontact/feature_gen.py ./tmp_feature ./tmp_pickle/feature.pkl
    Generate features, using input files under ./tmp_feature. Output the
    feature files, in python pickle format, to ./tmp_pickle/feature.pkl.
    Use the default configuration file at ./deepcontact/feature.yaml 
'''
#################################################################################
#     File Name           :     feature_gen.py
#     Created By          :     yang
#     Creation Date       :     [2017-11-15 16:59]
#     Last Modified       :     [2017-11-16 02:11]
#     Description         :      
#################################################################################
import yaml, h5py, os, sys
from feature_parser import *
import cPickle
DTYPE = 'float32'

def parse_args():
    import argparse
    parser = argparse.ArgumentParser(description = 'generate feature file given a set of configuration')
    parser.add_argument('configure_file_name', type = str, help='configuration file name ')
    args = parser.parse_args()
    return args

def load_config(filename):
    with open(filename) as fin:
        data = yaml.load(fin)
        global_setting = data['general']
        data.pop('general')
        feature_set = data
    return feature_set, global_setting

def generate_feature_2d(feature_name, feature_dir, suffix, length, parser_name, global_setting):
    max_len = int(global_setting['max_len'])
    ret = np.zeros((length, max_len, max_len))
    parsing_function = function_map[parser_name]
    input_file_name = os.path.join(feature_dir, 'test.'+suffix)
    data = parsing_function(input_file_name, max_len)
    if data is None:
        print "There is a error in %s" % input_file_name
    ret[:, :, :] = data[:, :, :]
    return ret

def generate_feature_1d(feature_name, feature_dir, suffix, length, parser_name, global_setting):
    max_len = int(global_setting['max_len'])
    ret = np.zeros((length, max_len))
    parsing_function = function_map[parser_name]
    input_file_name = os.path.join(feature_dir, "test."+suffix)
    data = parsing_function(input_file_name, max_len)
    if data is None:
        print "There is a error in %s" % input_file_name
    ret[:, :] = data[:, :]
    return ret

def generate_feature_0d(feature_name, feature_dir, suffix, length, parser_name, global_setting):
    max_len = int(global_setting['max_len'])
    ret = np.zeros((max_len))
    parsing_function = function_map[parser_name]
    input_file_name = os.path.join(feature_dir, 'test.'+suffix)
    data = parsing_function(input_file_name, max_len)
    if data is None:
        print "There is a error in %" % input_file_name
    ret[:] = data[:]
    return ret

def get_protein_length_by_ccmpred(feature_dir):
    protein_name = os.path.join(feature_dir, 'test.ccmpred')
    length = np.loadtxt(protein_name).shape[0]
    return length

if __name__=="__main__":
    if len(sys.argv)<=2:
        sys.stderr.write(docstring)
        exit()

    #arg = parse_args()
    feature_dir = sys.argv[-2]
    output_filename = sys.argv[-1]
    feature_config = sys.argv[1] if len(sys.argv)==4 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)),"feature.yaml")

    feature_set, global_setting = load_config(feature_config)
    max_len = global_setting['max_len']
    feature_map = {}
    for task_name in feature_set.keys():
        setting = feature_set[task_name]
        suffix = setting['suffix']
        length = setting['length']
        parser_name = setting['parser_name']
        feature_type = setting['type']
        if task_name == 'ccmpred':
            protein_length = get_protein_length_by_ccmpred(feature_dir)
        if 'skip' in setting:
            skip = bool(setting['skip'])
        else:
            skip = False
        if skip:
            continue
        if feature_type=='2d':
            ret = generate_feature_2d(task_name, feature_dir, suffix, length, parser_name, global_setting)
            feature_map[task_name] = (ret, feature_type)
        elif feature_type == '1d':
            ret = generate_feature_1d(task_name, feature_dir, suffix, length, parser_name, global_setting)
            feature_map[task_name] = (ret, feature_type)
        else:
            ret = generate_feature_0d(task_name, feature_dir, suffix, length, parser_name, global_setting)
            feature_map[task_name] = (ret, feature_type)
    
    combine_feature_list_2d = ['ccmpred', 'pairstats', 'evfold']
    combine_feature_list_1d = ['neff', 'ss2', 'solv', 'colstats', 'evfold_std', 'ccmpred_std']
    
    total_feature_length = 0
    for feature_name_2d in combine_feature_list_2d:
        total_feature_length += feature_map[feature_name_2d][0].shape[0]
    feature_2d = np.zeros((total_feature_length, max_len, max_len)).astype(DTYPE)
    cnt = 0
    for feature_name_2d in combine_feature_list_2d:
        current_feature_value = feature_map[feature_name_2d][0]
        feature_2d[cnt:cnt + current_feature_value.shape[0], :, :] = current_feature_value[:, :, :]
        cnt += current_feature_value.shape[0]
    
    total_feature_length = 0
    for feature_name_1d in combine_feature_list_1d:
        total_feature_length += feature_map[feature_name_1d][0].shape[0]
    feature_1d = np.zeros((total_feature_length, max_len)).astype(DTYPE)
    cnt = 0
    for feature_name_1d in combine_feature_list_1d:
        current_feature_value = feature_map[feature_name_1d][0]
        feature_1d[cnt:cnt + current_feature_value.shape[0], :] = current_feature_value[:,  :]
        cnt += current_feature_value.shape[0]

    with open(output_filename,"wb") as fout:
        cPickle.dump((feature_2d, feature_1d, protein_length), fout)

