# Checks to see if the imdb_data.csv file is created (for convenience).
# If not, load all files from the acllmdb folder into a dataframe object
# and then save the dataframe using to_csv with the specified encoding parameters.

import os, time
import numpy as np
import pandas as pd
from pathlib import Path


def process(folder: str, encoding='utf-8'):
    file = Path('data/imdb_data.csv')
    if file.exists():
        print('Data file exists and is loaded.')
        return

    start = time.time()
    labels = {'pos': 1, 'neg': 0}
    dataframe = pd.DataFrame()

    for s in ('test', 'train'):
        for l in ('pos', 'neg'):
            path = '{}/{}/{}'.format(folder, str(s), str(l))
            for file in os.listdir(path):
                with open(os.path.join(path, file), 'r', encoding=encoding) as infile:
                    print(path, file)
                    txt = infile.read()
                    dataframe = dataframe.append([[txt, labels[l]]], ignore_index=True)

    dataframe.columns = ['review', 'sentiment']
    np.random.seed(0)
    dataframe = dataframe.reindex(np.random.permutation(dataframe.index))
    dataframe.to_csv('data/imdb_data.csv', index=False, encoding=encoding)

    print('Data file successfully loaded.')
    print('Total time elapsed:', time.time() - start, 'sec')
    return
