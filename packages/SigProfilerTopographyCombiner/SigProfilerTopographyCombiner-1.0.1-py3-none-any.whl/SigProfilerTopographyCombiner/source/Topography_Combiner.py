# !/usr/bin/env python3

# Author: burcakotlu

# Contact: burcakotlu@eng.ucsd.edu

from Combined_Common import SBS_6
from Combined_Common import SBS_24
from Combined_Common import SBS_96
from Combined_Common import SBS_192
from Combined_Common import SBS_288
from Combined_Common import SBS_384
from Combined_Common import SBS_1536
from Combined_Common import SBS_6144

from Combined_Heatmaps_For_DNA_Elements import main as epigenomics_heatmap_main

from Combined_Strand_Bias_Figures import main as strand_bias_main
from Combined_Strand_Bias_Figures import MUTOGRAPHS_RCC_954

from Combined_Occupancy_ReplicationTime_Processivity import main as occupancy_replication_timing_processivity_main
from Combined_Occupancy_ReplicationTime_Processivity import NUCLEOSOME
from Combined_Occupancy_ReplicationTime_Processivity import CTCF
from Combined_Occupancy_ReplicationTime_Processivity import ATAC_SEQ
from Combined_Occupancy_ReplicationTime_Processivity import H3K4me1
from Combined_Occupancy_ReplicationTime_Processivity import H3K4me2
from Combined_Occupancy_ReplicationTime_Processivity import H3K4me3
from Combined_Occupancy_ReplicationTime_Processivity import H3K9ac
from Combined_Occupancy_ReplicationTime_Processivity import H3K9me3
from Combined_Occupancy_ReplicationTime_Processivity import H3K27ac
from Combined_Occupancy_ReplicationTime_Processivity import H3K27me3
from Combined_Occupancy_ReplicationTime_Processivity import H3K36me3
from Combined_Occupancy_ReplicationTime_Processivity import H3K79me2
from Combined_Occupancy_ReplicationTime_Processivity import H4K20me1
from Combined_Occupancy_ReplicationTime_Processivity import H2AFZ
from Combined_Occupancy_ReplicationTime_Processivity import NUCLEOSOME_OCCUPANCY
from Combined_Occupancy_ReplicationTime_Processivity import EPIGENOMICS_OCCUPANCY
from Combined_Occupancy_ReplicationTime_Processivity import AT_LEAST_1K_CONSRAINTS
from Combined_Occupancy_ReplicationTime_Processivity import MANUSCRIPT
from Combined_Occupancy_ReplicationTime_Processivity import COSMIC

import os

