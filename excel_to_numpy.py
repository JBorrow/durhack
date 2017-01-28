'''
Code to read/convert footfall excel data to numpy arrays
'''

import numpy as np
import pandas as pd

data15 = pd.read_excel('foot.xlsx', '2015')#, index_col=None, na_values=['NA'])
data15.as_matrix()
full_data15 = np.array(data15)          # Full 2015 data set as a numpy array
ss15 = full_data15[1:54,8:15]        # footfall for silver street from monday-sunday in 2015
eb15 = full_data15[1:54,17:24]       # -----------elvet bridge
nr15 = full_data15[1:54,25:32]       # -----------north road
events15 = full_data15[1:54,0:7]     # event data for 2015 (monday-sunday)

data16 = pd.read_excel('foot.xlsx', '2016')
data16.as_matrix()
full_data16 = np.array(data16)
ss16 = full_data16[1:54,8:15]
eb16 = full_data16[1:54,17:24]
nr16 = full_data16[1:54,26:33]
cp16 = full_data16[1:54,35:42]       # footfall data for claypath in 2016
mp16 = full_data16[1:54,44:51]       # footfall data for market place in 2016
