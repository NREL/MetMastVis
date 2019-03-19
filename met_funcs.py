"""
.. module: met_funcs
:platform: Unix, Windows
:synopsis: This code is used as a general family of functions and classes that can be used in the MET tower data analysis.
.. moduleauthor:: Nicholas Hamilton <Nicholas.Hamilton@nrel.gov> Rafael Mudafort <Rafael.Mudafort@nrel.gov> Lucas McCullum <Lucas.McCullum@nrel.gov>
"""

import numpy as np
import pandas as pd
from calendar import monthrange, month_name
import datetime as dt
import pickle as pkl

import utils

####################################
# Data loading
####################################


def load_met_data(inputfiles, verbose=False):
    """
    Load the data with a lambda function.

    This function extracts the data from the input Comma-Separated (.csv) files and outputs them into a pandas DataFrame.

    :param inputfiles: All of the input files (.csv) to be loaded for analysis.

    :param verbose: Defines whether or not the name of the file should be printed as the function runs.

    :type inputfiles: list

    :type verbose: Boolean

    :returns metdat: Contains all of the requested data extracted from the input files.

    :rtype metdat: pandas DataFrame
    """

    # date parser for pandas
    dp = lambda x: pd.datetime.strptime(x, '%d-%m-%Y %H:%M:%S')
    filecount = 0

    for fName in inputfiles:
        df_lo = pd.read_csv(fName,\
                            index_col=[0],\
                            parse_dates=[0],\
                            date_parser=dp,\
                            skiprows=[0,1,2,3,4,5,6,8,9],\
                            low_memory=False,
                            error_bad_lines=False)
        if filecount == 0:
            metdat = df_lo.copy()
        else:
            metdat = metdat.append(df_lo.copy())
        filecount += 1
        if verbose is True:
            print(fName)
    metdat.index = metdat.index.tz_localize('UTC').tz_convert('America/Denver')

    # replace flagged value '-999.0' with nans
    metdat[metdat == -999.0] = np.nan

    return metdat


####################################


####################################
def load_met_data_alt(inputfiles, verbose=False):
    """
    Load the data without a lambda function.

    This function extracts the data from the input Comma-Separated (.csv) files and outputs them into a pandas DataFrame. This is an alternate to the previous function to avoid the use of a data parser lambda function.

        :param inputfiles: All of the input files (.csv) to be loaded for analysis.

    :param verbose: Defines whether or not the name of the file should be printed as the function runs.

    :type inputfiles: list

    :type verbose: Boolean

    :returns metdat: A pandas DataFrame containing all of the requested data extracted from the input files.

    :rtype metdat: pandas DataFrame
    """

    filecount = 0

    for fName in inputfiles:
        df_lo = pd.read_csv(fName,\
                            skiprows=[0,1,2,3,4,5],\
                            low_memory=False)
        if filecount == 0:
            metdat = df_lo.copy()
            metdat.drop([0, 1])
        else:
            df_lo.drop([0, 1])
            metdat = metdat.append(df_lo.copy())
        filecount += 1
        if verbose is True:
            print(fName)

    metdat['Date'] = pd.to_datetime(
        metdat['Date'], errors='coerce', infer_datetime_format=True)
    metdat = metdat[metdat.Date.notnull()]
    metdat = metdat.set_index('Date')

    # metdat.index = metdat.index.tz_localize('UTC').tz_convert('America/Denver')

    temp = [name for name in list(metdat.columns.values) if ' QC' not in name]
    qcNames = [name for name in list(metdat.columns.values) if ' QC' in name]
    fNames = [name for name in temp if name + ' QC' in qcNames]

    metdat[fNames] = metdat[fNames].values.astype(np.float64)
    metdat[qcNames] = metdat[qcNames].values.astype(np.int32)

    if verbose is True:
        print('dtypes corrected')

    # replace flagged value '-999.0' with nans
    metdat[metdat == -999.0] = np.nan
    metdat.tz_localize('UTC').tz_convert('America/Denver')

    return metdat


####################################


####################################
# Data filtering
####################################
def drop_nan_cols(metdat):
    """
    Remove empty columns.

    This function takes the contents of the pandas DataFrame containing all of the data from the input files and filters it by removing any missing columns (e.g., N/A).

    :param metdat: Contains all of the requested data extracted from the input files.

    :type metdat: pandas DataFrame

    :returns temp: Contains all of the requested data extracted from the input files without any missing columns (e.g., N/A)

    :rtype temp: pandas DataFrame
    """

    temp = metdat.dropna(axis=1, how='all')

    return temp


###########################################


