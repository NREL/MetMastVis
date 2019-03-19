import sys, os
import numpy as np
import pandas as pd
import scipy.io as sio

# met mast functions and utilities
sys.path.append('../')
import met_funcs as MET
# import vis as vis
import utils as utils
import pickle as pkl
import datetime
import time

###########################################
# paths (must mount volume smb://nrel.gov/shared/wind/WindWeb/MetData/135mData/)
towerID = 'M5'
metDataPath = '/Volumes/135mData/{}Twr/20Hz/mat/'.format(towerID)

savepath = '/Users/nhamilto/Documents/Wake_Dynamics/SiteChar/data/IEC_tmp'
try:
    os.makedirs(savepath)
except:
    pass

today = datetime.date.today()
figpath = '../figs_{}{}{}'.format(
    str(today.year),
    str(today.month).zfill(2),
    str(today.day).zfill(2))

try:
    os.makedirs(figpath)
except:
    pass


###########################################
def EDC_alt(sonicdat, params, T=6.0):
    # smoothsonic = sonicdat.rolling(60, min_periods=1).mean()
    tmp = MET.sonic_data_resampler(sonicdat, 6.0)

    # calculate diff: Delta_WD = WD_(t+1) - WD_(t-1)
    tmpa = tmp['WD_mean'].diff(periods=1)
    tmpb = tmp['WD_mean'].diff(periods=-1)
    tmp['deltaWD'] = tmpa - tmpb

    # Orient Delta_WD onto compass (i.e. change > 180 degrees corresponds to a change in the other direction)
    tmp.deltaWD[tmp.deltaWD > 180] = -360 + tmp.deltaWD[tmp.deltaWD > 180]
    tmp.deltaWD[tmp.deltaWD < -180] = 360 + tmp.deltaWD[tmp.deltaWD < -180]

    # Turbulence standard deviation depends on mean wind speed
    tmp['sigma_1'] = params['Iref'] * (0.75 * tmp['WS_mean'] + 5.6)

    # Direction change threshold depends on wind speed
    tmp['delta_WD_thresh'] = np.degrees(4 * np.arctan(
        tmp['sigma_1'] / (tmp['WS_mean'] *
                          (1 + 0.1 * params['D'] / params['Lambda_1']))))

    # event detection
    tmpEDC = tmp[(tmp['deltaWD'] > tmp['delta_WD_thresh'])
                 | (tmp['deltaWD'] < -tmp['delta_WD_thresh'])]

    return tmpEDC


###########################################

# years = [2016]  #
# months = [11]
# days = [int(a) for a in np.arange(1, 31.1, 1)]

years = [int(a) for a in np.arange(2012, 2019, 1)]  #
months = [int(a) for a in np.arange(1, 12.1, 1)]
days = [int(a) for a in np.arange(1, 31.1, 1)]

wskeys = [
    'Cup_WS_C1_130m', 'Cup_WS_122m', 'Cup_WS_C1_105m', 'Cup_WS_87m',
    'Cup_WS_C1_80m', 'Cup_WS_C1_55m', 'Cup_WS_38m', 'Cup_WS_C1_30m',
    'Cup_WS_10m', 'Cup_WS_3m', 'Sonic_CupEqHorizSpeed_119m',
    'Sonic_CupEqHorizSpeed_100m', 'Sonic_CupEqHorizSpeed_74m',
    'Sonic_CupEqHorizSpeed_61m', 'Sonic_CupEqHorizSpeed_41m',
    'Sonic_CupEqHorizSpeed_15m'
]

wdkeys = [
    'Vane_WD_122m', 'Vane_WD_87m', 'Vane_WD_38m', 'Vane_WD_10m', 'Vane_WD_3m',
    'Sonic_direction_119m', 'Sonic_direction_100m', 'Sonic_direction_74m',
    'Sonic_direction_61m', 'Sonic_direction_41m', 'Sonic_direction_15m'
]

# %%timeit
probeheight = str(87)
datakeys = [['time_UTC'], [x for x in wskeys if probeheight in x],
            [x for x in wdkeys if probeheight in x]]
datakeys = [item for sublist in datakeys for item in sublist]
keys = ['time', 'WS', 'WD']
datakeys = {key: value for key, value in zip(keys, datakeys)}

# extract variables needed for classificiation of IEC events
params = MET.setup_IEC_params()  # sonicdat, probeheight=100

yearmonth = []
for year in years:
    for month in months:
        yearmonth.extend([(year, month)])

for year, month in yearmonth:
    # timing switch
    start_time = time.time()

    # if (year == 2013) & (month in list((range(5)))):
    #     continue

    # begin empty dataframes for events
    Ve01events = pd.DataFrame()
    Ve50events = pd.DataFrame()
    EOGevents = pd.DataFrame()
    ETMevents = pd.DataFrame()
    EDCevents = pd.DataFrame()
    ECDevents = pd.DataFrame()
    EWSevents = pd.DataFrame()

    print('reading 20Hz data for {}/{}'.format(year, month))
    for day in days:
        datapath = os.path.join(metDataPath, str(year),
                                str(month).zfill(2),
                                str(day).zfill(2))

        # temp arrays for data i/o
        WS = np.array([])
        WD = np.array([])
        timedat = np.array([])
        mats = []

        try:
            filelist = os.listdir(datapath)
        except:
            print('data not found: {}'.format(datapath))
            continue

        for file in filelist:
            try:
                tmp = sio.loadmat(
                    os.path.join(datapath, file),
                    variable_names=datakeys.values())
                WS = np.append(WS, tmp[datakeys['WS']][0][0][0].flatten())
                WD = np.append(WD, tmp[datakeys['WD']][0][0][0].flatten())
                timedat = np.append(timedat,
                                    tmp[datakeys['time']][0][0][0].flatten())
            except:
                print('problem loading data: {}'.format(datapath))

        if len(WS) != len(WD):
            veclen = np.min((len(WS), len(WD)))
            WS = WS[0:veclen]
            WD = WD[0:veclen]
            timedat = timedat[0:veclen]

        metdat = pd.DataFrame(
            index=pd.DatetimeIndex(
                utils.matlab_datenum_to_python_datetime(timedat)),
            data=np.vstack((WS, WD)).T,
            columns=['WS', 'WD'])
        metdat.index.name = 'datetime'

        # replace 0 values with nans,
        # drop all nan values,
        # rolling average of 3 s
        metdat = metdat.replace(
            to_replace=0.0, value=np.NaN).dropna(how='any').rolling(
                60, min_periods=1).mean()

        ECD_events_found = MET.find_EOG_events(metdat, params)
        ECDevents = pd.concat([ECDevents, ECD_events_found])

    event_dict = {
        'Ve01events': Ve01events,
        'Ve50events': Ve50events,
        'EOGevents': EOGevents,
        'ETMevents': ETMevents,
        'EDCevents': EDCevents,
        'ECDevents': ECDevents,
        'EWSevents': EWSevents,
    }

    # detected extreme events
    for name, event in event_dict.items():
        if len(event) > 0:
            print('saving {} for {}/{}'.format(name, year, month))
            filename = '{}_{}_{}.csv'.format(name, year, month)
            savefile = os.path.join(savepath, filename)
            event.to_csv(savefile)

    print('time to load and process {}/{} = {} \n '.format(
        year, month,
        time.time() - start_time))
