import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style({'font.family': 'Times New Roman'})
from sklearn.preprocessing import LabelEncoder

df = pd.read_csv('D:\\Combined_Data\\ANOVA_for_Paper.csv')

df = df.loc[df['Target'] == 'worst'] # goodday, Power Off, badday, worst
# print(df.columns)
print('selected data \n',df.head(10))
co = ['Timestamp', 'temp_diff', 'humi_diff', 'desi_temp', 'desi_humi', 'discrete_amps', 'discrete_temp_diff',
      'discrete_humi_diff', 'discrete_desi_temp', 'discrete_desi_humi', 'Ex_feellike', 'TimeOfDay', 'In_feellike',
      'Target', 'Consuming']
# co = ['target', 'ex_feellike']
df.drop(co, axis=1, inplace=True)
# The data is categorial so I convert it with LabelEncoder to transfer to ordinal.
# labelencoder = LabelEncoder()
# for column in df.columns:
#     df[column] = labelencoder.fit_transform(df[column])

print(df.head())

print(df.describe().to_string())

df_corr = df.corr()

# print(df.describe())
fig, ax = plt.subplots(1, figsize=(8, 6))
# mask
mask = np.triu(np.ones_like(df_corr, dtype=np.bool))
# adjust mask and df
mask = mask[1:, :-1]
corr = df_corr.iloc[1:, :-1].copy()

# color map
# cmap = sns.diverging_palette(0, 230, 90, 60, as_cmap=True)
cmap=sns.diverging_palette(240, 10, as_cmap=True)
reversed_color_map = cmap.reversed()
# # plot heatmap
# sns.heatmap(corr, mask=mask, annot=True, fmt=".2f", cmap='RdBu_r',
#            vmin=-1, vmax=1, cbar_kws={"shrink": 1.0},  annot_kws={"size": 15, 'rotation': 0})
# sns.heatmap(corr, mask=mask, annot=True, fmt=".3f", cmap=cmap,
#             vmin=-1, vmax=1, cbar_kws={"shrink": 1.}, annot_kws={"size": 15, 'rotation': 0})

sns.heatmap(corr, center=0,mask=mask, annot=True, fmt=".2f", cmap=reversed_color_map,
           vmin=-1, vmax=1, cbar_kws={"shrink": 1.0},  annot_kws={"size": 15, 'rotation': 0})

# # Set font for x-axis labels
plt.xticks(fontsize=15)
# # Set font for y-axis labels
plt.yticks(fontsize=15)

# title = 'Correlation Between Random Variables'
# plt.title(title, loc='center', fontsize=25)
plt.tight_layout()
plt.show()
