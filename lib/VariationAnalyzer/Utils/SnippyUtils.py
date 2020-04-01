import os
import subprocess

from pprint import pprint,pformat

class SnippyUtils:

    def __init__(self):
       self.callbackURL = os.environ['SDK_CALLBACK_URL']
       pass 

    def build_snippy_command(self, genome_file, output_dir):
        outpath = "/kb/module/work/tmp/"
        command = "/kb/module/deps/snippy/bin/snippy --outdir "+ output_dir +" --ref "+ genome_file + " --R1 "+ outpath + "f.fastq --R2 " + outpath + "r.fastq" 
        return command

    def run_snippy_command(self, command):
        os.system(command)

    def deinterleave(self, fastq_file):
        print("bash /kb/module/deps/deinterleave.sh > "+ fastq_file + " /kb/module/work/tmp/f.fastq  /kb/module/work/tmp/r.fastq")
        os.system("bash /kb/module/deps/deinterleave.sh > "+ fastq_file + " /kb/module/work/tmp/f.fastq  /kb/module/work/tmp/r.fastq")
