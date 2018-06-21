###########################################
# visualization
###########################################
"""
Met mast visualization library
Designed to work with MetDat objects from the met_funcs library
"""
import utils
import matplotlib.cm as cm
import matplotlib.pyplot as plt
from colour import Color
from windrose import WindroseAxes
import numpy as np
import pandas as pd

plt.rc('font', family='serif')
plt.rc('font', size=12)
plt.rc('facecolor')

###########################################
def cumulative_profile(metdat, catinfo, category=None):
###########################################
    """
    Plot vertical profile of a given variable (or category of variables) grouped by a given condition (or set of conditions)
    Parameters:
        metdat:
            Pandas dataframe containing met mast data
        catinfo:
            dict containing categorization info for the metmast data. Fore each category, 
            catinfo holds column names, labels, units, and save names
        category:
            string specifying category of information to plot (e.g. 'speed', 'stability', etc.)
        basecolor:
            string with the color code info to get from utils.
    """
    
    if category is None:
        print('not sure what to plot...')
        pass
    
    # extract vertical locations of data from variable names
    colnames, vertlocs, ind = utils.get_vertical_locations(catinfo['columns'][category]) 
 
    plotdat = metdat[colnames].mean()

    fig, ax = plt.subplots(figsize=(3.5,5))
    ax.plot(plotdat, vertlocs)

    ax.set_ylabel('Probe Height [m]')
    ax.set_xlabel(catinfo['labels'][category])
    fig.tight_layout()
        
    return fig, ax
###########################################

###########################################
def monthly_profile(metdat, catinfo, category=None, basecolor='cycle'):
###########################################
    """
    Plot monthly average profiles against one another.
    Parameters:
        metdat:
            Pandas dataframe containing met mast data
        catinfo:
            dict containing categorization info for the metmast data. Fore each category, 
            catinfo holds column names, labels, units, and save names
        category:
            string specifying category of information to plot (e.g. 'speed', 'stability', etc.)
        basecolor:
            string with the color code info to get from utils.
    """

    if category is None:
        print('not sure what to plot...')
        pass

    months = utils.monthnames()
    colors = utils.get_colors(len(months), basecolor=basecolor)
    colnames, vertlocs, ind = utils.get_vertical_locations(catinfo['columns'][category])
    
    plotdat = metdat[colnames].groupby(metdat.index.month).mean()

    fig, ax = plt.subplots(figsize=(3.5,5), sharex=True, sharey=True)
    for iax in range(len(months)):
        ax.plot(plotdat.xs(iax+1), vertlocs, color=colors[iax])

    leg = ax.legend(months, loc=7, bbox_to_anchor=(1.75, 0.5), edgecolor='w')
    ax.set_ylabel('Probe Height [m]')
    ax.set_xlabel(catinfo['labels'][category])

    fig.tight_layout()
    
    return fig, ax
###########################################

###########################################
def stability_profile(metdat, catinfo, category=None, vertloc=80, basecolor='cycle'):
###########################################
    """
    Plot cumulative average profiles sorted by stability.
    Parameters:
        metdat:
            Pandas dataframe containing met mast data
        catinfo:
            dict containing categorization info for the metmast data. Fore each category, 
            catinfo holds column names, labels, units, and save names
        category:
            string specifying category of information to plot (e.g. 'speed', 'stability', etc.)
        vertloc:
            int or float describing the exact or approximate height of interest along the tower
        basecolor:
            string with the color code info to get from utils.
    """
    if category is None:
        print('not sure what to plot...')
        pass

    stab, stabloc, ind = utils.get_vertical_locations(catinfo['columns']['stability flag'], location=vertloc)
    colors = utils.get_colors(5,basecolor=basecolor)
    stabconds = utils.get_stabconds()
    
    plotdat = metdat.groupby(stab).mean()
    pdat = plotdat[catinfo['columns'][category]].get_values()
    
    # extract vertical locations of data from variable names
    _, vertlocs, ind = utils.get_vertical_locations(catinfo['columns'][category]) 
    
    fig, ax = plt.subplots(figsize=(3.5,5))
    for ii, cond in enumerate(stabconds):

        ax.plot(pdat[ii,ind], vertlocs, color=colors[ii])

    ax.set_ylabel('Probe Height [m]')
    ax.set_xlabel(catinfo['labels'][category])
    fig.legend(stabconds, loc=6, bbox_to_anchor=(1,0.5), frameon=False)

    fig.tight_layout()
    
    return fig, ax
