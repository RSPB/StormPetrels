# Storm Petrels

We're am using Python and R. If you'd like to reproduce this work, do shout. In due time we will make it such that you will be able to reproduce it with a single click. Stay tuned!

## Data access

The data is stored on Google Cloud Platform [Storage](https://cloud.google.com/storage/docs/) in so-called *buckets*. Those granted access can browse the data via [GCS Browser](https://console.cloud.google.com/storage/browser/storm-petrels?project=birdman-project) - it's useful for browsing and downloading / uploading single files. For batch, there are two options:

* Software with GUI like [CrossFTP](http://www.crossftp.com/features.htm#crossftp)
* Command line tool: [gsutil](https://cloud.google.com/storage/docs/gsutil). 

### gsutil
When following installation procedure, make sure to execute `gcloud init` to set up the project. To download content of `training` "folder" (strictly speaking, there are no folders on GCS), execute the following:

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

### Training 