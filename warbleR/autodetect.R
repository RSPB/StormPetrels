library(warbleR)
library(data.table)
library(stats)

setwd(file.path("/mnt/data/Birdman/test"))

df.audio <- autodetec(threshold = 4, envt = "abs", ssmooth = 1200, power=1,
                      bp=c(1,8), xl = 2, picsize = 2, res = 200, 
                      flim= c(1,8), osci = FALSE, redo = TRUE,
                      wl = 256, ls = TRUE, sxrow = 10, rows = 8, 
                      mindur = 0.1, maxdur = 1, set = TRUE, parallel = 1)

df.audio <- df.audio[complete.cases(df.audio),]
df.features <- specan(X = df.audio, bp=c(1,8), fast = FALSE, parallel = 1, wl = 256, threshold = 10)
dt.features <- data.table(df.features) 

dt.features$start <- df.audio$start
dt.features$end <- df.audio$end

write.table(dt.features,
            file = "features_all.csv",
            row.names=FALSE, na="",col.names=TRUE, sep=",")

