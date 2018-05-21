# Storm Petrels

We're am using Python and R. If you'd like to reproduce this work, do shout. In due time we will make it such that you will be able to reproduce it with a single click. Stay tuned!

## Data access

The data is stored on Google Cloud Platform [Storage](https://cloud.google.com/storage/docs/) in so-called *buckets*. Those granted access can browse the data via [GCS Browser](https://console.cloud.google.com/storage/browser/storm-petrels?project=birdman-project) - it's useful for browsing and downloading / uploading single files. For batch, there are two options:

* Software with GUI like [CrossFTP](http://www.crossftp.com/features.htm#crossftp)
* Command line tool: [gsutil](https://cloud.google.com/storage/docs/gsutil). 

### gsutil
When following installation procedure, make sure to execute `gcloud init` to set up the project. To download content of *training* "folder" (strictly speaking, there are no folders on GCS), execute the following:

`gsutil -m rsync -r gs://storm-petrels/training your-destination`

Options:

* `-m` : run operation in parallel, i.e. start many downloads at once
* `rsync` : utility for syncronisation of two buckets / directories, see [manual](https://cloud.google.com/storage/docs/gsutil/commands/rsync)
* `-r` : recursive

## Useful commands

[Parallel](https://www.gnu.org/software/parallel/parallel_tutorial.html) is a shell tool for parallel processing on one or more computers. It is handy for processing of large volumes of files, as long as your operations are not I/O bound - meaning you're not limited by a read speed from hard drive. Solid State Drive (SSD) comes recommended. 

[SoX](http://sox.sourceforge.net/) is an excellent command-line tool for audio processing. We are using it to e.g.


* Cut audio files into 10-minute recordings.

  `find . -name '*.wav' -type f -print0 | parallel -0 sox {} {.}_.wav trim 0 600 : newfile : restart`
 
* Downsample, convert to mono and normalise the audio. Check details in the [manual](http://sox.sourceforge.net/sox.html).

  `find . -name '*.wav' -type f -print0 | parallel -0 sox --norm {} -r 16000 --channels 1 path/{} dither -s`
  
  
## Results

The results have been obtained on [STHELENA-02_20140605_200000](https://console.cloud.google.com/storage/browser/storm-petrels/training/recordings/?project=birdman-project) data set for which [labels](https://storage.cloud.google.com/storm-petrels/sthelena_labels.xls) have been provided. The original audio is stereo (2 channels) and has 44.1 kHz sampling rate. It has been converted to single channel 16 kHz for ease of processing. Recordings are 10 min long.

### warbleR

[Download warbleR results](https://storage.cloud.google.com/storm-petrels/training/features_warbler_buffer_250ms.csv)

[warbleR](https://github.com/cran/warbleR/) is a very handy R package for bioacoustics. Full description can be found in [this](https://besjournals.onlinelibrary.wiley.com/doi/epdf/10.1111/2041-210X.12624) paper. Among other features, the package offers [autodetect.R](warbleR/autodetect.R) routine that can detect, after tuning of parameters, relevant acoustic signals. After extraction of *start* and *end* of a potential bird call, we pass this information to `specan` function that calculates audio features described in [documentation](https://www.rdocumentation.org/packages/warbleR/versions/1.1.12/topics/specan). Note that we add a 250ms *buffor* to `start` and `end` of each call to avoid clipping of a call. Time will tell if we don't include too much noise.

Here is the complete list of acoustic features we calculate per call:

* **meanfreq**: mean frequency (in kHz)
* **sd**: standard deviation of frequency
* **freq.median**: median frequency (in kHz)
* **freq.Q25**: first quantile (in kHz)
* **freq.Q75**: third quantile (in kHz)
* **freq.IQR**: interquantile range (in kHz)
* **time.Q25**: first quartile time
* **time.Q75**: third quartile time
* **time.IQR**: interquartile time range
* **skew**: skewness - asymmetry of the spectrum
* **kurt**: kurtosis - peakedness of the spectrum
* **sp.ent**: spectral entropy
* **sfm**: spectral flatness
* **meanfun**: average of fundamental frequency
* **minfun**: minimum fundamental frequency
* **maxfun**: maximum fundamental frequency
* **meandom**: average of dominant frequency
* **mindom**: minimum of dominant frequency
* **maxdom**: maximum of dominant frequency
* **dfrange**: range of dominant frequency
* **modindx**: modulation index
* **startdom**: dominant frequency measurement at the start of the signal
* **enddom**: dominant frequency measurement at the end of the signal
* **dfslope**: slope of the change in dominant (kHz/s)
* **peakf**: peak frequency
* **meanpeakf**: mean peak frequency