###########################################


###########################################
def monthly_stability_profiles(metdat, catinfo, category=None, vertloc=80, basecolor='span'):
###########################################
    """
    Plot monthly average profiles against one another.
    Parameters:
        metdat:
            Pandas dataframe containing met mast data
        catinfo:
            dict containing categorization info for the metmast data. Fore each category, 
            catinfo holds column names, labels, units, and save names
        category:
            string specifying category of information to plot (e.g. 'speed', 'stability', etc.)
        vertloc:
            int or float describing the exact or approximate height of interest along the tower
        basecolor:
            string with the color code info to get from utils.
    """
    if category is None:
        print('not sure what to plot...')
        pass

    stab, stabloc, ind = utils.get_vertical_locations(catinfo['columns']['stability flag'], location=vertloc)

    plotdat = metdat.groupby([metdat.index.month, stab])
    colors = utils.get_colors(5,basecolor='span')
    months = utils.monthnames()
    stabconds = utils.get_stabconds()

    # extract vertical locations of data from variable names
    _, vertlocs, ind = utils.get_vertical_locations(catinfo['columns'][category]) 

    fig, ax = plt.subplots(4,3, figsize=(8,13), sharex=True, sharey=True)
    for iax, month in enumerate(months):
        
        for ii, cond in enumerate(stabconds):

            pdat = plotdat[catinfo['columns'][category]].get_group((iax+1, cond)).mean()
            ax.flatten()[iax].plot(pdat[ind], vertlocs, color=colors[ii])

        ax.flatten()[iax].set_title(month)

    fig.text(0,0.58, 'Probe Height [m]', ha='center', va='center', fontsize=14, rotation='vertical')
    leg = fig.legend(stabconds, loc=9, bbox_to_anchor=(0.55, 0.12), frameon=False)

    fig.tight_layout()
    fig.subplots_adjust(bottom=0.175)
    fig.text(0.525,0.135, catinfo['labels'][category], ha='center', va='center', fontsize=14)

    return fig, ax
###########################################


###########################################
def hourlyplot(metdat, catinfo, category=None, basecolor='span'):
###########################################
    """
    Plot monthly average profiles against one another.
     Parameters:
        metdat:
            Pandas dataframe containing met mast data
        catinfo:
            dict containing categorization info for the metmast data. Fore each category, 
            catinfo holds column names, labels, units, and save names
        category:
            string specifying category of information to plot (e.g. 'speed', 'stability', etc.)
        basecolor:
            string with the color code info to get from utils.
    """
    if category is None:
        print('not sure what to plot...')
        pass

    colors = utils.get_colors(len(catinfo['columns'][category]), basecolor=basecolor, reverse=True)
    colnames, vertlocs, ind = utils.get_vertical_locations(catinfo['columns'][category], reverse=True)
    
    plotdat = metdat[colnames].groupby(metdat.index.hour).mean()
    
    fig, ax = plt.subplots(figsize=(5,3.5), sharex=True, sharey=True)
    for iax in range(len(colnames)):
        ax.plot(plotdat[colnames[iax]], color=colors[iax])

    leg = ax.legend([str(v) + ' m' for v in vertlocs], loc=6, bbox_to_anchor=(1, 0.5), frameon=False)
    ax.set_xlabel('Time [hour]')
    ax.set_ylabel(catinfo['labels'][category])

    fig.tight_layout()
    
    return fig, ax
###########################################


