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
                  yaxis = dict(title = ystring),
                  )

    fig = dict(data=data, layout=layout)

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
                categoryarray = ["N", "NW", "W", "SW","S","SE","E","NE"]
            )
        ),
    )

    fig = dict(data=data, layout=layout)
         
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
         
    return fig

# Incomplete
def stability_winddir_scatter(metdat, catinfo, category, vertloc=80, basecolor='red', exclude_angles=[(46, 228)]):
    """**Get Wind Direction Stability Scatter Figure**.

    Plot the wind direction stability scatter of a given variable (or category of variables) grouped by a given condition (or set of conditions).
    
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
    
    stabconds = utils.get_stabconds()
    colors = utils.get_colors(5,basecolor='span')
    nrelcolors = utils.get_nrelcolors()

     # Set up data
    dircol, _, _= utils.get_vertical_locations(catinfo['columns']['direction'], location=vertloc)
    varcol, vertloc, _= utils.get_vertical_locations(catinfo['columns'][category], location=vertloc)
    stabcol, _, _= utils.get_vertical_locations(catinfo['columns']['stability flag'], location=vertloc)
    plotdat = metdat.groupby(stabcol)

    # dirind = utils.get_nearest_direction(metdat[category])
    fig = plotly.tools.make_subplots(rows=len(stabconds), cols=1)

    # Initialize data structures
    data = [None]*len(stabconds)
    
    for ind, stabcond in enumerate(stabconds):
        # Create a trace
        print(plotdat[dircol].get_group(stabcond).values.tolist())
        print(plotdat[varcol].get_group(stabcond).values.tolist())

        trace = go.Scatter(
            x = plotdat[dircol].get_group(stabcond).values.tolist(),
            y = plotdat[varcol].get_group(stabcond).values.tolist(),
            mode = 'markers',
            name = stabconds[ind],
            marker = dict(
                color = colors[ind],
                size = 16
            )
        )
        # Un-comment to keep all on same plot
        data[ind] = trace
        #fig.append_trace(trace, ind+1, 1)

    # Set title and labels
    titleS = 'Vertical Location = %i m' % (vertloc)
    xlabel = 'Wind Direction [degrees]'
    ylabel = catinfo['labels'][category]

    layout = {
        'title' :titleS,
        'xaxis' : {
            'title' : xlabel,
            'range' : [0, 360]
        },
        'yaxis' : {
            'title' : ylabel,
            'range' : [0, max(plotdat[varcol]) + min(plotdat[varcol])]
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
            'fillcolor': nrelcolors[basecolor][0],
            'opacity': 0.2,
            'line': {
                'width': 0,
            }
        },]
    }

    # Un-comment to keep all on same plot
    fig = {
        'data': data,
        'layout': layout,
    }
         
    return fig

# Incomplete
def groupby_scatter(metdat, catinfo, category, abscissa='direction', groupby='ti', nbins=5, vertloc=80, basecolor='span'):
    """**Get Wind Direction Grouped Scatter Figure**.

    Plot the wind direction grouped scatter of a given variable (or category of variables) grouped by a given condition (or set of conditions).
    
    Parameters:
        1. metdat (Pandas DataFrame): The desired input data (Met Mast).
        2. catinfo (dictionary): Categorization information for the desired input data. Holds column names, labels, units, and save names.
        3. category (string): Specifies the category of information that is desired for plotting.
        4. abscissa (string): independent variable to plot again
        5. groupby (string): Describes which categories to group by.
        6. nbins (integer): Divides the *groupby* variable into bins.
        7. vertloc (integer, float): Describes the desired vertical location alond the tower for analysis.        
        8. basecolor (string): Provides the color code information to get from "utils.py".

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

# Incomplete
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

    return fig