if __name__ == '__main__':

    # For Epigenomics Heatmaps --> Please note that the path for the hms, CTCFs, ATAC-seq files are important.
    # For Strand Bias --> Please note that discreet mode or probability mode can be seen in the upper plot.
    occupancy_combiner = False
    extra_plot_occupancy_combiner = False # optional
    replication_timing_combiner = False
    processivity_combiner = False
    strand_bias_combiner = True
    epigenomics_heatmap_combiner = False
    using_multiprocessing = True # Set True for faster runs, set False for debugging/testing purposes.
    discreet_mode = False # Set True for strand bias combiner for upper panel of the circle bar plot in discreet mode

    #  Mutographs RCC 954 Samples
    # Individual SigProfilerTopography runs directory (becomes input for this python code)
    topography_runs_output_dir = os.path.join('/restricted/alexandrov-group/burcak/SigProfilerTopographyRuns/Mutographs_RCC_954/topography_prob_mode_v2')

    # Combined output directory
    topography_combined_output_dir = os.path.join('/oasis/tscc/scratch/burcak/SigProfilerTopographyRuns/Mutographs_RCC_954/combined_prob_mode_v2/')

    cancer_types = [
        # 'all_954_samples',
        'alcohol_never_423_samples',
        'alcohol_current_drinker_321_samples',
        'alcohol_ex-drinker_60_samples',
        'alcohol_ever_drinker_134_samples',
        'alcohol_drinker_515_samples',
        'alcohol_missing_16_samples',
        'tobacco_never_484_samples',
        'tobacco_current_smoker_238_samples',
        'tobacco_ex-smoker_225_samples',
        'tobacco_ever_smoker_5_samples',
        'tobacco_smoker_468_samples',
        'tobacco_missing_2_samples',
        'sex_male_573_samples',
        'sex_female_381_samples',
        # 'grade_1_32_samples',
        # 'grade_2_436_samples',
        # 'grade_3_388_samples',
        # 'grade_3-4_1_samples',
        # 'grade_4_51_samples',
        # 'grade_cannot_be_assessed_25_samples',
        # 'grade_grade_disagreement_5_samples',
        # 'grade_not_applicable_7_samples',
        # 'grade_1-2_9_samples',
        'stage_i_389_samples',
        'stage_ii_100_samples',
        'stage_iii_248_samples',
        'stage_iv_119_samples',
        'stage_missing_98_samples',
        'country_romania_64_samples',
        'country_czech_republic_259_samples',
        'country_serbia_69_samples',
        'country_brazil_96_samples',
        'country_canada_73_samples',
        'country_japan_28_samples',
        'country_lithuania_16_samples',
        'country_poland_13_samples',
        'country_russia_216_samples',
        'country_thailand_5_samples',
        'country_united_kingdom_115_samples'
    ]

    sbs_signatures = [ 'SBS1536A', 'SBS1536B', 'SBS1536C', 'SBS1536D', 'SBS1536E', 'SBS1536F', 'SBS1536G', 'SBS1536H',
                       'SBS1536I', 'SBS1536J', 'SBS1536K', 'SBS1536L', 'SBS1536M' ]

    dbs_signatures = None

    id_signatures = None

    dna_elements = [(NUCLEOSOME, NUCLEOSOME_OCCUPANCY),
                    (CTCF, EPIGENOMICS_OCCUPANCY),
                    (ATAC_SEQ, EPIGENOMICS_OCCUPANCY),
                    (H3K4me1, EPIGENOMICS_OCCUPANCY),
                    # (H3K4me2, EPIGENOMICS_OCCUPANCY),
                    (H3K4me3, EPIGENOMICS_OCCUPANCY),
                    (H3K9ac, EPIGENOMICS_OCCUPANCY),
                    (H3K27ac, EPIGENOMICS_OCCUPANCY),
                    (H3K36me3, EPIGENOMICS_OCCUPANCY),
                    # (H3K79me2, EPIGENOMICS_OCCUPANCY),
                    # (H4K20me1, EPIGENOMICS_OCCUPANCY),
                    # (H2AFZ, EPIGENOMICS_OCCUPANCY),
                    (H3K9me3, EPIGENOMICS_OCCUPANCY),
                    (H3K27me3, EPIGENOMICS_OCCUPANCY)]


    # Strand Bias Combiner
    if strand_bias_combiner:
        # Mutographs RCC 954 samples
        matrix_generator_output_dir = os.path.join('/restricted/alexandrov-group/burcak/SigProfilerTopographyRuns')
        # sbs384_matrix_file = os.path.join(matrix_generator_output_dir, source, cancer_type, 'output', 'SBS', cancer_type + '.SBS384.all')

        # 1st version
        # SBS_probabilities_file_path = os.path.join('/restricted', 'alexandrov-group', 'burcak', 'SigProfilerTopographyRuns', 'Mutographs_RCC_954', 'probability_files', 'RCC_954_Samples_SBS1536_S13_Probabilities.txt')

        # 2nd version
        SBS_probabilities_file_path = os.path.join('/restricted', 'alexandrov-group', 'burcak',
                                                   'SigProfilerTopographyRuns', 'Mutographs_RCC_954',
                                                   'probability_files', 'RCC_v2_SBS1536_S13_SigProfilerAssignment_COSMIC_fit',
                                                   'Decomposed_Mutation_Probabilities.txt')

        SBS_probabilities_file_mutation_context = SBS_1536
        topography_combined_strand_bias_output_dir = os.path.join(topography_combined_output_dir, 'strand_bias')

        cancer_type2source_cancer_type_tuples_dict = {
            'alcohol_never_423_samples' : [(MUTOGRAPHS_RCC_954, 'alcohol_never_423_samples')],
            'alcohol_current_drinker_321_samples' : [(MUTOGRAPHS_RCC_954, 'alcohol_current_drinker_321_samples')],
            'alcohol_ex-drinker_60_samples' : [(MUTOGRAPHS_RCC_954, 'alcohol_ex-drinker_60_samples')],
            'alcohol_ever_drinker_134_samples' : [(MUTOGRAPHS_RCC_954, 'alcohol_ever_drinker_134_samples')],
            'alcohol_drinker_515_samples' : [(MUTOGRAPHS_RCC_954, 'alcohol_drinker_515_samples')],
            'alcohol_missing_16_samples' : [(MUTOGRAPHS_RCC_954, 'alcohol_missing_16_samples')],

            'tobacco_never_484_samples' : [(MUTOGRAPHS_RCC_954, 'tobacco_never_484_samples')],
            'tobacco_current_smoker_238_samples' : [(MUTOGRAPHS_RCC_954, 'tobacco_current_smoker_238_samples')],
            'tobacco_ex-smoker_225_samples' : [(MUTOGRAPHS_RCC_954, 'tobacco_ex-smoker_225_samples')],
            'tobacco_ever_smoker_5_samples' : [(MUTOGRAPHS_RCC_954, 'tobacco_ever_smoker_5_samples')],
            'tobacco_smoker_468_samples' : [(MUTOGRAPHS_RCC_954, 'tobacco_smoker_468_samples')],
            'tobacco_missing_2_samples' : [(MUTOGRAPHS_RCC_954, 'tobacco_missing_2_samples')],

            'sex_male_573_samples' : [(MUTOGRAPHS_RCC_954, 'sex_male_573_samples')],
            'sex_female_381_samples' : [(MUTOGRAPHS_RCC_954, 'sex_female_381_samples')],

            'stage_i_389_samples' : [(MUTOGRAPHS_RCC_954, 'stage_i_389_samples')],
            'stage_ii_100_samples' : [(MUTOGRAPHS_RCC_954, 'stage_ii_100_samples')],
            'stage_iii_248_samples' : [(MUTOGRAPHS_RCC_954, 'stage_iii_248_samples')],
            'stage_iv_119_samples' : [(MUTOGRAPHS_RCC_954, 'stage_iv_119_samples')],
            'stage_missing_98_samples' : [(MUTOGRAPHS_RCC_954, 'stage_missing_98_samples')],

            'country_romania_64_samples' : [(MUTOGRAPHS_RCC_954, 'country_romania_64_samples')],
            'country_czech_republic_259_samples' : [(MUTOGRAPHS_RCC_954, 'country_czech_republic_259_samples')],
            'country_serbia_69_samples' : [(MUTOGRAPHS_RCC_954, 'country_serbia_69_samples')],
            'country_brazil_96_samples' : [(MUTOGRAPHS_RCC_954, 'country_brazil_96_samples')],
            'country_canada_73_samples' : [(MUTOGRAPHS_RCC_954, 'country_canada_73_samples')],
            'country_japan_28_samples' : [(MUTOGRAPHS_RCC_954, 'country_japan_28_samples')],
            'country_lithuania_16_samples' : [(MUTOGRAPHS_RCC_954, 'country_lithuania_16_samples')],
            'country_poland_13_samples' : [(MUTOGRAPHS_RCC_954, 'country_poland_13_samples')],
            'country_russia_216_samples' : [(MUTOGRAPHS_RCC_954, 'country_russia_216_samples')],
            'country_thailand_5_samples' : [(MUTOGRAPHS_RCC_954, 'country_thailand_5_samples')],
            'country_united_kingdom_115_samples' : [(MUTOGRAPHS_RCC_954, 'country_united_kingdom_115_samples')]
        }

        strand_bias_main(topography_runs_output_dir,
                         matrix_generator_output_dir,
                         SBS_probabilities_file_path,
                         SBS_probabilities_file_mutation_context,
                         topography_combined_strand_bias_output_dir,
                         cancer_types = cancer_types,
                         sbs_signatures = sbs_signatures,
                         dbs_signatures = dbs_signatures,
                         id_signatures = id_signatures,
                         cancer_type2source_cancer_type_tuples_dict = cancer_type2source_cancer_type_tuples_dict,
                         discreet_mode = discreet_mode,
                         min_required_number_of_mutations_on_strands=200, # 1000 legacy
                         min_required_percentage_of_mutations_on_strands=5,
                         using_multiprocessing = using_multiprocessing)

    # Epigenomics Heatmap Combiner
    if epigenomics_heatmap_combiner:
        MUTOGRAPHS_RCC_954_BIOSAMPLES = ['kidney', 'HEK293', 'kidney-epithelial-cell', 'ureter',
                                         'epithelial-cell-of-proximal-tubule']

        # Each cancer type (in fact subgroup of samples of same cancer type) uses same list of biosamples
        cancer_type2biosamples_dict = {
            'alcohol_never_423_samples' : MUTOGRAPHS_RCC_954_BIOSAMPLES,
            'alcohol_current_drinker_321_samples' : MUTOGRAPHS_RCC_954_BIOSAMPLES,
            'alcohol_ex-drinker_60_samples' : MUTOGRAPHS_RCC_954_BIOSAMPLES,
            'alcohol_ever_drinker_134_samples' : MUTOGRAPHS_RCC_954_BIOSAMPLES,
            'alcohol_drinker_515_samples' : MUTOGRAPHS_RCC_954_BIOSAMPLES,
            'alcohol_missing_16_samples' : MUTOGRAPHS_RCC_954_BIOSAMPLES,
            'tobacco_never_484_samples' : MUTOGRAPHS_RCC_954_BIOSAMPLES,
            'tobacco_current_smoker_238_samples' : MUTOGRAPHS_RCC_954_BIOSAMPLES,
            'tobacco_ex-smoker_225_samples' : MUTOGRAPHS_RCC_954_BIOSAMPLES,
            'tobacco_ever_smoker_5_samples' : MUTOGRAPHS_RCC_954_BIOSAMPLES,
            'tobacco_smoker_468_samples' : MUTOGRAPHS_RCC_954_BIOSAMPLES,
            'tobacco_missing_2_samples' : MUTOGRAPHS_RCC_954_BIOSAMPLES,
            'sex_male_573_samples' : MUTOGRAPHS_RCC_954_BIOSAMPLES,
            'sex_female_381_samples' : MUTOGRAPHS_RCC_954_BIOSAMPLES,
            'stage_i_389_samples' : MUTOGRAPHS_RCC_954_BIOSAMPLES,
            'stage_ii_100_samples' : MUTOGRAPHS_RCC_954_BIOSAMPLES,
            'stage_iii_248_samples' : MUTOGRAPHS_RCC_954_BIOSAMPLES,
            'stage_iv_119_samples' : MUTOGRAPHS_RCC_954_BIOSAMPLES,
            'stage_missing_98_samples' : MUTOGRAPHS_RCC_954_BIOSAMPLES,
            'country_romania_64_samples' : MUTOGRAPHS_RCC_954_BIOSAMPLES,
            'country_czech_republic_259_samples' : MUTOGRAPHS_RCC_954_BIOSAMPLES,
            'country_serbia_69_samples' : MUTOGRAPHS_RCC_954_BIOSAMPLES,
            'country_brazil_96_samples' : MUTOGRAPHS_RCC_954_BIOSAMPLES,
            'country_canada_73_samples' : MUTOGRAPHS_RCC_954_BIOSAMPLES,
            'country_japan_28_samples' : MUTOGRAPHS_RCC_954_BIOSAMPLES,
            'country_lithuania_16_samples' : MUTOGRAPHS_RCC_954_BIOSAMPLES,
            'country_poland_13_samples' : MUTOGRAPHS_RCC_954_BIOSAMPLES,
            'country_russia_216_samples' : MUTOGRAPHS_RCC_954_BIOSAMPLES,
            'country_thailand_5_samples' : MUTOGRAPHS_RCC_954_BIOSAMPLES,
            'country_united_kingdom_115_samples' : MUTOGRAPHS_RCC_954_BIOSAMPLES
        }

        # Provide your library files path for epigenomics heatmaps
        hm_path = os.path.join('/restricted', 'alexandrov-group', 'burcak', 'data', 'ENCODE', 'GRCh38', 'HM')
        ctcf_path = os.path.join('/restricted', 'alexandrov-group', 'burcak', 'data', 'ENCODE', 'GRCh38', 'CTCF')
        atac_path = os.path.join('/restricted', 'alexandrov-group', 'burcak', 'data', 'ENCODE', 'GRCh38', 'ATAC-seq')

        epigenomics_heatmap_main(topography_runs_output_dir,
             topography_combined_output_dir,
             hm_path = hm_path,
             ctcf_path = ctcf_path,
             atac_path = atac_path,
             cancer_types = cancer_types,
             sbs_signatures = sbs_signatures,
             dbs_signatures = dbs_signatures,
             id_signatures = id_signatures,
             cancer_type2biosamples_dict = cancer_type2biosamples_dict,
             step1_data_ready = False,
             window_size = 100,
             combine_p_values_method = 'fisher',
             depleted_fold_change = 0.95,
             enriched_fold_change = 1.05,
             significance_level = 0.05,
             consider_both_real_and_sim_avg_overlap = True,
             minimum_number_of_overlaps_required_for_sbs = 100,
             minimum_number_of_overlaps_required_for_dbs = 100,
             minimum_number_of_overlaps_required_for_indels = 100,
             signature_cancer_type_number_of_mutations = AT_LEAST_1K_CONSRAINTS,
             signature_cancer_type_number_of_mutations_for_ctcf = AT_LEAST_1K_CONSRAINTS,
             sort_cancer_types = True,
             remove_columns_rows_with_no_significant_result = True,
             heatmap_rows_signatures_columns_dna_elements = True,
             colorbar = 'seismic',
             figure_types = [MANUSCRIPT, COSMIC],
             cosmic_release_version = 'v3.2',
             figure_file_extension = 'jpg',
             using_multiprocessing = using_multiprocessing)


    # Occupancy -- Replication Timing -- Strand-coordinate Mutagenesis
    if occupancy_combiner or replication_timing_combiner or processivity_combiner:
        occupancy_replication_timing_processivity_main(topography_runs_output_dir,
                                                  topography_combined_output_dir,
                                                  cancer_types = cancer_types,
                                                  sbs_signatures = sbs_signatures,
                                                  dbs_signatures = dbs_signatures,
                                                  id_signatures = id_signatures,
                                                  dna_elements = dna_elements,
                                                  occupancy = occupancy_combiner,
                                                  plot_occupancy = extra_plot_occupancy_combiner,
                                                  replication_time = replication_timing_combiner,
                                                  processivity = processivity_combiner,
                                                  figure_types = [MANUSCRIPT, COSMIC],
                                                  number_of_mutations_required_list_for_others = [AT_LEAST_1K_CONSRAINTS],
                                                  number_of_mutations_required_list_for_ctcf = [AT_LEAST_1K_CONSRAINTS],
                                                  consider_both_real_and_sim_avg_overlap = True,
                                                  minimum_number_of_overlaps_required_for_sbs = 100,
                                                  minimum_number_of_overlaps_required_for_dbs = 100,
                                                  minimum_number_of_overlaps_required_for_indels = 100,
                                                  number_of_simulations = 100,
                                                  depleted_fold_change = 0.95,
                                                  enriched_fold_change = 1.05,
                                                  occupancy_significance_level = 0.05,
                                                  replication_time_significance_level = 0.05,
                                                  replication_time_slope_cutoff = 0.020,
                                                  replication_time_difference_between_min_and_max = 0.2,
                                                  replication_time_difference_between_medians = 0.135,
                                                  processivity_significance_level = 0.05,
                                                  minimum_required_processive_group_length = 2, # 4 legacy
                                                  minimum_required_number_of_processive_groups = 2,
                                                  pearson_spearman_correlation_cutoff = 0.5,
                                                  cosmic_release_version = 'v3.2',
                                                  figure_file_extension = 'jpg',
                                                  using_multiprocessing = using_multiprocessing)

