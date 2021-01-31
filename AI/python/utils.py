import os
import ffmpeg
import numpy as np
import pandas as pd

#####
# Requires the above packages, if not installed: pip install <package name>
#####



def dir_convert_mp32wav(directory, keep_file=False):
    '''
    Processes a directory, applying file_convert_mp32wav to every mp3 file
    Parameters:
    - str directory: path to directory
    - bool keep_file: whether to delete original mp3 file or not
    '''
    res = np.array([file_convert_mp32wav(os.path.join(directory, f), keep_file=keep_file) for f in os.listdir(directory) 
                    if os.path.splitext(f)[-1] == '.mp3']).sum(axis=0)
    
    print(f'Directory {directory} processed, {res[0]} conversions, {res[1]} deletions')

    
def file_convert_mp32wav(input_file, keep_file=False):
    '''
    Converts a sound file from mp3 to wav using ffmpeg
    Parameters:
    - str input_file: path to file to convert
    - bool keep_file: whether to delete original mp3 file or not
    Returns
    - tuple (int convert, int delete) indicating if conversion/deletion was performed or not
    '''
    
    output_file = '.'.join([os.path.splitext(input_file)[0], 'wav'])
    convert = 0
    delete = 0
    
    if not os.path.isfile(output_file):
        # if output file doesn't already exist
        stream = ffmpeg.input(input_file)
        stream = ffmpeg.output(stream, output_file)
        ffmpeg.run(stream)
        convert = 1
        
    if not keep_file:
        os.remove(input_file)
        delete = 1
        
    return convert, delete


def read_txt_file(file):
    '''
    Opens a text file and copy content in a pandas df. Audacity outputs that span 2 lines are put back to a single line
    Parameters:
    - str file: path to txt file
    Returns 
    dataframe containing txt file information
    '''
    
    df = pd.read_table(file, header=None)
    
    # From two to one row per recording
    even = df.loc[[i for i in range(len(df)) if i%2 == 0], [0, 1, 2]].rename(columns={0: 't_start', 1: 't_end', 2: 'species'})
    even.index = range(len(even))

    odd = df.loc[[i for i in range(len(df)) if i%2 == 1], [1, 2]].rename(columns={1: 'f_start', 2: 'f_end'})
    odd.index = range(len(odd))
    
    df = pd.concat([even, odd], axis=1)
    df['filename'] = os.path.basename(file).split('.')[0]
    
    return df


def create_label_dataset(directory):
    '''
    Concatenates text files contents into a pandas df containing recordings information
    Parameters:
    - str directory: path to directory
    Returns:
    dataframe containing recordings information
    '''
    
    df_list = [read_txt_file(os.path.join(directory, f)) for f in os.listdir(directory) if os.path.splitext(f)[-1] == '.txt']
    
    return pd.concat(df_list)