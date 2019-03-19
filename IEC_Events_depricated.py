#####
#
# Depricated IEC events detection functions


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

    # extreme coherent gust velocity magnitude (delta)
    Vcg = 15  # m/s See IEC standards
    # T seconds at 20 Hz
    t = np.linspace(0, 10, int(T * params['freq']))
    stride = int(T * params['freq'])

    # function forms of coherent gust velocity and direction
    # vzt = cupspeed[starttime] + 0.5*Vcg*(1-np.cos(np.pi*t/T))
    # thetat = winddir[starttime] + 0.5*Vcg*(1-np.cos(np.pi*t/T))

    # scan for ECD
    # index times of EDC events
    ECDeventfound = pd.DataFrame()

    for itime in range(0, len(sonicdat), stride):
        # for itime, tempspeed in sonicdat['WS'].iloc[::int(T*params['freq'])].items():

        # extract 6 second slice of direction data
        vslice = sonicdat.iloc[itime:itime + stride]

        # start and end velocities
        vstart = vslice['WS'].iloc[0]
        vend = vslice['WS'].iloc[stride - 1]

        # extreme  cohcerent gust velocity change
        V_ECD = vstart + Vcg

        # test for wind speed condition
        if vend >= V_ECD:
            # start and end directions
            dstart = vslice['WD'].iloc[0]
            dend = vslice['WD'].iloc[stride - 1]

            # extreme  cohcerent gust direction change
            if params['vhub'] < 4:
                theta_cg = 180  # degrees
            elif params['vhub'] < params['Vref']:
                theta_cg = 720 / params['vhub']  # degrees

            # test for wind direction condition

            if np.abs(dend - dstart) > theta_cg:
                temp = pd.DataFrame([[vslice['WS'].iloc[0],vslice['WS'].max(),vslice['WS'].min(),\
                                    vslice['WD'].iloc[0],vslice['WD'].max(),vslice['WD'].min()]], \
                                columns=['WS','WSmax','WSmin','WD','WDmax','WDmin'], index=vslice.index[0:1])
                ECDeventfound = pd.concat([ECDeventfound, temp])

    return ECDeventfound


