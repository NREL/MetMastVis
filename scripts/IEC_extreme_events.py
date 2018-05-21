# Extreme events detection
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

# fundamentals
import os, glob
import numpy as np
import pandas as pd
from calendar import monthrange, month_name
import scipy.stats as stats
import datetime
import imp
import scipy.io as sio
import pickle as pkl

# met mast functions and utilities
import met_funcs as MET


# time range
# years  = [ int(a) for a in np.arange(2012,2019,1) ] #
months = [ int(a) for a in np.arange(1,12.1,1) ]
days = [int(a) for a in np.arange(1,31.1,1)]

# paths (must mount volume smb://nrel.gov/shared/wind/WindWeb/MetData/135mData/)
towerID = 'M5'
figPath = '../../figs/{}'.format(towerID)

metDataPath = '/Volumes/135mData/{}Twr/20Hz/mat/'.format(towerID)

#################
# read data, look for events, save time index
#################

years = [2017,2018]
# months = [4]
# days=[1]
probeheight=100
            
try:
    savepath = '/Users/nhamilto/Documents/Wake_Dynamics/SiteChar/data/IEC'
    os.makedirs(savepath)
except:
    pass

for year in years:
    for month in months:
        
        # begin empty lists for events
        Ve01events = []
        Ve50events = []
        EOGevents = []
        ETMevents = []
        EDCevents = []
        ECDevents = []
        EWSevents = []
        
        print('reading 20Hz data for {}/{}'.format(year,month))

        for day in days:
            datapath = os.path.join(metDataPath,str(year),str(month).zfill(2),str(day).zfill(2))

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
                    data = sio.loadmat(os.path.join(datapath,file))
                except:
                    continue
                    
                # if data is not complete, move on. No need to fight here.
                ndat = 10*60*20 # minutes*seconds/minute*samples/second
                if len(data['Sonic_CupEqHorizSpeed_100m'][0][0][0].flatten()) != 12000:
                    continue
                    
                # make a vector of datetimes for the data
                timerange = MET.make_datetime_vector(file)
                # make a dataframe for the instrument at probeheight
                sonicdat = MET.make_dataframe_for_height(data, timerange, probeheight=probeheight)
                temp = sonicdat['Sonic_CupEqHorizSpeed_100m'].dropna()
                if len(temp)<1000:
                    continue
                    
                # extract variables needed for classificiation of IEC events
                cupspeed, winddir, sigma_data, params = MET.setup_IEC_params(sonicdat, probeheight=100)
                
                # look for extreme wind speed model events
                Ve01eventfound, Ve50eventfound = MET.find_EWM_events(cupspeed, params)
                Ve01events.extend(Ve01eventfound)
                Ve50events.extend(Ve50eventfound)
                
                # look for extreme operating gust events
                EOGeventfound = MET.find_EOG_events(cupspeed, params)
                EOGevents.extend(EOGeventfound)
                
                # look for extreme turbulence model events
                ETMeventfound = MET.find_ETM_events(cupspeed, sigma_data, params)
                ETMevents.extend(ETMeventfound)

                # look for extreme direction change events
                EDCeventfound = MET.find_EDC_events(cupspeed, winddir, params)
                EDCevents.extend(EDCeventfound)
                
                # look Extreme coherent gust with direction change events
                ECDeventfound = MET.find_ECD_events(cupspeed, winddir, params)
                ECDevents.extend(ECDeventfound)
                
                # look Extreme wind shear events
                EWSeventfound = MET.find_EWS_events(cupspeed, params)
                EWSevents.extend(EWSeventfound)
                
        # save the data for each month        
        eventlist = {'EWS_Ve01': Ve01events, 
                     'EWS_Ve50': Ve50events, 
                     'EOG': EOGevents, 
                     'ETM': ETMevents, 
                     'EDC': EDCevents, 
                     'ECD': ECDevents, 
                     'EWS': EWSevents}  
                
        filename = 'IEC_events_{}_{}.pkl'.format(year,month)
        savefile = os.path.join(savepath,filename)
        with open(savefile, 'wb') as f:
            pkl.dump(eventlist, f, pkl.HIGHEST_PROTOCOL)
                
print('done')


# demo load data
loadfile = savefile
# loadfile = '/Users/nhamilto/Documents/Wake_Dynamics/SiteChar/data/IEC/IEC_events_2015_1.pkl'
with open(loadfile, 'rb') as f:
    test= pkl.load(f)
for key in test:
    print(len(test[key]))

