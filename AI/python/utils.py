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


def read_txt_file(file, extra_str_label=''):
    '''
    Opens a text file and copy content in a pandas df. Audacity outputs that span 2 lines are put back to a single line
    Parameters:
    - str file: path to txt file
    - str extra_str_label: the substring that is added in label files, depending of the birder
    Returns 
    dataframe containing txt file information
    '''
    
    df = pd.read_table(file, header=None)

    # Separate time and frequency lines (the latter start with "\")
    df['line_type'] = (df[0] == '\\').astype(int)

    # Assign recording id to each line
    df['id'] = [elt for elt in assign_idx(df['line_type'])]
    
    # Suppression of duplicate entries
    df.drop_duplicates(['line_type', 'id'], inplace=True)
    
    # From two to one row per recording
    df = df.loc[df['line_type'] == 0].merge(df.loc[df['line_type'] == 1], on='id').dropna().rename(columns={
    '0_x': 't_start', '1_x': 't_end', '2_x': 'species', '1_y': 'f_start', '2_y': 'f_end'
    })
    df = df[['t_start', 't_end', 'f_start', 'f_end', 'species']]

    df['filename'] = os.path.basename(file).split('.')[0]
    df['filename'] = df['filename'].str.replace(extra_str_label, '')

    for dt_col in ['t_start', 't_end']:
        df[dt_col] = df[dt_col].astype(float)
    
    return df


def create_label_dataset(directory, extra_str_label=''):
    '''
    Concatenates text files contents into a pandas df containing recordings information
    Parameters:
    - str directory: path to directory
    - str extra_str_label: the substring that is added in label files, depending of the birder
    Returns:
    dataframe containing recordings information
    '''
    
    df_list = [read_txt_file(os.path.join(directory, f), extra_str_label=extra_str_label) 
        for f in os.listdir(directory) if os.path.splitext(f)[-1] == '.txt']
    labels = pd.concat(df_list)
    
    # Deduplication of recording labels, label with the largest frequency range is kept
    labels['f_delta'] = labels['f_end'].astype(float) - labels['f_start'].astype(float)
    labels = labels.sort_values('f_delta', ascending=False).drop_duplicates(['filename', 't_start']).sort_values(['filename', 't_start'])
    del labels['f_delta']

    # Suppression of sounds that do not belong to birds
    not_bird_labels = ['Bruit de fond', 'Autre antropophonie', 'Autre biophonie', 'Vent geophonie', 'Capreolus capreolus',
     'Background', 'Pelophylax sp.', 'Vulpes vulpes', 'Autre biophonie chien', 'Oecanthus pellucens', 'ruspolia nitidula',
     'Backgroud', 'Autre anthropophonie', 'orthoptère', 'parasite', 'voix humaine', 'bruit parasite', 'passage moto au loin',
     'saturation HF par orthoptères']
    not_bird_labels = [noise_label.lower() for noise_label in not_bird_labels]
    labels = labels.loc[~labels['species'].str.lower().isin(not_bird_labels)]

    labels.index = range(len(labels))
    
    return labels


def assign_idx(col):
    '''
    Function to be used in read_txt_file, increment a recording index each time a new recording is detected, 
    corresponding to a float value in column 0
    '''
    
    idx = -1
    
    for elt in col:
        if elt == 0:
            idx += 1
        yield idx
