import plotly
import vis
import utils
import met_funcs

import plotly.plotly as py
import plotly.graph_objs as go

inputfiles_here = ['2012_August.csv']

actual_data = met_funcs.load_met_data(inputfiles_here)
actual_data = met_funcs.drop_nan_cols(actual_data)
actual_data = met_funcs.qc_mask(actual_data)

cate_info = met_funcs.get_catinfo(actual_data)

category = 'speed'
colnames, vertlocs, ind = utils.get_vertical_locations(cate_info['columns'][category]) 
 
plotdat = actual_data[colnames].mean()

xstring = cate_info['labels'][category]
ystring = 'Probe Height [m]'

trace0 = go.Scatter(
    x = plotdat,
    y = vertlocs,
    mode = 'lines+markers',
    name = xstring
)

# Edit the layout
layout = dict(title = "%s vs. %s" % (xstring,ystring),
            xaxis = dict(title = xstring),
            yaxis = dict(title = ystring),
            )

data = [trace0]
fig = dict(data=data, layout=layout)
py.iplot(fig, filename = 'MetMast-Test2')