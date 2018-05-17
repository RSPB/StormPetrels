# Don't mind me - work in progress

import sys
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy import fft
from skimage.filters import rank
from skimage.util import img_as_ubyte
from skimage.morphology import disk, remove_small_objects

def pic_to_ubyte (pic):
    a = (pic-np.min(pic) ) /(np.max(pic - np.min(pic))) 
    a = img_as_ubyte(a)
    return a

if len(sys.argv) == 2:
    input_file = sys.argv[1]
else:
    input_file = r'STHELENA-02_20140520_200000_1_0.wav'

fs, sig = wavfile.read(input_file)
#dtype = np.dtype('float64')
#sig = sig.astype(dtype) # / dtype.type(-np.iinfo(sig.dtype).min)

N = len(sig)
K = 512
Step = 4
wind =  0.5*(1 -np.cos(np.array(range(K))*2*np.pi/(K-1) ))

MIN_SEGMENT_SIZE = 99
p = 90

SPEC_SEGMENTS = []
LOG_SPEC_SEGMENTS = []

Spectogram = []

for j in range(int(Step*N/K)-Step):
    vec = sig[j * K/Step : (j+Step) * K/Step] * wind
    Spectogram.append(abs(fft(vec,K)[:K/2]))
    
mypic = np.transpose(Spectogram)
mypic_rev = np.zeros_like(mypic)
for i in range(mypic.shape[0]):
    mypic_rev[i] = mypic[-i - 1]
    
fig = plt.figure()

sigma=3
disk_val=3

mypic_rev_small = mypic_rev[120:200,:]
mypic_rev = mypic_rev
mypic_rev_log = np.log10(mypic_rev+ 0.001)
mypic_rev_gauss = sp.ndimage.gaussian_filter(mypic_rev, sigma=sigma)
mypic_rev_log_gauss = sp.ndimage.gaussian_filter(mypic_rev_log, sigma=sigma)
mypic_rev_gauss_bin = mypic_rev_gauss > np.percentile(mypic_rev_gauss, p)
mypic_rev_log_gauss_bin = mypic_rev_log_gauss > np.percentile(mypic_rev_log_gauss,p)
mypic_rev_gauss_bin_close =sp.ndimage.binary_closing( sp.ndimage.binary_opening(mypic_rev_gauss_bin))
mypic_rev_log_gauss_bin_close =sp.ndimage.binary_closing( sp.ndimage.binary_opening(mypic_rev_log_gauss_bin))
mypic_rev_gauss_grad = rank.gradient(pic_to_ubyte(mypic_rev_gauss), disk(disk_val))
mypic_rev_log_gauss_grad = rank.gradient(pic_to_ubyte(mypic_rev_log_gauss), disk(disk_val))
mypic_rev_gauss_grad_bin = mypic_rev_gauss_grad > np.percentile(mypic_rev_gauss_grad,p)
mypic_rev_log_gauss_grad_bin = mypic_rev_log_gauss_grad > np.percentile(mypic_rev_log_gauss_grad,p )
mypic_rev_gauss_grad_bin_close =sp.ndimage.binary_closing( sp.ndimage.binary_opening(mypic_rev_gauss_grad_bin))
mypic_rev_log_gauss_grad_bin_close =sp.ndimage.binary_closing( sp.ndimage.binary_opening(mypic_rev_log_gauss_grad_bin))
bfh = sp.ndimage.binary_fill_holes(mypic_rev_gauss_grad_bin_close)        
bfh_rm = remove_small_objects(bfh, MIN_SEGMENT_SIZE)
log_bfh = sp.ndimage.binary_fill_holes(mypic_rev_log_gauss_grad_bin_close)        
log_bfh_rm = remove_small_objects(log_bfh, MIN_SEGMENT_SIZE)

labeled_segments, num_seg = sp.ndimage.label(bfh_rm)

