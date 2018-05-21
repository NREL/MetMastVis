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
def make_dataframe_for_height(inputdata, timerange, probeheight=74):
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
    # include the UTC time
    varnames.append('time_UTC')
    
    # get variables of interest into a new dict
    sonicdat = {var: inputdata[var][0][0][0].squeeze() for var in varnames}
    # make a Pandas DataFrame
    sonicdat = pd.DataFrame.from_dict(sonicdat)
    # setup datetime index
    sonicdat['datetime'] = timerange[0:len(sonicdat.index)]
    sonicdat.set_index('datetime', inplace=True)
    sonicdat.index.to_datetime()
    
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
    # cup-equivalent horizontal wind speed 
    cupspeed = sonicdat['Sonic_CupEqHorizSpeed_{}m'.format(probeheight)]
    # turbulence estimate over period, standard deviation of cupspeed
    sigma_data = np.std(cupspeed)
    # wind direction from sonic data channels
    winddir = sonicdat['Sonic_direction_{}m'.format(probeheight)]
    # filter wind directions that cross the 360/0 threshold
    if winddir.mean() > 180:
        winddir[winddir<10] = winddir[winddir<10]+360
    else:
        winddir[winddir<350] = winddir[winddir<350]-360
    
    ######## parameters
    ### IEC parameters
    params = {'turbclass': 'IA'}
    # Based on class IA
    params['Vref'] = 50 #m/s
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
    params['vhub'] = cupspeed.mean() # m/s
    # dummy vertical coordinate
    params['z'] = np.linspace(0,120,120)
    # standard normal velocity profile
    params['vprofile'] = params['vhub']*(params['z']/params['zhub'])**params['alpha']
    
    ### Normal Wind speed distributions
    # dummy velocity data
    params['vrange'] = np.linspace(0,params['Vref'],100)
    # velocity probability density function
    params['pdf'] = params['vrange']/(params['Vave']**2)* \
        np.exp(-np.pi*params['vrange']**2/(np.sqrt(2)*params['Vave']**2))
    # velocity cumulative probability density function
    params['cdf'] = 1.0-np.exp(-np.pi* (params['vrange']/(2*params['Vave']))**2)
    
    
    return cupspeed, winddir, sigma_data, params
###########################################

###########################################
def find_EWM_events(cupspeed, params):
    """
    look for extreme wind speed events,
    if found, return True, will be used to index files later
    """
    # Extreme wind speed model (EWM)
    Ve50 = 1.4*params['Vref']*(params['z']/params['zhub'])**(0.11)
    Ve01 = 0.8*Ve50

    # Compare extreme wind speeds to data
    # if an extreme event occurs, append filename to list
    Ve50test = cupspeed[cupspeed > Ve50[params['probeheight']]]
    if len(Ve50test) > 0:
        Ve50eventfound = [cupspeed.index[0]]
    else:
        Ve50eventfound = []
        
    Ve01test = cupspeed[cupspeed > Ve01[params['probeheight']]]
    if len(Ve01test) > 0:
        Ve01eventfound = [cupspeed.index[0]]
    else:
        Ve01eventfound = []
    
    return Ve01eventfound, Ve50eventfound
###########################################


###########################################
def find_EOG_events(cupspeed, params):
    """
    look for extreme operating gust events,
    if found, return True, will be used to index files later
    """
    # Extreme operating gust (EOG)
    Ve50 = 1.4*params['Vref']*(params['z']/params['zhub'])**(0.11)
    Ve01 = 0.8*Ve50
    T = 10.5 # seconds
    t = np.linspace(0,T,100)

    # Compare maximum gust speed to data
    # if an extreme events occurs, append time to list
    EOGeventfound = []
    for itime, tempdir in cupspeed.iloc[::int(T*params['freq'])].items():
        starttime = itime
        endtime = starttime + dt.timedelta(seconds=T) # starttime + 6 seconds
        # extract 6 second slice of direction data
        vslice = cupspeed.loc[starttime:endtime]
        # standard velocity variance
        sigma_1 = params['Iref']*(0.75*vslice.mean() + 5.6)

        Vgust = np.min([1.35*(Ve01[params['zhub']]-vslice.iloc[0]), \
                    3.3*(sigma_1/(1+0.1*params['D']/params['Lambda_1']))])
        Vgust = vslice.iloc[0]-0.37*Vgust*np.sin(3*np.pi*t/T)*(1-np.cos(2*np.pi*t/T))
        
        # test 
        Vgusttest = vslice[vslice > Vgust.max()]
        # index times of EOG events
        if len(Vgusttest) > 0:
            EOGeventfound.append(starttime)
            
    return EOGeventfound
###########################################


###########################################
def find_ETM_events(cupspeed, sigma_data, params):
    """
    look for extreme turbulence model events,
    if found, return True, will be used to index files later
    """
    # Extreme turbulence model
    c = 2 # m/s
    sigmatest = c*params['Iref']*(0.072*(params['Vave']/c+3)*(params['vhub']/c+4)+10)

    # Compare maximum turbulence to data
    # if an extreme event occurs, append filename to list
    sigmatest = sigma_data > sigmatest
    ETMeventfound = []
    if sigmatest:
        ETMeventfound.append(cupspeed.index[0])
        
    return ETMeventfound
###########################################