###########################################
def qc_mask(metdat):
    """
    Remove columns for quality control.

    This function takes the contents of the pandas DataFrame containing all of the data from the input files and filters data based on a mask of columns containing the term ‘qc’ (Quality Control parameters).

    :param metdat: Contains all of the requested data extracted from the input files.

    :type metdat: pandas DataFrame

    :returns dfFilt: Contains a filtered version of the requested data extracted from the input files by removing columns containing a quality control parameter.

    :rtype dfFilt: pandas DataFrame
    """

    temp = [name for name in list(metdat.columns.values) if ' QC' not in name]
    temp = [
        name for name in list(metdat.columns.values) if ' QC' not in name
        if 'records' not in name.lower()
    ]

    qcNames = [name for name in list(metdat.columns.values) if ' QC' in name]
    fNames = [name for name in temp if name + ' QC' in qcNames]

    print('number of data columns:', len(fNames))
    print('number of QC columns:', len(qcNames))

    # initialize filtered dataframe with 'record', 'version'
    dfFilt = pd.DataFrame(index=metdat.index)
    # apply QC mask to each set of columns individually
    for f, q in zip(fNames, qcNames):
        #     print(fname, qname)
        temp = metdat[[f, q]].copy()
        mask = temp[q] == 1
        temp = temp[mask]
        dfFilt[f] = temp[f]

    return dfFilt


###########################################


###########################################
def flag_stability(metdat):
    """
    Denote stability based on Obukhov Length.

    This function takes the contents of the pandas DataFrame containing all of the data from the input files and adds a new set of columns denoting a stability class based on the Obukhov Length at various heights.

    :param metdat: Contains all of the requested data extracted from the input files.

    :type metdat: pandas DataFrame

    :returns stabcat: Contains the stability flag parameter for each desired row of the input data based on the Obukhov Length and can be classified as Very Stable, Stable, Neutral, Unstable, and Very Unstable.

    :returns stabconds: Contains the values of the Obukhov Length for each desired row of the input data.

    :rtype stabcat: dictionary

    :rtype stabconds: list
    """

    MOLcols = [
        col for col in metdat.columns if 'monin-obukhov length' in col.lower()
    ]
    for col in MOLcols:
        # get probe height
        z = int(col.split('m')[0].split('(')[-1])

        # extract data from MetDat
        L = metdat[col].copy()
        categoriesIdx = {
            'Very Stable': (L > 0) & (L <= 200),
            'Stable': (L > 200) & (L <= 500),
            'Neutral': (L < -500) | (L > 500),
            'Unstable': (L >= -500) & (L < -200),
            'Very Unstable': (L >= -200) & (L < 0)
        }

        # make new column
        newcolname = 'Stability Flag ({}m)'.format(z)
        metdat[newcolname] = np.nan
        for cat in categoriesIdx.keys():
            metdat.loc[categoriesIdx[cat], newcolname] = cat

    stabcat = {
        'stability flag': [x for x in metdat.columns if 'Stability Flag' in x]
    }
    stabconds = [x for x in categoriesIdx]

    return stabconds, stabcat


###########################################


###########################################
def groom_data(metdat, varcats):
    """
    Trim data based on several parameters.

    This function takes the contents of the pandas DataFrame containing all of the data from the input files as well as a list of categories that are desired to be kept and outputs a statement displaying the remaining number of columns left after filtering.

    *Possible Edit: This function could be divided into separate functions or could be made more general. Additionally the following code could be used… *
    .. code-block:: python
        dropcols = True
        filter = [‘ti’, 'monin-obukhov length','temperature','gradient richarson']):

    :param metdat: Contains all of the requested data extracted from the input files.

    :param varcats: All the categories which are desired to be kept after filtering.

    :type metdat: pandas DataFrame

    :type varcats: list

    :returns: A print statement displaying the number of columns after filtering for columns not contained in the list of desired columns, Turbulent Intensity, Obukhov Length, Sonic Temperature, and Gradient Richardson Number.

    :rtype: string
    """
    ## drop columns
    keepcols = [v for x in varcats for v in varcats[x]]
    dropcols = [col for col in metdat.columns if col not in keepcols]
    metdat.drop(dropcols, axis=1, inplace=True)

    # filter TI to where wind speed >= 1 m/s
    # spdcols = [col for col in varcats['speed'] if 'sonic' not in col.lower()]
    for ii, item in enumerate(varcats['speed']):
        if 'sonic' in item.lower():
            continue
        metdat.loc[metdat[varcats['speed'][ii]] < 1, varcats['ti'][
            ii]] = np.nan

    # filter obukhov length
    for col in varcats['monin-obukhov length']:
        metdat.loc[np.abs(metdat[col]) > 2000, col] = np.nan

    # filter sonic temperatures (kelvins vs degrees C)
    for col in varcats['air temperature']:
        metdat.loc[np.abs(metdat[col]) > 200,
                   col] = metdat.loc[np.abs(metdat[col]) > 200, col] - 273

    # filter gradient richardson number
    for col in varcats['gradient richardson']:
        metdat.loc[np.abs(metdat[col]) > 20, col] = np.nan

    # print('number of columns after filtering: {}'.format(len(metdat.columns)))


###########################################


