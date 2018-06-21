import vis
import utils
import met_funcs
import plotly_vis
import MetMastData
import pandas as pd
import matplotlib.pyplot as plt
from colour import Color
import plotly
from plotly import tools
#import plotly.tools as tls
import plotly.plotly as py
import plotly.graph_objs as go

# Place input files here
#inputfiles_here = ['2012_August.csv']
#inputfiles_here = ['2013_January.csv','2013_February.csv','2013_March.csv','2013_April.csv','2013_May.csv','2013_June.csv','2013_July.csv','2013_August.csv','2013_September.csv','2013_October.csv','2013_November.csv','2013_December.csv']
#inputfiles_here = ['2013_January.csv']
year = 2017
inputfiles_here = [str(year) + '_' + s + '.csv' for s in utils.monthnames()]
'''
inputfiles_here = MetMastData()
actual_data = 
cate_info = actual_data.cate_info
'''

# Load and filter data
actual_data = met_funcs.load_met_data(inputfiles_here)
actual_data = met_funcs.drop_nan_cols(actual_data)
actual_data = met_funcs.qc_mask(actual_data)

# Extract categorical information
keep_cats = met_funcs.categories_to_keep()
ex_cats = met_funcs.categories_to_exclude()
var_cats,var_units,var_labels,var_save = met_funcs.categorize_fields(actual_data,keep_cats,ex_cats)

# Extract more information
met_funcs.groom_data(actual_data,var_cats)
stab_conds,stab_cats = met_funcs.flag_stability(actual_data)
cate_info = met_funcs.get_catinfo(actual_data)


# Plot the data with the desired category and function
category = 'speed'
#fig1 = plotly_vis.monthly_rose_fig(actual_data,cate_info,category)
fig1 = plotly_vis.monthlyhourlyplot(actual_data,cate_info,category)

py.iplot(fig1, filename = 'MetMast-Test_funcMonthlyHourly')