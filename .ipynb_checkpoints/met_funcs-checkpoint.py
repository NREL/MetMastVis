"""
family of functions and classes to be used in met tower data analysis
"""

import numpy as np
import pandas as pd
from calendar import monthrange, month_name
import datetime as dt
import pickle as pkl


####################################
# Data loading
####################################
def load_met_data(inputfiles, verbose=False):
    """

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
        if filecount==0:
            metdat = df_lo.copy()
        else:
            metdat = metdat.append(df_lo.copy())
        filecount += 1
        if verbose is True:
            print(fName)
    metdat.index = metdat.index.tz_localize('UTC').tz_convert('America/Denver')   

    # replace flagged value '-999.0' with nans
    metdat[metdat==-999.0] = np.nan

    return metdat
####################################

####################################
def load_met_data_alt(inputfiles, verbose=False):
    """
    alternate data load to avoid use of data parser lambda function
    """
    filecount = 0

    for fName in inputfiles:
        df_lo = pd.read_csv(fName,\
                            skiprows=[0,1,2,3,4,5],\
                            low_memory=False)
        if filecount==0:
            metdat = df_lo.copy()
            metdat.drop([0,1])
        else:
            df_lo.drop([0,1])
            metdat = metdat.append(df_lo.copy())
        filecount += 1
        if verbose is True:
            print(fName)

    metdat['Date'] = pd.to_datetime(metdat['Date'], errors='coerce', infer_datetime_format=True)
    metdat = metdat[metdat.Date.notnull()]
    metdat =  metdat.set_index('Date')

    # metdat.index = metdat.index.tz_localize('UTC').tz_convert('America/Denver')   

    temp = [name for name in list(metdat.columns.values) if ' QC' not in name]
    qcNames = [name for name in list(metdat.columns.values) if ' QC' in name]
    fNames = [name for name in temp if name + ' QC' in qcNames]
    
    metdat[fNames] = metdat[fNames].values.astype(np.float64)
    metdat[qcNames] = metdat[qcNames].values.astype(np.int32)

    if verbose is True:
        print('dtypes corrected')

    # replace flagged value '-999.0' with nans
    metdat[metdat==-999.0] = np.nan
    metdat.tz_localize('UTC').tz_convert('America/Denver')

    return metdat
####################################

####################################
# Data filtering
####################################
def drop_nan_cols(metdat):
    """
    Use columns with 'qc' suffix as a mask to filter data
    """
    
    temp = metdat.dropna(axis=1,how='all')

    return temp

    
###########################################

###########################################
def qc_mask(metdat):
    temp = [name for name in list(metdat.columns.values) if ' QC' not in name]
    qcNames = [name for name in list(metdat.columns.values) if ' QC' in name]
    fNames = [name for name in temp if name + ' QC' in qcNames]
    
    print('number of data columns:', len(fNames))
    print('number of QC columns:', len(qcNames))
    
    # initialize filtered dataframe with 'record', 'version'
    dfFilt = metdat[metdat.columns.values[[0,1]]].copy()
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
    Add a new set of columns denoting stability class based on 
    monin-obukhov length at various heights.
    """
    MOLcols = [col for col in metdat.columns if 'monin-obukhov length' in col.lower()]
    for col in MOLcols:
        # get probe height
        z = int(col.split('m')[0].split('(')[-1])

        # extract data from MetDat
        L = metdat[col].copy()
        categoriesIdx = {'Very Stable': (L>0) & (L<=200),
                        'Stable' : (L>200) & (L<=500),
                        'Neutral' : (L<-500) | (L>500),
                        'Unstable' : (L>=-500) & (L<-200),
                        'Very Unstable': (L>=-200) & (L<0)}

        # make new column
        newcolname = 'Stability Flag ({}m)'.format(z)
        metdat[newcolname] = np.nan
        for cat in categoriesIdx.keys():
            metdat.loc[categoriesIdx[cat],newcolname] = cat
    
    stabcat = {'stability flag': [x for x in metdat.columns if 'Stability Flag' in x]}
    stabconds = [x for x in categoriesIdx]
    
    return stabconds, stabcat
###########################################

