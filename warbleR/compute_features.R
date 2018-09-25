library(warbleR)
library(data.table)

path = '/mnt/data/Birdman/samples/labels/merged.csv'
all <- read.csv(file=path, header=TRUE, sep=",")
all$sound.files <- paste(all$sound.files, '.wav', sep='')

bp <- c(1,6)
wl <- 256
th <- 2

df.features <- specan(X = all, bp=bp, fast = TRUE, parallel = 12, wl = wl, threshold = th, path = "/mnt/data/Birdman/samples/recordings/")

out_filename <- sprintf('features_petrels_bp%s_wl%s_th%s.csv', paste(bp, collapse = '-'), wl, th)

df.features$start <- all$start
df.features$end <- all$end
df.features$petrel <- all$petrel

write.table(df.features,
            file = out_filename,
            row.names=FALSE, na="",col.names=TRUE, sep=",")