###########################################
def reject_outliers(data, m=5):
    """
    Remove any outliers.

    This function takes the contents of the pandas DataFrame containing all of the data from a desired data file and outputs a filtered version by removing any outliers.

    :param data: Contains the desired data that is to be filtered for outliers.

    :param m: Denotes the number of standard deviations that are desired as a cutoff for defining outliers.

    :type data: pandas DataFrame

    :type m: integer

    :returns data: A filtered version of the input data file by rejecting any outliers above *m* (5) standard deviations.

    :rtype data: pandas DataFrame
    """

    return data[abs(data - np.mean(data)) < m * np.std(data)]


###########################################


###########################################
def fix_pressure_data(metdat, catinfo):
    """
    Bad pressure data correction

    There is a period of data for which the pressure signals are
    not to be trusted It appears that there was a poor calibration
    between two periods of downtime. Data has been correted by
    adding an offset to that range of data. The offset is equal to
    the difference between the mean value of the bad data and the mean
    value of the annual average over that period.

    Parameters:
    metdat, pandas dataframe: contains all of the relevant met mast timeseries data
    catinfo, dict: contains all of the categorical information for data channels in metdat
    """
    pcols, pheights, _ = utils.get_vertical_locations(
        catinfo['columns']['air pressure'])
    metdat.sort_index(inplace=True)

    for pcol in pcols:
        # pressure data
        pdat = metdat[pcol].copy()
        # find start and stop times of bad data
        timediff = np.abs(np.diff(pdat.index.values))
        temp = timediff.copy()
        temp.sort()
        limits = [
            np.where(timediff == temp[-1])[0][0],
            np.where(timediff == temp[-2])[0][0]
        ]
        # extract bad data
        limdates = metdat.index.values[limits]
        bdat = pdat.iloc[limits[0] + 1:limits[1]].copy()
        # good data is outside of that range
        gdat = pdat[(pdat.index < pdat.index[limits[0]])
                    | (pdat.index >= pdat.index[limits[1]])].copy()
        # average value of pressure for that day of year
        dayofyearaverage = gdat.groupby(gdat.index.dayofyear).mean()
        # correction is just the difference of mean values
        pressure_correction = dayofyearaverage.values[bdat.index.
                                                      dayofyear].mean(
                                                      ) - bdat.mean()
        # corrected data
        # cdat = bdat+(dayofyearaverage.values[bdat.index.dayofyear].mean()-bdat.mean())

        # # metdat[col].iloc[limits[0]+1:limits[1]] = cdat

        metdat.loc[((metdat.index>limdates[0]) & (metdat.index<limdates[1])), pcol] += \
                (dayofyearaverage.values[bdat.index.dayofyear].mean()-bdat.mean())

    return metdat


###########################################


###########################################
# Data organization
###########################################
def categorize_fields(metdat, keeplist=None, excludelist=None):
    """
    Categorize all of the fields of the data.

    This function takes the contents of the pandas DataFrame containing all of the data from a desired input data file and outputs the variable categories, units, ≈ for plotting, and strings for saving files and figures.

        :param metdat: A pandas DataFrame containing all of the requested data extracted from the input files.

        :param keeplist: A list containing all of the categories that are to be kept after filtering the desired input data.

        :param excludelist: A list containing all of the categories that are to be excluded after the filtering desired input data.

        :returns varcats: A dictionary containing all of the categories in the desired data.

        :returns varunits: A dictionary containing all of the units of the desired data.

        :returns varlabels: A dictionary containing all of the labels that will be used for plotting the desired data.

        :returns varsave: A dictionary containing all of the string values that will be used for saving files and figures of the desired data.
    """

    colnames = metdat.columns

    temp = [
        x.split(' (')[0].lower() if '(u)' not in x and '(v)' not in x
        and '(w)' not in x else x.split(') (')[0].lower() + ')'
        for x in colnames
    ]
    temp = set(temp)
    temp = list(temp)

    # remove unwanted fields
    if excludelist is not None:
        if excludelist is True:
            excludelist = categories_to_exclude()
        for excl in excludelist:
            for x in temp:
                if excl.lower() in x.lower():
                    ind = temp.index(x)
                    temp.pop(ind)
        temp.sort()

    # or keep only a select list
    if keeplist is not None:
        if keeplist is True:
            keeplist = categories_to_keep()
        temp = list(set(temp).intersection(keeplist))
        temp.sort()

    varcats = {
        cat: [x for x in colnames if x.lower().split(cat)[0] == '']
        for cat in temp
    }

    varcats['speed'] = [x for x in varcats['speed'] if 'speed (' in x.lower()]
    # varcats['dissipation rate'] = [x for x in varcats['dissipation rate'] if 'sf' not in x.lower()]
    varcats['ti'] += [x for x in colnames if 'cup equivalent ti' in x.lower()]

    # units
    units = get_units()
    varunits = {
        cat: v
        for cat in varcats for x, v in units.items()
        if x.title() in cat.title()
    }

    # labels for plotting
    varlabels = {x: x.title() + ' ' + varunits[x] for x in varcats}
    # a few ad hoc corrections
    varlabels[
        'coherent tke'] = 'Coherent TKE ' + varunits['turbulent kinetic energy']
    varlabels[
        'turbulent kinetic energy'] = 'TKE ' + varunits['turbulent kinetic energy']
    varlabels['direction'] = 'Wind ' + varlabels['direction']
    varlabels['speed'] = 'Wind ' + varlabels['speed']
    varlabels['stability parameter z/l'] = 'Stability Parameter z/L [--]'
    varlabels['ti'] = 'TI [%]'

    # strings for saving files and figures
    varsave = {x: x.replace(' ', '_').replace('/', '') for x in varcats}

    return varcats, varunits, varlabels, varsave