###########################################
def monthlyhourlyplot(metdat, catinfo, category=None, basecolor='span'):
###########################################
    """
    Plot monthly average profiles against one another.
    Parameters:
        metdat:
            Pandas dataframe containing met mast data
        catinfo:
            dict containing categorization info for the metmast data. Fore each category, 
            catinfo holds column names, labels, units, and save names
        category:
            string specifying category of information to plot (e.g. 'speed', 'stability', etc.)
        basecolor:
            string with the color code info to get from utils.
    """
    if category is None:
        print('not sure what to plot...')
        pass

    months = utils.monthnames()
    colors = utils.get_colors(len(catinfo['columns'][category]), basecolor=basecolor, reverse=True)
    colnames, vertlocs, ind = utils.get_vertical_locations(catinfo['columns'][category], reverse=True)
    
    plotdat = metdat[colnames].groupby([metdat.index.month, metdat.index.hour]).mean()
    
    fig, ax = plt.subplots(4,3, figsize=(9,11), sharex=True, sharey=True)
    for iax in range(len(months)):
        for catitem in range(len(colnames)):
            ax.flatten()[iax].plot(plotdat[colnames[catitem]].xs(iax+1), color=colors[catitem])
        ax.flatten()[iax].set_title(months[iax], fontsize=12)
    
    
    fig.text(0.5,0.2, 'Time of Day [hour]', ha='center', va='center')
    leg = fig.legend([str(v) + ' m' for v in vertlocs], loc = 'upper center', bbox_to_anchor = (0,-0.825,1,1), bbox_transform = plt.gcf().transFigure, frameon=False, ncol=2)
    fig.tight_layout()
    fig.subplots_adjust(bottom=0.25)
    fig.text(0,0.6125, catinfo['labels'][category], ha='center', va='center', rotation='vertical')

    return fig, ax
###########################################

###########################################
def rose_fig(metdat, catinfo, category=None, vertloc=80, bins=6, nsector=36, ylim=None, noleg=False):
###########################################
    """
    make wind rose from pandas.Series wind direction and some other value of the same size.
    Parameters:
        metdat:
            Pandas dataframe containing met mast data
        catinfo:
            dict containing categorization info for the metmast data. Fore each category, 
            catinfo holds column names, labels, units, and save names
        category:
            string specifying category of information to plot (e.g. 'speed', 'stability', etc.)
        vertloc:
            int or float describing the exact or approximate height of interest along the tower
        bins:
            int specifying number of equally spaced bins to divide var.
            OR
            list of bin division limits (eg [0,4,8,12,16])
        nsector:
            number or direction sectors to divide rose
        ylim:
            optional float with maximum value for frequency of observations, use to 
            plot different roses with uniform limits
        noleg: 
            bool switch to turn legend off
    """

    # set up data
    dircol, _, _= utils.get_vertical_locations(catinfo['columns']['direction'], location=vertloc)
    varcol, vertloc, _= utils.get_vertical_locations(catinfo['columns'][category], location=vertloc)
    winddir = metdat[dircol]
    var = metdat[varcol]

    # get var divisions set up
    if isinstance(bins, int):
        nbins = bins
    else:
        nbins = len(bins)

    # set up plotting colors
    colors = utils.get_colors(nbins-1, basecolor='span')
    colors += ['#3A4246'] # add something dark to the end.
    colors = tuple(colors[0:nbins])
    
    # built figure
    fig = plt.figure()
    ax = WindroseAxes.from_ax(fig=fig)
    ax.bar(winddir, var, normed=True, opening=0.95, edgecolor='white', bins=bins, nsector=nsector,colors=colors, linewidth=0.35)

    # legend
    leg=['blank']
    if noleg is not True:
        leg = ax.set_legend(loc=7,bbox_to_anchor=(1.55,0.5), fontsize=10, frameon=False)
        # add labels to legend
        leg.set_title(catinfo['labels'][category])
        fig.text(0.875, 0.275, r'$z={}$ m'.format(vertloc))

    # adjust plot for specified max frequency
    if ylim is None:
        ylim = ax.get_ylim()[-1]

    # frequency axis limits and labels
    ax.set_ylim(0,ylim)
    ax.set_yticks(np.linspace(0,ylim,4))
    ax.set_yticklabels([str(round(x,1)) for x in np.linspace(0,ylim,4)])

         
    return fig, ax, leg
###########################################

