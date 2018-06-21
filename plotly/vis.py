"""
:module: vis
:platform: Unix, Windows
:synopsis: This code is used as a visualization library for the Met Mast data so it is specifically designed to handle MetDat object from the "met_funcs.py" library. 
:moduleauthor: Nicholas Hamilton <Nicholas.Hamilton@nrel.gov> Rafael Mudafort <Rafael.Mudafort@nrel.gov> Lucas McCullum <Lucas.McCullum@nrel.gov>   
"""

###########################################
# Visualization
###########################################

import utils
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np
from colour import Color
from windrose import WindroseAxes
import pandas as pd

plt.rc('font', family='serif')
plt.rc('font', size=12)
plt.rc('facecolor')

def cumulative_profile(metdat, catinfo, category=None):

    """**Get Variable Profile**.

    Plot the vertical profile of a given variable (or category of variables) grouped by a given condition (or set of conditions).
    
    Parameters:
        1. metdat (Pandas DataFrame): The desired input data (Met Mast).
        2. catinfo (dictionary): Categorization information for the desired input data. Holds column names, labels, units, and save names.
        3. category (string): Specifies the category of information that is desired for plotting.

    Returns:
        1. fig (Matplotlib Figure): The figure object for the desired input data and categories.
        2. ax (Matplotlib Axes): The axes object for the desired input data and categories.
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

def monthly_profile(metdat, catinfo, category=None, basecolor='cycle'):
    """**Get Monthly Profile**.

    Plot the monthly profile of a given variable (or category of variables) grouped by a given condition (or set of conditions).
    
    Parameters:
        1. metdat (Pandas DataFrame): The desired input data (Met Mast).
        2. catinfo (dictionary): Categorization information for the desired input data. Holds column names, labels, units, and save names.
        3. category (string) [default: None]: Specifies the category of information that is desired for plotting.
        4. basecolor (string) [default: 'cycle']: Provides the color code information to get from "utils.py".

    Returns:
        1. fig (Matplotlib Figure): The figure object for the desired input data and categories.
        2. ax (Matplotlib Axes): The axes object for the desired input data and categories.
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

def stability_profile(metdat, catinfo, category=None, vertloc=80, basecolor='cycle'):
    """**Get Stability Profile**.

    Plot the stability profile of a given variable (or category of variables) grouped by a given condition (or set of conditions).
    
    Parameters:
        1. metdat (Pandas DataFrame): The desired input data (Met Mast).
        2. catinfo (dictionary): Categorization information for the desired input data. Holds column names, labels, units, and save names.
        3. category (string) [default: None]: Specifies the category of information that is desired for plotting.
        4. vertloc (integer, float) [default: 80]: Describes the desired vertical location alond the tower for analysis.
        5. basecolor (string) [default: 'cycle]: Provides the color code information to get from "utils.py".

    Returns:
        1. fig (Matplotlib Figure): The figure object for the desired input data and categories.
        2. ax (Matplotlib Axes): The axes object for the desired input data and categories.
    """

    if category is None:
        print('not sure what to plot...')
        pass

    stab, stabloc, ind = utils.get_vertical_locations(catinfo['columns']['stability flag'], location=vertloc)
    colors = utils.get_colors(5,basecolor=basecolor)
    stabconds = utils.get_stabconds()
    
    plotdat = metdat.groupby(stab).mean()
    pdat = plotdat[catinfo['columns'][category]].get_values()
    
    # Extract vertical locations of data from variable names
    _, vertlocs, ind = utils.get_vertical_locations(catinfo['columns'][category]) 
    
    fig, ax = plt.subplots(figsize=(3.5,5))
    for ii, cond in enumerate(stabconds):

        ax.plot(pdat[ii,ind], vertlocs, color=colors[ii])

    ax.set_ylabel('Probe Height [m]')
    ax.set_xlabel(catinfo['labels'][category])
    fig.legend(stabconds, loc=6, bbox_to_anchor=(1,0.5), frameon=False)

    fig.tight_layout()
    
    return fig, ax

