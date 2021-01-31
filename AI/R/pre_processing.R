library(seewave)
library(tidyverse)
library(data.table)
library(warbleR)
library(bioacoustics)

#Set Working directory (were are all your files txt, wav or mp3)

path_to_files = "Enter path to the folder containing" #Think about moving this to config file later 
setwd(path_to_files)

#If sound files are in mp3, convert them in wav with : 
mp32wav(samp.rate = 44.1, parallel = 2)

#List all .txt files in the folder
all_files <- list.files(path_to_files, pattern = "*.txt")

#Read the .txt files with all the label extract from Audacity
essai<-lapply(all_files, read.audacity)

#Bin all the data frame into a super dataframe, add a unique number and the name of the soundfile
x<-do.call("rbind", essai)
write.table(x)
x2<-setDT(x, keep.rownames = TRUE)[]
x3<-rename(x2, selec=rn)
x4<-rename(x3, start=t1)
x5<-rename(x4, end=t2)
x5$sound.files <-str_replace(x5$file, ".txt", ".wav")

#extract audio clip and rename each clip with annoation name and the unique number.
# 
# fonction utilisée : 
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


cut_sels(x5, mar= 0.05, path=path_to_files, dest.path =path_to_files, labels = c("selec", "label"))


