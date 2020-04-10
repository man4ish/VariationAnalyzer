import os
import subprocess

from pprint import pprint,pformat

class SnippyUtils:

    def __init__(self):
       self.callbackURL = os.environ['SDK_CALLBACK_URL']
       pass 

    def build_snippy_command(self, genome_file, output_dir, outpath):
        command = "/kb/module/deps/snippy/bin/snippy --outdir "+ output_dir +" --ref "+ genome_file + " --R1 "+ outpath + "/fwd.fastq --R2 " + outpath + "/rev.fastq"
        return command

    def run_snippy_command(self, command):
        try:
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
            stdout, stderr = process.communicate()
            if stdout:
                print("ret> ", process.returncode)
                print("OK> output ", stdout)
            if stderr:
                print("ret> ", process.returncode)
                print("Error> error ", stderr.strip())

        except OSError as e:
            print("OSError > ", e.errno)
            print("OSError > ", e.strerror)
            print("OSError > ", e.filename)


    def deinterleave(self, fastq_file, path):
        try:
            with open(path + "/rev.fastq",'w') as fastq_1, open(path + "/fwd.fastq",'w') as fastq_2:
                [fastq_1.write(line) if (i % 8 < 4) else fastq_2.write(line) for i, line in enumerate(open(fastq_file))]
        except IOError as e:
            print ('Operation failed: %s' % e.strerror)


