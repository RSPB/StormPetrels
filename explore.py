from scipy.signal import firwin, lfilter, butter
from scipy.io import wavfile
from sklearn.preprocessing import normalize
import matplotlib.pyplot as plt
import yaafelib
import numpy as np
# from features import FeatureExtractor

plt.interactive(False)

def butter_bandpass(lowcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    b, a = butter(order, low, btype='highpass')
    return b, a

def butter_bandpass_filter(data, lowcut, fs, order=5):
    b, a = butter_bandpass(lowcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

def highpass_filter(signal, rate, cut):
    """ Apply highpass filter. Everything below 'cut' frequency level will
        be greatly reduced. """
    ntaps = 99
    nyq = 0.5 * rate
    highpass = firwin(ntaps, cut, nyq=nyq)
    filteredSignal = lfilter(highpass, 1.0, signal)
    return filteredSignal

fs, sig = wavfile.read('STHELENA-02_20140520_200000_1.wav')
sig = butter_bandpass_filter(sig, 1000, fs)
# sig = highpass_filter(sig, fs, 1000)
if sig.ndim > 1:
    sig = sig[:,0]

feature_plan = yaafelib.FeaturePlan(sample_rate=fs)
success = feature_plan.loadFeaturePlan('features.config')
engine = yaafelib.Engine()
engine.load(feature_plan.getDataFlow())
features = engine.processAudio(np.array([sig.astype('float64')]))

feature_list = []

for feature in features.itervalues():
    feature_list.append(feature)

all_features = np.concatenate(feature_list, axis=1)
np.savetxt('STHELENA-02_20140520_200000_1.csv', all_features, delimiter=',')
print('Done!')

# feature = FeatureExtractor(fs)

#plt.specgram(sig, NFFT=2**11, Fs=fs)
#plt.show()