###########################################


###########################################
def get_catinfo(metdat):
    """
    Get categorical information of the data.

    This function takes the contents of the pandas DataFrame containing all of the data from a desired input data file and returns a set containing all of the categories, units, labels for plotting, and strings for saving files and figures.

        :param metdat: A pandas DataFrame containing all of the requested data extracted from the input files.

        :returns catinfo: A set containing all of the categories, units, labels for plotting, and strings for saving files and figures for the desired data.
    """

    varcats, varunits, varlabels, varsave = categorize_fields(
        metdat, keeplist=True)

    catinfo = {}
    catinfo['columns'] = varcats
    catinfo['units'] = varunits
    catinfo['labels'] = varlabels
    catinfo['save'] = varsave

    return catinfo


###########################################


###########################################
def fix_data_for_transfer(metdat, fix_pressure=False):
    """
    Combined QC and filtering of 10-minute data for transfer to web server.

    parameters:
    metdat (pandas dataframe)

    outputs:
    metdat (filtered pandas dataframe)
    catinfo (dictionary)
        contains all categorical information about
    """
    ## get rid of columns that are 100% NaN
    metdat = drop_nan_cols(metdat)
    # simply applies Pandas DataFrame method:
    # metdat.dropna(axis=1,how='all', inplace=True)

    keepcols = categories_to_keep()
    keepcols = [
        col for col in metdat.columns if col.split(' (')[0].lower() in keepcols
        if '.1' not in col
    ]
    dropcols = [col for col in metdat.columns if col not in keepcols]

    metdat.drop(dropcols, axis=1, inplace=True)

    metdat = qc_mask(metdat)

    ## flag data by stability class
    stabconds, stabcat = flag_stability(metdat)

    ## group columns based on category, assign units, labels, savenames
    varcats, varunits, varlabels, varsave = categorize_fields(
        metdat, keeplist=True)

    ## drop columns not in any of the categories, filter TI, temperature, stability parameters
    groom_data(metdat, varcats)

    ## Finally, reject outliers more than 5 standard deviations from the mean
    for col in metdat.columns:
        try:
            metdat[col] = reject_outliers(metdat[col], m=6)
        except:
            continue

    catinfo = {}
    catinfo['columns'] = varcats
    catinfo['units'] = varunits
    catinfo['labels'] = varlabels
    catinfo['save'] = varsave

    if fix_pressure:
        metdat = fix_pressure_data(metdat, catinfo)

    return metdat, catinfo


###########################################

###########################################
# auxiliary functions
###########################################


###########################################
def categories_to_exclude():
    """
    Define categories to exclude for filtering.

    This function does not take in any inputs but does output a list containing all of the categories that are chosen to be excluded from the desired input data.

        :param: None.

        :returns excats: A list containing all of the categories that are chosen to be excluded from the desired input data.
    """

    excats = [
        'advection', 'angle', 'boom', 'equivalent', 'Log-Law',
        'Preciptation Sensor', 'peak', 'record', 'spectral', 'kaimal',
        'speed U', 'SF_', 'std. dev.', 'surface', '*', 'structure', 'total',
        'zero-crossing', 'sigma', 'd(t)', 'Virtual', 'Brunt', 'height',
        'sigma', 'version', 'sensible', 'potential',
        'zero-crossing integral length scale (u)', 'peak coherent', '(SF_',
        'zero-crossing', 'boom', 'speed u', 'valid', 'kaimal', 'peak downward',
        'peak upward', 'velocity structure'
    ]
    return excats


###########################################


###########################################
def categories_to_keep():
    """
    Define categories to keep for filtering.

    This function does not take in any inputs but does output a list containing all of the categories that are chosen to be included from the desired input data.

        :param: None.

        :returns keepcats: A list containing all of the categories that are chosen to be included from the desired input data.
    """

    keepcats = [
        'air density',
        'air pressure',
        'air temperature',
        'coherent tke',
        # 'cov(u_w)',
        # 'cov(w_t)',
        'direction',
        #  'dissipation rate',
        'gradient richardson',
        #  'integral length scale (u)',
        #  'integral length scale (v)',
        #  'integral length scale (w)',
        # "mean(w't')",
        # 'momentum flux',
        'monin-obukhov length',
        'relative humidity',
        'speed',
        # 'speed gradient richardson',
        'stability flag',
        'stability parameter z/l',
        'ti',
        'turbulent kinetic energy',
        'wind shear',
        'wind veer'
    ]
    return keepcats


