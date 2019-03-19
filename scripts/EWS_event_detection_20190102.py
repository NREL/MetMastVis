# coding: utf-8

# In[17]:

# get_ipython().run_line_magic('load_ext', 'autoreload')
# get_ipython().run_line_magic('autoreload', '2')

import sys, os
import numpy as np
# import matplotlib.pyplot as plt
# fs = 12
# plt.rc('font', family='serif')
# plt.rc('font', size=fs)
# plt.rc('facecolor', )
import pandas as pd
import scipy.io as sio

# met mast functions and utilities
sys.path.append('../')
import met_funcs as MET
# import vis as vis
import utils as utils
import pickle as pkl


###########################################
def calc_all_shear_events(sonicdat,
                          sonicdat_lo,
                          sonicdat_hi,
                          params,
                          alpha_neg,
                          alpha_pos,
                          alpha_reference_velocity,
                          T=12,
                          write_out_all=False):
    '''
    Find extreme coherent wind shear events.

    Parameters
    ----------
    sonicdat : [type]
        [description]
    sonicdat_lo : [type]
        [description]
    sonicdat_hi : [type]
        [description]
    params : [type]
        [description]
    alpha_neg : [type]
        [description]
    alpha_pos : [type]
        [description]
    alpha_reference_velocity : [type]
        [description]
    T : int, optional
        [description] (the default is 12, which [default_description])
    write_out_all : bool, optional
        [description] (the default is False, which [default_description])

    '''

    # extract wind speed and perform 3 sec rolling average (3 sec * 20 Hz = 60 pts)
    sonicdat = sonicdat.rolling(60, center=True, min_periods=1).mean()
    sonicdat_lo = sonicdat_lo['WS'].rolling(
        60, center=True, min_periods=1).mean()
    sonicdat_hi = sonicdat_hi['WS'].rolling(
        60, center=True, min_periods=1).mean()

    # calculate shear exponent
    alpha = np.log(sonicdat_hi / sonicdat_lo) / np.log(122 / 38)
    alpha.index = pd.DatetimeIndex(alpha.index)

    # make dataframe for shear events (include wind speed and direction)
    sonicdat.index = pd.DatetimeIndex(sonicdat.index)
    shearevents = pd.concat(
        [
            sonicdat['WS'].resample('12S').mean(),
            sonicdat['WS'].resample('12S').max(),
            sonicdat['WS'].resample('12S').min(),
            sonicdat['WD'].resample('12S').mean(),
            alpha.resample('12S').mean(),
            alpha.resample('12S').max(),
            alpha.resample('12S').min()
        ],
        axis=1)
    # rename columns
    shearevents.columns = [
        'Vhub', 'Vmax', 'Vmin', 'wdir', 'alpha_mean', 'alpha_max', 'alpha_min'
    ]
    # add limits of shear exponent based on vhub
    shearevents['alpha_pos_limit'] = np.interp(
        shearevents['Vhub'], alpha_reference_velocity, alpha_pos)
    shearevents['alpha_neg_limit'] = np.interp(
        shearevents['Vhub'], alpha_reference_velocity, alpha_neg)

    # create mask to identify valid extreme events
    vhub_mask = shearevents['Vhub'] > alpha_reference_velocity.min()
    aneg_mask = shearevents['alpha_min'] < shearevents['alpha_neg_limit']
    apos_mask = shearevents['alpha_max'] > shearevents['alpha_pos_limit']

    # identify extreme shear events (EWS)
    extreme_events = shearevents[vhub_mask & (aneg_mask | apos_mask)]

    return shearevents, extreme_events