###########################################
def monthly_rose_fig(metdat, catinfo, category=None, vertloc=80, bins=6, nsector=36, ylim=None, noleg=False):
###########################################
    """
    make wind rose from pandas.Series wind direction and some other value of the same size.
    Parameters:
        metdat:
            Pandas dataframe containing met mast data
        catinfo:
            dict containing categorization info for the metmast data. Fore each category, 
            catinfo holds column names, labels, units, and save names
        category:
            string specifying category of information to plot (e.g. 'speed', 'stability', etc.)
        vertloc:
            int or float describing the exact or approximate height of interest along the tower
        bins:
            int specifying number of equally spaced bins to divide var.
            OR
            list of bin division limits (eg [0,4,8,12,16])
        nsector:
            number or direction sectors to divide rose
        ylim:
            optional float with maximum value for frequency of observations, use to 
            plot different roses with uniform limits
        noleg: 
            bool switch to turn legend off
    """
    
    # set up data
    dircol, _, _= utils.get_vertical_locations(catinfo['columns']['direction'], location=vertloc)
    varcol, vertloc, _= utils.get_vertical_locations(catinfo['columns'][category], location=vertloc)
    plotdat = metdat.groupby(metdat.index.month)
    winddir = plotdat[dircol]
    var = plotdat[varcol]

    months = utils.monthnames()
    # wind speed bins to use in wind roses
    # get var divisions set up
    if isinstance(bins, int):
        nbins = bins
    else:
        nbins = len(bins)

    # set up plotting colors
    colors = utils.get_colors(nbins-1, basecolor='span')
    colors += ['#3A4246'] # add something dark to the end.
    colors = tuple(colors[0:nbins])

    fig = plt.figure(figsize=(9,13))

    for iax,month in enumerate(months):

        ax = fig.add_subplot(4,3,iax+1, projection="windrose")

        ax.bar(winddir.get_group(iax+1), var.get_group(iax+1),
               bins=bins, nsector=36, colors=colors,
                linewidth=0.35,
              normed=True)

        # Set the tick labels font
        for label in (ax.get_xticklabels() + ax.get_yticklabels()):
            label.set_fontname('Arial')
            label.set_fontsize(12)
        ax.set_title(month,fontsize=12,y=1.15)

        if iax == 10:
            leg = plt.legend(loc=8, ncol=2, bbox_to_anchor = (0.5,-0.65), frameon=False)
            leg.set_title(catinfo['labels'][category])
            fig.text(0.5, -0.085, r'$z={}$ m'.format(vertloc), ha='center', va='center')

    axes = fig.get_children()[1:]
    # adjust plot for specified max frequency
    if ylim is None:
        ylim = 0.0
        for iax,month in enumerate(months):
            ylim = np.max([ylim, axes[iax].get_ylim()[-1]])
    
    for iax,month in enumerate(months):
        axes[iax].set_ylim(0,ylim)
        axes[iax].set_yticks(np.linspace(0.0,ylim,4))
        # print(axes[iax].get_yticks())
        axes[iax].set_yticklabels([str(np.round(x,decimals=1)) for x in axes[iax].get_yticks()])

    fig.tight_layout() 

    return fig, axes, leg
###########################################

###########################################
def winddir_scatter(metdat, catinfo, category, vertloc=80, basecolor='red', exclude_angles=[(46, 228)]):
###########################################
    """
    make scatter plot from pandas.Series wind direction and some other value of the same size. Includes blocked off angles from IEC standards.
        Plot monthly average profiles against one another.
    Parameters:
        metdat:
            Pandas dataframe containing met mast data
        catinfo:
            dict containing categorization info for the metmast data. Fore each category, 
            catinfo holds column names, labels, units, and save names
        category:
            string specifying category of information to plot (e.g. 'speed', 'stability', etc.)
        vertloc:
            int or float describing the exact or approximate height of interest along the tower
        basecolor:
            string with the color code info to get from utils.
        exclude_angles:
            tuple or list of tuples of start and stop angles to shade out regions according to IEC standards
    """

     # set up data
    dircol, _, _= utils.get_vertical_locations(catinfo['columns']['direction'], location=vertloc)
    varcol, vertloc, _= utils.get_vertical_locations(catinfo['columns'][category], location=vertloc)

    colors = utils.get_nrelcolors()
    
    fig = plt.figure(figsize=(8,2.5))
    ax  = fig.add_subplot(111)

    ax.scatter(metdat[dircol], metdat[varcol], marker='o',facecolor='w',color='k',lw=0.5,alpha=0.7)
    ax.set_xlim([0,360])

    for ii in range(len(exclude_angles)):
        ax.axvspan(exclude_angles[ii][0], exclude_angles[ii][1], alpha=0.1, color=colors[basecolor][0])
    ax.set_title(r'$z={}$ m'.format(vertloc))
    ax.set_xlabel(r'Wind Direction [$^\circ$]')
    ax.set_ylabel(catinfo['labels'][category])
    
    return fig, ax#, leg
###########################################

