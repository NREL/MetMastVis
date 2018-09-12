import vis
import utils
import met_funcs
import numpy as np
import pandas as pd
from colour import Color
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
from numpy.lib.twodim_base import histogram2d

list_test = [0,1,2,11,1,0,1,8]
list_final = []

for i in list(range(len(list_test))):
    list_final.append(0)
    list_final.append(list_test[i])
    list_final.append(list_test[i])
    list_final.append(0)

print(list_final)