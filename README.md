# Storm Petrels

We're am using Python and R. If you'd like to reproduce this work, do shout. In due time we will make it such that you will be able to reproduce it with a single click. Stay tuned!

## Useful commands

[Parallel](https://www.gnu.org/software/parallel/parallel_tutorial.html) is a shell tool for parallel processing on one or more computers. It is handy for processing of large volumes of files, as long as your operations are not I/O bound - meaning you're not limited by a read speed from hard drive. Solid State Drive (SSD) comes recommended. 

[SoX](http://sox.sourceforge.net/) is an excellent command-line tool for audio processing. We are using it to e.g.


* Cut audio files into 10-minute recordings.

  `find . -name '*.wav' -type f -print0 | parallel -0 sox {} {.}_.wav trim 0 600 : newfile : restart`
 
* Downsample, convert to mono and normalise the audio. Check details in the [manual](http://sox.sourceforge.net/sox.html).

  `find . -name '*.wav' -type f -print0 | parallel -0 sox --norm {} -r 16000 --channels 1 path/{} dither -s`