###########################################
def groom_data(metdat, varcats):
    """
    drop columns not in any of the categories
    filter TI, temperature, stability parameters

    TODO: break out into separate functions? make more general?
    #, dropcols=True, filter=['ti','monin-obukhov length','temperature','gradient richarson']):
    """
    ## drop columns
    keepcols = [v  for x in varcats for v in varcats[x]]
    dropcols = [col for col in metdat.columns if col not in keepcols]
    metdat.drop(dropcols, axis=1, inplace=True)

    # filter TI to where wind speed >= 1 m/s
    for ii,_ in enumerate(varcats['speed']):
        metdat.loc[metdat[varcats['speed'][ii]]<1,varcats['ti'][ii]] = np.nan

    # filter obhukov length
    for col in varcats['monin-obukhov length']:
        metdat.loc[np.abs(metdat[col])>2000, col] = np.nan
        
    # filter sonic temperatures (kelvins vs degrees C)
    for col in varcats['air temperature']:
        metdat.loc[np.abs(metdat[col])>200, col] = metdat.loc[np.abs(metdat[col])>200, col]-273

    # filter gradient richardson number
    for col in varcats['gradient richardson']:
        metdat.loc[np.abs(metdat[col])>20, col] = np.nan

    print('number of columns after filtering: {}'.format(len(metdat.columns)))
###########################################

###########################################
def reject_outliers(data, m=5):
    return data[abs(data - np.mean(data)) < m * np.std(data)]
###########################################


###########################################
# Data organization
###########################################
def categorize_fields(metdat, keeplist=None, excludelist=None):
    """read categories from pandas dataframe of met mast data"""
    
    colnames = metdat.columns
    
    temp = [x.split(' (')[0].lower() if '(u)' not in x and '(v)' not in x and '(w)' not in x else x.split(') (')[0].lower() + ')' for x in colnames]
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
    
    varcats = {cat:[x for x in colnames if x.lower().split(cat)[0]==''] for cat in temp}
    
    varcats['speed'] = [x for x in varcats['speed'] if 'speed (' in x.lower()]
    varcats['dissipation rate'] = [x for x in varcats['dissipation rate'] if 'sf' not in x.lower()]
    varcats['ti'] += [x for x in colnames if 'cup equivalent ti' in x.lower()]
    
    # units
    units = get_units()
    varunits = {cat: v for cat in varcats for x,v in units.items() if x.title() in cat.title()}

    # labels for plotting
    varlabels = {x: x.title()+' '+ varunits[x] for x in varcats}
    # a few ad hoc corrections
    varlabels['turbulent kinetic energy'] = 'TKE'+ varunits['turbulent kinetic energy']
    varlabels['direction'] = 'Wind ' + varlabels['direction']
    varlabels['speed'] = 'Wind ' + varlabels['speed']
    varlabels[ 'stability parameter z/l'] =  'Stability Parameter z/L [--]'

    # strings for saveing files and figures
    varsave = {x: x.replace(' ','_').replace('/','') for x in varcats}
    
    return varcats, varunits, varlabels, varsave
    
########################################### 

########################################### 
def get_catinfo(metdat):
    """
    get and collect categorical info for met mast data
    """
    varcats, varunits, varlabels, varsave = categorize_fields(metdat, keeplist=True)

    catinfo = {}
    catinfo['columns'] = varcats
    catinfo['units'] = varunits
    catinfo['labels'] = varlabels
    catinfo['save'] = varsave

    return catinfo
########################################### 


###########################################
# auxiliary functions
###########################################     


###########################################
def categories_to_exclude():
    excats = ['advection',
              'angle',
              'boom',
              'equivalent',
              'Log-Law',
              'Preciptation Sensor',
              'peak',
              'record',
              'spectral',
              'kaimal',
              'speed U',
              'SF_',
              'std. dev.',
              'surface','*',
              'structure',
              'total',
              'zero-crossing',
              'sigma',
              'd(t)',
              'Virtual',
              'Brunt',
              'height',
              'sigma',
              'version',
              'sensible',
              'potential',
              'zero-crossing integral length scale (u)',
              'peak coherent',
              '(SF_','zero-crossing',
              'boom',
              'speed u',
              'valid',
              'kaimal',
              'peak downward',
              'peak upward',
              'velocity structure']
    return excats
###########################################

###########################################
def categories_to_keep():
    keepcats = ['air density',
                 'air pressure',
                 'air temperature',
                 'coherent tke',
                 # 'cov(u_w)',
                 # 'cov(w_t)',
                 'direction',
                 'dissipation rate',
                 'gradient richardson',
                 'integral length scale (u)',
                 'integral length scale (v)',
                 'integral length scale (w)',
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
                 'wind veer']
    return keepcats
###########################################

