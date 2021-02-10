library(seewave)
library(tidyverse)
library(data.table)
library(warbleR)
library(bioacoustics)
library(soundgen)

#Set Working directory (were are all your files txt, wav or mp3)

setwd("D:/BioPhonia/MathurinAubry")

#If sound files are in mp3, convert them in wav with : 
mp32wav(samp.rate = 44.1, parallel = 2)

#List all .txt files in the folder
all_files <- list.files("D:/BioPhonia/MathurinAubry/", pattern = "*.txt")

#Read the .txt files with all the label extract from Audacity
essai<-lapply(all_files, read.audacity, format="dir")


#Bin all the data frame into a super dataframe, add a unique number and the name of the soundfile
x<-do.call("rbind", essai)
write.table(x)
x2<-setDT(x, keep.rownames = TRUE)[]

setnames(x2, old = c('rn', 't1', 't2','f1', 'f2'), new =c('selec', 'start', 'end', 'bottom.freq', 'top.freq'))

x2$sound.files <-str_replace(x2$file, ".txt", ".wav")

#extract audio clip and rename each clip with annoation name and the unique number.
# 
# fonction utilis�e : 
# cut_sels(X, mar = 0.05, parallel = 1, path = NULL, dest.path = NULL, pb = TRUE,
#          labels = c("sound.files", "selec"), overwrite = FALSE, norm = FALSE, ...)

# X : object of class 'selection_table', 'extended_selection_table' or data frame containing columns for sound file name (sound.files), selection number (selec), and start and end time of signals (start and end).
# mar : Numeric vector of length 1. Specifies the margins adjacent to the start and end points of selections, delineating spectrogram limits. Default is 0.05.
# parallel : Numeric. Controls whether parallel computing is applied. It specifies the number of cores to be used. Default is 1 (i.e. no parallel computing).
# path : Character string containing the directory path where the sound files are located. If NULL (default) then the current working directory is used.
# dest.path : Character string containing the directory path where the cut sound files will be saved. If NULL (default) then the directory containing the sound files will be used instead.
# pb : Logical argument to control progress bar. Default is TRUE.
# labels : String vector. Provides the column names that will be used as labels to create sound file names. Note that they should provide unique names (otherwise sound files will be overwritten). Default is c("sound.files", "selec").
# overwrite : Logical. If TRUE sound files with the same name will be overwritten. Default is FALSE.
# norm : Logical indicating whether wave objects must be normalized first using the function normalize. Additional arguments can be passed to normalize using `...`.` Default is FALSE. See normalize for available options.


cut_sels(x2, mar= 0.05, path="D:/BioPhonia/MathurinAubry/", dest.path = "D:/BioPhonia/MathurinAubry/", labels = c("selec", "label"))



#Create spectro images for all files  (https://marce10.github.io/warbleR/reference/specreator.html)
specreator(x2, flim = c(0, 11), ovlp = 90, )


