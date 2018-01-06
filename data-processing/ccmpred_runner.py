#################################################################################
#     File Name           :     ccmpred_runner.py
#     Created By          :     Qing Ye
#     Creation Date       :     [2016-04-17 22:30]
#     Last Modified       :     [2017-11-15 16:28]
#     Description         :      
#################################################################################
import util_zcx as util
import os


class CCMPredRunner:
    def __init__(self, config):
        self.config = config
        self.output_file = os.path.join(config['path']['output'], 
            config['id'] + '.ccmpred')

    def run(self, force=False):
        if util.getsize(self.output_file) and force==False:
            print self.output_file,"exists. skip CCMPred"
            return

        print "-" * 60
        print "Running CCMPred"
        self._run()
        print "Done\n"

    def _run(self):
        ccmpred_config = self.config['ccmpred']

        id = self.config['id']

        aln_file = os.path.join(self.config['path']['output'], id + '.aln')
        output_file = self.output_file

        if self.config['ccmpred']['n_threads'] == 0:
            if 'cuda_dev' in self.config['ccmpred']:
                args = [self.config['ccmpred']['command'],
                        '-d', str(self.config['ccmpred']['cuda_dev']),
                        aln_file,
                        output_file]
            else:
                gpu_id = 0
                print gpu_id
                args = [self.config['ccmpred']['command'],
                        '-d', str(gpu_id), 
                        aln_file,
                        output_file]
        else:
            args = [self.config['ccmpred']['command'],
                    '-t', str(self.config['ccmpred']['n_threads']),
                    aln_file,
                    output_file]

        util.run_command(args)