###########################################
def find_EDC_events(cupspeed, winddir, params):
    """
    look for extreme direction change events,
    if found, return True, will be used to index files later
    """
    # Extreme direction change (EDC)
    
    T = 6 # seconds * sampling freq
    stride = int(T*params['freq'])
    
    # index times of EDC events
    EDCeventfound=[]
    for itime, tempdir in winddir.iloc[:-stride:stride].items():
        # timerange for search
        # extract 6 second slice of direction data
        starttime = itime
        endtime = starttime + dt.timedelta(seconds=T) # starttime + 6 seconds
        
        vslice = cupspeed.loc[starttime:endtime]
        tslice = winddir.loc[starttime:endtime]
        
        sigma_1 = params['Iref']*(0.75*vslice.mean() + 5.6)
        
        # Maximum allowable change in wind direction over a 6 second period
        theta_e = np.degrees(4*np.arctan(sigma_1/ \
                                     (vslice.iloc[0]*(1+0.1*params['D']/params['Lambda_1']))))
    
#         # test 
#         dirtest = tslice[np.abs(tslice-tempdir) > theta_e]

#         # append event times to output
#         if len(dirtest) > 0:
#             EDCeventfound.append(starttime)
            
        # test 
        if np.abs(tslice[starttime] - tslice[endtime]) > theta_e:
            EDCeventfound.append(starttime)
        
    # # if no EDC events found, set to false
    # if len(EDCeventfound)<1:
    #     EDCeventfound=False   
        
    return EDCeventfound
###########################################

###########################################
def find_ECD_events(cupspeed, winddir, params):
    """
    look Extreme coherent gust with direction change (ECD),
    if found, return True, will be used to index files later
    """
    # Extreme coherent gust with direction change (ECD)
    
    # extreme coherent gust velocity magnitude (delta)
    Vcg = 15 # m/s See IEC standards
    # rise time
    T = 10 # s 
    # 10 seconds at 20 Hz
    t = np.linspace(0,10,int(T*params['freq']))
    stride = int(T*params['freq'])
    
    # function forms of coherent gust velocity and direction
    # vzt = cupspeed[starttime] + 0.5*Vcg*(1-np.cos(np.pi*t/T))
    # thetat = winddir[starttime] + 0.5*Vcg*(1-np.cos(np.pi*t/T))

    # scan for ECD
    # index times of EDC events
    ECDeventfound=[]
    for itime, tempdir in cupspeed.iloc[:-stride:stride].items():
        # start and end times
        starttime = itime
        endtime = starttime + dt.timedelta(seconds=T) # starttime + 10 seconds
        # start and end velocities
        vstart = cupspeed.loc[starttime]
        vend = cupspeed.loc[endtime]

        # extreme  cohcerent gust velocity change
        V_ECD = vstart + Vcg
        # test for wind speed condition
        if vend >= V_ECD:
            # start and end directions
            dstart = winddir.loc[starttime]
            dend = winddir.loc[endtime]

            # extreme  cohcerent gust direction change
            if params['vhub'] < 4:
                theta_cg = 180 # degrees
            elif params['vhub'] < params['Vref']:
                theta_cg = 720/params['vhub'] # degrees
            
            # test for wind direction condition
            
            if np.abs(dend-dstart) > theta_cg:
                ECDeventfound.append(starttime)
        
    return ECDeventfound
###########################################


###########################################
def find_EWS_events(cupspeed, params):
    """
    look Extreme wind shear (EWS),
    if found, return True, will be used to index files later
    """
    # Extreme wind shear (EWS)

    # extreme coherent gust velocity magnitude
    Vcg = 15 # m/s
    # rise time
    T = 12 # s 
    # 12 seconds at 20 Hz
    t = np.linspace(0,T,int(T*params['freq']))
    stride = int(T*params['freq'])
    
    

    # # transient horizontal shear (not applicable in our data...)
    # v_horz_pos = vhub*(probeheight/zhub)**alpha + ((probeheight-zhub)/D)*(2.5 + 0.2*beta*sigma_1*(D/Lambda_1)**0.25)*(1-np.cos(np.pi*T/T))

    # scan for EWS
    EWSeventfound = []
    for itime, tempdir in cupspeed.iloc[:-stride:stride].items():
        starttime = itime
        endtime = starttime + dt.timedelta(seconds=T) # starttime + 10 seconds

        vslice = cupspeed.loc[starttime:endtime]
        sigma_1 = params['Iref']*(0.75*vslice.mean() + 5.6)
        
        extreme = ((params['probeheight']-params['zhub'])/params['D'])*\
            (2.5 + 0.2*params['beta']*sigma_1*(params['D']/params['Lambda_1'])**0.25)\
            *(1-np.cos(np.pi*T/T))

        # transient vertical shear
        v_vert_pos = vslice.iloc[0]*(params['probeheight']/params['zhub'])**params['alpha'] + extreme
        v_vert_neg = vslice.iloc[0]*(params['probeheight']/params['zhub'])**params['alpha'] - extreme
    
        # test
        vtest = vslice[(vslice > v_vert_pos) | (vslice < v_vert_neg)]

        if len(vtest) > 0:
            EWSeventfound.append(starttime)
    
    # if len(EWSeventfound) < 1:
    #     EWSeventfound = False
        
    return EWSeventfound
###########################################


