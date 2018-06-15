"""
:module: utils
:platform: Unix, Windows
:synopsis: This code is used as a general family of utilities that can be used for plotting. 
:moduleauthor: Nicholas Hamilton <Nicholas.Hamilton@nrel.gov> Rafael Mudafort <Rafael.Mudafort@nrel.gov> Lucas McCullum <Lucas.McCullum@nrel.gov>   
"""

###########################################
# Helper Functions
###########################################

import numpy as np
import pandas as pd
from calendar import monthrange, month_name
import datetime as dt

###########################################
# Arithmetic (Rounding)
###########################################

def Round_To_n(x, n):
    """
    **Round input values**.

    This function takes in a desired value and rounds it to the specified number of decimel places.
    
    Parameters:
        1. x (integer, float): The input number that will be rounded.
        2. n (integer): The number of digits that the result will be rounded to.
    
    Returns:
        1. N/A (float): The rounded version of the input number to the specified number of decimel places.
    """

    return round(x, -int(np.floor(np.sign(x) * np.log10(abs(x)))) + n)

###########################################
# Get Values of Interest
###########################################

def get_vertical_locations(category, location=None, reverse=False):
    """**Get vertical locations**.

    This function takes in variables in the form of a category and returns a list of the resulting variable names, their associated vertical locations, and the index nearest to the location.
    
    Parameters:
        1. category (list): The desired vertical locations in the form of variables for analysis.
        2. location (integer, float) [default: None]: The desired vertical location for analysis.
        3. reverse (Boolean) [default: False]: Determines whether or not to reverse the resulting output.

    Returns:
        1. category (list): The list of the resulting variable names.
        2. vertlocs (list): The list of the associated resulting vertical locations for each variable.
        3. ind (integer): The values of the index nearest to the location.
    """
    
    vertlocs = [int(var.replace(' ', '').split('(')[-1].split('_')[-1].split('m')[0]) for var in category]
    ind = sorted(range(len(vertlocs)), key=lambda k: vertlocs[k])
    # sort vertical locations
    vertlocs = [vertlocs[x] for x in ind]
    category = [category[x] for x in ind]
    
    if location is not None:
        temp = np.array(vertlocs)
        ind = int(np.argmin(np.abs(temp - location)))
        category = category[ind]
        vertlocs = vertlocs[ind]
    
    if reverse is True:
        category = [x for x in category[-1::-1]]
        vertlocs = [x for x in vertlocs[-1::-1]]

    return category, vertlocs, ind

def get_nearest_direction(metdat, directions, category):
    """**Get Nearest Direction**.

    This function takes in the desired input data variables in the form of a category and returns the nearest direction and its associated variable name.
    
    Parameters:
        1. metdat (Pandas DataFrame): The input data that is desired to be analyzed.
        2. directions (list): The desired directions for analysis.
        3. category (list): The list of the resulting variable names.

    Returns:
        1. dirind (list): The values of the index nearest to the direction.
        2. catind (list): The values of the index for the associated vertical location.
        3. vertlocs (list): The list of the associated resulting vertical locations for each variable.
    """
    
    vertlocs = [int(var.replace(' ', '').split('(')[-1].split('_')[-1].split('m')[0]) for var in metdat[category]]
    dirlocs = [int(var.replace(' ', '').split('(')[-1].split('_')[-1].split('m')[0]) for var in metdat[directions]]
    
    # for loc in vertlocs:
    dirind = [np.argmin(np.abs(np.array(dirlocs) - loc)) for loc in vertlocs]
    catind = [vertlocs.index(loc) for loc in vertlocs]    

    return dirind, catind, vertlocs

