"""
:module: plotly_vis
:platform: Unix, Windows
:synopsis: This code is used as a Plotly visualization library for the Met Mast data so it is specifically designed to handle MetDat object from the "met_funcs.py" library. 
:moduleauthor: Nicholas Hamilton <Nicholas.Hamilton@nrel.gov> Rafael Mudafort <Rafael.Mudafort@nrel.gov> Lucas McCullum <Lucas.McCullum@nrel.gov>   
"""

###########################################
# Visualization
###########################################

import vis
import utils
import met_funcs
import numpy as np
import pandas as pd
from colour import Color
import plotly
from plotly import tools
import plotly.plotly as py
import plotly.graph_objs as go
import matplotlib.pyplot as plt
from numpy.lib.twodim_base import histogram2d

# Complete
def cumulative_profile(metdat, catinfo, category=None):
    """**Get Variable Profile**.

    Plot the vertical profile of a given variable (or category of variables) grouped by a given condition (or set of conditions).
    
    Parameters:
        1. metdat (Pandas DataFrame): The desired input data (Met Mast).
        2. catinfo (dictionary): Categorization information for the desired input data. Holds column names, labels, units, and save names.
        3. category (string): Specifies the category of information that is desired for plotting.

    Returns:
        1. fig (Plotly Figure): The figure object for the desired input data and categories.
    """
    
    if category is None:
        print('not sure what to plot...')
        pass
    
    # extract vertical locations of data from variable names
    colnames, vertlocs, ind = utils.get_vertical_locations(catinfo['columns'][category]) 
 
    plotdat = metdat[colnames].mean()

    xstring = catinfo['labels'][category]
    ystring = 'Probe Height [m]'

    trace0 = go.Scatter(
        x = plotdat,
        y = vertlocs,
        mode = 'lines+markers',
        name = xstring
    )

    # Edit the layout
    layout = dict(title = "%s vs. %s" % (xstring,ystring),
                xaxis = dict(title = xstring),
                yaxis = dict(title = ystring),
                )

    data = [trace0]
    fig = dict(data=data, layout=layout)

    return fig

# Incomplete
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

    fig = plotly.tools.make_subplots(rows=1, cols=1)
    data = [None]*len(months)

    for iax in range(len(months)):
        # Get trace
        trace = go.Scatter(
            x = plotdat.xs(iax+1), 
            y = vertlocs, 
            mode = 'lines+markers',
            name = months[iax],
            connectgaps = True,
            line = dict(
                color = (colors[iax])
                )
        )
        data[iax] = trace

    # Set the string labels
    xstring = catinfo['labels'][category]
    ystring = 'Probe Height [m]'
    
    # Edit the layout
    layout = dict(
        title = "%s vs. %s" % (xstring,ystring),
        xaxis = dict(
            title = xstring
        ),
        yaxis = dict(
            title = ystring
        )
    )

    fig = dict(data=data, layout=layout)

    return fig

