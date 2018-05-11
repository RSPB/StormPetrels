library(warbleR)
library(data.table)
set.seed(1)
working_dir <- getwd()
setwd(file.path("/mnt/data/Birdman/16khz"))

df.audio <- autodetec(threshold = 4, envt = "abs", ssmooth = 1200, power=1,
                      bp=c(1,8), xl = 2, picsize = 2, res = 200, 
                      flim= c(1,8), osci = FALSE, redo = TRUE,
                      wl = 256, ls = TRUE, sxrow = 10, rows = 8, 
                      mindur = 0.1, maxdur = 1, set = TRUE, parallel = 16, smadj = "both")

df.features <- specan(X = df.audio, bp=c(1,8), fast = FALSE, parallel = 16, wl = 256, threshold = 10)
dt.features <- data.table(df.features) 

dt.features$start <- df.audio$start
dt.features$end <- df.audio$end

write.table(dt.features,
            file = "features2.csv",
            row.names=FALSE, na="",col.names=TRUE, sep=",")