def get_nearest_stability(metdat, stability, category):
    """**Get Nearest Stability**.

    This function takes in the desired input data variables in the form of a category and returns the nearest stability and its associated variable name.
    
    Parameters:
        1. metdat (Pandas DataFrame): The input data that is desired to be analyzed.
        2. stability (list): The desired stabilities for analysis.
        3. category (list): The list of the resulting variable names.

    Returns:
        1. stabind (list): The values of the index nearest to the stability.
        2. catind (list): The values of the index for the associated vertical location.
        3. vertlocs (list): The list of the associated resulting vertical locations for each variable.
    """
    
    if isinstance(category, list):
        vertlocs = [int(var.replace(' ', '').split('(')[-1].split('_')[-1].split('m')[0]) for var in metdat[category]]
        stablocs = [int(var.replace(' ', '').split('(')[-1].split('_')[-1].split('m')[0]) for var in metdat[stability]]
    elif isinstance(category, str):
        vertlocs = [int(category.replace(' ', '').split('(')[-1].split('_')[-1].split('m')[0])]
        stablocs = [int(var.replace(' ', '').split('(')[-1].split('_')[-1].split('m')[0]) for var in metdat[stability]]
        
    # for loc in vertlocs:
    stabind = [np.argmin(np.abs(np.array(stablocs) - loc)) for loc in vertlocs]
    catind = [vertlocs.index(loc) for loc in vertlocs]    

    return stabind, catind, vertlocs

###########################################
# Get Desired Information for Plotting
###########################################

def monthnames():
    """**Get Month Names**.

    This function takes in no parameters, but returns the values of each month of the year.

    Parameters:
        1. N/A: N/A
    
    Returns:
        1. N/A (list): The values of each month of the year.
    """

    months = ['January',
             'February',
             'March',
             'April',
             'May',
             'June',
             'July',
             'August',
             'September',
             'October',
             'November',
             'December']
    return months

def get_stabconds():
    """**Get Stability Conditions**.

    This function takes in no parameters, but returns the values of the stability conditions.

    Parameters:
        1. N/A: N/A
    
    Returns:
        1. N/A (list): The values of the stability conditions.
    """

    stabconds = ['Very Stable', 'Stable', 'Neutral', 'Unstable', 'Very Unstable']
    return stabconds

def matlab_datenum_to_python_datetime(datenum):
    """**Create Color Dictionary**.

    This function takes in a numerical value of the date as stored in Matlab and returns the resulting date and time value.

    Parameters:
        1. datenum (integer): The numerical value of the date as stored in Matlab.
    
    Returns:
        1. dateout(list): The resulting date and time value of the desired input date number.
    """

    if isinstance(datenum,int):
        dateout = dt.datetime.fromordinal(int(datenum)) +\
                dt.timedelta(days=datenum%1) - dt.timedelta(days = 366)
    else:
        dateout = [dt.datetime.fromordinal(int(date)) +\
                dt.timedelta(days=date%1) - dt.timedelta(days = 366) for date in datenum]


    return dateout

###########################################
# Setup Colors for Plotting
###########################################

def get_colors(ncolors, basecolor='cycle', reverse=False):
    """**Get Plot Colors**.

    This function takes in the desired number of colors and the base color and determines the resulting gradient of colors that should be used for the plot.

    Parameters:
        1. ncolors (int): The desired number of colors for the plot.
        2. basecolor (string): The desired base color for the plot.
        3. reverse (Boolean): Determines whether or not the colors should be reversed.
    
    Returns:
        1. colors (list): The values of the resulting gradient of colors that should be used for the plot.
    """
    
    # nrel official colors
    nrelcolors = get_nrelcolors()

    if isinstance(basecolor, list):
        colors = basecolor#[ nrelcolors[basecolor[x]][1] for x in range(len(basecolor))]
        cdict = polylinear_gradient(colors,ncolors+2)
        colors = cdict['hex']

    elif basecolor in nrelcolors:
        nc = ncolors+2
        colors = []
        while len(colors) < ncolors:
            nc += 1
            colors = ['#D1D5D8',nrelcolors[basecolor][1],nrelcolors[basecolor][0]]
            cdict = polylinear_gradient(colors,nc)
            colors = cdict['hex']
            del colors[2]
        
    elif basecolor is 'cycle':
        nc = ncolors+2
        colors = []
        while len(colors) < ncolors:
            nc += 1
            colors = ['#0079C2','#D1D5D8','#D9531E','#00A4E4']
            cdict = polylinear_gradient(colors,nc)
            colors = cdict['hex']
            del colors[2]
        
    elif basecolor is 'span':
        colors = [nrelcolors['blue'][0], '#D1D5D8', nrelcolors['red'][0]]
        cdict = polylinear_gradient(colors,ncolors+2)
        colors = cdict['hex']
        
    if reverse is True:
        colors = colors[-1::-1]
        
    return colors

