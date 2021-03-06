#################################################################################
#     File Name           :     freecontact_runner.py
#     Created By          :     Qing Ye
#     Creation Date       :     [2016-04-17 22:30]
#     Last Modified       :     [2017-11-15 16:32]
#     Description         :      
#################################################################################
import util_zcx as util
import os


class FreeContactRunner:
    def __init__(self, config):
        self.config = config
        self.output_file = os.path.join(config['path']['output'], 
            config['id'] + '.evfold')

    def run(self, force=False):
        if util.getsize(self.output_file) and force==False:
            print self.output_file,"exists. skip FreeContact"
            return

        print "-" * 60
        print "Running FreeContact"
        self._run()
        print "Done\n"

    def _run(self):
        id = self.config['id']
        aln_file = os.path.join(self.config['path']['output'], id + '.aln')
        output_file = self.output_file

        args = [self.config['freecontact']['command'],
                '-a', str(self.config['freecontact']['n_threads']),
                '-f', aln_file]

        util.run_command(args, output_file)
