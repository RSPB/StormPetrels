import numpy as np
import os
from glob import glob
from scipy.io import wavfile

length = 60

def wav_to_floats(filename):
    import wave
    s = wave.open(filename,'r')
    strsig = s.readframes(s.getnframes())
    y = np.fromstring(strsig, np.short)
    s.close()
    return y

if __name__ == '__main__':

    for filename in glob('*.wav'):
        basename = os.path.splitext(filename)[0]
        fs, sig = wavfile.read(filename)
        sig = sig[:,0]  # only first channel for a starter
        audio_len = len(sig)
        audio_len_s = int(audio_len / fs)
        frames_per_file = length * fs
        if audio_len_s > length:
            for idx, start in enumerate(range(0, audio_len, frames_per_file)):
                end = start + frames_per_file
                if end > audio_len:
                    end = audio_len
                wavfile.write(basename + '_' + str(idx) + '.wav', fs, sig[start:end])