def monthly_stability_profiles(metdat, catinfo, category=None, vertloc=80, basecolor='span'):
    """**Get Monthly Stability Profile**.

    Plot the monthly stability profile of a given variable (or category of variables) grouped by a given condition (or set of conditions).
    
    Parameters:
        1. metdat (Pandas DataFrame): The desired input data (Met Mast).
        2. catinfo (dictionary): Categorization information for the desired input data. Holds column names, labels, units, and save names.
        3. category (string) [default: None]: Specifies the category of information that is desired for plotting.
        4. vertloc (integer, float) [default: 80]: Describes the desired vertical location alond the tower for analysis.
        5. basecolor (string) [default: 'span']: Provides the color code information to get from "utils.py".

    Returns:
        1. fig (Matplotlib Figure): The figure object for the desired input data and categories.
        2. ax (Matplotlib Axes): The axes object for the desired input data and categories.
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

def hourlyplot(metdat, catinfo, category=None, basecolor='span'):
    """**Get Hourly Averaged Profile**.

    Plot the hourly averaged profile of a given variable (or category of variables) grouped by a given condition (or set of conditions).
    
    Parameters:
        1. metdat (Pandas DataFrame): The desired input data (Met Mast).
        2. catinfo (dictionary): Categorization information for the desired input data. Holds column names, labels, units, and save names.
        3. category (string): Specifies the category of information that is desired for plotting.
        4. basecolor (string): Provides the color code information to get from "utils.py".

    Returns:
        1. fig (Matplotlib Figure): The figure object for the desired input data and categories.
        2. ax (Matplotlib Axes): The axes object for the desired input data and categories.
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

def monthlyhourlyplot(metdat, catinfo, category=None, basecolor='span'):
    """**Get Monthly Hourly Averaged Profile**.

    Plot the monthly hourly averaged profile of a given variable (or category of variables) grouped by a given condition (or set of conditions).
    
    Parameters:
        1. metdat (Pandas DataFrame): The desired input data (Met Mast).
        2. catinfo (dictionary): Categorization information for the desired input data. Holds column names, labels, units, and save names.
        3. category (string) [default: None]: Specifies the category of information that is desired for plotting.
        4. basecolor (string) [default: 'span']: Provides the color code information to get from "utils.py".

    Returns:
        1. fig (Matplotlib Figure): The figure object for the desired input data and categories.
        2. ax (Matplotlib Axes): The axes object for the desired input data and categories.
    """

    if category is None:
        print('not sure what to plot...')
        pass

    months = utils.monthnames()
    colors = utils.get_colors(len(catinfo['columns'][category]), basecolor=basecolor, reverse=True)
    colnames, vertlocs, ind = utils.get_vertical_locations(catinfo['columns'][category], reverse=True)
    
    plotdat = metdat[colnames].groupby([metdat.index.month.rename('month'), metdat.index.hour.rename('hour')]).mean()
    
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

def rose_fig(metdat, catinfo, category=None, vertloc=80, bins=6, nsector=36, ylim=None, noleg=False):
    """**Get Wind Rose Figure**.

    Plot the wind rose of a given variable (or category of variables) grouped by a given condition (or set of conditions).
    
    Parameters:
        1. metdat (Pandas DataFrame): The desired input data (Met Mast).
        2. catinfo (dictionary): Categorization information for the desired input data. Holds column names, labels, units, and save names.
        3. category (string) [default: None]: Specifies the category of information that is desired for plotting.
        4. vertloc (integer, float) [default: 80]: Describes the desired vertical location alond the tower for analysis.        
        5. bins (integer, list) [default: 6]: Indicates the number of equally spaced bins to divide the variable.
        6. nsector (integer) [default: 36]: Indicated the number of sector directions to divide the rose figure.
        7. ylim (float) [default: None]: Provides the maximum value for the frequency of observations and is used to plot different roses with uniform limits.
        8. noleg (Boolean) [default: False]: Determines whether or not there will be a legend to the figure.

    Returns:
        1. fig (Matplotlib Figure): The figure object for the desired input data and categories.
        2. ax (Matplotlib Axes): The axes object for the desired input data and categories.
        3. leg (Matplotlib Legend): The legend object for the desired input data and categories. 
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

def monthly_rose_fig(metdat, catinfo, category=None, vertloc=80, bins=6, nsector=36, ylim=None, noleg=False):
    """**Get Monthly Wind Rose Figure**.

    Plot the monthly wind rose of a given variable (or category of variables) grouped by a given condition (or set of conditions).
    
    Parameters:
        1. metdat (Pandas DataFrame): The desired input data (Met Mast).
        2. catinfo (dictionary): Categorization information for the desired input data. Holds column names, labels, units, and save names.
        3. category (string) [default: None]: Specifies the category of information that is desired for plotting.
        4. vertloc (integer, float) [default: 80]: Describes the desired vertical location alond the tower for analysis.        
        5. bins (integer, list) [default: 6]: Indicates the number of equally spaced bins to divide the variable.
        6. nsector (integer) [default: 36]: Indicated the number of sector directions to divide the rose figure.
        7. ylim (float) [default: None]: Provides the maximum value for the frequency of observations and is used to plot different roses with uniform limits.
        8. noleg (Boolean) [default: False]: Determines whether or not there will be a legend to the figure.

    Returns:
        1. fig (Matplotlib Figure): The figure object for the desired input data and categories.
        2. ax (Matplotlib Axes): The axes object for the desired input data and categories.
        3. leg (Matplotlib Legend): The legend object for the desired input data and categories. 
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

