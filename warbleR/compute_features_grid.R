library(data.table)
library(warbleR)

sample_len <- 0.8
dir_pattern <- '/mnt/data/Birdman/samples/recordings/STHELENA*.wav'
paths <- Sys.glob(dir_pattern)

datalist = list()

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
  df <- data.frame(sound.files, selec, start, end)
  datalist[[name]] <- df
}

grid.petrels <- do.call(rbind, datalist)
rownames(grid.petrels) <- 1:nrow(grid.petrels)

write.table(grid.petrels,
            file = 'petrels_grid_08.csv',
            row.names=FALSE, na="",col.names=TRUE, sep=",")

bp <- c(1,8)
wl <- 256
th <- 2

df.features <- specan(X = grid.petrels, bp=bp, fast = TRUE, parallel = 14, wl = wl, threshold = th, path = "/mnt/data/Birdman/samples/recordings/")

out_filename <- sprintf('grid_08_features_petrels_bp%s_wl%s_th%s.csv', paste(bp, collapse = '-'), wl, th)

df.features$start <- grid.petrels$start
df.features$end <- grid.petrels$end
df.features$petrel <- grid.petrels$petrel

write.table(df.features,
            file = out_filename,
            row.names=FALSE, na="",col.names=TRUE, sep=",")