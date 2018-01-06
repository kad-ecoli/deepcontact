#################################################################################
#     File Name           :     alnstats_runner.py
#     Created By          :     Qing Ye
#     Creation Date       :     [2016-04-17 22:30]
#     Last Modified       :     [2017-11-15 16:35]
#     Description         :      
#################################################################################
import util_zcx as util
import os


class AlnstatsRunner:
    def __init__(self, config):
        self.config = config
        self.colstats_file = os.path.join(config['path']['output'], 
            config['id'] + '.colstats')
        self.pairstat_file = os.path.join(self.config['path']['output'],
            config['id'] + '.pairstats')

    def run(self, force=False):
        if util.getsize(self.colstats_file) and \
           util.getsize(self.pairstat_file) and force==False:
            print "%s and %s exists. skip Alnstats"%(
                self.colstats_file,self.pairstat_file)
            return

        print "-" * 60
        print "Running Alnstats"
        self._run()
        print "Done\n"

    def _run(self):
        id = self.config['id']

        aln_file = os.path.join(self.config['path']['output'], id + '.aln')
        colstats_file = self.colstats_file
        pairstat_file = self.pairstat_file

        args = [self.config['alnstats']['command'],
                aln_file,
                colstats_file,
                pairstat_file
                ]

        util.run_command(args)
