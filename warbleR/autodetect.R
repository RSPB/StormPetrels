library(warbleR)
library(data.table)
library(stats)

setwd(file.path("/mnt/data/Birdman/samples/recordings/"))

bp <- c(1,8)
wl <- 512
th <- 10
smooth <- 1200

df.audio <- autodetec(threshold = th, envt = "abs", power=1,
                      bp = bp, flim = bp, ssmooth = smooth, redo = TRUE,
                      wl = wl,  mindur = 0.2, maxdur = 4, set = TRUE, parallel = 14)

df.audio <- df.audio[complete.cases(df.audio),]
#df.audio$sound.files <- tools::file_path_sans_ext(df.audio$sound.files)

# df.audio$start <- df.audio$start - 0.25
# df.audio$end <- df.audio$end + 0.25

df.features <- specan(X = df.audio, bp=bp, fast = TRUE, parallel = 14, wl = wl, threshold = th)
df.features <- data.table(df.features) 

df.features$start <- df.audio$start
df.features$end <- df.audio$end

out_filename <- sprintf('autodetect_petrels_bp%s_wl%s_th%s_smooth%s_maxdur4.csv', paste(bp, collapse = '-'), wl, th, smooth)

write.table(df.features,
            file = out_filename,
            row.names=FALSE, na="",col.names=TRUE, sep=",")