# Complete
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
    
    fig = plotly.tools.make_subplots(rows=1, cols=1)
    data = [None]*len(stabconds)

    for ii,cond in enumerate(stabconds):
        # Get trace
        trace = go.Scatter(
            x = pdat[ii,ind], 
            y = vertlocs, 
            mode = 'lines+markers',
            name = stabconds[ii],
            line = dict(
                color = (colors[ii])
                )
        )
        data[ii] = trace

    # Set the string labels
    xstring = catinfo['labels'][category]
    ystring = 'Probe Height [m]'
    
    # Edit the layout
    layout = dict(title = "%s vs. %s" % (xstring,ystring),
                  xaxis = dict(title = xstring),
                  yaxis = dict(title = ystring)
                  )

    fig = dict(data=data, layout=layout)

    return fig

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

    # Extract vertical locations of data from variable names
    _, vertlocs, ind = utils.get_vertical_locations(catinfo['columns'][category]) 

    # Setup data structures
    fig = plotly.tools.make_subplots(rows=4, cols=3, subplot_titles = utils.monthnames())
    max_x = 0

    for iax, month in enumerate(months):
        for ii,cond in enumerate(stabconds):
            # Get trace
            pdat = plotdat[catinfo['columns'][category]].get_group((iax+1, cond)).mean()
            if iax == 0:
                show_leg = True
            else:
                show_leg = False
            
            if max(pdat[ind]) > max_x:
                max_x = max(pdat[ind])

            trace = go.Scatter(
                x = pdat[ind], 
                y = vertlocs, 
                mode = 'lines+markers',
                name = stabconds[ii],
                connectgaps = True,
                showlegend = show_leg,
                line = dict(
                    color = (colors[ii])
                    )
            )
            fig.append_trace(trace, (iax//3)+1, (iax%3)+1)
        
    # Set the string labels
    xstring = catinfo['labels'][category]
    ystring = 'Probe Height [m]'
    titleS = "%s vs. %s" % (xstring,ystring)
    
    # Edit layout
    for i in range(1,13):
        fig['layout']['xaxis'+str(i)].update(title = xstring, range = [0, max_x+0.1*max_x])
        fig['layout']['yaxis'+str(i)].update(title = ystring, range=[0, max(vertlocs)+0.1*max(vertlocs)])
        
    fig['layout'].update(height=2000, width=1000, title=titleS)

    return fig

# Complete
def hourlyplot(metdat, catinfo, category=None, basecolor='span'):
    """**Get Hourly Averaged Profile**.

    Plot the hourly averaged profile of a given variable (or category of variables) grouped by a given condition (or set of conditions).
    
    Parameters:
        1. metdat (Pandas DataFrame): The desired input data (Met Mast).
        2. catinfo (dictionary): Categorization information for the desired input data. Holds column names, labels, units, and save names.
        3. category (string): Specifies the category of information that is desired for plotting.
        4. basecolor (string): Provides the color code information to get from "utils.py".

    Returns:
        1. fig (Plotly Figure): The figure object for the desired input data and categories.
    """

    if category is None:
        print('not sure what to plot...')
        pass

    colors = utils.get_colors(len(catinfo['columns'][category]), basecolor=basecolor, reverse=True)
    colnames, vertlocs, ind = utils.get_vertical_locations(catinfo['columns'][category], reverse=True)
    
    plotdat = metdat[colnames].groupby(metdat.index.hour).mean()
    data = [None]*len(colnames)
    xstring = 'Time [hour]'
    ystring = catinfo['labels'][category]
  
    fig = plotly.tools.make_subplots(rows=1, cols=1)

    for iax in range(len(colnames)):
        #print(iax)

        trace = go.Scatter(
            x = list(range(len(plotdat[colnames[iax]].values.tolist()))), 
            y = plotdat[colnames[iax]].values.tolist(), 
            mode = 'lines+markers',
            name = str(vertlocs[iax]) + ' m',
            line = dict(
                color = (colors[iax])
                )
        )
        data[iax] = trace
    
    # Edit the layout
    layout = dict(title = "%s vs. %s" % (xstring,ystring),
                  xaxis = dict(title = xstring),
                  yaxis = dict(title = ystring),
                  )

    fig = dict(data=data, layout=layout)

    return fig

# Incomplete
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
    
    # Setup data structures
    fig = plotly.tools.make_subplots(rows=4, cols=3, subplot_titles = utils.monthnames())
    max_y = 0

    for iax in range(len(months)):
        for catitem in range(len(colnames)):
            # Find maximum y-value to get consistent range for plots
            if max(plotdat[colnames[catitem]].xs(iax+1).values.tolist()) > max_y:
                max_y = max(plotdat[colnames[catitem]].xs(iax+1).values.tolist())

            # Only show legend once
            if iax == 0:
                show_leg = True
            else:
                show_leg = False

            # Get trace
            trace = go.Scatter(
                x = list(range(len(plotdat[colnames[catitem]].xs(iax+1).values.tolist()))), 
                y = plotdat[colnames[catitem]].xs(iax+1).values.tolist(), 
                mode = 'lines+markers',
                name = str(vertlocs[catitem]) + 'm',
                connectgaps = True,
                showlegend = show_leg,
                line = dict(
                    color = (colors[catitem])
                    )
            )
            fig.append_trace(trace, (iax//3)+1, (iax%3)+1)

    # Set the string labels
    xstring = 'Time of Day [hour]'
    ystring = catinfo['labels'][category]
    titleS = '%s vs. %s' % (xstring,ystring)

    for i in range(1,13):
        fig['layout']['xaxis'+str(i)].update(title = xstring, range = [0, 24])
        fig['layout']['yaxis'+str(i)].update(title = ystring, range=[0, max_y+0.1*max_y])
    
    fig['layout'].update(height=2000, width=1000, title=titleS)

    return fig

# Incomplete (reverse degree directions/add cardinal directions)
def rose_fig(metdat, catinfo, category=None, vertloc=80, bins=6, nsector=36, ylim=None, noleg=False,normed=True):
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
        9. normed (Boolean) [default: True]: Determines whether or not the values of the Windrose should be in terms of percentages of the total.

    Returns:
        1. fig (Plotly Figure): The figure object for the desired input data and categories.
    """

    # Set up data
    dircol, _, _= utils.get_vertical_locations(catinfo['columns']['direction'], location=vertloc)
    varcol, vertloc, _= utils.get_vertical_locations(catinfo['columns'][category], location=vertloc)
    winddir = metdat[dircol]
    var = metdat[varcol]

    # Get var divisions set up
    if isinstance(bins, int):
        nbins = bins
    else:
        nbins = len(bins)

    # Set up plotting colors
    colors = utils.get_colors(nbins-1, basecolor='span')
    colors += ['#3A4246'] # add something dark to the end.
    colors = tuple(colors[0:nbins])

    data = [None]*bins

    # Start: From Matplotlib windrose GitHub
    angle = 360. / nsector

    dir_bins = np.arange(-angle / 2, 360. + angle, angle, dtype=np.float)
    dir_edges = dir_bins.tolist()
    dir_edges.pop(-1)
    dir_edges[0] = dir_edges.pop(-1)
    dir_bins[0] = 0.

    if isinstance(bins, int):
        bins = np.linspace(np.min(var), np.max(var), bins)
    bins = np.asarray(bins)

    var_bins = bins.tolist()
    var_bins.append(np.inf)

    table = histogram2d(x=var, y=winddir, bins=[var_bins, dir_bins],
                        normed=False)[0]
    # Add the last value to the first to have the table of North winds
    table[:, 0] = table[:, 0] + table[:, -1]
    # Remove the last col
    table = table[:, :-1]
    # Norm the values of the table
    if normed:
        table = table * 100 / table.sum()
    # End: From Matplotlib windrose GitHub

    #Convert radii to Plotly style  
    table_final = []
    list_final = []

    for sect_num in range(nsector):
        list_final.append(0)
        list_final.append(table[0,sect_num])
        list_final.append(table[0,sect_num])
        list_final.append(0)
    
    table_final.append(list_final)

    for bin_ind in range(nbins-1):
        list2_final = []
        test_list = table[bin_ind+1,:].tolist()

        for i in range(nsector):
            list2_final.append(table_final[bin_ind][(i+1)*4-2])
            list2_final.append(table_final[bin_ind][(i+1)*4-2] + test_list[i])
            list2_final.append(table_final[bin_ind][(i+1)*4-2] + test_list[i])
            list2_final.append(table_final[bin_ind][(i+1)*4-2])

        table_final.append(list2_final)

    #Convert directions to Plotly style  
    list_test = dir_bins.tolist()
    dir_final = []

    dir_final.append(list_test[-1])
    dir_final.append(list_test[-1])
    dir_final.append(list_test[1])
    dir_final.append(list_test[1])

    for i in range(1,len(list_test)-1):
        dir_final.append(list_test[i])
        dir_final.append(list_test[i])
        dir_final.append(list_test[i+1])
        dir_final.append(list_test[i+1])

    # Set labels
    name = [None]*nbins
    for j in range(nbins):
        j_ind = range(nbins-1,-1,-1)
        j_ind = j_ind[j]
        name[j] = '[%.2f : %.2f) m/s' % (var_bins[j_ind],var_bins[j_ind+1])


    # Build figure
    for iax in range(len(colors)):
        index = range(len(colors)-1,-1,-1)
        index = index[iax]

        trace = go.Scatterpolar(
            r = table_final[index][:],
            theta = dir_final[::-1],
            mode = 'lines',
            name = name[iax],
            fill = 'toself',
            fillcolor = colors[index],
            line =  dict(
                color = 'black'
            )
        )
        data[iax] = trace

    # Set title
    if normed:
        titleS = "Windrose for %s (normed)" % (category)
    else:
        titleS = "Windrose for %s (not normed)" % (category)
    
    # Set tick suffix
    if normed:
        ticksuffixS = "%"
    else:
        ticksuffixS = "m/s"

    # Set layout
    layout = go.Layout(
        title = titleS,
        font = dict(
        size = 15
        ),
        polar = dict(
            radialaxis = dict(
                ticksuffix = ticksuffixS
            ),
            angularaxis = dict(
                tickfont = dict(
                    size = 16
                ),
                rotation = 90,
                direction = "counterclockwise",
                #categoryarray = ["N", "NW", "W", "SW","S","SE","E","NE"]
            )
        ),
    )
    
    fig = dict(data=data, layout=layout)

    return fig

# Incomplete (maybe think about replacing with Plotly Wind Rose?)
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

    # Setup data structures
    data = []
    #fig = plotly.tools.make_subplots(rows=4, cols=3, subplot_titles = utils.monthnames())
    max_x = 0

    for iax,month in enumerate(months):

        # Start: From Matplotlib windrose GitHub
        angle = 360. / nsector

        dir_bins = np.arange(-angle / 2, 360. + angle, angle, dtype=np.float)
        dir_edges = dir_bins.tolist()
        dir_edges.pop(-1)
        dir_edges[0] = dir_edges.pop(-1)
        dir_bins[0] = 0.

        if isinstance(bins, int):
            bins = np.linspace(np.min(var.get_group(iax+1)), np.max(var.get_group(iax+1)), bins)
        bins = np.asarray(bins)

        var_bins = bins.tolist()
        var_bins.append(np.inf)

        a = var.get_group(iax+1)
        b = winddir.get_group(iax+1)

        table = histogram2d(x=var.get_group(iax+1), y=winddir.get_group(iax+1), bins=[var_bins, dir_bins],
                            normed=False)[0]
        # Add the last value to the first to have the table of North winds
        table[:, 0] = table[:, 0] + table[:, -1]
        # Remove the last col
        table = table[:, :-1]
        table = table * 100 / table.sum()
        # End: From Matplotlib windrose GitHub

        #Convert radii to Plotly style  
        table_final = []
        list_final = []

        for sect_num in range(nsector):
            list_final.append(0)
            list_final.append(table[0,sect_num])
            list_final.append(table[0,sect_num])
            list_final.append(0)
        
        table_final.append(list_final)

        for bin_ind in range(nbins-1):
            list2_final = []
            test_list = table[bin_ind+1,:].tolist()

            for i in range(nsector):
                list2_final.append(table_final[bin_ind][(i+1)*4-2])
                list2_final.append(table_final[bin_ind][(i+1)*4-2] + test_list[i])
                list2_final.append(table_final[bin_ind][(i+1)*4-2] + test_list[i])
                list2_final.append(table_final[bin_ind][(i+1)*4-2])

            table_final.append(list2_final)

        #Convert directions to Plotly style  
        list_test = dir_bins.tolist()
        dir_final = []

        dir_final.append(list_test[-1])
        dir_final.append(list_test[-1])
        dir_final.append(list_test[1])
        dir_final.append(list_test[1])

        for i in range(1,len(list_test)-1):
            dir_final.append(list_test[i])
            dir_final.append(list_test[i])
            dir_final.append(list_test[i+1])
            dir_final.append(list_test[i+1])

        # Set labels
        name = [None]*nbins
        for j in range(nbins):
            j_ind = range(nbins-1,-1,-1)
            j_ind = j_ind[j]
            name[j] = '[%.2f : %.2f) m/s' % (var_bins[j_ind],var_bins[j_ind+1])


        # Build figure
        for ii in range(len(colors)):
            index = range(len(colors)-1,-1,-1)
            index = index[ii]

            if max(table_final[index][:]) > max_x:
                max_x = max(table_final[index][:])
            
            if iax == 0:
                show_leg = True
            else:
                show_leg = False

            if iax == 0:
                trace = go.Scatterpolar(
                    r = table_final[index][:],
                    theta = dir_final[::-1],
                    mode = 'lines',
                    thetaunit = None,
                    name = name[ii],
                    fill = 'toself',
                    fillcolor = colors[index],
                    showlegend = show_leg,
                    subplot = 'polar',
                    line =  dict(
                        color = 'black'
                    )
                )
            else:
                trace = go.Scatterpolar(
                    r = table_final[index][:],
                    theta = dir_final[::-1],
                    mode = 'lines',
                    name = name[ii],
                    fill = 'toself',
                    fillcolor = colors[index],
                    showlegend = show_leg,
                    subplot = 'polar'+str(iax+1),
                    line =  dict(
                        color = 'black'
                    )
                )
            data.append(trace)
            #fig.append_trace(trace, (iax//3)+1, (iax%3)+1)

    # Set the string labels
    xstring = catinfo['labels'][category]
    ystring = 'Probe Height [m]'
    titleS = "%s vs. %s" % (xstring,ystring)

    # Eventually find a way to loop this
    layout = go.Layout(
        title = titleS,
        annotations = [dict(
            showarrow = False,
            x = 0,
            y = 0.98,
            xref = 'paper',
            text = utils.monthnames()[0],
            font = dict(
                size = 16
            )
        ),
        dict(
            showarrow = False,
            x = 0.35,
            y = 0.98,
            text = utils.monthnames()[1],
            font = dict(
                size = 16
            )
        ),
        dict(
            showarrow = False,
            x = 0.75,
            y = 0.98,
            text = utils.monthnames()[2],
            font = dict(
                size = 16
            )
        ),
        dict(
            showarrow = False,
            x = 0,
            y = 0.71,
            text = utils.monthnames()[3],
            font = dict(
                size = 16
            )
        ),
        dict(
            showarrow = False,
            x = 0.35,
            y = 0.71,
            text = utils.monthnames()[4],
            font = dict(
                size = 16
            )
        ),
        dict(
            showarrow = False,
            x = 0.75,
            y = 0.71,
            text = utils.monthnames()[5],
            font = dict(
                size = 16
            )
        ),
        dict(
            showarrow = False,
            x = 0,
            y = 0.46,
            text = utils.monthnames()[6],
            font = dict(
                size = 16
            )
        ),
        dict(
            showarrow = False,
            x = 0.35,
            y = 0.46,
            text = utils.monthnames()[7],
            font = dict(
                size = 16
            )
        ),
        dict(
            showarrow = False,
            x = 0.75,
            y = 0.46,
            text = utils.monthnames()[8],
            font = dict(
                size = 16
            )
        ),
        dict(
            showarrow = False,
            x = 0,
            y = 0.2,
            text = utils.monthnames()[9],
            font = dict(
                size = 16
            )
        ),
        dict(
            showarrow = False,
            x = 0.35,
            y = 0.2,
            text = utils.monthnames()[10],
            font = dict(
                size = 16
            )
        ),
        dict(
            showarrow = False,
            x = 0.75,
            y = 0.2,
            text = utils.monthnames()[11],
            font = dict(
                size = 16
            )
        )
        ],
        polar = dict(
            domain = dict(
                x = [0, 0.29],
                y = [0.79, 0.96]
            ),
            radialaxis = dict(
                range = [0, max_x+0.1*max_x]
            ),
            angularaxis = dict(
                rotation = 90,
                direction = "counterclockwise",
            )
        ),
        polar2 = dict(
            domain = dict(
                x = [0.37, 0.62],
                y = [0.79, 0.96]
            ),
            radialaxis = dict(
                range = [0, max_x+0.1*max_x]
            ),
            angularaxis = dict(
                rotation = 90,
                direction = "counterclockwise",
            )
        ),
        polar3 = dict(
            domain = dict(
                x = [0.70, 1],
                y = [0.79, 0.96]
            ),
            radialaxis = dict(
                range = [0, max_x+0.1*max_x]
            ),
            angularaxis = dict(
                rotation = 90,
                direction = "counterclockwise",
            )
        ),
        polar4 = dict(
            domain = dict(
                x = [0, 0.29],
                y = [0.54, 0.71]
            ),
            radialaxis = dict(
                range = [0, max_x+0.1*max_x]
            ),
            angularaxis = dict(
                rotation = 90,
                direction = "counterclockwise",
            )
        ),
        polar5 = dict(
            domain = dict(
                x = [0.37, 0.62],
                y = [0.54, 0.71]
            ),
            radialaxis = dict(
                range = [0, max_x+0.1*max_x]
            ),
            angularaxis = dict(
                rotation = 90,
                direction = "counterclockwise",
            )
        ),
        polar6 = dict(
            domain = dict(
                x = [0.70, 1],
                y = [0.54, 0.71]
            ),
            radialaxis = dict(
                range = [0, max_x+0.1*max_x]
            ),
            angularaxis = dict(
                rotation = 90,
                direction = "counterclockwise",
            )
        ),
        polar7 = dict(
            domain = dict(
                x = [0, 0.29],
                y = [0.29, 0.46]
            ),
            radialaxis = dict(
                range = [0, max_x+0.1*max_x]
            ),
            angularaxis = dict(
                rotation = 90,
                direction = "counterclockwise",
            )
        ),
        polar8 = dict(
            domain = dict(
                x = [0.37, 0.62],
                y = [0.29, 0.46]
            ),
            radialaxis = dict(
                range = [0, max_x+0.1*max_x]
            ),
            angularaxis = dict(
                rotation = 90,
                direction = "counterclockwise",
            )
        ),
        polar9 = dict(
            domain = dict(
                x = [0.70, 1],
                y = [0.29, 0.46]
            ),
            radialaxis = dict(
                range = [0, max_x+0.1*max_x]
            ),
            angularaxis = dict(
                rotation = 90,
                direction = "counterclockwise",
            )
        ),
        polar10 = dict(
            domain = dict(
                x = [0, 0.29],
                y = [0.04, 0.21]
            ),
            radialaxis = dict(
                range = [0, max_x+0.1*max_x]
            ),
            angularaxis = dict(
                rotation = 90,
                direction = "counterclockwise",
            )
        ),
        polar11 = dict(
            domain = dict(
                x = [0.37, 0.62],
                y = [0.04, 0.21]
            ),
            radialaxis = dict(
                range = [0, max_x+0.1*max_x]
            ),
            angularaxis = dict(
                rotation = 90,
                direction = "counterclockwise",
            )
        ),
        polar12 = dict(
            domain = dict(
                x = [0.70, 1],
                y = [0.04, 0.21]
            ),
            radialaxis = dict(
                range = [0, max_x+0.1*max_x]
            ),
            angularaxis = dict(
                rotation = 90,
                direction = "counterclockwise",
            )
        )
    )

    fig = dict(data = data, layout = layout)

    return fig

# Complete
def winddir_scatter(metdat, catinfo, category, vertloc=80, basecolor='red', exclude_angles=[(46, 228)]):
    """**Get Wind Direction Scatter Figure**.

    Plot the wind direction scatter of a given variable (or category of variables) grouped by a given condition (or set of conditions).
    
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

    # Set up data
    dircol, _, _= utils.get_vertical_locations(catinfo['columns']['direction'], location=vertloc)
    varcol, vertloc, _= utils.get_vertical_locations(catinfo['columns'][category], location=vertloc)

    colors = utils.get_nrelcolors()

    # Create a trace
    trace = go.Scatter(
        x = metdat[dircol],
        y = metdat[varcol],
        mode = 'markers',
    )
    data = [trace]

    # Set title and labels
    titleS = 'Vertical Location = %i m' % (vertloc)
    xlabel = 'Wind Direction [degrees]'
    ylabel = catinfo['labels'][category]

    # NOTE: This code does not loop through exclude_angles if there happens
    # to be multiple input ranges due to the extensive complications.
    # It is planned in the future to fix this.

    layout = {
        'title' :titleS,
        'xaxis' : {
            'title' : xlabel,
            'range' : [0, 360]
        },
        'yaxis' : {
            'title' : ylabel,
            'range' : [0, max(metdat[varcol]) + min(metdat[varcol])]
        },

        # NOTE: This code does not loop through exclude_angles if there happens
        # to be multiple input ranges due to the extensive complications.
        # It is planned in the future to fix this.

        'shapes' : [{
            'type': 'rect',
            # x-reference is assigned to the x-values
            'xref': 'x',
            # y-reference is assigned to the plot paper [0,1]
            'yref': 'y',
            'x0': exclude_angles[0][0],
            'y0': 0,
            'x1': exclude_angles[0][1],
            'y1': max(metdat[varcol]) + min(metdat[varcol]),
            'fillcolor': colors[basecolor][0],
            'opacity': 0.2,
            'line': {
                'width': 0,
            }
        },]
    }

    fig = {
        'data': data,
        'layout': layout,
    }

    fig = dict(data=data, layout=layout)
         
    return fig

# Complete
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
    plotdat = metdat.groupby(stabcol)

    # dirind = utils.get_nearest_direction(metdat[category])
    fig = plotly.tools.make_subplots(rows=5, cols=1,specs=[[{}], [{}], [{}], [{}], [{}]], shared_xaxes=False, shared_yaxes=False, vertical_spacing=0.05)
    
    # Initialize data structures
    fig_shape = []
    
    for ind, stabcond in enumerate(stabconds):
        # Create a trace
        trace = go.Scatter(
            x = plotdat[dircol].get_group(stabcond).values.tolist(),
            y = plotdat[varcol].get_group(stabcond).values.tolist(),
            mode = 'markers',
            name = stabcond,
            marker = dict(
                color = colors[ind],
                size = 16
            )
        )
        fig.append_trace(trace, ind+1, 1)

        shapes = dict(
            type = 'rect',
            xref = 'x'+str(ind+1),
            yref = 'y'+str(ind+1),
            x0 = exclude_angles[0][0],
            y0 = 0,
            x1 = exclude_angles[0][1],
            y1 = max(metdat[varcol]) + min(metdat[varcol]),
            fillcolor = nrelcolors[basecolor][0],
            opacity = 0.2,
            line=dict(
                width = 0
            )
        )
        fig_shape.append(shapes)

    # Set title and labels
    titleS = 'Vertical Location = %i m' % (vertloc)
    xlabel = 'Wind Direction [degrees]'
    ylabel = catinfo['labels'][category]

    for i in range(1,6):
        fig['layout']['xaxis'+str(i)].update(title = xlabel, range = [0, 360])
        fig['layout']['yaxis'+str(i)].update(title = ylabel, range=[0, max(metdat[varcol]) + min(metdat[varcol])])
    
    fig['layout'].update(height=2000, width=1000, title=titleS, shapes = fig_shape)

    return fig

# Complete
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

    fig = plotly.tools.make_subplots(rows=1, cols=1)
    
    # Initialize data structures
    data = [None]*(len(groups))

    for iax, group in enumerate(groups):
        # Create a trace
        trace = go.Scatter(
            x = plotdat[abscol].get_group(group).values.tolist(),
            y = plotdat[varcol].get_group(group).values.tolist(),
            mode = 'markers',
            name = '('+str(groups[iax].left)+', '+str(groups[iax].right)+']',
            marker = dict(
                color = colors[iax],
                size = 16
            )
        )
        data[iax] = trace

    # Set title and labels
    titleS = 'Vertical Location = %i m' % (vertloc)
    xlabel = str(catinfo['labels'][abscissa])
    #a = str(catinfo['labels'][abscissa])
    xlabel = xlabel.replace('$^\\circ$', 'degrees')
    ylabel = catinfo['labels'][category]

    # Set layout
    layout = go.Layout(
        title = titleS,        
        xaxis = dict(
            title = xlabel
        ),
        yaxis = dict(
            title = ylabel
        ),
        font = dict(
            size = 15
        ),
        annotations = [
            dict(
                x = 1.12,
                y = 1.05,
                align = "right",
                valign = "top",
                text = catinfo['labels'][groupby],
                showarrow = False,
                xref = "paper",
                yref = "paper",
                xanchor = "middle",
                yanchor = "top"
            )
        ]
    )

    fig = dict(data=data, layout=layout)

    return fig
    
# Complete
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

    # Set title and labels
    titleS = 'Vertical Location = %i m' % (vertloc)
    xlabel = catinfo['labels'][category]
    ylabel = 'Frequency [%]'

    trace = go.Histogram(
        x = data,
        nbinsx = 35,
        histnorm = 'probability',
        marker = dict(
            color = color,
            line = dict(
                width = 2
            )
        )
    )

    data = [trace]

    layout = go.Layout(
        title = titleS,
        xaxis = dict(
            title = xlabel
        ),
        yaxis = dict(
            title = ylabel
        ),
        bargap = 0,
    )

    fig = dict(data=data, layout=layout)

    return fig

# Incomplete (need to scale y-axis to bin height)
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

    # Setup data structures
    fig = plotly.tools.make_subplots(rows=4, cols=3, subplot_titles = utils.monthnames())
    max_x = 0

    for im,month in enumerate(months):
        # Get trace
        data = temp.get_group(im+1).dropna()

        # Get x-bounds
        if max(data) > max_x:
            max_x = max(data)

        trace = go.Histogram(
            x = data,
            nbinsx = bins,
            histnorm = 'probability',
            showlegend = False,
            marker = dict(
                color = color,
                line = dict(
                    width = 2
                )
            )
        )
        fig.append_trace(trace, (im//3)+1, (im%3)+1)
    
    # Set the string labels
    xstring = catinfo['labels'][category]
    ystring = 'Frequency [%]'
    titleS = "%s vs. %s" % (xstring,ystring)
    
    # Edit layout
    for i in range(1,13):
        fig['layout']['xaxis'+str(i)].update(title = xstring, range = [0, max_x+0.1*max_x])
        fig['layout']['yaxis'+str(i)].update(title = ystring, range = [0, 0.5])
        
    fig['layout'].update(height=2000, width=1000, title=titleS)

    return fig

# Incomplete (make vertical scale better)
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
    specs = []

    for i in range(len(stabconds)):
        specs.append([{}])

    fig = plotly.tools.make_subplots(rows=len(stabconds), cols=1,specs=specs, shared_xaxes=False, shared_yaxes=False, vertical_spacing=0.05)
    
    # Initialize data structures
    maxi = 0
    #maxy = 0
    bin_num = 50
    
    for ii, stab in enumerate(stabconds):
        # Create a trace
        data = metdat[varcol].get_group(stab).dropna()

        if max(data) > maxi:
            maxi = max(data)

        #if max(bin_height) > maxy:
        #    maxy = max(bin_height)

        trace = go.Histogram(
            x = data,
            nbinsx = bin_num,
            histnorm = 'probability',
            name = stab,
            marker = dict(
                color = colors[ii],
                line = dict(
                    width = 2
                )
            )
        )
        fig.append_trace(trace, ii+1, 1)

    # Set title and labels
    titleS = 'Vertical Location = %i m' % (vertloc)
    xlabel = catinfo['labels'][category]
    ylabel = 'Frequency [%]'

    for i in range(1,6):
        fig['layout']['xaxis'+str(i)].update(title = xlabel, range = [0, maxi+0.1*maxi])
        fig['layout']['yaxis'+str(i)].update(title = ylabel, range = [0, 1])
    
    fig['layout'].update(height=2000, width=1000, title=titleS)

    return fig

# Complete
def stacked_hist_by_stability(metdat, catinfo, category, vertloc=80):
    """**Get Stacked Stability Grouped Histogram Figure**.

    Plot the stacked stability grouped histogram of a given variable (or category of variables) grouped by a given condition (or set of conditions).
    
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

    plotdat = metdat.groupby(stabcol)

    # Initialize data structures    
    data = [None]*len(stabconds)

    for ii, stab in enumerate(stabconds):
        # Create a trace
        plot_data = plotdat[varcol].get_group(stab)

        trace = go.Histogram(
            x = plot_data,
            nbinsx = 17,
            histnorm = 'probability density',
            name = stab,
            marker = dict(
                color = colors[ii],
                line = dict(
                    width = 2
                )
            )
        )
        data[ii] = trace

    # Set title and labels
    titleS = 'Vertical Location = %i m' % (vertloc)
    xlabel = catinfo['labels'][category]
    ylabel = 'Frequency'

    layout = go.Layout(
        height = 1000,
        width = 1000,
        title = titleS,
        xaxis = dict(
            title = xlabel
        ),
        yaxis = dict(
            title = ylabel
        ),
        barmode = 'stack'
    )

    fig = go.Figure(data=data, layout=layout)

    return fig

# Incomplete (scale y-axis based on max bin height)
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

    # Initialize data structures    
    fig = plotly.tools.make_subplots(rows=4, cols=3, subplot_titles = utils.monthnames())
    data = [None]*len(stabconds)
    max_x = 0

    for iax, month in enumerate(months):
        for ii, stab in enumerate(stabconds):
            # Create a trace
            temp = plotdat.get_group((iax+1,stab))

            if iax == 0:
                show_leg = True
            else:
                show_leg = False
            
            if max(temp) > max_x:
                max_x = max(temp)

            trace = go.Histogram(
                x = temp,
                nbinsx = 17,
                histnorm = 'probability density',
                name = stab,
                showlegend = show_leg,
                marker = dict(
                    color = colors[ii],
                    line = dict(
                        width = 2
                    )
                )
            )
            fig.append_trace(trace, (iax//3)+1, (iax%3)+1)

    # Set title and labels
    xlabel = catinfo['labels'][category]
    ylabel = 'Frequency'
    titleS = "%s vs. %s" % (xlabel,ylabel)

    # Edit layout
    for i in range(1,len(utils.monthnames())+1):
        fig['layout']['xaxis'+str(i)].update(title = xlabel, range = [0, max_x+0.1*max_x])
        fig['layout']['yaxis'+str(i)].update(title = ylabel, range=[0, 5])
        
    fig['layout'].update(height=2000, width=1000, barmode = 'stack', title=titleS)

    return fig

# Complete
def normalized_hist_by_stability(metdat, catinfo, vertloc=80):
    """**Get Normalized Stability Grouped Histogram Figure**.

    Plot the normalized stability grouped histogram of a given variable (or category of variables) grouped by a given condition (or set of conditions).
    
    Parameters:
        1. metdat (Pandas DataFrame): The desired input data (Met Mast).
        2. catinfo (dictionary): Categorization information for the desired input data. Holds column names, labels, units, and save names.
        3. vertloc (integer, float): Describes the desired vertical location alond the tower for analysis.        

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

    data = [None]*len(stabconds)

    fig = plotly.tools.make_subplots(rows=1, cols=1)    

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

        trace = go.Bar(
            x = b,
            y = c,
            name = cond,
            marker = dict(
                color = colors[jj]
            )
        )

        data[jj] = trace

    # Set title and labels
    xlabel = 'Time of Day [hour]'
    ylabel = 'Probability [%]'
    titleS = "%s vs. %s" % (xlabel,ylabel)

    layout = go.Layout(
        barmode='stack',
        xaxis = dict(
            title = xlabel
        ),
        yaxis = dict(
            title = ylabel
        ),
        title = titleS
    )

    fig = dict(data = data, layout = layout)

    return fig

# Complete
def normalized_monthly_hist_by_stability(metdat, catinfo, vertloc=80):
    """**Get Normalized Monthly Stability Grouped Histogram Figure**.

    Plot the normalized monthly stability grouped histogram of a given variable (or category of variables) grouped by a given condition (or set of conditions).
    
    Parameters:
        1. metdat (Pandas DataFrame): The desired input data (Met Mast).
        2. catinfo (dictionary): Categorization information for the desired input data. Holds column names, labels, units, and save names.
        3. vertloc (integer, float): Describes the desired vertical location alond the tower for analysis.        

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

    fig = plotly.tools.make_subplots(rows=4, cols=3, subplot_titles = utils.monthnames())

    for iax, month in enumerate(months):
        for jj, cond in enumerate(stabconds):
            # Use this for missing data, also works for full data
            a = temp.loc[iax+1,cond]
            b = a.index.tolist()
            c = a.values.tolist()
            for i in range(len(hours)):
                if (hours[i]) in b:
                    pass
                else:
                    b.insert(i,hours[i])
                    c.insert(i,0)

            if iax == 0:
                show_leg = True
            else:
                show_leg = False

            trace = go.Bar(
                x = b,
                y = c,
                name = cond,
                showlegend = show_leg,
                marker = dict(
                    color = colors[jj]
                )
            )
            fig.append_trace(trace, (iax//3)+1, (iax%3)+1)

    # Set title and labels
    xlabel = 'Time of Day [Hour]'
    ylabel = 'Probability [%]'
    titleS = "%s vs. %s" % (xlabel,ylabel)

    # Edit layout
    for i in range(1,len(utils.monthnames())+1):
        fig['layout']['xaxis'+str(i)].update(title = xlabel)
        fig['layout']['yaxis'+str(i)].update(title = ylabel)
        
    fig['layout'].update(height=2000, width=1000, barmode = 'stack', title=titleS)

    return fig