###########################################
def stability_winddir_scatter(metdat, catinfo, category, vertloc=80, basecolor='red', exclude_angles=[(46, 228)]):
###########################################
    """
    make scatter plot from pandas.Series wind direction and some other value of the same size. Includes blocked off angles from IEC standards.
    Subplots correspond to stability conditions from Obukhov length
    Parameters:
        metdat:
            Pandas dataframe containing met mast data
        catinfo:
            dict containing categorization info for the metmast data. Fore each category, 
            catinfo holds column names, labels, units, and save names
        category:
            string specifying category of information to plot (e.g. 'speed', 'stability', etc.)
        vertloc:
            int or float describing the exact or approximate height of interest along the tower
        basecolor:
            string with the color code info to get from utils.
        exclude_angles:
            tuple or list of tuples of start and stop angles to shade out regions according to IEC standards
    """
    
    stabconds = utils.get_stabconds()
    colors = utils.get_colors(5,basecolor='span')
    nrelcolors = utils.get_nrelcolors()

     # set up data
    dircol, _, _= utils.get_vertical_locations(catinfo['columns']['direction'], location=vertloc)
    varcol, vertloc, _= utils.get_vertical_locations(catinfo['columns'][category], location=vertloc)
    stabcol, _, _= utils.get_vertical_locations(catinfo['columns']['stability flag'], location=vertloc)

    # dirind = utils.get_nearest_direction(metdat[category])
    
    fig, ax = plt.subplots(5,1, sharex=True, sharey=True, figsize=(6,8))

    plotdat = metdat.groupby(stabcol)

    for ind, stabcond in enumerate(stabconds):

        ax.flatten()[ind].scatter(plotdat[dircol].get_group(stabcond),plotdat[varcol].get_group(stabcond),
        marker='o',facecolor=colors[ind],color='k',lw=0.5,alpha=0.7)

        ax.flatten()[ind].set_xlim([0,360])
        # ax.flatten()[ind].set_ylim([0,120])
        ax.flatten()[ind].legend([stabcond], fontsize=12, loc=1, frameon=False)

        for ii in range(len(exclude_angles)):
             ax.flatten()[ind].axvspan(exclude_angles[ii][0], exclude_angles[ii][1], alpha=0.1, color=nrelcolors[basecolor][0])

        if ind == 0:
             ax.flatten()[ind].set_title(r'$z={}$ m'.format(vertloc))
    
    
    fig.tight_layout()
    fig.text(0.5,0, r'Wind Direction [$^\circ$]', ha='center', va='center')
    fig.text(0, 0.5, catinfo['labels'][category], ha='center', va='center', rotation='vertical')
    return fig, ax #, leg
###########################################


###########################################
def groupby_scatter(metdat, catinfo, category, abscissa='direction', groupby='ti', nbins=5, vertloc=80, basecolor='span'):
###########################################
    """
    make scatter plot from pandas.Series wind direction and some other value of the same size. Includes blocked off angles from IEC standards.
    Parameters:
        metdat:
            Pandas dataframe containing met mast data
        catinfo:
            dict containing categorization info for the metmast data. Fore each category, 
            catinfo holds column names, labels, units, and save names
        category:
            string specifying category of information to plot (e.g. 'speed', 'stability', etc.)
        abscissa:
            independet variable category to plot agains
        groupby:
            string describing column or category to use for groupby
        nbins: 
            used to cut groupyby values into bins
        vertloc:
            int or float describing the exact or approximate height of interest along the tower
        basecolor:
            string with the color code info to get from utils.
    """
    # set up data
    varcol, vertloc, _= utils.get_vertical_locations(catinfo['columns'][category], location=vertloc)
    groupcol, _, _= utils.get_vertical_locations(catinfo['columns'][groupby], location=vertloc)
    abscol, _, _= utils.get_vertical_locations(catinfo['columns'][abscissa], location=vertloc)

    temp = pd.cut(metdat[groupcol],5)
    plotdat = metdat[[varcol,abscol,groupcol]].groupby(temp)
    
    groups = list(plotdat.indices.keys())

    colors = utils.get_colors(len(groups), basecolor=basecolor)
    
    fig, ax = plt.subplots(figsize=(5,3), sharex=True, sharey=True)

    for iax,group in enumerate(groups):
        ax.scatter(plotdat[abscol].get_group(group), plotdat[varcol].get_group(group),facecolor=colors[iax],color='k',lw=0.5,alpha=0.7)
    leg = ax.legend(groups, loc=6, bbox_to_anchor=(1, 0.5), frameon=False)
    leg.set_title(catinfo['labels'][groupby])
    # labels
    ax.set_xlabel(catinfo['labels'][abscissa])
    ax.set_ylabel(catinfo['labels'][category])  
    ax.set_title(r'$z={}$ m'.format(vertloc))

    fig.tight_layout()
    
    return fig, ax #, leg
