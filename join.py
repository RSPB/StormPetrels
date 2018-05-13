import os
import pandas as pd
from birdutils import read_labels

features = pd.read_csv('/mnt/data/Birdman/results/warbler/features.csv')
labels_dict = read_labels('/mnt/data/Birdman/sthelena_labels.xls')
feature_group = features.groupby('sound.files', group_keys=True)
labels_all = pd.concat(labels_dict, axis=0, ignore_index=True)
print('Found signals: ', len(features))
print('Labelled calls: ', len(labels_all))

def find_overlap(group):
    name = os.path.splitext(group.name)[0]
    labels = labels_dict[name]
    label_start = labels['Time Start']
    label_end = labels['Time End']

    result = []

    for index, row in group.iterrows():
        start = row['start']
        end = row['end']
        overlap = any((label_start <= end) & (label_end >= start))
        result.append(overlap)
        # print('start {} end {} overlap {}'.format(start, end, overlap))
    group['overlap'] = result

    return group

x = feature_group.apply(find_overlap)