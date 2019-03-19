# coding: utf-8

# # Extreme events detection
#
# According to IEC standards there are 6 main classes of exteme events:
#
#     - Extreme wind speed model (EWM)
#     - Extreme operating gust (EOG)
#     - Extreme turbuelnce model (ETM)
#     - Extreme direction change (EDC)
#     - Extreme coherent gust wind direction change (ECD)
#     - Extreme wind shear (EWS)
#
# Each of these are to be quantified through the high resolution data, as they typically happen over a range of < 10s.

# In[1]:

# fundamentals
import os, sys
import numpy as np
import pandas as pd
import datetime
import scipy.io as sio
import pickle as pkl
import csv

# met mast functions and utilities
sys.path.append('/Users/nhamilto/Documents/Wake_Dynamics/SiteChar/coderepo/')
import met_funcs as MET
# import vis as vis
import utils as utils

#%%
# time range
# years  = [ int(a) for a in np.arange(2012,2019,1) ] #
# months = [ int(a) for a in np.arange(1,12.1,1) ]
# days = [int(a) for a in np.arange(1,31.1,1)]
##### uncomment these to load and search within specific dates
years = [2017]
months = [2]
days = [4]

# paths (must mount volume smb://nrel.gov/shared/wind/WindWeb/MetData/135mData/)
towerID = 'M5'
metDataPath = '/Volumes/135mData/{}Twr/20Hz/mat/'.format(towerID)

#%%
probeheight = 87

try:
    savepath = '/Users/nhamilto/Documents/Wake_Dynamics/SiteChar/data/IEC_2'
    os.makedirs(savepath)
except:
    pass

for year in years:
    for month in months:

        # begin empty lists for events
        # Ve01events = pd.DataFrame()
        # Ve50events = pd.DataFrame()
        # EOGevents = pd.DataFrame()
        # ETMevents = pd.DataFrame()
        # EDCevents = pd.DataFrame()
        # ECDevents = pd.DataFrame()
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
                continue

            if len(fPaths) is 0:
                continue

            for filenum, file in enumerate(fPaths):

                # load data
                try:
                    data = sio.loadmat(os.path.join(
                        datapath, file))  #, variable_names=varnames)
                except:
                    continue

                # if data is not complete, move on. No need to fight here.
                ndat = 10 * 60 * 20  # minutes*seconds/minute*samples/second
                if len(data['Sonic_CupEqHorizSpeed_100m'][0][0][0]
                       .flatten()) != 12000:
                    continue

                # make a vector of datetimes for the data
                timerange = utils.matlab_datenum_to_python_datetime(
                    data['time_UTC'][0][0][0].flatten())

                # make a dataframe for the instrument at probeheight
                sonicdat = MET.make_dataframe_for_height(
                    data, timerange, probeheight=probeheight)
                sonicdat_lo = MET.make_dataframe_for_height(
                    data, timerange, probeheight=38)
                sonicdat_hi = MET.make_dataframe_for_height(
                    data, timerange, probeheight=122)
                temp = sonicdat['WS'].dropna()
                if len(temp) < 1000:
                    continue

                # extract variables needed for classificiation of IEC events
                params = MET.setup_IEC_params(sonicdat, probeheight=100)

                # # look for extreme wind speed model events
                # Ve01eventfound, Ve50eventfound = MET.find_EWM_events(sonicdat, params)
                # Ve01events = pd.concat([Ve01events,Ve01eventfound])
                # Ve50events = pd.concat([Ve50events,Ve50eventfound])

                # # look for extreme operating gust events
                # EOGeventfound = MET.find_EOG_events(sonicdat, params)
                # EOGevents = pd.concat([EOGevents,EOGeventfound])

                # # look for extreme turbulence model events
                # ETMeventfound = MET.find_ETM_events(sonicdat, params)
                # ETMevents = pd.concat([ETMevents,ETMeventfound])

                # # look for extreme direction change events
                # EDCeventfound = MET.find_EDC_events(sonicdat, params)
                # EDCevents = pd.concat([EDCevents,EDCeventfound])

                # # look Extreme coherent gust with direction change events
                # ECDeventfound = MET.find_ECD_events(sonicdat, params)
                # ECDevents = pd.concat([ECDevents,ECDeventfound])

                ######### skip extreme wind shear for now. This needs more than one probe location I think
                # look Extreme wind shear events
                EWSeventfound = MET.find_EWS_events(sonicdat, sonicdat_lo,
                                                    sonicdat_hi, params)
                EWSevents = pd.concat([EWSevents, EWSeventfound])

        # # save the data for each month
        # eventlist = {'EWS_Ve01': Ve01events,
        #              'EWS_Ve50': Ve50events,
        #              'EOG': EOGevents,
        #              'ETM': ETMevents,
        #              'EDC': EDCevents,
        #              'ECD': ECDevents,
        #              'EWS': EWSevents}

        filename = 'EWSevents_{}_{}.pkl'.format(year, month)
        savefile = os.path.join(savepath, filename)
        with open(savefile, 'wb') as f:
            pkl.dump(EWSevents, f, pkl.HIGHEST_PROTOCOL)
#%%

# # demo load data
# loadfile = savefile
# # loadfile = '/Users/nhamilto/Documents/Wake_Dynamics/SiteChar/data/IEC/IEC_events_2015_1.pkl'
# with open(loadfile, 'rb') as f:
#     test= pkl.load(f)
# for key in test:
#     print(len(test[key]))
