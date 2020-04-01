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
        path = "/kb/module/work/tmp/"
        fastq_1 = open(path + "r.fastq",'w')
        fastq_2 = open(path + "f.fastq",'w')
        [fastq_1.write(line) if (i % 8 < 4) else fastq_2.write(line) for i, line in enumerate(open(fastq_file))]
        fastq_1.close()
        fastq_2.close()
    
        #print("bash /kb/module/deps/deinterleave.sh > "+ fastq_file + " /kb/module/work/tmp/f.fastq  /kb/module/work/tmp/r.fastq")
        #os.system("bash /kb/module/deps/deinterleave.sh > "+ fastq_file + " /kb/module/work/tmp/f.fastq  /kb/module/work/tmp/r.fastq")

#su = SnippyUtils()
#su.deinterleave("/home/manish/Desktop/VariationAnalyzer/test_local/workdir/tmp/7b7fa138-4fee-47ae-83e4-d23f7481dc8d.inter.fastq")