def winddir_scatter(metdat, catinfo, category, vertloc=80, basecolor='red', exclude_angles=[(46, 228)]):
    """**Get Wind Direction Scatter Figure**.

    Plot the wind direction scatter of a given variable (or category of variables) grouped by a given condition (or set of conditions).
    
    Parameters:
        1. metdat (Pandas DataFrame): The desired input data (Met Mast).
        2. catinfo (dictionary): Categorization information for the desired input data. Holds column names, labels, units, and save names.
        3. category (string): Specifies the category of information that is desired for plotting.
        4. vertloc (integer, float): Describes the desired vertical location alond the tower for analysis.        
        5. basecolor (string): Provides the color code information to get from "utils.py".
        6. exclude_angles (tuple, list): Defines the start and stop angles to shade out regions according to International Electrotechnical Commission (IEC) standards.

    Returns:
        1. fig (Matplotlib Figure): The figure object for the desired input data and categories.
        2. ax (Matplotlib Axes): The axes object for the desired input data and categories.
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

def stability_winddir_scatter(metdat, catinfo, category, vertloc=80, basecolor='red', exclude_angles=[(46, 228)]):
    """**Get Wind Direction Stability Scatter Figure**.

    Plot the wind direction stability scatter of a given variable (or category of variables) grouped by a given condition (or set of conditions).
    
    Parameters:
        1. metdat (Pandas DataFrame): The desired input data (Met Mast).
        2. catinfo (dictionary): Categorization information for the desired input data. Holds column names, labels, units, and save names.
        3. category (string): Specifies the category of information that is desired for plotting.
        4. vertloc (integer, float) [default: 80]: Describes the desired vertical location alond the tower for analysis.        
        5. basecolor (string) [default: 'red']: Provides the color code information to get from "utils.py".
        6. exclude_angles (tuple, list) [default: [(46, 228)]]: Defines the start and stop angles to shade out regions according to International Electrotechnical Commission (IEC) standards.

    Returns:
        1. fig (Matplotlib Figure): The figure object for the desired input data and categories.
        2. ax (Matplotlib Axes): The axes object for the desired input data and categories.
    """
    
    stabconds = utils.get_stabconds()
    colors = utils.get_colors(len(stabconds),basecolor='span')
    nrelcolors = utils.get_nrelcolors()

     # Set up data
    dircol, _, _= utils.get_vertical_locations(catinfo['columns']['direction'], location=vertloc)
    varcol, vertloc, _= utils.get_vertical_locations(catinfo['columns'][category], location=vertloc)
    stabcol, _, _= utils.get_vertical_locations(catinfo['columns']['stability flag'], location=vertloc)

    # dirind = utils.get_nearest_direction(metdat[category])
    
    fig, ax = plt.subplots(len(stabconds),1, sharex=True, sharey=True, figsize=(6,8))

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

def groupby_scatter(metdat, catinfo, category, abscissa='direction', groupby='ti', nbins=5, vertloc=80, basecolor='span'):
    """**Get Wind Direction Grouped Scatter Figure**.

    Plot the wind direction grouped scatter of a given variable (or category of variables) grouped by a given condition (or set of conditions).
    
    Parameters:
        1. metdat (Pandas DataFrame): The desired input data (Met Mast).
        2. catinfo (dictionary): Categorization information for the desired input data. Holds column names, labels, units, and save names.
        3. category (string): Specifies the category of information that is desired for plotting.
        4. abscissa (string) [default: 'direction']: independent variable to plot again
        5. groupby (string) [default: 'ti']: Describes which categories to group by.
        6. nbins (integer) [default: 5]: Divides the *groupby* variable into bins.
        7. vertloc (integer, float) [default: 80]: Describes the desired vertical location alond the tower for analysis.        
        8. basecolor (string) [default: 'span']: Provides the color code information to get from "utils.py".

    Returns:
        1. fig (Matplotlib Figure): The figure object for the desired input data and categories.
        2. ax (Matplotlib Axes): The axes object for the desired input data and categories.
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