###########################################


###########################################
def get_units():
    """
    Get units for the data.

    This function does not take in any inputs but does output a dictionary containing all of the units of the desired input data.

        :param: None.

        :returns units: A dictionary containing all of the units of the desired input data.
    """

    units = {
        'density': r'[kg/m$^3$]',
        'pressure': r'[mbar]',
        'temperature': r'[$^\circ C$]',
        'tke': r'[m$^2$/s$^2$]',
        'direction': r'[$^\circ$]',
        'dissipation': r'[m$^2$/s$^3$]',
        'richardson': r'[--]',
        'length': r'[m]',
        'humidity': r'[%]',
        'speed': r'[m/s]',
        'stability parameter z/l': r'[--]',
        'ti': r'[%]',
        'turbulent kinetic energy': r'[m$^2$/s$^2$]',
        'shear': r'[--]',
        'veer': r'[$^\circ$]',
        'flag': r'[--]'
    }
    return units


###########################################


###########################################
def make_datetime_vector(filename, span=10, freq=20.0):
    """
    Generate a time range for the data.

    This function takes inputs from filenames of the form ‘%m_%d_%y_%H_%M_%S_%U.mat' of the desired span and frequency of data and generates a vector for the date and time for the data.

        :param filename: A string denoting the desired file name for the input data.

        :param span: An integer value used to define the span of the data included in the filename (Minutes).

        :returns timerange: A pandas DatetimeIndex value used to define the range of times with which the data covers.
    """

    # caluclate number of data (periods) in file
    periods = int(span * 60 * freq)

    # format frequency as a string denoting resolution in microseconds
    freq = '{}U'.format(int(1000000 / freq))

    # make start time as datetime.datetime from filename
    starttime = list(map(int, filename.strip('.mat').split('_')))
    starttime = dt.datetime(starttime[2], starttime[0], starttime[1],
                            starttime[3], starttime[4], starttime[5])

    # get timerange as vector of datetimes
    timerange = pd.date_range(start=starttime, periods=periods, freq=freq)

    return timerange


###########################################


###########################################
# Begin sections of code for IEC event detection
###########################################
def make_dataframe_for_height(inputdata,
                              timerange,
                              probeheight=74,
                              include_UTC=False):
    """
    Generate a DataFrame based on the probe height.

    This function takes inputs from desired input data and returns a pandas DataFrame containing all of the desired data at the given probe height including wind speed, wind direction, and the date and timestamps of the input data.

        :param inputdata: A dictionary containing all of the desired input data.

        :param timerange: A pandas DatetimeIndex value used to define the range of times with which the data covers.

        :param probeheight: An integer or float value used to define the desired height of the probe from which to begin data analysis (m).

        :param include_UTC: A Boolean value used to determine whether or not an UTC timestamp is desired of the form ‘time_UTC’.

        :returns sonicdat: A pandas DataFrame containing all of the desired data at the given probe height including wind speed, wind direction, and the date and timestamps of the input data.
    """

    # select all variables at a given height
    varnames = list(inputdata.keys())
    varnames = [var for var in varnames if str(probeheight) in var]
    # get windspeed variable
    temp = [var for var in varnames if 'WS' in var]
    temp.extend([var for var in varnames if 'CupEqHorizSpeed' in var])
    # get winddirection variable
    temp.extend([var for var in varnames if 'WD' in var])
    temp.extend([var for var in varnames if 'direction' in var])
    # include the UTC time
    if include_UTC is True:
        temp.append('time_UTC')

    # get variables of interest into a new dict
    sonicdat = {var: inputdata[var][0][0][0].squeeze() for var in temp}
    # make a Pandas DataFrame
    sonicdat = pd.DataFrame.from_dict(sonicdat)
    # setup datetime index
    sonicdat['datetime'] = pd.to_datetime(timerange[0:len(sonicdat.index)])
    sonicdat.set_index('datetime', inplace=True)
    # sonicdat.index.to_datetime()

    sonicdat = sonicdat.rename(
        index=str, columns={
            temp[0]: 'WS',
            temp[1]: 'WD'
        })

    return sonicdat


###########################################