###########################################

###########################################
def hist(metdat, catinfo, category, vertloc=80, basecolor='blue'):
###########################################
    """
    Histogram of a given field without any sorting.
    Parameters:
        metdat:
            Pandas dataframe containing met mast data
        catinfo:
            dict containing categorization info for the metmast data. Fore each category, 
            catinfo holds column names, labels, units, and save names
        category:
            string specifying category of information to plot (e.g. 'speed', 'stability', etc.)
        vertloc:
            int or float describing the exact or approximate height of interest along the tower
        basecolor:
            string with the color code info to get from utils.
    """
    colors = utils.get_nrelcolors()
    color = colors[basecolor][0]

    # set up data
    varcol, vertloc, _= utils.get_vertical_locations(catinfo['columns'][category], location=vertloc)

    data = metdat[varcol].dropna(how='any')

    fig, ax = plt.subplots(figsize=(5,3))
    ax.hist(data, 
            bins = 35, 
            facecolor=color, 
            edgecolor='k',
            weights=np.ones(len(data)) / len(data), density=False)
    ax.set_title(r'$z={}$ m'.format(vertloc))
    fig.text(0,0.5,'Frequency [%]',rotation='vertical', ha='center', va='center')
    fig.text(0.5,0,catinfo['labels'][category], ha='center', va='center')
    fig.tight_layout()
    
    return fig, ax
###########################################   

###########################################
def monthly_hist(metdat, catinfo, category, vertloc=80, basecolor='blue'):
###########################################
    """
    Histogram of a given field without any sorting.
    Parameters:
        metdat:
            Pandas dataframe containing met mast data
        catinfo:
            dict containing categorization info for the metmast data. Fore each category, 
            catinfo holds column names, labels, units, and save names
        category:
            string specifying category of information to plot (e.g. 'speed', 'stability', etc.)
        vertloc:
            int or float describing the exact or approximate height of interest along the tower
        basecolor:
            string with the color code info to get from utils.
    """
    
    colors = utils.get_nrelcolors()
    color = colors[basecolor][0]
    months = utils.monthnames()
    
    # set up data
    varcol, vertloc, _= utils.get_vertical_locations(catinfo['columns'][category], location=vertloc)

    temp = metdat.groupby(metdat.index.month)
    temp = temp[varcol]

    binwidth = (metdat[varcol].dropna().max() - metdat[varcol].dropna().min())/35
    bins = np.arange(metdat[varcol].dropna().min(),metdat[varcol].dropna().max(), binwidth)

    fig, ax = plt.subplots(4,3, figsize=(9,9), sharex=True, sharey=True)
    
    for im,month in enumerate(months):
        data = temp.get_group(im+1).dropna()
        ax.flatten()[im].hist(data, 
                              bins=bins, 
                              color=color, 
                              edgecolor='k',
                              weights=np.ones(len(data))/len(data)*100)
        ax.flatten()[im].set_title(month, fontsize=12)
        
    fig.tight_layout()
    fig.text(0,0.5,'Frequency [%]',rotation='vertical', ha='center', va='center')
    fig.text(0.5,0,catinfo['labels'][category], ha='center', va='center')
        
    return fig, ax
###########################################   