def hist(metdat, catinfo, category, vertloc=80, basecolor='blue'):
    """**Get Histogram Figure**.

    Plot the histogram of a given variable (or category of variables) grouped by a given condition (or set of conditions).
    
    Parameters:
        1. metdat (Pandas DataFrame): The desired input data (Met Mast).
        2. catinfo (dictionary): Categorization information for the desired input data. Holds column names, labels, units, and save names.
        3. category (string): Specifies the category of information that is desired for plotting.
        4. vertloc (integer, float) [default: 80]: Describes the desired vertical location alond the tower for analysis.        
        5. basecolor (string) [default: 'blue']: Provides the color code information to get from "utils.py".

    Returns:
        1. fig (Matplotlib Figure): The figure object for the desired input data and categories.
        2. ax (Matplotlib Axes): The axes object for the desired input data and categories.
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

def monthly_hist(metdat, catinfo, category, vertloc=80, basecolor='blue'):
    """**Get Monthly Histogram Figure**.

    Plot the monthly histogram of a given variable (or category of variables) grouped by a given condition (or set of conditions).
    
    Parameters:
        1. metdat (Pandas DataFrame): The desired input data (Met Mast).
        2. catinfo (dictionary): Categorization information for the desired input data. Holds column names, labels, units, and save names.
        3. category (string): Specifies the category of information that is desired for plotting.
        4. vertloc (integer, float) [default: 80]: Describes the desired vertical location alond the tower for analysis.        
        5. basecolor (string) [default: 'blue']: Provides the color code information to get from "utils.py".

    Returns:
        1. fig (Matplotlib Figure): The figure object for the desired input data and categories.
        2. ax (Matplotlib Axes): The axes object for the desired input data and categories.
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

def hist_by_stability(metdat, catinfo, category, vertloc=80, basecolor='span'):
    """**Get Stability Grouped Histogram Figure**.

    Plot the stability grouped histogram of a given variable (or category of variables) grouped by a given condition (or set of conditions).
    
    Parameters:
        1. metdat (Pandas DataFrame): The desired input data (Met Mast).
        2. catinfo (dictionary): Categorization information for the desired input data. Holds column names, labels, units, and save names.
        3. category (string): Specifies the category of information that is desired for plotting.
        4. vertloc (integer, float) [default: 80]: Describes the desired vertical location alond the tower for analysis.        
        5. basecolor (string) [default: 'span']: Provides the color code information to get from "utils.py".

    Returns:
        1. fig (Matplotlib Figure): The figure object for the desired input data and categories.
        2. ax (Matplotlib Axes): The axes object for the desired input data and categories.
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

def stacked_hist_by_stability(metdat, catinfo, category, vertloc=80):
    """**Get Stacked Stability Grouped Histogram Figure**.

    Plot the stacked stability grouped histogram of a given variable (or category of variables) grouped by a given condition (or set of conditions).
    
    Parameters:
        1. metdat (Pandas DataFrame): The desired input data (Met Mast).
        2. catinfo (dictionary): Categorization information for the desired input data. Holds column names, labels, units, and save names.
        3. category (string): Specifies the category of information that is desired for plotting.
        4. vertloc (integer, float): Describes the desired vertical location alond the tower for analysis.        

    Returns:
        1. fig (Matplotlib Figure): The figure object for the desired input data and categories.
        2. ax (Matplotlib Axes): The axes object for the desired input data and categories.
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