###########################################
def setup_IEC_params(probeheight=100):
    """
    Establish IEC parameters.

    This function takes inputs from a pandas DataFrame containing all of the desired data at the given probe height and establishes all of the International Electrotechnical Commission (IEC) parameters for the given input data and probe height.

        :param sonicdat: A pandas DataFrame containing all of the desired data at the given probe height including wind speed, wind direction, and the date and timestamps of the input data.

        :param probeheight: An integer or float value used to define the desired height of the probe from which to begin data analysis (m).

        :returns params: A dictionary containing all of the parameters established by the IEC for the given input data and probe height.
    """

    ### quantities of interest for IEC
    # turbulence estimate over period, standard deviation of cupspeed
    # filter wind directions that cross the 360/0 threshold
    #     if sonicdat['WD'].mean() > 180:
    #         sonicdat.loc[sonicdat['WD'] < 100, 'WD'] += 360
    #     else:
    #         sonicdat.loc[sonicdat['WD'] > 350, 'WD'] += -360

    params = {'turbclass': 'IA'}

    # dummy vertical coordinate
    params['z'] = np.linspace(0, 135, 136)
    # dummy velocity span
    params['z'] = np.linspace(0, 40, 120)

    ######## parameters
    ### IEC parameters

    # Based on IEC Class IA
    params['Vref'] = 50.0  #m/s
    params['Iref'] = 0.16  # turbulence intensity
    # 'average' velocity
    params['Vave'] = 0.2 * params['Vref']
    # shear exponent
    params['alpha'] = 0.2
    # longitudinal turbulence scale parameter
    if probeheight < 60:
        params['Lambda_1'] = 0.7 * probeheight  # m
    else:
        params['Lambda_1'] = 42  # m

    # shear exponent
    params['alpha'] = 0.2
    params['beta'] = 6.4

    ### data parameters
    # NREL GE1.5MW rotor diameter
    params['D'] = 80
    # sampling frequency
    params['freq'] = 20  # Hz
    # probe height
    params['probeheight'] = probeheight
    ### normal wind profile model
    params['zhub'] = 80  # m
    # 'hub' height velocity (really just mean probe velocity)
    #     params['vhub'] = sonicdat['WS'].mean()  # m/s
    # dummy vertical coordinate
    #     params['z'] = np.linspace(0, 120, 120)
    #     # standard normal velocity profile
    #     params['vprofile'] = params['vhub'] * (
    #         params['z'] / params['zhub'])**params['alpha']
    #     params['sigma_data'] = sonicdat['WS'].std()

    ### Normal Wind speed distributions
    # dummy velocity data
    params['vrange'] = np.linspace(0, params['Vref'], 100)
    # velocity probability density function
    params['pdf'] = params['vrange']/(params['Vave']**2)* \
        np.exp(-np.pi*params['vrange']**2/(np.sqrt(2)*params['Vave']**2))
    # velocity cumulative probability density function
    params['cdf'] = 1.0 - np.exp(
        -np.pi * (params['vrange'] / (2 * params['Vave']))**2)

    # Extreme wind speed model (EWM)
    params['Ve50'] = 1.4 * params['Vref'] * (
        params['probeheight'] / params['zhub'])**(0.11)
    params['Ve01'] = 0.8 * params['Ve50']

    return params


###########################################


###########################################
def find_EWM_events(sonicdat, params):
    """
    Find extreme wind speed events.

    This function takes inputs from a pandas DataFrame containing all of the desired data and International Electrotechnical Commission (IEC) parameters at the given probe height, determines extreme wind speed events, and returns the findings in lists separating one-year and 50-year events. These lists will be concatenated to a larger list which will be used to index files later.

        :param sonicdat: A pandas DataFrame containing all of the desired data at the given probe height including wind speed, wind direction, and the date and timestamps of the input data.

        :param params: A dictionary containing all of the parameters established by the IEC for the given input data and probe height.

        :returns Ve01eventfound: A list of all the extreme wind events higher than within the past year.

        :returns Ve50eventfound: A list of all the extreme wind events higher than within the past 50 years.
    """

    # Compare extreme wind speeds to data
    # extract df of events
    Ve50eventfound = sonicdat[sonicdat['WS'] > params['Ve50']]
    Ve01eventfound = sonicdat[sonicdat['WS'] > params['Ve01']]

    return Ve01eventfound, Ve50eventfound


###########################################