###########################################
def hist_by_stability(metdat, catinfo, category, vertloc=80, basecolor='span'):
###########################################
    """
    make histograms separating the variable (colname) by stability class.
    stability is the list of column names containing stability flags
    Parameters:
        metdat:
            Pandas dataframe containing met mast data
        catinfo:
            dict containing categorization info for the metmast data. Fore each category, 
            catinfo holds column names, labels, units, and save names
        category:
            string specifying category of information to plot (e.g. 'speed', 'stability', etc.)
        vertloc:
            int or float describing the exact or approximate height of interest along the tower
        basecolor:
            string with the color code info to get from utils.
    """
    stabconds = utils.get_stabconds()
    stabcol, _, _= utils.get_vertical_locations(catinfo['columns']['stability flag'], location=vertloc)
    varcol, vertloc, _= utils.get_vertical_locations(catinfo['columns'][category], location=vertloc)
    colors = utils.get_colors(len(stabconds),basecolor=basecolor)

    metdat = metdat.groupby(stabcol)
    
    fig,ax = plt.subplots(len(stabconds),1, figsize=(4,6), sharex=True, sharey=True)
    for ii,stab in enumerate(stabconds):
        data = metdat[varcol].get_group(stab).dropna()
        ax.flatten()[ii].hist(data,
                              facecolor=colors[ii], 
                              edgecolor='k',
                              bins=50,
                              weights=np.ones(len(data)) / len(data), 
                              density=False)
        ax.flatten()[ii].legend([stab], fontsize=10, frameon=False)
    
    ax.flatten()[0].set_title(r'$z={}$m'.format(vertloc))

    fig.text(-0.03,0.5,'Frequency [%]',rotation='vertical', ha='center', va='center')
    fig.text(0.5,0,catinfo['labels'][category], ha='center', va='center')

    fig.tight_layout()
    
    return fig, ax
###########################################

###########################################
def stacked_hist_by_stability(metdat, catinfo, category, vertloc=80):
###########################################
    """
    make a stacked histogram of data separated by stability class.
    Parameters:
        metdat:
            Pandas dataframe containing met mast data
        catinfo:
            dict containing categorization info for the metmast data. Fore each category, 
            catinfo holds column names, labels, units, and save names
        category:
            string specifying category of information to plot (e.g. 'speed', 'stability', etc.)
        vertloc:
            int or float describing the exact or approximate height of interest along the tower
    """
    stabconds = utils.get_stabconds()
    stabcol, _, _= utils.get_vertical_locations(catinfo['columns']['stability flag'], location=vertloc)
    varcol, vertloc, _= utils.get_vertical_locations(catinfo['columns'][category], location=vertloc)
    colors = utils.get_colors(len(stabconds), basecolor='span')

    plotdat = metdat.groupby(stabcol)

    fig, ax = plt.subplots()
    temp = pd.DataFrame({cond: plotdat[varcol].get_group(cond) for cond in stabconds})
    temp.plot.hist(ax=ax,
                   stacked=True,
                   color=colors,
                   bins=35,
                   edgecolor='k',
                   legend=False,
                #    weights = np.ones(temp.shape) / len(temp.index), 
                   density=True)
    
    ax.set_xlabel(catinfo['labels'][category])
    ax.set_title(r'$z={}$m'.format(vertloc))
    fig.legend(stabconds, loc=6, bbox_to_anchor=(1, 0.5), frameon=False)
    
    fig.tight_layout()
    
    return fig, ax
###########################################


###########################################
def monthly_stacked_hist_by_stability(metdat, catinfo, category, vertloc=80):
###########################################
    """
    make histograms of data separated by month and stability class.
    Parameters:
        metdat:
            Pandas dataframe containing met mast data
        catinfo:
            dict containing categorization info for the metmast data. Fore each category, 
            catinfo holds column names, labels, units, and save names
        category:
            string specifying category of information to plot (e.g. 'speed', 'stability', etc.)
        vertloc:
            int or float describing the exact or approximate height of interest along the tower
    """
    stabconds = utils.get_stabconds()
    stabcol, _, _= utils.get_vertical_locations(catinfo['columns']['stability flag'], location=vertloc)
    varcol, vertloc, _= utils.get_vertical_locations(catinfo['columns'][category], location=vertloc)
    colors = utils.get_colors(len(stabconds), basecolor='span')
    months = utils.monthnames()
    
    plotdat = metdat.groupby([metdat.index.month, stabcol])
    plotdat = plotdat[varcol]

    fig, ax = plt.subplots(4,3, figsize=(9,10), sharex=True, sharey=True)

    for iax, month in enumerate(months):
        temp = pd.DataFrame({cond: plotdat.get_group((iax+1,cond)) for cond in stabconds})
        temp.plot.hist(ax=ax.flatten()[iax],
                       stacked=True,
                       color=colors,
                       bins=35,
                       edgecolor='k',
                       legend=False,
                    #    weights = np.ones(temp.dropna().shape) / np.prod(temp.shape), 
                              density=True)
        ax.flatten()[iax].set_title(month)
        ax.flatten()[iax].set_ylabel('') 
        
    # fig.legend(stabconds, loc=8, bbox_to_anchor=(0, -0.1), edgecolor='w')
    fig.text(0,0.58, 'Frequency', ha='center', va='center', fontsize=14, rotation='vertical')
    leg = fig.legend(stabconds, loc=9,  bbox_to_anchor=(0.55, 0.15), frameon=False)
    fig.tight_layout()
    fig.subplots_adjust(bottom=0.21)
    fig.text(0.5, 0.16, catinfo['labels'][category], ha='center', va='center', fontsize=14)

    return fig, ax#, leg

