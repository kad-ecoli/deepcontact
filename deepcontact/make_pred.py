#!/usr/bin/env python
docstring='''
./deepcontact/make_pred.py test.fasta ./tmp_feature test.deepcontact
    Using input fasta sequence test.fasta and input files under
    ./tmp_feature, predict final contact map, and output it 
    (in gremlin/ccmpred format) to test.deepcontact

option:
    -only_ccmpred={false,true}
        false: (default) use full set of feature
        true:  only ccmpred features
'''
import os, sys
from feature_parser import *

import feature
import feature_only_ccmpred

from feature_gen import generate_feature_2d,generate_feature_1d,DTYPE
from feature_gen import generate_feature_0d,get_protein_length_by_ccmpred

from main import main
from predict_using_ccmpred import predict_using_ccmpred

if __name__=="__main__":
    if len(sys.argv)<=3:
        sys.stderr.write(docstring)
        exit()
    
    only_ccmpred=False # use full feature set

    argv=[]
    for arg in sys.argv[1:]:
        if arg.startswith("-only_ccmpred="):
            only_ccmpred=(arg.lower()=="-only_ccmpred=true")
        elif arg.startswith("-"):
            sys.stderr.write("ERROR! No such option %s\n"%arg)
            exit()
        else:
            argv.append(arg)
    input_sequence  = argv[0]
    feature_dir     = argv[1]
    output_filename = argv[2]

    output_name = os.path.basename(input_sequence)
    if output_name.endswith('.fasta'):
        output_name = output_name[:-6]

    global_setting    =feature.global_setting
    feature_set       =feature.feature_set
    if only_ccmpred:
        global_setting=feature_only_ccmpred.global_setting
        feature_set   =feature_only_ccmpred.feature_set

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
    combine_feature_list_2d = [x for x in combine_feature_list_2d if x in feature_map]
    combine_feature_list_1d = [x for x in combine_feature_list_1d if x in feature_map]
    
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

    if only_ccmpred:
        predict_using_ccmpred(
            ccmpred_feature =feature_2d[0],
            output_filename =output_filename)
    else:
        main(
            feature_2d      = feature_2d, 
            feature_1d      = feature_1d,
            protein_length  = protein_length, 
            output_filename = output_filename)