def get_nrelcolors():
    """**Get NREL Colors**.

    This function takes in no parameters, but returns the values of the standard colors used by the National Renewable Energy Laboratory (NREL).

    Parameters:
        1. N/A: N/A
    
    Returns:
        1. N/A (dictionary): The values of the standard colors used by NREL.
    """

    nrelcolors = {'blue': ['#0079C2','#00A4E4'],
                  'red': ['#933C06','#D9531E'],
                  'green': ['#3D6321','#5D9732'],
                  'gray': ['#3A4246','#5E6A71']}
    return nrelcolors

def hex_to_RGB(hex):
    """**Convert Hex Values to RGB**.

    This function takes in the desired hex value for conversion and returns the resulting RGB value of the color.

    Parameters:
        1. hex (string): The desired hex value to be converted.
    
    Returns:
        1. N/A (list): The RGB values of the desired input hex value.
    """

    # Pass 16 to the integer function for change of base
    return [int(hex[i:i+2], 16) for i in range(1,6,2)]

def RGB_to_hex(RGB):
    """**Convert RGB Values to Hex**.

    This function takes in the desired RGB values for conversion and returns the resulting hex value of the color.

    Parameters:
        1. RGB (list): The RGB values of the desired input hex value.
    
    Returns:
        1. N/A (string): The hex value of the desired input RGB values.
    """

    # Components need to be integers for hex to make sense
    RGB = [int(x) for x in RGB]
    return "#"+"".join(["0{0:x}".format(v) if v < 16 else
            "{0:x}".format(v) for v in RGB])

def linear_gradient(start_hex, finish_hex="#FFFFFF", n=10):
    """**Convert Hex Values to RGB**.

    This function takes in the desired hex values for the start and end of a gradient as well as the desired number of levels and returns a list containing the resulting color gradient.

    Parameters:
        1. start_hex (string): The desired starting hex value for the color gradient.
        2. finish_hex (string): The desired ending hex value for the color gradient.
        3. n (integer): The desired number of total colors to form a gradient.
    
    Returns:
        1. N/A (list): The RGB values of the desired color gradient.
    """

    # Starting and ending colors in RGB form
    s = hex_to_RGB(start_hex)
    f = hex_to_RGB(finish_hex)
    # Initilize a list of the output colors with the starting color
    RGB_list = [s]
    # Calcuate a color at each evenly spaced value of t from 1 to n
    for t in range(1, n):
        # Interpolate RGB vector for color at the current value of t
        curr_vector = [
          int(s[j] + (float(t)/(n-1))*(f[j]-s[j]))
          for j in range(3)
        ]
        # Add it to our list of output colors
        RGB_list.append(curr_vector)

    return color_dict(RGB_list)

def color_dict(gradient):
    """**Create Color Dictionary**.

    This function takes in a list of RGB sub-lists and returns a dictionary of colors in RGB and hex form for the use in plotting.

    Parameters:
        1. gradient (list): The desired RGB sub-lists.
    
    Returns:
        1. N/A (dictionary): The resulting colors in RGB and hex form.
    """

    return {"hex":[RGB_to_hex(RGB) for RGB in gradient],
      "r":[RGB[0] for RGB in gradient],
      "g":[RGB[1] for RGB in gradient],
      "b":[RGB[2] for RGB in gradient]}

def polylinear_gradient(colors, n):
    """**Create Polylinear Color Gradient**.

    This function takes in a list of RGB sub-lists and returns a dictionary of colors in RGB and hex form for the use in plotting.

    Parameters:
        1. colors (list): The desired pairs of input colors.
        2. n (integer): The desired number of output colors.
    
    Returns:
        1. N/A (list): The resulting colors forming linear gradients between all sequential pairs of colors.
    """

    # The number of colors per individual linear gradient
    n_out = int(float(n) / (len(colors) - 1))
    # returns dictionary defined by color_dict()
    gradient_dict = linear_gradient(colors[0], colors[1], n_out)

    if len(colors) > 1:
        for col in range(1, len(colors) - 1):
            next = linear_gradient(colors[col], colors[col+1], n_out)
            for k in ("hex", "r", "g", "b"):
                # Exclude first point to avoid duplicates
                gradient_dict[k] += next[k][1:]

    return gradient_dict

###########################################
# End of Code
###########################################