def monthly_stacked_hist_by_stability(metdat, catinfo, category, vertloc=80):
    """**Get Monthly Stacked Stability Grouped Histogram Figure**.

    Plot the monthly stacked stability grouped histogram of a given variable (or category of variables) grouped by a given condition (or set of conditions).
    
    Parameters:
        1. metdat (Pandas DataFrame): The desired input data (Met Mast).
        2. catinfo (dictionary): Categorization information for the desired input data. Holds column names, labels, units, and save names.
        3. category (string): Specifies the category of information that is desired for plotting.
        4. vertloc (integer, float) [default: 80]: Describes the desired vertical location alond the tower for analysis.        

    Returns:
        1. fig (Matplotlib Figure): The figure object for the desired input data and categories.
        2. ax (Matplotlib Axes): The axes object for the desired input data and categories.
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

def normalized_hist_by_stability(metdat, catinfo, vertloc=80):
    """**Get Normalized Stability Grouped Histogram Figure**.

    Plot the normalized stability grouped histogram of a given variable (or category of variables) grouped by a given condition (or set of conditions).
    
    Parameters:
        1. metdat (Pandas DataFrame): The desired input data (Met Mast).
        2. catinfo (dictionary): Categorization information for the desired input data. Holds column names, labels, units, and save names.
        3. vertloc (integer, float) [default: 80]: Describes the desired vertical location alond the tower for analysis.        

    Returns:
        1. fig (Matplotlib Figure): The figure object for the desired input data and categories.
        2. ax (Matplotlib Axes): The axes object for the desired input data and categories.
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
        # Use this for missing data, also works for full data
        a = garb.loc[cond]
        b = a.index.tolist()
        c = a.values.tolist()
        for i in range(len(hours)):
            if (hours[i]) in b:
                pass
            else:
                b.insert(i,hours[i])
                c.insert(i,0)

        d = pd.Series(data = c, index = b)
        ax.bar(hours, d, color=colors[jj], bottom=newbottom)
        newbottom += c  #<-- for if missing data, also works for full data 

        #ax.bar(hours, garb.loc[cond], color=colors[jj], bottom=newbottom)
        #newbottom += garb.loc[cond]

    ax.set_ylabel('Probability [%]')
    ax.set_xlabel('Time of Day [Hour]')
    fig.legend(stabconds)   
    #fig.legend(stabconds, loc=6, bbox_to_anchor=(1,0.5),framealpha=0)
    fig.tight_layout()

    return fig, ax

def normalized_monthly_hist_by_stability(metdat, catinfo, vertloc=80):
    """**Get Normalized Monthly Stability Grouped Histogram Figure**.

    Plot the normalized monthly stability grouped histogram of a given variable (or category of variables) grouped by a given condition (or set of conditions).
    
    Parameters:
        1. metdat (Pandas DataFrame): The desired input data (Met Mast).
        2. catinfo (dictionary): Categorization information for the desired input data. Holds column names, labels, units, and save names.
        3. vertloc (integer, float) [default: 80]: Describes the desired vertical location alond the tower for analysis.        

    Returns:
        1. fig (Matplotlib Figure): The figure object for the desired input data and categories.
        2. ax (Matplotlib Axes): The axes object for the desired input data and categories.
    """

    months = utils.monthnames()
    hours = np.arange(24)
    stabcol, _, _= utils.get_vertical_locations(catinfo['columns']['stability flag'], location=vertloc)
    stabconds = utils.get_stabconds()
    colors = utils.get_colors(5,basecolor='span')

    temp = metdat[stabcol].dropna()
    plotdata = temp.groupby([temp.index.month.rename('month'), temp.index.hour.rename('hour')]).value_counts(normalize=True)
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
# End of Code
###########################################