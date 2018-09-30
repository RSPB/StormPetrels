import pandas as pd
import dask.dataframe as dd
from tsnecuda import TSNE
from sklearn.preprocessing import StandardScaler
import glob


path = '/mnt/data/Birdman/full/results/warbler_grid08_bp1-6_wl256_th2/*.csv'

print(path)
types = {'mindom': 'float64'}
columns_to_pop = ['sound.files', 'selec', 'start', 'end']
columns_to_remove = ['duration']

df_dd = dd.read_csv(path, dtype=types)
df = df_dd.persist().compute()

df_extra = df[columns_to_pop]
df = df.drop(labels=columns_to_pop + columns_to_remove, axis=1)
df = df.fillna(0)

selected_features = (
    ('meanfreq', 'mean frequency (in kHz)'),
    ('sd', 'standard deviation of frequency'),
    ('freq.Q75', 'third quantile (in kHz)'),
    ('freq.IQR', 'interquantile range (in kHz)'),
    ('skew', 'skewness - asymmetry of the spectrum'),
    ('kurt', 'kurtosis - peakedness of the spectrum'),
    ('sp.ent', 'spectral entropy'),
    ('sfm', 'spectral flatness'),
    ('meanfun', 'average of fundamental frequency'),
    ('maxfun', 'maximum fundamental frequency'),
    ('meandom', 'average of dominant frequency'),
    ('dfrange', 'range of dominant frequency'),
    ('modindx', 'modulation index'),
    ('meanpeakf', 'mean peak frequency'))

selected_features_names = [name for name, desc in selected_features]
df = df[selected_features_names]


scaler = StandardScaler()
X = scaler.fit_transform(df.values)

X_emb = TSNE(perplexity=30, n_iter=2).fit_transform(X)