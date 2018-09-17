import aubio
import numpy as np
from scipy.signal import butter, lfilter


def _find_pitches(win, pitch_o, tolerance):
    pitches = []
    for frame_idx, frame in enumerate(win[:-1]):
        pitch = pitch_o(frame)[0]
        confidence = pitch_o.get_confidence()
        if confidence > tolerance:
            pitches.append((frame_idx, pitch))
    return pitches


def get_pitch(signal, sr, block_size, hop, tolerance = 0.7, unit = 'seconds'):
    pitch_o = aubio.pitch("yin", block_size, hop, sr)
    pitch_o.set_unit('Hz')
    pitch_o.set_tolerance(tolerance)
    signal = signal.astype('float32')
    signal_win = np.array_split(signal, np.arange(hop, len(signal), hop))

    pitches = _find_pitches(signal_win, pitch_o, tolerance)

    if unit == 'seconds':
        pitches = [(frame_idx * hop / sr, value) for frame_idx, value in pitches]
    elif unit == 'samples':
        pitches = [(frame_idx * hop, value) for frame_idx, value in pitches]
    else:
        raise NotImplemented('Unit %s is not implemented', unit)

    if not pitches:
        raise ValueError('No pitches!')

    return pitches


def bandpass_filter(signal, sr, lowcut, highcut, order=5):
    nyq = 0.5 * sr
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    y = lfilter(b, a, signal)
    return y


def lowpass_filter(signal, sr, lowcut, order=5):
    nyq = 0.5 * sr
    low = lowcut / nyq
    b, a = butter(order, low, btype='lowpass')
    y = lfilter(b, a, signal)
    return y


def highpass_filter(signal, sr, highcut, order=5):
    nyq = 0.5 * sr
    high = highcut / nyq
    b, a = butter(order, high, btype='highpass')
    y = lfilter(b, a, signal)
    return y