###########################################
def get_units():
    units = {'density': r'[kg/m$^3$]',
             'pressure': r'[mmHg]',
             'temperature': r'[$^\circ C$]',
             'tke':r'[m$^2$/s$^2$]',
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
             'flag': r'[--]'}
    return units
###########################################


###########################################
def make_datetime_vector(filename, span=10, freq=20.0):
    """
    Assumes the input is a string with format
        '%m_%d_%y_%H_%M_%S_%U.mat'
        and that each file represents 10 minutes worth of data at 20 Hz.
    Parameters
    ----------
    filename : str
    span : int 
        span in minutes of data included in filename
    freq : float
        frequency of data in Hz
    """
    # caluclate number of data (periods) in file
    periods = int(span*60*freq)
    
    # format frequency as a string denoting resolution in microseconds
    freq = '{}U'.format(int(1000000/freq))
    
    # make start time as datetime.datetime from filename
    starttime = list(map(int,filename.strip('.mat').split('_')))
    starttime = dt.datetime(starttime[2],starttime[0],starttime[1],
                                  starttime[3],starttime[4],starttime[5])
    
    # get timerange as vector of datetimes
    timerange = pd.date_range(start=starttime, periods=periods, freq=freq)
    
    return timerange
###########################################


###########################################
# Begin sections of code for IEC event detection
###########################################
def make_dataframe_for_height(inputdata, timerange, probeheight=74, include_UTC=False):
    """
    
    Parameters
    ----------
    inputdata : dict
    timerange : pandas.core.indexes.datetimes.DatetimeIndex
    probeheight : int
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
    sonicdat['datetime'] = timerange[0:len(sonicdat.index)]
    sonicdat.set_index('datetime', inplace=True)
    sonicdat.index.to_datetime()

    sonicdat = sonicdat.rename(index=str, columns={temp[0]:'WS', temp[1]:'WD'})

    return sonicdat
###########################################

###########################################
def setup_IEC_params(sonicdat, probeheight=100):
    """
    parameters
    ----------
    sonicdat : Pandas.DataFrame
        dataframe with at least
    probeheight : int, float
    """
    
    ### quantities of interest for IEC 
    # turbulence estimate over period, standard deviation of cupspeed
    # filter wind directions that cross the 360/0 threshold
    if sonicdat['WD'].mean() > 180:
        sonicdat.loc[sonicdat['WD'] < 100,'WD'] += 360
    else:
       sonicdat.loc[sonicdat['WD'] > 350,'WD'] += -360
    
    ######## parameters
    ### IEC parameters
    params = {'turbclass': 'IA'}
    # Based on IEC Class IA
    params['Vref'] = 50.0 #m/s
    params['Iref'] = 0.16 # turbulence intensity
    # 'average' velocity
    params['Vave'] = 0.2*params['Vref']
    # shear exponent
    params['alpha'] = 0.2
    # longitudinal turbulence scale parameter
    if probeheight < 60:
        params['Lambda_1'] = 0.7*probeheight # m
    else:
        params['Lambda_1'] = 42 # m
    # shear exponent
    params['alpha'] = 0.2
    params['beta'] = 6.4
    
    ### data parameters
    # NREL GE1.5MW rotor diameter
    params['D'] = 80
    # sampling frequency
    params['freq'] = 20 # Hz
    # probe height
    params['probeheight'] = probeheight
    ### normal wind profile model
    params['zhub'] = 80 # m
    # 'hub' height velocity (really just mean probe velocity)
    params['vhub'] = sonicdat['WS'].mean() # m/s
    # dummy vertical coordinate
    params['z'] = np.linspace(0,120,120)
    # standard normal velocity profile
    params['vprofile'] = params['vhub']*(params['z']/params['zhub'])**params['alpha']
    params['sigma_data'] = sonicdat['WS'].std()

    ### Normal Wind speed distributions
    # dummy velocity data
    params['vrange'] = np.linspace(0,params['Vref'],100)
    # velocity probability density function
    params['pdf'] = params['vrange']/(params['Vave']**2)* \
        np.exp(-np.pi*params['vrange']**2/(np.sqrt(2)*params['Vave']**2))
    # velocity cumulative probability density function
    params['cdf'] = 1.0-np.exp(-np.pi* (params['vrange']/(2*params['Vave']))**2)
    
    # Extreme wind speed model (EWM)
    params['Ve50'] = 1.4*params['Vref']*(params['probeheight']/params['zhub'])**(0.11)
    params['Ve01'] = 0.8*params['Ve50']

    return params
###########################################

###########################################
def find_EWM_events(sonicdat, params):
    """
    look for extreme wind speed events,
    events will be extracted from df and concatenated to 
    a larger  will be used to index files later
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
    look for extreme operating gust events,
    if found, return True, will be used to index files later
    
    Parameters
    ----------
    T: float, Period for search
    """

    t = np.linspace(0,T,100)

    # Compare maximum gust speed to data
    # if an extreme events occurs, append time to list
    EOGeventfound = pd.DataFrame()

    for itime in range(0,len(sonicdat),int(T*params['freq'])):
    # for itime, tempspeed in sonicdat['WS'].iloc[::int(T*params['freq'])].items():
        
        # extract 6 second slice of direction data
        vslice = sonicdat.iloc[itime:itime+int(T*params['freq'])]

        # standard velocity variance
        sigma_1 = params['Iref']*(0.75*vslice['WS'].mean() + 5.6)

        Vgust = np.min([1.35*(params['Ve01']-vslice['WS'].iloc[0]), \
                    3.3*(sigma_1/(1+0.1*params['D']/params['Lambda_1']))])
        Vgust = vslice['WS'].iloc[0]-0.37*Vgust*np.sin(3*np.pi*t/T)*(1-np.cos(2*np.pi*t/T))
        
        # test 
        Vgusttest = vslice[vslice['WS'] > Vgust.max()]
        # index times of EOG events
        if len(Vgusttest) > 0:
            temp = pd.DataFrame([[vslice['WS'].iloc[0],vslice['WS'].max(),vslice['WS'].min(),\
                                    vslice['WD'].iloc[0],vslice['WD'].max(),vslice['WD'].min()]], \
                                columns=['WS','WSmax','WSmin','WD','WDmax','WDmin'], index=vslice.index[0:1])
            EOGeventfound = pd.concat([EOGeventfound, temp])

    return EOGeventfound
###########################################


###########################################
def find_ETM_events(sonicdat, params):
    """
    look for extreme turbulence model events,
    if found, return True, will be used to index files later
    """
    # Extreme turbulence model
    c = 2 # m/s
    sigmatest = c*params['Iref']*(0.072*(params['Vave']/c+3)*(params['vhub']/c+4)+10)

    # Compare maximum turbulence to data
    # if an extreme event occurs, append filename to list
    sigmatest = params['sigma_data'] > sigmatest
    ETMeventfound = pd.DataFrame()
    if sigmatest:
        temp = pd.DataFrame([[sonicdat['WS'].iloc[0],sonicdat['WS'].max(),sonicdat['WS'].min(),\
                                    sonicdat['WD'].iloc[0],sonicdat['WD'].max(),sonicdat['WD'].min()]], \
                                columns=['WS','WSmax','WSmin','WD','WDmax','WDmin'], index=sonicdat.index[0:1])
        ETMeventfound = pd.concat([ETMeventfound, temp])
        
    return ETMeventfound
###########################################

###########################################     
def find_EDC_events(sonicdat, params, T = 6):
    """
    look for extreme direction change events,
    if found, return True, will be used to index files later
    """
    # seconds * sampling freq
    stride = int(T*params['freq'])
    
    # index times of EDC events
    EDCeventfound = pd.DataFrame()
    for itime in range(0,len(sonicdat),stride):
    # for itime, tempspeed in sonicdat['WS'].iloc[::int(T*params['freq'])].items():
        
        # extract 6 second slice of direction data
        vslice = sonicdat.iloc[itime:itime+stride]
        
        sigma_1 = params['Iref']*(0.75*vslice['WS'].mean() + 5.6)
        
        # Maximum allowable change in wind direction over a 6 second period
        theta_e = np.degrees(4*np.arctan(sigma_1/(vslice['WS'].iloc[0]*(1+0.1*params['D']/params['Lambda_1']))))
            
        # test 
        if np.abs(vslice['WD'].iloc[0] - vslice['WD'].iloc[stride-1]) > theta_e:
            temp = pd.DataFrame([[vslice['WS'].iloc[0],vslice['WS'].max(),vslice['WS'].min(),\
                                    vslice['WD'].iloc[0],vslice['WD'].max(),vslice['WD'].min()]], \
                                columns=['WS','WSmax','WSmin','WD','WDmax','WDmin'], index=vslice.index[0:1])
            EDCeventfound = pd.concat([EDCeventfound, temp])
        
    return EDCeventfound
###########################################

###########################################
def find_ECD_events(sonicdat, params, T = 10):
    """
    look Extreme coherent gust with direction change (ECD),
    if found, return True, will be used to index files later
    """
    # Extreme coherent gust with direction change (ECD)
    
    # extreme coherent gust velocity magnitude (delta)
    Vcg = 15 # m/s See IEC standards
    # T seconds at 20 Hz
    t = np.linspace(0,10,int(T*params['freq']))
    stride = int(T*params['freq'])
    
    # function forms of coherent gust velocity and direction
    # vzt = cupspeed[starttime] + 0.5*Vcg*(1-np.cos(np.pi*t/T))
    # thetat = winddir[starttime] + 0.5*Vcg*(1-np.cos(np.pi*t/T))

    # scan for ECD
    # index times of EDC events
    ECDeventfound = pd.DataFrame()
    for itime in range(0,len(sonicdat),stride):
    # for itime, tempspeed in sonicdat['WS'].iloc[::int(T*params['freq'])].items():
        
        # extract 6 second slice of direction data
        vslice = sonicdat.iloc[itime:itime+stride]

        # start and end velocities
        vstart = vslice['WS'].iloc[0]
        vend = vslice['WS'].iloc[stride-1]

        # extreme  cohcerent gust velocity change
        V_ECD = vstart + Vcg

        # test for wind speed condition
        if vend >= V_ECD:
            # start and end directions
            dstart = vslice['WD'].iloc[0]
            dend = vslice['WD'].iloc[stride-1]

            # extreme  cohcerent gust direction change
            if params['vhub'] < 4:
                theta_cg = 180 # degrees
            elif params['vhub'] < params['Vref']:
                theta_cg = 720/params['vhub'] # degrees
            
            # test for wind direction condition
            
            if np.abs(dend-dstart) > theta_cg:
                temp = pd.DataFrame([[vslice['WS'].iloc[0],vslice['WS'].max(),vslice['WS'].min(),\
                                    vslice['WD'].iloc[0],vslice['WD'].max(),vslice['WD'].min()]], \
                                columns=['WS','WSmax','WSmin','WD','WDmax','WDmin'], index=vslice.index[0:1])
                ECDeventfound = pd.concat([ECDeventfound, temp])
        
    return ECDeventfound
###########################################


###########################################
def find_EWS_events(sonicdat, params, T = 12):
    """
    look Extreme wind shear (EWS),
    if found, return True, will be used to index files later
    """
    # Extreme wind shear (EWS)

    # extreme coherent gust velocity magnitude
    Vcg = 15 # m/s
    # T seconds at 20 Hz
    t = np.linspace(0,T,int(T*params['freq']))
    stride = int(T*params['freq'])

    # # transient horizontal shear (not applicable in our data...)
    # v_horz_pos = vhub*(probeheight/zhub)**alpha + ((probeheight-zhub)/D)*(2.5 + 0.2*beta*sigma_1*(D/Lambda_1)**0.25)*(1-np.cos(np.pi*T/T))

    # scan for EWS
    EWSeventfound = pd.DataFrame()
    for itime in range(0,len(sonicdat),stride):

        # extract 6 second slice of direction data
        vslice = sonicdat.iloc[itime:itime+stride]
        
        sigma_1 = params['Iref']*(0.75*vslice['WS'].mean() + 5.6)
        
        extreme = ((params['probeheight']-params['zhub'])/params['D'])*\
            (2.5 + 0.2*params['beta']*sigma_1*(params['D']/params['Lambda_1'])**0.25)\
            *(1-np.cos(np.pi*T/T))

        # transient vertical shear
        v_vert_pos = vslice['WS'].iloc[0]*(params['probeheight']/params['zhub'])**params['alpha'] + extreme
        v_vert_neg = vslice['WS'].iloc[0]*(params['probeheight']/params['zhub'])**params['alpha'] - extreme
    
        # test
        vtest = vslice['WS'][(vslice['WS'] > v_vert_pos) & (vslice['WS'] < v_vert_neg)]

        if len(vtest) > 0:
            temp = pd.DataFrame([[vslice['WS'].iloc[0],vslice['WS'].max(),vslice['WS'].min(),\
                                    vslice['WD'].iloc[0],vslice['WD'].max(),vslice['WD'].min()]], \
                                columns=['WS','WSmax','WSmin','WD','WDmax','WDmin'], index=vslice.index[0:1])
            EWSeventfound = pd.concat([EWSeventfound, temp])
    
        
    return EWSeventfound
###########################################