###########################################
def find_EOG_events(sonicdat, params, T=10.5):
    """
    Find extreme operating wind gust events.

    This function takes inputs from a pandas DataFrame containing all of the desired data and International Electrotechnical Commission (IEC) parameters at the given period for search, determines extreme operating wind gust events, and returns the findings in an object which can be used to index files later.

        :param sonicdat: A pandas DataFrame containing all of the desired data at the given probe height including wind speed, wind direction, and the date and timestamps of the input data.

        :param params: A dictionary containing all of the parameters established by the IEC for the given input data and probe height.

        :param T: A float used to define the period for search (Seconds).

        :returns EOGeventfound: An object used to store any significant extreme operating wind gust events.
    """
    # resample at T seconds
    sonic_10_5s = sonic_data_resampler(sonicdat, T)

    sonic_10_5s['WS_mean'] = sonic_10_5s.WS_mean.resample('10T').mean()
    try:
        sonic_10_5s['WS_mean'].interpolate('nearest')
    except:
        return pd.DataFrame()
    # calc IEC standard velocity variance
    sigma_1 = params['Iref'] * (0.75 * sonic_10_5s['WS_mean'] + 5.6)

    test1 = 1.35 * (params['Ve01'] - sonic_10_5s['WS_mean'])
    test2 = 3.3 * (sigma_1 / (1 + 0.1 * params['D'] / params['Lambda_1']))

    # IEC gust velocity magnitude threshold
    Vgust = np.min(np.vstack([test1.values, test2.values]), axis=0)

    t = np.linspace(0, T, 101)
    WS_pos_gustlim = np.zeros(Vgust.shape)
    WS_neg_gustlim = np.zeros(Vgust.shape)
    for ii, vv in enumerate(Vgust):
        mod = 0.37 * vv * np.sin(
            3 * np.pi * t / T) * (1 - np.cos(2 * np.pi * t / T))
        WS_pos_gustlim[ii] = sonic_10_5s['WS_mean'].iloc[ii] - mod.min()
        WS_neg_gustlim[ii] = sonic_10_5s['WS_mean'].iloc[ii] - mod.max()

    sonic_10_5s['WS_pos_gustlim'] = WS_pos_gustlim
    sonic_10_5s['WS_neg_gustlim'] = WS_neg_gustlim

    posmask = sonic_10_5s['WS_max'] > sonic_10_5s['WS_pos_gustlim']
    negmask = sonic_10_5s['WS_min'] < sonic_10_5s['WS_neg_gustlim']

    # test for EOG events (pos or pos+neg)
    singletest = sonic_10_5s[posmask]
    # doubletest = sonic_10_5s[posmask & negmask]

    return singletest  #, doubletest


###########################################


###########################################
def find_ETM_events(sonicdat, params):
    """
    Find extreme turbulence model events.

    This function takes inputs from a pandas DataFrame containing all of the desired data and International Electrotechnical Commission (IEC) parameters at the given period for search, determines extreme turbulence model events, and returns the findings in an object which can be used to index files later.

        :param sonicdat: A pandas DataFrame containing all of the desired data at the given probe height including wind speed, wind direction, and the date and timestamps of the input data.

        :param params: A dictionary containing all of the parameters established by the IEC for the given input data and probe height.

        :returns ETMeventfound: An object used to store any significant extreme turbulence model events.
    """

    # Extreme turbulence model
    tmp = sonic_data_resampler(sonicdat, 600)

    c = 2  # m/s
    tmp['sigmatest'] = c * params['Iref'] * (
        0.072 * (params['Vave'] / c + 3) *
        (sonicdat['WS'].resample('10T').mean() / c + 4) + 10)
    tmp['sigma_1'] = sonicdat['WS'].resample('10T').std()

    ETM_events_found = tmp[tmp['sigma_1'] > tmp['sigmatest']]

    return ETM_events_found


###########################################


###########################################
def find_EDC_events(sonicdat, params, T=6):
    """
    Find extreme wind direction change events.

    This function takes inputs from a pandas DataFrame containing all of the desired data and International Electrotechnical Commission (IEC) parameters at the given period for search, determines extreme wind direction change events, and returns the findings in an object which can be used to index files later.

        :param sonicdat: A pandas DataFrame containing all of the desired data at the given probe height including wind speed, wind direction, and the date and timestamps of the input data.

        :param params: A dictionary containing all of the parameters established by the IEC for the given input data and probe height.

        :param T: A float used to define the period for search (Seconds).

        :returns EDCeventfound: An object used to store any significant extreme wind direction change events.
    """

    # Resample data at 6 second period
    sonic_6s = sonic_data_resampler(sonicdat, 6)

    # turbulence standard dev from IEC def.
    sonic_6s['sigma_1'] = params['Iref'] * (0.75 * sonic_6s['WS_mean'] + 5.6)

    # Maximum allowable change in wind direction over a 6 second period
    sonic_6s['delta_WD_thresh'] = np.degrees(4 * np.arctan(
        sonic_6s['sigma_1'] / (sonic_6s['WS_mean'] *
                               (1 + 0.1 * params['D'] / params['Lambda_1']))))

    # recorded wind direction change in 6 second period
    sonic_6s['delta_WD'] = np.abs(sonic_6s['WD_max'] - sonic_6s['WD_min'])

    sonic_6s['delta_WD'][
        sonic_6s['delta_WD'] >
        180] = 360 - sonic_6s['delta_WD'][sonic_6s['delta_WD'] > 180]

    EDC_events_found = sonic_6s[(sonic_6s['delta_WD'] >
                                 sonic_6s['delta_WD_thresh'])]

    return EDC_events_found


###########################################


