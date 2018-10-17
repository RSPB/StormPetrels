library(data.table)
library(warbleR)

sample_len <- 0.8
dir_pattern <- '/home/tracek/Data/StormPetrels-full/*.wav'
paths <- Sys.glob(dir_pattern)

bp <- c(1,6)
wl <- 256
th <- 2

for(path in paths)
{
  print(path)
  sound <- readWave(path)
  name <- basename(path)
  sampleRate <- sound@samp.rate
  len <- length(sound)/sampleRate
  start <- seq(from=0, to=len - sample_len, by=sample_len)
  end <- start + sample_len
  start_overlap <- seq(from=sample_len/2, to=len - sample_len, by=sample_len)
  end_overlap <- start_overlap + sample_len
  
  start <- sort(c(start, start_overlap))
  end <- sort(c(end, end_overlap))
  sound.files <- name
  selec <- seq(0,length(start)-1)
  df.grid <- data.frame(sound.files, selec, start, end)
  
  df.features <- specan(X = df.grid, bp=bp, fast = TRUE, parallel = 32, wl = wl, threshold = th, path = "/home/tracek/Data/StormPetrels-full/")
  df.features$start <- df.grid$start
  df.features$end <- df.grid$end
  df.features$petrel <- df.grid$sound.files
  
  out_filename <- sprintf('%s-grid_08_features_petrels_bp%s_wl%s_th%s.csv', tools::file_path_sans_ext(name), paste(bp, collapse = '-'), wl, th)
  
  write.table(df.features,
              file = out_filename,
              row.names=FALSE, na="",col.names=TRUE, sep=",")
  gc()
}
