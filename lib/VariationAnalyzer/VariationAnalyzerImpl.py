# -*- coding: utf-8 -*-
#BEGIN_HEADER
import logging
import os
from VariationAnalyzer.Utils.DownloadFastqUtils import DownloadFastqUtils
from VariationAnalyzer.Utils.SnippyUtils import SnippyUtils
from installed_clients.KBaseReportClient import KBaseReport
from installed_clients.VariationUtilClient import VariationUtil
#END_HEADER


class VariationAnalyzer:
    '''
    Module Name:
    VariationAnalyzer

    Module Description:
    A KBase module: VariationAnalyzer
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.0.1"
    GIT_URL = ""
    GIT_COMMIT_HASH = ""

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.callback_url = os.environ['SDK_CALLBACK_URL']
        self.shared_folder = config['scratch']
        logging.basicConfig(format='%(created)s %(levelname)s: %(message)s',
                            level=logging.INFO)
        self.dfu = DownloadFastqUtils()
        self.su = SnippyUtils()
        self.vu = VariationUtil(self.callback_url)
        #END_CONSTRUCTOR
        pass


    def run_VariationAnalyzer(self, ctx, params):
        """
        This example function accepts any number of parameters and returns results in a KBaseReport
        :param params: instance of type "InputParams" -> structure: parameter
           "obj_name" of String, parameter "workspace_name" of String,
           parameter "fastq_ref" of String, parameter "map_qual" of Long,
           parameter "base_qual" of Long, parameter "min_cov" of Long,
           parameter "min_qual" of Long
        :returns: instance of type "ReportResults" -> structure: parameter
           "report_name" of String, parameter "report_ref" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN run_VariationAnalyzer

        logging.info("Downloading Fastq File")
        fastq_file = self.dfu._stage_input_file(params['fastq_ref'], "paired_end")

        logging.info("Downloading assembly file")
        genome_assembly = self.dfu.download_genome(params['genome_or_assembly_ref'])

        self.su.deinterleave(fastq_file['files']['fwd'], self.shared_folder)

        sample_name = "snippy_output"  #hardcoded to match with attribute mapping file
        #sample_name = (fastq_file['files']['fwd']).replace(".inter.fastq", "")
        snippy_output = self.shared_folder + "/" + sample_name

        cmd = self.su.build_snippy_command(genome_assembly['path'], snippy_output, self.shared_folder)

        self.su.run_snippy_command(cmd)

        params['vcf_staging_file_path'] = self.shared_folder + "/" + sample_name + "/snps.vcf"

        self.vu.save_variation_from_vcf(params)

        report = KBaseReport(self.callback_url)
        report_info = report.create({'report': {'objects_created':[],
                                                'text_message': params['fastq_ref']},
                                                'workspace_name': params['workspace_name']})
        output = {
            'report_name': report_info['name'],
            'report_ref': report_info['ref'],
        }
        #END run_VariationAnalyzer

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method run_VariationAnalyzer return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