########################
def EWS_fig(allshearcalcs,
            EWSevents,
            alpha_reference_velocity,
            alpha_pos,
            alpha_neg,
            lim=6.5):
    '''
    make a figure showing EWS events vs hub-height velocity

    Parameters
    ----------
    allshearcalcs : pd.DataFrame
        [description]
    EWSevents : pd.DataFrame
        [description]
    alpha_reference_velocity : np.array
        [description]
    alpha_pos :  np.array
        [description]
    alpha_neg :  np.array
        [description]
    lim : float, optional
        [description] (the default is 8, which is the minimum defined vhub for extreme alpha)

    '''
    fig, ax = plt.subplots(figsize=(5, 3))

    allshearcalcs[(allshearcalcs['Vhub'] > lim) & ~(
        (allshearcalcs['alpha_mean'] > allshearcalcs['alpha_pos_limit']) |
        (allshearcalcs['alpha_mean'] < allshearcalcs['alpha_neg_limit'])
    )].plot.scatter(
        'Vhub', 'alpha_mean', ax=ax, color='w', edgecolor='C0')
    apos = EWSevents[
        EWSevents['alpha_max'] > EWSevents['alpha_pos_limit']].plot.scatter(
            'Vhub',
            'alpha_max',
            ax=ax,
            color='C2',
            edgecolor='C2',
            label=r'$\alpha_+$')
    aneg = EWSevents[
        EWSevents['alpha_min'] < EWSevents['alpha_neg_limit']].plot.scatter(
            'Vhub',
            'alpha_min',
            ax=ax,
            color='C1',
            edgecolor='C1',
            label=r'$\alpha_-$')

    ax.plot(alpha_reference_velocity, alpha_pos, color='C0')
    ax.plot(alpha_reference_velocity, alpha_neg, color='C0')

    ax.legend(frameon=False)  #loc=6, bbox_to_anchor = (1,0.5))

    ax.set_ylabel('Shear Exponent [-]')
    ax.set_xlabel('Hub-Height Velocity [m/s]')

    fig.tight_layout()

    return fig, ax


# paths (must mount volume smb://nrel.gov/shared/wind/WindWeb/MetData/135mData/)
towerID = 'M5'
metDataPath = '/Volumes/135mData/{}Twr/20Hz/mat/'.format(towerID)

savepath = '/Users/nhamilto/Documents/Wake_Dynamics/SiteChar/data/IEC_3'
try:
    os.makedirs(savepath)
except:
    pass

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
years = [int(a) for a in np.arange(2017, 2019, 1)]  #
months = [int(a) for a in np.arange(1, 12.1, 1)]
days = [int(a) for a in np.arange(1, 31.1, 1)]

# years = [2015]  #
# months = [2]
# days = np.arange(1, 11.1).astype(int)
yearmonth = []
for year in years:
    for month in months:
        yearmonth.extend([(year, month)])

for year, month in yearmonth:

    if (year == 2015) & (month in list((range(12)))):
        continue

    # begin empty lists for events
    EWSevents = pd.DataFrame()
    allshearcalcs = pd.DataFrame()

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

        for filenum, file in enumerate(fPaths):

            if str(year) not in file:
                continue

            # load data
            try:
                data = sio.loadmat(os.path.join(
                    datapath, file))  #, variable_names=varnames)
                print('data loaded from {}'.format(
                    os.path.join(datapath, file)))
            except:
                print('data not found? looks like you have some homework...')
                continue

            ndat = 10 * 60 * 20  # minutes*seconds/minute*samples/second
            if len(data['Sonic_CupEqHorizSpeed_100m'][0][0][0]
                   .flatten()) < 10000:
                print('data size mismatch, {}'.format(file))
                continue

            # make a vector of datetimes for the data
            timerange = utils.matlab_datenum_to_python_datetime(
                data['time_UTC'][0][0][0].flatten())

            probeheight = 87  # m
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

            shearevents, extreme_events = calc_all_shear_events(
                sonicdat, sonicdat_lo, sonicdat_hi, params, alpha_neg,
                alpha_pos, alpha_reference_velocity)

            EWSevents = pd.concat([EWSevents, extreme_events])
            allshearcalcs = pd.concat([allshearcalcs, shearevents])

        # ###### Save Data!
        # # all shear data
        # filename = 'ShearCalcs_{}_{}.csv'.format(year, month)
        # savefile = os.path.join(savepath, filename)
        # allshearcalcs.to_csv(savefile)

    # detected extreme events
    if len(EWSevents) > 0:
        filename = 'EWSevents_{}_{}.csv'.format(year, month)
        savefile = os.path.join(savepath, filename)
        print('EWS event detected. Stored to: {}'.format(filename))
        EWSevents.to_csv(savefile)
