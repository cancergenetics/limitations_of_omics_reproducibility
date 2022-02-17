import seaborn as sns
import common_utils as cu
from matplotlib.offsetbox import AnchoredText

def customise_plot(ax, args):
    ax.set_xlabel(args.xlab) 
    ax.set_ylabel(args.ylab)
    ax.xaxis.grid(args.xaxis_grid, linewidth=0.5) if args.xaxis_grid else ax.xaxis.grid(args.xaxis_grid)
    ax.yaxis.grid(args.yaxis_grid, linewidth=0.5) if args.yaxis_grid else ax.yaxis.grid(args.yaxis_grid)
    
def draw_histogram(ax, replicates_cor, args, ymax=0.9):
    sns.histplot(replicates_cor, kde=False, stat='density', ax=ax, edgecolor='white')
    ax.axvline(replicates_cor.median(), color='black', linestyle='--', linewidth=1, ymax=ymax,
               label='Median = {:1.3f}'.format(replicates_cor.median()))
    
    ax.text(replicates_cor.median() - 0.25, ax.get_ylim()[1],
            "Median = " + str(round(replicates_cor.median(), 2)), 
            horizontalalignment='left', size='9', color='black', weight='normal')
    customise_plot(ax, args)
    
def draw_boxplot(ax, x, y, args, stratify=True):
    dataframe = cu.stratify_into_deciles(x, y)    
    sns.boxplot(y=y.name, x='Decile_Altered', data=dataframe, showfliers=False, ax=ax,
               medianprops={'color':'black', 'linewidth':1.25, 'linestyle': '-'},
               whiskerprops={'color': args.palette[0], 'linewidth':1.5, 'linestyle': '--'}, 
               capprops={'linewidth': 0}, boxprops={'facecolor': args.palette[0], 'linewidth': 0})
  
    ax.set_title(args.title, weight='bold', y=1.05, size=11)
    ax.xaxis.labelpad = 10
    medians = dataframe.groupby(['deciles'])[y.name].median().round(2)
    for xtick in ax.get_xticks():        
        ax.text(xtick, medians.iloc[xtick] + 0.025, medians.iloc[xtick], horizontalalignment='center',size='9',color='black')
    count = len(dataframe)
    ax.text(xtick, ax.get_ylim()[1] , 'N = '+ str(count), horizontalalignment='center',size='10', color='black')   
    if(args.r2!=None):
        at = AnchoredText("$\mathregular{R^2}$ = "+ str(round(args.r2, 2))+"%", loc="lower right", frameon=True, 
                               prop=dict(fontsize='10', color='black'))
        at.patch.set_edgecolor('white')
        at.patch.set_facecolor('white')
        at.patch.set_alpha(1)
        
        ax.add_artist(at)
    customise_plot(ax, args)
    
def draw_dotplot(ax, x, y, data, hue, order, args, hue_order=None, jitter=False):
    sns.stripplot(x=x, y=y, data=data, hue=hue, ax=ax, order=order, palette=args.palette, s=7, hue_order=hue_order, jitter=jitter)
    if(args.show_legend):
        ax.legend(title='Feature', title_fontsize='medium', facecolor='white', framealpha=1,
                  bbox_to_anchor = args.anchor_legend_at)._legend_box.align = "left"
    customise_plot(ax, args)
    
def draw_ranged_dotplot(ax, x, y, complex_subunits, args):
    dataframe = cu.stratify_into_deciles(x, y, complex_subunits)   
    sns.scatterplot(x='Decile_Altered', y = y.name, data=dataframe, hue='ComplexSubunit', palette=args.palette[:2], s=60, ax=ax, zorder=4) 
    dataframe = dataframe.pivot(index='Decile_Altered', columns='ComplexSubunit', values=y.name)
    ax.vlines(dataframe.index.values, dataframe[True], dataframe[False], lw=1.5, colors=args.palette[2], zorder=2)    
    if(not args.show_legend): 
        ax.get_legend().remove()
    else: 
        ax.legend(title='Protein Complex\nSubunit?', title_fontsize='medium', framealpha=1, facecolor='white', bbox_to_anchor = (-0.35, 1))._legend_box.align = "left"
    ax.set_title(args.title, weight='bold', y=1.05, size=11)
    ax.xaxis.labelpad = 10
    ax.set(ylim=(0.075, 0.7))
    customise_plot(ax, args)