###########################################
###########################################
def find_EOG_events_DEPRICATED(sonicdat, params, T=10.5):
    """
    Find extreme operating wind gust events.

    This function takes inputs from a pandas DataFrame containing all of the desired data and International Electrotechnical Commission (IEC) parameters at the given period for search, determines extreme operating wind gust events, and returns the findings in an object which can be used to index files later.

        :param sonicdat: A pandas DataFrame containing all of the desired data at the given probe height including wind speed, wind direction, and the date and timestamps of the input data.

        :param params: A dictionary containing all of the parameters established by the IEC for the given input data and probe height.

        :param T: A float used to define the period for search (Seconds).

        :returns EOGeventfound: An object used to store any significant extreme operating wind gust events.
    """

    t = np.linspace(0, T, 100)

    # Compare maximum gust speed to data
    # if an extreme events occurs, append time to list
    EOGeventfound = pd.DataFrame()

    for itime in range(0, len(sonicdat), int(T * params['freq'])):
        # for itime, tempspeed in sonicdat['WS'].iloc[::int(T*params['freq'])].items():

        # extract 6 second slice of direction data
        vslice = sonicdat.iloc[itime:itime + int(T * params['freq'])]

        # standard velocity variance
        sigma_1 = params['Iref'] * (0.75 * vslice['WS'].mean() + 5.6)

        Vgust = np.min([1.35*(params['Ve01']-vslice['WS'].iloc[0]), \
                    3.3*(sigma_1/(1+0.1*params['D']/params['Lambda_1']))])
        Vgust = vslice['WS'].iloc[0] - 0.37 * Vgust * np.sin(
            3 * np.pi * t / T) * (1 - np.cos(2 * np.pi * t / T))

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
def find_ETM_events_DEPRICATED(sonicdat, params):
    """
    Find extreme turbulence model events.

    This function takes inputs from a pandas DataFrame containing all of the desired data and International Electrotechnical Commission (IEC) parameters at the given period for search, determines extreme turbulence model events, and returns the findings in an object which can be used to index files later.

        :param sonicdat: A pandas DataFrame containing all of the desired data at the given probe height including wind speed, wind direction, and the date and timestamps of the input data.

        :param params: A dictionary containing all of the parameters established by the IEC for the given input data and probe height.

        :returns ETMeventfound: An object used to store any significant extreme turbulence model events.
    """

    # Extreme turbulence model
    c = 2  # m/s
    sigmatest = c * params['Iref'] * (0.072 * (params['Vave'] / c + 3) *
                                      (params['vhub'] / c + 4) + 10)

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
def find_EWS_events_DEPRICATED(sonicdat,
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

    # Extreme wind shear (EWS)

    # extreme coherent gust velocity magnitude
    Vhub = sonicdat  # m/s
    # T seconds at 20 Hz
    t = np.linspace(0, T, int(T * params['freq']))
    stride = int(T * params['freq'])

    # # transient horizontal shear (not applicable in our data...)
    # v_horz_pos = vhub*(probeheight/zhub)**alpha + ((probeheight-zhub)/D)*(2.5 + 0.2*beta*sigma_1*(D/Lambda_1)**0.25)*(1-np.cos(np.pi*T/T))

    # scan for EWS
    EWSeventfound = pd.DataFrame()
    for itime in range(0, len(sonicdat), stride):

        # extract 6 second slice of direction data
        vslice = sonicdat.iloc[itime:itime + stride]
        # mean hub height velocity
        Vhub = vslice['WS'].mean()

        alpha_pos_limit = np.interp(Vhub, alpha_reference_velocity, alpha_pos)
        alpha_neg_limit = np.interp(Vhub, alpha_reference_velocity, alpha_neg)

        # extract velocities at lower and upper rotor tips

        vlo = sonicdat_lo.iloc[itime:itime + stride]
        vhi = sonicdat_hi.iloc[itime:itime + stride]

        alpha = np.log(vhi / vlo) / np.log(122 / 38)

        alpha = pd.DataFrame(data=alpha, index=vslice.index, columns=['alpha'])
        alpha.dropna(how='any', inplace=True)
        atest = alpha[(alpha < alpha_neg_limit) | (alpha > alpha_pos_limit)]

        # sigma_1 = params['Iref']*(0.75*Vhub + 5.6)

        # extreme = ((params['probeheight']-params['zhub'])/params['D'])*\
        #     (2.5 + 0.2*params['beta']*sigma_1*(params['D']/params['Lambda_1'])**0.25)\
        #     *(1-np.cos(np.pi*T/T))

        # # transient vertical shear
        # v_vert_pos = vslice['WS'].iloc[0]*(params['probeheight']/params['zhub'])**params['alpha'] + extreme
        # v_vert_neg = vslice['WS'].iloc[0]*(params['probeheight']/params['zhub'])**params['alpha'] - extreme

        # # test
        # atest = vslice['WS'][(vslice['WS'] > v_vert_pos) & (vslice['WS'] < v_vert_neg)]

        if len(atest) > 0:
            temp = pd.DataFrame([[Vhub, vslice['WS'].max(),vslice['WS'].min(),\
                                    vslice['WD'].iloc[0],vslice['WD'].max(),vslice['WD'].min(), atest['alpha'].mean(), atest['alpha'].max(), atest['alpha'].min()]], \
                                columns=['WSmean','WSmax','WSmin','WDmean','WDmax','WDmin','alphamean', 'alphamax', 'alphamin'], index=vslice.index[0:1])
            EWSeventfound = pd.concat([EWSeventfound, temp])

    return EWSeventfound


###########################################


###########################################
def find_EDC_events_DEPRICATED(sonicdat, params, T=6):
    """
    Find extreme wind direction change events.

    This function takes inputs from a pandas DataFrame containing all of the desired data and International Electrotechnical Commission (IEC) parameters at the given period for search, determines extreme wind direction change events, and returns the findings in an object which can be used to index files later.

        :param sonicdat: A pandas DataFrame containing all of the desired data at the given probe height including wind speed, wind direction, and the date and timestamps of the input data.

        :param params: A dictionary containing all of the parameters established by the IEC for the given input data and probe height.

        :param T: A float used to define the period for search (Seconds).

        :returns EDCeventfound: An object used to store any significant extreme wind direction change events.
    """

    # seconds * sampling freq
    stride = int(T * params['freq'])

    # index times of EDC events
    EDCeventfound = pd.DataFrame()
    for itime in range(0, len(sonicdat), stride):
        # for itime, tempspeed in sonicdat['WS'].iloc[::int(T*params['freq'])].items():

        # extract 6 second slice of direction data
        vslice = sonicdat.iloc[itime:itime + stride]

        sigma_1 = params['Iref'] * (0.75 * vslice['WS'].mean() + 5.6)

        # Maximum allowable change in wind direction over a 6 second period
        theta_e = np.degrees(4 * np.arctan(
            sigma_1 / (vslice['WS'].iloc[0] *
                       (1 + 0.1 * params['D'] / params['Lambda_1']))))

        # test
        if np.abs(vslice['WD'].iloc[0] -
                  vslice['WD'].iloc[stride - 1]) > theta_e:
            temp = pd.DataFrame([[vslice['WS'].iloc[0],vslice['WS'].max(),vslice['WS'].min(),\
                                    vslice['WD'].iloc[0],vslice['WD'].max(),vslice['WD'].min()]], \
                                columns=['WS','WSmax','WSmin','WD','WDmax','WDmin'], index=vslice.index[0:1])
            EDCeventfound = pd.concat([EDCeventfound, temp])

    return EDCeventfound


###########################################


###########################################
def setup_IEC_params_DEPRICATED(sonicdat, probeheight=100):
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
    if sonicdat['WD'].mean() > 180:
        sonicdat.loc[sonicdat['WD'] < 100, 'WD'] += 360
    else:
        sonicdat.loc[sonicdat['WD'] > 350, 'WD'] += -360

    ######## parameters
    ### IEC parameters
    params = {'turbclass': 'IA'}
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
    params['vhub'] = sonicdat['WS'].mean()  # m/s
    # dummy vertical coordinate
    params['z'] = np.linspace(0, 120, 120)
    # standard normal velocity profile
    params['vprofile'] = params['vhub'] * (
        params['z'] / params['zhub'])**params['alpha']
    params['sigma_data'] = sonicdat['WS'].std()

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