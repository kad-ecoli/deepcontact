#!/usr/bin/env python
docstring='''
./deepcontact/make_pred.py test.fasta ./tmp_feature test.deepcontact
    Using input fasta sequence test.fasta and input files under
    ./tmp_feature, predict final contact map, and output it 
    (in gremlin/ccmpred format) to test.deepcontact
'''
import os, sys
from feature_parser import *
from feature import feature_set,global_setting

from feature_gen import generate_feature_2d,generate_feature_1d,DTYPE
from feature_gen import generate_feature_0d,get_protein_length_by_ccmpred
from main import load_model,main

if __name__=="__main__":
    if len(sys.argv)<=3:
        sys.stderr.write(docstring)
        exit()

    input_sequence = sys.argv[1]
    feature_dir = sys.argv[2]
    output_filename = sys.argv[3]

    output_name = os.path.basename(input_sequence)
    if output_name.endswith('.fasta'):
        output_name = output_name[:-6]

    protein_length = get_protein_length_by_ccmpred(feature_dir, output_name)
    global_setting['max_len']=max([protein_length,global_setting['max_len']])
    max_len = global_setting['max_len']
    feature_map = {}
    for task_name in feature_set.keys():
        setting = feature_set[task_name]
        suffix = setting['suffix']
        length = setting['length']
        parser_name = setting['parser_name']
        feature_type = setting['type']
        if 'skip' in setting:
            skip = bool(setting['skip'])
        else:
            skip = False
        if skip:
            continue
        if feature_type=='2d':
            ret = generate_feature_2d(task_name, feature_dir, suffix, length,
                parser_name, global_setting, output_name)
            feature_map[task_name] = (ret, feature_type)
        elif feature_type == '1d':
            ret = generate_feature_1d(task_name, feature_dir, suffix, length,
                parser_name, global_setting, output_name)
            feature_map[task_name] = (ret, feature_type)
        else:
            ret = generate_feature_0d(task_name, feature_dir, suffix, length,
                parser_name, global_setting, output_name)
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

    main(feature_2d = feature_2d, feature_1d = feature_1d,
        protein_length = protein_length, output_filename = output_filename)
