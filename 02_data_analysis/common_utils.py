import os, re
import numpy as np
import pandas as pd 
from IPython.display import display, HTML

def get_matched_index(x1, x2):
    common_proteins = x1.index[x1.index.isin(x2.index)]
    return x1.reindex(common_proteins), x2.reindex(common_proteins)

def stratify_into_deciles(x, y, complex_subunits=[]):
    x_subset, y_subset = get_matched_index(x, y)
    dataframe = pd.DataFrame('', index=x_subset.index, columns=['maximum', 'deciles'])
    dataframe['maximum'] = pd.qcut(x_subset, 10).apply(lambda x: round(x.right, 2))
    dataframe['deciles'] = pd.qcut(x_subset, 10, labels = False) + 1
    dataframe = dataframe.sort_values(by='deciles')
    dataframe['Decile_Altered'] = dataframe['deciles'].astype(str) +  '\n('+  dataframe['maximum'].astype(str) + ')'
    dataframe = pd.concat([dataframe, x_subset, y_subset], axis=1)
    if(len(complex_subunits) > 0):
        dataframe['ComplexSubunit'] = [True if x in complex_subunits else False for x in dataframe.index] 
        dataframe = dataframe.groupby(by=['Decile_Altered','ComplexSubunit']).mean()       
        dataframe = dataframe.reset_index().sort_values('deciles').drop(columns='deciles')
    return dataframe

def dataframe_from_dict(factors, *dict_args, repeat_factor=1, interchange_factor_data=False):
    dataframe = pd.DataFrame.from_dict(dict_args[0], orient='index')
    for i in range(1, len(dict_args)-1):
        dataframe = dataframe.append(pd.DataFrame.from_dict(dict_args[i], orient='index'))
    dataframe.reset_index(inplace=True)
    dataframe.columns=['Data', 'R-squared']
    protein_count = factors.pop()
    dataframe['Factor'] = np.repeat(factors, repeat_factor)
    if(interchange_factor_data):
        dataframe.rename(columns={'Factor': 'Data', 'Data':'Factor'}, inplace=True)
        dataframe.Factor = dataframe.Factor.str.replace('Reproducibility', 'Protein\nReproducibility')
    #to print the dataframe 
    dataframe = dataframe.pivot(index='Data', columns='Factor', values='R-squared').reset_index()
    dataframe[protein_count] = dataframe['Data'].map(dict_args[-1])
    display( HTML( dataframe.to_html().replace("\\n","<br>") ) )
    #to plot the data along with the protein count used for the analysis 
    dataframe['Data'] = r'$\mathbf{' + dataframe['Data'] + '}$' +'\n' + '(N=' + dataframe[protein_count].astype(int).astype(str) + ')'
    dataframe['Data'].replace('$\mathbf{Transcriptomic Reproducibility}$\n(N=10036)',     
                              '$\mathbf{Transcriptomic}$\n$\mathbf{Reproducibility}$\n$\mathbf{(CCLE-Klijn)}$\n(N=10036)', inplace=True) 
    dataframe.drop(columns=protein_count, inplace=True)    
    dataframe = pd.melt(dataframe, id_vars='Data').rename(columns={'value':'R-squared'})
    dataframe["Factor"] = pd.Categorical(dataframe["Factor"], categories=factors) if(not interchange_factor_data) else \
                          pd.Categorical(dataframe["Factor"], categories=['Ovarian Protein\nReproducibility Rank', 
                                                                          'CCLE Protein\nReproducibility Rank', 
                                                                          'Colon Protein\nReproducibility Rank', 
                                                                          'Aggregated Protein\nReproducibility Rank'])
    dataframe.sort_values(by="Factor", inplace=True)
    return dataframe