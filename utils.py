###########################################
# helper functions
###########################################

import numpy as np
import pandas as pd
from calendar import monthrange, month_name
import datetime as dt

###########################################
def Round_To_n(x, n):
    return round(x, -int(np.floor(np.sign(x) * np.log10(abs(x)))) + n)
###########################################

###########################################
def get_vertical_locations(category, location=None, reverse=False):
    """
    Extract vertical locations from a group of variables (in a category, usually)
    If no specific location is provided, return a sorted list of vertical locations,
    otherwise, provided the variable name, vertical location, and index nearest to location
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
###########################################

###########################################
def get_nearest_direction(metdat, directions, category):
    """Extract vertical locations from a group of variables (in a category, usually)"""
    
    vertlocs = [int(var.replace(' ', '').split('(')[-1].split('_')[-1].split('m')[0]) for var in metdat[category]]
    dirlocs = [int(var.replace(' ', '').split('(')[-1].split('_')[-1].split('m')[0]) for var in metdat[directions]]
    
    # for loc in vertlocs:
    dirind = [np.argmin(np.abs(np.array(dirlocs) - loc)) for loc in vertlocs]
    catind = [vertlocs.index(loc) for loc in vertlocs]    

    return dirind, catind, vertlocs
###########################################

###########################################
def get_nearest_stability(metdat, stability, category):
    """Extract vertical locations from a group of variables (in a category, usually)"""
    
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

###########################################
def monthnames():
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
###########################################

###########################################
def get_stabconds():
    stabconds = ['Very Stable', 'Stable', 'Neutral', 'Unstable', 'Very Unstable']
    return stabconds
###########################################

###########################################
# color info functions
###########################################

###########################################
def get_colors(ncolors, basecolor='cycle', reverse=False):
    """make a gradient of colors for use in plotting"""
    
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
        colors = [nrelcolors['blue'][0], '#a1a5a7', nrelcolors['red'][0]]
        cdict = polylinear_gradient(colors,ncolors+2)
        colors = cdict['hex']
        
    if reverse is True:
        colors = colors[-1::-1]
        
    return colors

def get_nrelcolors():
    nrelcolors = {'blue': ['#0079C2','#00A4E4'],
                  'red': ['#933C06','#D9531E'],
                  'green': ['#3D6321','#5D9732'],
                  'gray': ['#3A4246','#5E6A71']}
    return nrelcolors

def hex_to_RGB(hex):
    ''' "#FFFFFF" -> [255,255,255] '''
    # Pass 16 to the integer function for change of base
    return [int(hex[i:i+2], 16) for i in range(1,6,2)]

def RGB_to_hex(RGB):
    ''' [255,255,255] -> "#FFFFFF" '''
    # Components need to be integers for hex to make sense
    RGB = [int(x) for x in RGB]
    return "#"+"".join(["0{0:x}".format(v) if v < 16 else
            "{0:x}".format(v) for v in RGB])

def linear_gradient(start_hex, finish_hex="#FFFFFF", n=10):
    ''' returns a gradient list of (n) colors between
    two hex colors. start_hex and finish_hex
    should be the full six-digit color string,
    inlcuding the number sign ("#FFFFFF") '''
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
    ''' Takes in a list of RGB sub-lists and returns dictionary of
    colors in RGB and hex form for use in a graphing function
    defined later on '''
    return {"hex":[RGB_to_hex(RGB) for RGB in gradient],
      "r":[RGB[0] for RGB in gradient],
      "g":[RGB[1] for RGB in gradient],
      "b":[RGB[2] for RGB in gradient]}

def polylinear_gradient(colors, n):
    """
    returns a list of colors forming linear gradients between 
    all sequential pairs of colors. n specifies the total
    number of desired output colors
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

###########################################
def matlab_datenum_to_python_datetime(datenum):
    """
    Parameters
    ----------
    datenum : int
    """
    if isinstance(datenum,int):
        dateout = dt.datetime.fromordinal(int(datenum)) +\
                dt.timedelta(days=datenum%1) - dt.timedelta(days = 366)
    else:
        dateout = [dt.datetime.fromordinal(int(date)) +\
                dt.timedelta(days=date%1) - dt.timedelta(days = 366) for date in datenum]


    return dateout
###########################################
