#!/usr/bin/env python
docstring='''
data-processing/run_pipeline.py default.yaml test.fasta ./tmp_feature
    use default.yaml as configuration file and test.fasta as input
    sequence to generate input files under ./tmp_feature

data-processing/run_pipeline.py test.fasta ./tmp_feature
    use data-processing/default.py as configuration file and test.fasta as input
    sequence to generate input files under ./tmp_feature
'''
#################################################################################
#     File Name           :     run_pipeline.py
#     Created By          :     Qing Ye
#     Creation Date       :     [2016-04-17 22:30]
#     Last Modified       :     [2017-11-15 17:09]
#     Description         :      
#################################################################################
#import yaml

import sys
#import fasta_spliter
import hhblits_runner
import ccmpred_runner
import freecontact_runner
import alnstats_runner
import ss_runner
import jackhmmer_runner
import hhmake_runner
import util_zcx as util
import default

if __name__ == '__main__':
    if len(sys.argv)<3:
        sys.stderr.write(docstring)
        exit()

    input_sequence = sys.argv[-2]
    output_dir = sys.argv[-1]

    if len(sys.argv)==4:
        default_config = sys.argv[1]
        import config_parser
        config = config_parser.parse(default_config, input_sequence, output_dir)
    else:
        config = default.parse(default.default_config, input_sequence, output_dir)

    default.set_HHLIB(config)

    print "=" * 60
    print "Running Pipeline with the following configuration"
    print config

    util.make_dir_if_not_exist(config['path']['output'])

    if config["gen_feature_with_jackhmmer"]:
        r = jackhmmer_runner.Jackhmmer_Runner(config)
        r.run()
    else:
        r = hhblits_runner.HHBlitsRunner(config)
        r.run()

    r = ccmpred_runner.CCMPredRunner(config)
    r.run()

    r = freecontact_runner.FreeContactRunner(config)
    r.run()

    r = alnstats_runner.AlnstatsRunner(config)
    r.run()

    r = ss_runner.SSRunner(config)
    r.run()

    r = hhmake_runner.HHMakeRunner(config)
    r.run()
