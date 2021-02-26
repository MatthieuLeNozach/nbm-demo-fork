import os
import time
import numpy as np
import birdvoxdetect as bvd
import pandas as pd
import datetime as dt
from utils import *


#####
## How to proceed in practice:

## Choose a birder directory
# directory = 'data\MathurinAubry'

## Figure out what is the extra_str_label string (ex. '' for Mathurin, 'Piste de marqueur' for Maxence) and evaluate compute_bvd_score
# precision, recall = compute_bvd_score(directory, extra_str_label='')

## Split results into score and binary score
# precision, binary_precision = precision
# recall, binary_recall = recall
#####


def bvd_process_directory(directory):
    '''
    Process all wav files in a given directory with birdvoxdetect detection AI. Outputs are gathered in a pandas DataFrame.
    Parameters:
    - str directory: path to directory to process
    Returns:
    - pandas DataFrame containing information on detected calls in all wav files
    - list of wav files that raised BirdVoxDectectError

    '''
    
    df = []
    columns = ['Time (hh:mm:ss)', 'Species (4-letter code)', 'Family', 'Order', 'Confidence (%)']
    empty_dict = {col: [np.nan] for col in columns}
    processed = 0
    failed = []
    
    for f in os.listdir(directory):
        split = f.split('.')
        if split[-1].lower() == 'wav':
            try:
                to_append = bvd.process_file(os.path.join(directory, f))
                if len(to_append) == 0:
                    # if no sound is detected an empty dataframe is created
                    to_append = pd.DataFrame(empty_dict)
                to_append['filename'] = split[0]
                df.append(to_append)
                processed += 1
            except:
                failed.append(split[0])

    df = pd.concat(df)
    df.index = range(len(df))
    df.rename(columns={'Time (hh:mm:ss)': 't_start_detect'}, inplace=True)

    # Conversion to datetime format
    df['t_start_detect'] = pd.to_datetime(df['t_start_detect'])
    df['t_end_detect'] = df['t_start_detect'].add(dt.timedelta(milliseconds=150))
    
    # Supression of overlaps between sucessively detected sounds
    grouped = df.groupby('filename')
    df = pd.DataFrame()

    for filename, ds in grouped:

        ds['t_end_detect'] = [min(start, end) for start, end in zip(ds['t_end_detect'][:-1], ds['t_start_detect'][1:])] + \
            [ds['t_end_detect'].iloc[-1]]
        df = df.append(ds)
    
    print(f'Directory process, {processed} file analyzed, {len(failed)} errors')
    
    remove = [os.remove(os.path.join(directory, f)) for f in os.listdir(directory) if 'checklist' in f]
    
    return df, failed


def dt_to_sec(dt_object):
    '''
    Takes a pandas Timestamp object as input and convert it into seconds
    Parameters:
    - pandas Timestamp (equivalent to python datetime) dt_object: a date format object that is first parsed to a string then split into
    a list of time elements
    Returns:
    - float indicating the corresponding amount of seconds rounded at the millisecond
    '''
    
    hrs, mins, secs, microsecs = dt_object.strftime('%H.%M.%S.%f').split('.')
    secs = 3600*int(hrs) + 60*int(mins) + int(secs)
    
    return np.round((1000*secs + int(microsecs)/1000)/1000, 3)


def compute_bvd_score(directory, extra_str_label=''):
    '''
    Computes precision and recall of birdvoxdetect on a birder's recordings.
    Parameters:
    - str directory: path to directory to process
    - str extra_str_label: the substring that is added in label files, depending of the birder
    Returns:
    - a tuple (tuple precision, tuple recall), each composed in turn of a tuple (int value, int binary_value). Binary precision/recall
    measure the existence of intersections between detected and labelled events, while non-binary values measure the size of these
    intersection regarding the whole duration of detected and labelled events.
    '''

    ### Labels dataset
    labels = create_label_dataset(directory, extra_str_label=extra_str_label)

    ### Bvd detected calls dataset
    df, failed = bvd_process_directory(directory)

    ### Merging detected sounds with labels dataframe

    # TODO: Gérer les cas où on n'a pas le fichier audio
    # labels = labels.loc[labels['filename']].isin(df['filename'])
    
    bvd_labels = df.merge(labels.loc[~(labels['filename'].isin(failed))], on='filename', how='outer')
    
    # Conversion of datetime columns to float
    temp = bvd_labels.loc[bvd_labels['t_start_detect'].notnull(), ['t_start_detect', 't_end_detect']]

    for dt_col in ['t_start_detect', 't_end_detect']:
        temp[dt_col] = temp[dt_col].map(dt_to_sec)
        del bvd_labels[dt_col]
        
    bvd_labels = bvd_labels.merge(temp, how='outer', left_index=True, right_index=True).sort_values(['filename', 't_start_detect'])

    # Addition of duration information
    bvd_labels['delta_detect'] = (bvd_labels['t_end_detect'] - bvd_labels['t_start_detect']).fillna(0).round(3)
    bvd_labels['delta'] = (bvd_labels['t_end'] - bvd_labels['t_start']).round(3)

    # True positives (one line per detected call per labelled sound), 'tp' is the duration in sec of the intersection between
    # detected call and labelled sound
    bvd_labels['tp'] = [np.round(max(0, min(end, end_detect) - max(start, start_detect)), 3) 
                        for (start, end, start_detect, end_detect) in zip(bvd_labels['t_start'], bvd_labels['t_end'],
                                                                        bvd_labels['t_start_detect'], bvd_labels['t_end_detect'])]
    # If the sound was not detected, intersection equals zero
    bvd_labels.loc[bvd_labels['t_start_detect'].isnull(), 'tp'] = 0

    ### Precision matrix

    precision_df = bvd_labels[['filename', 't_start_detect', 't_end_detect', 'delta_detect']].drop_duplicates()\
        .merge(bvd_labels.groupby(['filename', 't_start_detect'], as_index=False)['tp'].sum(), on=['filename', 't_start_detect'],
            how='outer')
    precision_df['tp'].fillna(0, inplace=True)

    # False positive
    precision_df['fp'] = precision_df['delta_detect'] - precision_df['tp']

    # Precision scores: for binary precision, a call is counted as true positive if at least part of it corresponds to an actual bird sound.
    # binary_precision is therefore higher than precision.
    precision = precision_df['tp'].sum()/(precision_df['tp'].sum() + precision_df['fp'].sum())
    binary_count = precision_df.dropna()['tp'].astype(bool).astype(int).value_counts()
    binary_precision = binary_count[1]/(binary_count[0] + binary_count[1])

    output = ((precision, binary_precision),)

    ### Recall matrix

    recall_df = bvd_labels[['filename', 't_start', 't_end', 'delta']].drop_duplicates()\
        .merge(bvd_labels.groupby(['filename', 't_start'], as_index=False)['tp'].sum(), on=['filename', 't_start'])
    
    # False negative
    recall_df['fn'] = recall_df['delta'] - recall_df['tp']

    # Recall scores
    recall = recall_df['tp'].sum()/(recall_df['tp'].sum() + recall_df['fn'].sum())
    binary_count = recall_df['tp'].astype(bool).astype(int).value_counts()
    binary_recall = binary_count[1]/(binary_count[0] + binary_count[1])

    output += ((recall, binary_recall),)

    return output