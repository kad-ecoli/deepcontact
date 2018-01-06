import os
import util_zcx as util


class HHMakeRunner:
    def __init__(self, config):
        self.config = config
        self.output_file = os.path.join(config['path']['output'], 
            config['id'] + '.hhmake')

    def run(self, force=False):
        if util.getsize(self.output_file) and force==False:
            print self.output_file,"exists. skip HHMake"
            return

        print "-" * 60
        print "Running HHMake"
        self._run()
        print "Done\n"

    def _run(self):
        id = self.config['id']

        input_file = os.path.join(self.config['path']['output'], id + '.a3m')
        log_file = self.output_file
        hhm_file = os.path.join(self.config['path']['output'], id + '.hhm')

        args = [self.config['hhmake']['command'],
                '-i', input_file,
                '-o', hhm_file]
        util.run_command(args, log_file)
