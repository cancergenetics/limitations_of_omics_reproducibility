#install.packages("RobustRankAggreg")
library(tidyverse)
library(plyr)
library(dplyr)
library(RobustRankAggreg)

file_proteomic_replicates_cor <- file.path("../local_data/processed/", "proteomic_replicates_correlation.csv")
file_rra = file.path("../local_data/processed/rank_aggregation/", 'RRA.csv')

proteomic_replicates_cor <- read.csv(file_proteomic_replicates_cor, header = TRUE, row.names = 1)
colnames(proteomic_replicates_cor) <- c('Ovarian (JHU-PNNL)', 'Colon (TMT-LF)', 'CCLE (R1-R3)')

ov_replicates_cor = proteomic_replicates_cor %>%
  dplyr::select(`Ovarian (JHU-PNNL)`)%>% 
  drop_na(`Ovarian (JHU-PNNL)`) %>%
  dplyr::arrange(desc(`Ovarian (JHU-PNNL)`)) %>%
  rownames_to_column("Gene Symbol") %>%
  pull("Gene Symbol")

colon_replicates_cor = proteomic_replicates_cor %>%
  dplyr::select(`Colon (TMT-LF)`)%>% 
  drop_na(`Colon (TMT-LF)`) %>%
  dplyr::arrange(desc(`Colon (TMT-LF)`)) %>%
  rownames_to_column("Gene Symbol") %>%
  pull("Gene Symbol")

ccle_replicates_cor = proteomic_replicates_cor %>%
  dplyr::select(`CCLE (R1-R3)`)%>% 
  drop_na(`CCLE (R1-R3)`) %>%
  dplyr::arrange(desc(`CCLE (R1-R3)`)) %>%
  rownames_to_column("Gene Symbol") %>%
  pull("Gene Symbol") 

glist <- list(ov_replicates_cor, 
              colon_replicates_cor, 
              ccle_replicates_cor)
r = rankMatrix(glist, full = TRUE)

aggregate_ranks <- function(r, method, exact=FALSE){
  ranks <- aggregateRanks(rmat = r, method = method, exact) %>%
    select(Score) %>%
    rownames_to_column("Gene Symbol")
  return(ranks)
}
ranks <- join_all(list(aggregate_ranks(r, "RRA"),
                       aggregate_ranks(r, "stuart"),
                       aggregate_ranks(r, "mean"),
                       aggregate_ranks(r, "median"),
                       aggregate_ranks(r, "min"),
                       aggregate_ranks(r, "geom.mean")), 
                  by = "Gene Symbol") %>% 
          column_to_rownames("Gene Symbol")

colnames(ranks) <- c("RRA", "Stuart", "Mean", "Median", "Min", 
                     "Geom_Mean")
write.csv(ranks, file_rra)