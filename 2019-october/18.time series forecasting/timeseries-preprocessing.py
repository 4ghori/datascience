import pandas as pd
import numpy as np
from sklearn import metrics, ensemble
import os
import matplotlib.pyplot as plt

path = "F:/"
data = pd.read_csv(os.path.join(path, 'Sales_Transactions_Dataset_Weekly.csv'))
data = data.filter(regex=r'Product|W')
data.head()

melt = data.melt(id_vars='Product_Code', var_name='Week', value_name='Sales')
melt['Product_Code'] = melt['Product_Code'].str.extract('(\d+)', expand=False).astype(int)
melt['Week'] = melt['Week'].str.extract('(\d+)', expand=False).astype(int)
melt = melt.sort_values(['Week', 'Product_Code'])
melt.head()

df = pd.read_csv(os.path.join(path,'uk-deaths-from-bronchitis-emphys.csv'))
df.info()

df.columns = ['timestamp', 'y']
index = pd.to_datetime(df['timestamp'], format='%Y-%m').copy()
df.index = index
df.drop('timestamp', axis=1, inplace=True)
plt.plot(df)