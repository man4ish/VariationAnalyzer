/*
A KBase module: VariationAnalyzer
*/

module VariationAnalyzer {
    typedef structure {
        string report_name;
        string report_ref;
    } ReportResults;

    typedef structure{
        string obj_name;
        string workspace_name; 
        string fastq_ref;
        int map_qual;
        int base_qual;
        int min_cov;
        int min_qual;        
    } InputParams;

    /*
        This example function accepts any number of parameters and returns results in a KBaseReport
    */
    funcdef run_VariationAnalyzer(InputParams params) returns (ReportResults output) authentication required;

};
