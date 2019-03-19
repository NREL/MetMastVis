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

import time

# paths (must mount volume smb://nrel.gov/shared/wind/WindWeb/MetData/135mData/)
towerID = 'M5'
metDataPath = '/Volumes/135mData/{}Twr/20Hz/mat/'.format(towerID)

savepath = '/Users/nhamilto/Documents/Wake_Dynamics/SiteChar/data/IEC_4'
try:
    os.makedirs(savepath)
except:
    pass

# setup IEC parameters for NWTC
params = MET.setup_IEC_params()

# load some threshold data
alpha_pos = np.load(
    '/Users/nhamilto/Documents/Wake_Dynamics/SiteChar/data/pos_alpha_limit.npy'
)
alpha_neg = np.load(
    '/Users/nhamilto/Documents/Wake_Dynamics/SiteChar/data/neg_alpha_limit.npy'
)
alpha_reference_velocity = np.load(
    '/Users/nhamilto/Documents/Wake_Dynamics/SiteChar/data/alpha_reference_velocity.npy'
)

#### Detect over given date range
# time range
years = [int(a) for a in np.arange(2014, 2019, 1)]  #
months = [int(a) for a in np.arange(1, 12.1, 1)]
days = [int(a) for a in np.arange(1, 31.1, 1)]

# years = [2015]  #
# months = [1, 2, 3]
# days = [int(a) for a in np.arange(1, 31.1, 1)]

yearmonth = []
for year in years:
    for month in months:
        yearmonth.extend([(year, month)])

for year, month in yearmonth:
    # timing switch
    start_time = time.time()

    if (year == 2014) & (month in list((range(5)))):
        continueh

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

        # establish existence of directory
        try:
            fPaths = os.listdir(datapath)
        except:
            print('empty datapath: {}'.format(datapath))
            continue

        if len(fPaths) is 0:
            continue

        # make empty dataframe
        sonicdat = pd.DataFrame()
        sonicdat_lo = pd.DataFrame()
        sonicdat_hi = pd.DataFrame()

        for filenum, file in enumerate(fPaths):

            # load data
            try:
                data = sio.loadmat(os.path.join(
                    datapath, file))  #, variable_names=varnames)
                # print('data loaded from {}'.format(
                #     os.path.join(datapath, file)))
            except:
                # print('data not found? looks like you have some homework...')
                continue

            # make a vector of datetimes for the data
            try:
                timerange = utils.matlab_datenum_to_python_datetime(
                    data['time_UTC'][0][0][0].flatten())
            except:
                print('No time data channel, skipping file: {}'.format(
                    os.path.join(datapath, file)))
                continue

            tmp = MET.make_dataframe_for_height(
                data, timerange, probeheight=100)
            sonicdat = pd.concat((sonicdat, tmp))

            # tmp = MET.make_dataframe_for_height(
            #     data, timerange, probeheight=38)
            # sonicdat_lo = pd.concat((sonicdat_lo, tmp))

            # tmp = MET.make_dataframe_for_height(
            #     data, timerange, probeheight=122)
            # sonicdat_hi = pd.concat((sonicdat_hi, tmp))

        # 3 second rolling average
        sonicdat = sonicdat.rolling(60, center=True, min_periods=1).mean()
        sonicdat.index = pd.DatetimeIndex(sonicdat.index)

        # sonicdat_lo = sonicdat_lo['WS'].rolling(
        #     60, center=True, min_periods=1).mean()
        # sonicdat_hi = sonicdat_hi['WS'].rolling(
        #     60, center=True, min_periods=1).mean()

        # # look for extreme wind speed model events
        # Ve01eventfound, Ve50eventfound = MET.find_EWM_events(sonicdat, params)
        # Ve01events = pd.concat([Ve01events, Ve01eventfound])
        # Ve50events = pd.concat([Ve50events, Ve50eventfound])

        # # look for extreme operating gust events
        # EOGeventfound = MET.find_EOG_events(sonicdat, params)
        # EOGevents = pd.concat([EOGevents, EOGeventfound])

        # # look for extreme turbulence model events
        # ETMeventfound = MET.find_ETM_events(sonicdat, params)
        # ETMevents = pd.concat([ETMevents, ETMeventfound])

        # look for extreme direction change events
        EDCeventfound = MET.find_EDC_events(sonicdat, params)
        EDCevents = pd.concat([EDCevents, EDCeventfound])

        # look Extreme coherent gust with direction change events
        ECDeventfound = MET.find_ECD_events(sonicdat, params)
        ECDevents = pd.concat([ECDevents, ECDeventfound])

        # # look Extreme wind shear events
        # EWSeventsfound = MET.find_EWS_events(
        #     sonicdat, sonicdat_lo, sonicdat_hi, params, alpha_neg, alpha_pos,
        #     alpha_reference_velocity)
        # EWSevents = pd.concat([EWSevents, EWSeventsfound])

    ######### Save data!
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

    print('\n time to load and process {}/{} = {}'.format(
        year, month,
        time.time() - start_time))