#plt.subplot(6,2,1)
#plt.imshow(mypic_rev,cmap=plt.cm.afmhot_r)
#plt.axis('off')
#plt.title('Spectrogram')
#plt.subplot(6,2,2)
#plt.imshow(mypic_rev_log,cmap=plt.cm.afmhot_r)
#plt.axis('off')
#plt.title('Spectrogram (log)')       
#plt.subplot(6,2,3)
#plt.imshow(mypic_rev_log_gauss,cmap=plt.cm.afmhot_r)
#plt.axis('off')
#plt.title('+ Gaussian Filtering')
#plt.subplot(6,2,4)
#plt.imshow(mypic_rev_log,cmap=plt.cm.afmhot_r)
#plt.axis('off')
#plt.title('+ Gaussian Filtering (log)')        
#plt.subplot(6,2,5)
#plt.imshow(mypic_rev_gauss_grad,cmap=plt.cm.afmhot_r)
#plt.axis('off')
#plt.title('+ Gradient')
#plt.subplot(6,2,6)
#plt.imshow(mypic_rev_log_gauss_grad,cmap=plt.cm.afmhot_r)
#plt.axis('off')
#plt.title('+ Gradient (log)')    
#plt.subplot(6,2,7)
#plt.imshow(mypic_rev_gauss_grad_bin,cmap=plt.cm.gray)
#plt.axis('off')
#plt.title('+ >90%')
#plt.subplot(6,2,8)
#plt.imshow(mypic_rev_log_gauss_grad_bin,cmap=plt.cm.gray)
#plt.axis('off')
#plt.title('+ >90% (log)')          
#plt.subplot(6,2,9)
#plt.imshow(mypic_rev_gauss_grad_bin_close,cmap=plt.cm.gray)
#plt.axis('off')
#plt.title('+ binary_closing + binary_opening')
#plt.subplot(6,2,10)
#plt.imshow(mypic_rev_log_gauss_grad_bin_close,cmap=plt.cm.gray)
#plt.axis('off')
#plt.title('+ binary_closing + binary_opening (log)') 


#plt.subplot(6,2,11)
#plt.imshow(labeled_segments)
#plt.axis('off')
#plt.title('+ binary_fill_holes + remove_small_objects')

plt.imshow(labeled_segments)
plt.axis('off')
plt.title('labeled_segments')

for current_segment_id in range(1,num_seg+1):
    current_segment = (labeled_segments == current_segment_id)*1
    xr = current_segment.max(axis =  0)
    yr = current_segment.max(axis =  1)
    xr_max = np.max(xr*np.arange(len(xr)))
    xr[xr==0] = xr.shape[0]
    xr_min = np.argmin(xr)
    yr_max = np.max(yr*np.arange(len(yr)))
    yr[yr==0] = yr.shape[0]
    yr_min = np.argmin(yr)
    segment_frame = [yr_min, yr_max, xr_min, xr_max]
    subpic = mypic_rev_gauss[yr_min:yr_max+1,xr_min:xr_max+1]
    SPEC_SEGMENTS.append([0, current_segment_id, segment_frame, subpic])

fig.savefig('patterns.png',dpi = 300)
fig.clear()
#plt.show()

# LOG SEGMENTS
log_labeled_segments, log_num_seg = sp.ndimage.label(log_bfh_rm)
#plt.subplot(6,2,12)
#plt.imshow(labeled_segments)
#plt.axis('off')
#plt.title('+ binary_fill_holes + remove_small_objects (log)')        
for current_segment_id in range(1,log_num_seg+1):
    current_segment = (log_labeled_segments == current_segment_id)*1
    xr = current_segment.max(axis =  0)
    yr = current_segment.max(axis =  1)
    xr_max = np.max(xr*np.arange(len(xr)))
    xr[xr==0] = xr.shape[0]
    xr_min = np.argmin(xr)
    yr_max = np.max(yr*np.arange(len(yr)))
    yr[yr==0] = yr.shape[0]
    yr_min = np.argmin(yr)
    segment_frame = [yr_min, yr_max, xr_min, xr_max]
    subpic = mypic_rev_log_gauss[yr_min:yr_max+1,xr_min:xr_max+1]
    LOG_SPEC_SEGMENTS.append([0, current_segment_id, segment_frame, subpic])   