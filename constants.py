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