###########################################
def find_ECD_events(sonicdat, params, T=10):
    """
    Find extreme coherent wind gust with wind direction change events.

    This function takes inputs from a pandas DataFrame containing all of the desired data and International Electrotechnical Commission (IEC) parameters at the given period for search, determines extreme coherent wind gust with wind direction change events, and returns the findings in an object which can be used to index files later.

        :param sonicdat: A pandas DataFrame containing all of the desired data at the given probe height including wind speed, wind direction, and the date and timestamps of the input data.

        :param params: A dictionary containing all of the parameters established by the IEC for the given input data and probe height.

        :param T: A float used to define the period for search (Seconds).

        :returns ECDeventfound: An object used to store any significant extreme coherent wind gust with wind direction change events.
    """

    # Extreme coherent gust with direction change (ECD)

    Vcg = 15  # m/s See IEC standards

    # resample sonic data at 10 s
    sonic_10s = sonic_data_resampler(sonicdat, 10)

    sonic_10s['WS_mean'] = sonic_10_5s.WS_mean.resample('10T').mean()
    try:
        sonic_10s['WS_mean'].interpolate('nearest')
    except:
        return pd.DataFrame()

    theta_cg = pd.Series(
        index=sonic_10s.index, data=180 * np.ones(len(sonic_10s.index)))
    theta_cg[sonic_10s['WS_mean'] >
             4.0] = 720.0 / sonic_10s['WS_mean'][sonic_10s['WS_mean'] > 4.0]

    sonic_10s['delta_WD'] = sonic_10s['WD_mean'].diff(periods=2)
    sonic_10s['delta_WS'] = sonic_10s['WS_mean'].diff(periods=2)

    ECDeventfound = sonic_10s[(sonic_10s['delta_WD'] > theta_cg)
                              & (sonic_10s['delta_WS'] > 0.5 * Vcg)]

    return ECDeventfound


###########################################


###########################################
def find_EWS_events(sonicdat,
                    sonicdat_lo,
                    sonicdat_hi,
                    params,
                    alpha_neg,
                    alpha_pos,
                    alpha_reference_velocity,
                    T=12):
    """
    Find extreme coherent wind shear events.

    This function takes inputs from a pandas DataFrame containing all of the desired data and International Electrotechnical Commission (IEC) parameters at the given period for search, determines extreme coherent wind shear events, and returns the findings in an object which can be used to index files later.

        :param sonicdat_lo: A pandas DataFrame containing data at the given probe height including wind speed, wind direction, and the date and timestamps of the input data.

        :param sonicdat_hi: A pandas DataFrame containing all of the desired data at the given probe height including wind speed, wind direction, and the date and timestamps of the input data.

        :param params: A dictionary containing all of the parameters established by the IEC for the given input data and probe height.

        :param T: A float used to define the period for search (Seconds).

        :returns EWSeventfound: An object used to store any significant extreme wind shear events.
    """

    alpha = np.log(sonicdat_hi / sonicdat_lo) / np.log(122 / 38)
    alpha.index = pd.DatetimeIndex(alpha.index)

    tmp = pd.concat(
        [
            alpha.resample('12S').min(),
            alpha.resample('12S').max(),
            alpha.resample('12S').mean()
        ],
        axis=1)
    tmp.columns = ['alpha_min', 'alpha_max', 'alpha_mean']

    # resample sonic data at 12 s
    sonic_12s = sonic_data_resampler(sonicdat, 12)

    # add shear calc to dataframe
    shearevents = pd.concat([sonic_12s, tmp], axis=1)

    # add limits of shear exponent based on vhub
    shearevents['alpha_pos_limit'] = np.interp(
        shearevents['WS_mean'], alpha_reference_velocity, alpha_pos)
    shearevents['alpha_neg_limit'] = np.interp(
        shearevents['WS_mean'], alpha_reference_velocity, alpha_neg)

    # create mask to identify valid extreme events
    vhub_mask = shearevents['WS_mean'] > alpha_reference_velocity.min()
    aneg_mask = shearevents['alpha_min'] < shearevents['alpha_neg_limit']
    apos_mask = shearevents['alpha_max'] > shearevents['alpha_pos_limit']

    # identify extreme shear events (EWS)
    EWS_event_found = shearevents[vhub_mask & (aneg_mask | apos_mask)]

    return EWS_event_found


###########################################


###########################################
def sonic_data_resampler(sonicdat, T):
    '''
    [summary]

    Parameters
    ----------
    sonicdat : [type]
        [description]
    T : [type]
        [description]

    Returns
    -------
    [type]
        [description]
    '''
    mins = sonicdat.resample('{}S'.format(T)).min()
    mins.columns = ['{}_min'.format(x) for x in mins.columns]

    maxs = sonicdat.resample('{}S'.format(T)).max()
    maxs.columns = ['{}_max'.format(x) for x in maxs.columns]

    means = sonicdat.resample('{}S'.format(T)).mean()
    means.columns = ['{}_mean'.format(x) for x in means.columns]

    sonic_resample = pd.concat([mins, maxs, means], axis=1)

    return sonic_resample


###########################################
