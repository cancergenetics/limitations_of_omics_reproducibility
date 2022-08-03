# Experimental reproducibility limits the correlation between mRNA and protein abundances in tumour proteomic profiles #


### Data analysis overview:
     
All the figures and statistics are generated in these notebooks
        
Notebook / R Script                           | Figures        | Description           |
:---------------------------------------------|:-------------  |:----------------------|
1_proteomic_replicate_correlation_analysis    | Figure 1, 3    | Analyse the variation in proteomic reproducibility |
2_compare_replicate-cor_with_mRNA-protein-cor | Figure 2, S1   | Investigate the variation in mRNA-protein correlation with the variation in protein-protein correlation |
3a_robust_rank_aggregation.R                  | -              | Perform Robust Rank Aggregation and Stuart aggregation over the proteomic replicate correlation |
3b_aggregate_ranks_comparison                 | Figure S2B, S3 | Compare the different rank aggregation algorithms |
4_other_studies_and_aggregated_ranks          | Figure 4       | Assess the variation in mRNA-protein correlation for studies without replicate proteomic profiles with respect to change in aggregated protein reproducibility rank |
5_protein_predictability_analysis             | Figure S4      | Analyse the predictability of proteins with respect to protein reproducibility |
6a_factors_affecting_protein_reproducibility   | Figure 5, S5   | Identify the potential factors affecting protein reproducibility |
6b_factors_affecting_mRNA_protein_correlation   | Figure S6   | Identify the whether the factors identified above affect mRNA-protein correlation |
7_transcriptomic_replicate_analysis           | Figure 6, S5E   | Analyse the variation in transcriptomic reproducibility and its impact on mRNA-protein correlation |
8_pathway_enrichment_analysis                 | Figure 7, S7   | Perform KEGG Pathway enrichment analysis using Mann-Whitney U test |
          
     
### Data processing overview:
        
 All the raw/external data were processed in these notebooks

Notebook / Script                      | Description                              |
:--------------------------------------| -----------------------------------------|
1a_process_older_tumour_studies        | Process the transcriptomic and proteomic data of tumour studies published prior to 2019 |
1b_process_newer_tumour_studies        | Process the transcriptomic and proteomic data of tumour studies available in CPTAC Python API |
1c_process_non_tumour_studies          | Process CCLE and GTEx transcriptomic and proteomic data |
1d_merge_standardised_pipeline_results | Merge data from all studies to create Table S1   |
2_process_proteomic_replicates         | Process proteomic replicates from cancer studies containing replicates |
3_process_protein_properties           | Process properties of proteins such as abundance, unique peptides, half-lives, complex membership. |
4_process_transcriptomic_replicates    | Process the transcriptomic replicates of cancer cell lines |
5_get_genes_by_kegg_pathways           | Obtain KEGG pathways and the associated genes using REST API |
standardised_pipeline_utils.py         | Contains standardised pipeline applied to all the data before computing correlation |


### To run Jupyter notebooks:
* Obtain external data - sources are listed in data_sources
* Set path to external data in environment.yml (DATA_PATH)
  * Note: this can also be set in the activated environment with: `conda env config vars set external_data=directory_of_choice`
* Create [conda](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file) environment from the environment.yml file: `conda env create -n omics_reproducibility_limits -f environment.yml`
* Activate conda environment: `conda activate omics_reproducibility_limits`
* Start notebooks: `jupyter notebook`
