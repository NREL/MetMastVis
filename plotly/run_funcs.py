import vis
import utils
import met_funcs
import plotly_vis
import pandas as pd
from colour import Color
import plotly
from plotly import tools
import plotly.plotly as py
import plotly.graph_objs as go

inputfiles_here = ['2012_August.csv']

actual_data = met_funcs.load_met_data(inputfiles_here)
actual_data = met_funcs.drop_nan_cols(actual_data)
actual_data = met_funcs.qc_mask(actual_data)

keep_cats = met_funcs.categories_to_keep()
ex_cats = met_funcs.categories_to_exclude()
var_cats,var_units,var_labels,var_save = met_funcs.categorize_fields(actual_data,keep_cats,ex_cats)
print(actual_data)
met_funcs.groom_data(actual_data,var_cats)
print(actual_data)
stab_conds,stab_cats = met_funcs.flag_stability(actual_data)
cate_info = met_funcs.get_catinfo(actual_data)

category = 'speed'

#fig1 = plotly_vis.stability_winddir_scatter(actual_data,cate_info,category)

#py.iplot(fig1, filename = 'MetMast-Test_funcStabWinddirScatter')