###########################################

###########################################
def normalized_hist_by_stability(metdat, catinfo, vertloc=80):
###########################################
    """
    make a normlizec histogram of data separated by stability class.
    Parameters:
        metdat:
            Pandas dataframe containing met mast data
        catinfo:
            dict containing categorization info for the metmast data. Fore each category, 
            catinfo holds column names, labels, units, and save names
        vertloc:
            int or float describing the exact or approximate height of interest along the tower
    """
    stabconds = utils.get_stabconds()
    stabcol, _, _= utils.get_vertical_locations(catinfo['columns']['stability flag'], location=vertloc)
    colors = utils.get_colors(len(stabconds), basecolor='span')

    temp = metdat[stabcol].dropna()
    garb = temp.groupby(temp.index.hour).value_counts(normalize=True)
    garb.index.names = ['hour','stabclass']
    garb = garb.reorder_levels(['stabclass','hour'])

    hours = np.arange(24)
    newbottom = np.zeros(24)

    fig,ax = plt.subplots()
    for jj,cond in enumerate(stabconds):
        
        ax.bar(hours, garb.loc[cond], color=colors[jj], bottom=newbottom)
        newbottom += garb.loc[cond]

    ax.set_ylabel('Probability [%]')
    ax.set_xlabel('Time of Day [Hour]')
    fig.legend(stabconds, loc=6, bbox_to_anchor=(1,0.5),framealpha=0)
    fig.tight_layout()

    return fig, ax
###########################################

###########################################
def normalized_monthly_hist_by_stability(metdat, catinfo, vertloc=80):
###########################################
    """
    make a normlizec histogram of data separated by stability class.
    Parameters:
        metdat:
            Pandas dataframe containing met mast data
        catinfo:
            dict containing categorization info for the metmast data. Fore each category, 
            catinfo holds column names, labels, units, and save names
        vertloc:
            int or float describing the exact or approximate height of interest along the tower
    """

    months = utils.monthnames()
    hours = np.arange(24)
    stabcol, _, _= utils.get_vertical_locations(catinfo['columns']['stability flag'], location=vertloc)
    stabconds = utils.get_stabconds()
    colors = utils.get_colors(5,basecolor='span')

    temp = metdat[stabcol].dropna()
    plotdata = temp.groupby([temp.index.month, temp.index.hour]).value_counts(normalize=True)
    plotdata.index.names = ['month','hour','stabclass']
    temp = plotdata.reorder_levels(['month','stabclass','hour'])

    indexvals = [np.arange(1,13),stabconds, np.arange(24)]
    indx = pd.MultiIndex.from_product(indexvals, names=['month','stabclass','hour'])
    temp = temp.reindex(index=indx).fillna(0.0)

    fig,ax = plt.subplots(4,3, figsize=(9,10), sharex=True, sharey=True)
    for ii,month in enumerate(months):
        newbottom = np.zeros(24)

        for jj,cond in enumerate(stabconds):
            
            pdat = temp.loc[ii+1,cond]
            
            ax.flatten()[ii].bar(hours, pdat, color=colors[jj],bottom=newbottom)
            
            newbottom += pdat
            
    # fig.legend(stabconds, loc=8, bbox_to_anchor=(0, -0.1), edgecolor='w')
    fig.text(-0.02,0.58, 'Probability [%]', ha='center', va='center', rotation='vertical')
    leg = fig.legend(stabconds, loc=9, bbox_to_anchor=(0.55, 0.125), frameon=False)
    
    fig.tight_layout()
    fig.subplots_adjust(bottom=0.21)
    fig.text(0.5, 0.165, 'Time of Day [Hour]', ha='center', va='center')

    return fig, ax
###########################################