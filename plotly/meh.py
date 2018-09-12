def rose_fig(metdat, catinfo, category=None, vertloc=80, bins=6, ylim=None, noleg=False,normed=True):
    """**Get Wind Rose Figure**.

    Plot the wind rose of a given variable (or category of variables) grouped by a given condition (or set of conditions).
    
    Parameters:
        1. metdat (Pandas DataFrame): The desired input data (Met Mast).
        2. catinfo (dictionary): Categorization information for the desired input data. Holds column names, labels, units, and save names.
        3. category (string) [default: None]: Specifies the category of information that is desired for plotting.
        4. vertloc (integer, float) [default: 80]: Describes the desired vertical location alond the tower for analysis.        
        5. bins (integer, list) [default: 6]: Indicates the number of equally spaced bins to divide the variable.
        6. nsector (integer) [default: 36]: Indicated the number of sector directions to divide the rose figure.
        7. ylim (float) [default: None]: Provides the maximum value for the frequency of observations and is used to plot different roses with uniform limits.
        8. noleg (Boolean) [default: False]: Determines whether or not there will be a legend to the figure.
        9. normed (Boolean) [default: True]: Determines whether or not the values of the Windrose should be in terms of percentages of the total.

    Returns:
        1. fig (Plotly Figure): The figure object for the desired input data and categories.
    """
    
    # set up data
    dircol, _, _= utils.get_vertical_locations(catinfo['columns']['direction'], location=vertloc)
    varcol, vertloc, _= utils.get_vertical_locations(catinfo['columns'][category], location=vertloc)
    winddir = metdat[dircol]
    var = metdat[varcol]

    # get var divisions set up
    if isinstance(bins, int):
        nbins = bins
    else:
        nbins = len(bins)

    # set up plotting colors
    colors = utils.get_colors(nbins-1, basecolor='span')
    colors += ['#3A4246'] # add something dark to the end.
    colors = tuple(colors[0:nbins])
    print(colors)
    print(type(colors))

    fish = [None]*bins
    data = [None]*len(range(4,36,4))
    index_test = 0

    for nsector in range(4,36,4):
        # Start: From Matplotlib windrose GitHub
        angle = 360. / nsector

        dir_bins = np.arange(-angle / 2, 360. + angle, angle, dtype=np.float)
        dir_edges = dir_bins.tolist()
        dir_edges.pop(-1)
        dir_edges[0] = dir_edges.pop(-1)
        dir_bins[0] = 0.

        if isinstance(bins, int):
            bins = np.linspace(np.min(var), np.max(var), bins)
        bins = np.asarray(bins)

        var_bins = bins.tolist()
        var_bins.append(np.inf)

        table = histogram2d(x=var, y=winddir, bins=[var_bins, dir_bins],
                            normed=False)[0]
        # Add the last value to the first to have the table of North winds
        table[:, 0] = table[:, 0] + table[:, -1]
        # Remove the last col
        table = table[:, :-1]
        # Norm the values of the table
        if normed:
            table = table * 100 / table.sum()
        # End: From Matplotlib windrose GitHub

        #Convert radii to Plotly style  
        table_final = []
        list_final = []

        for sect_num in range(nsector):
            list_final.append(0)
            list_final.append(table[0,sect_num])
            list_final.append(table[0,sect_num])
            list_final.append(0)
        
        table_final.append(list_final)

        for bin_ind in range(nbins-1):

            list2_final = []
            
            #print(bin_ind)
            #print(table_final[bin_ind-1][:])

            #print(table[bin_ind,:])

            test_list = table[bin_ind+1,:].tolist()
            #print(*test_list)

            for i in range(nsector):
                #print(i)
                #print((i+1)*4-1)
                #print(table_final[bin_ind][(i+1)*4-2])
                list2_final.append(table_final[bin_ind][(i+1)*4-2])
                list2_final.append(table_final[bin_ind][(i+1)*4-2] + test_list[i])
                list2_final.append(table_final[bin_ind][(i+1)*4-2] + test_list[i])
                list2_final.append(table_final[bin_ind][(i+1)*4-2])

            #print(*list2_final)     
            table_final.append(list2_final)
            #print(table_final)
        
        #print(table_final)

        #Convert directions to Plotly style  
        list_test = dir_bins.tolist()
        #print(list_test)
        dir_final = []

        dir_final.append(list_test[-1])
        dir_final.append(list_test[-1])
        dir_final.append(list_test[1])
        dir_final.append(list_test[1])

        for i in range(1,len(list_test)-1):
            dir_final.append(list_test[i])
            dir_final.append(list_test[i])
            dir_final.append(list_test[i+1])
            dir_final.append(list_test[i+1])

        #print(dir_final)

        # Set labels
        name = [None]*nbins
        for j in range(nbins):
            j_ind = range(nbins-1,-1,-1)
            j_ind = j_ind[j]
            name[j] = '[%.2f : %.2f) m/s' % (var_bins[j_ind],var_bins[j_ind+1])


        # Build figure
        for iax in range(len(colors)):
            index = range(len(colors)-1,-1,-1)
            index = index[iax]

            trace = go.Scatterpolar(
                r = table_final[index][:],
                theta = dir_final[::-1],
                mode = 'lines',
                name = name[iax],
                fill = 'toself',
                fillcolor = colors[index],
                line =  dict(
                    color = 'black'
                )
            )
            fish[iax] = trace

        data[index_test] = fish
        #print(index_test)
        #print(nsector)
        #print(type(data))
        #print(len(data[0]))
        #print(data)
        index_test += 1

        # Set title
        if normed:
            titleS = "Windrose for %s (normed)" % (category)
        else:
            titleS = "Windrose for %s (not normed)" % (category)
        
        # Set tick suffix
        if normed:
            ticksuffixS = "%"
        else:
            ticksuffixS = "m/s"

        # Set layout
        layout = go.Layout(
            title = titleS,
            font = dict(
            size = 15
            ),
            polar = dict(
                radialaxis = dict(
                    ticksuffix = ticksuffixS
                ),
                angularaxis = dict(
                    tickfont = dict(
                        size = 16
                    ),
                    rotation = 90,
                    direction = "counterclockwise",
                    categoryarray = ["N", "NW", "W", "SW","S","SE","E","NE"]
                )
            ),
        )

        
    print(len(data))
    steps = []
    for k in range(len(data)):
        step = dict(
            method = 'restyle',
            args = ['visible', [False] * len(data)],
        )
        step['args'][1][k] = True # Toggle i'th trace to "visible"
        steps.append(step)
    
    sliders = [dict(
        active = 2,
        currentvalue = {"prefix": "Frequency: "},
        pad = {"t": 50},
        steps = steps
    )]

    layout = dict(sliders=sliders)#, layout=layout)

    fig = dict(data=data[0], layout=layout)
         
    return fig