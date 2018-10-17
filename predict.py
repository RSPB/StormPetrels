import os
import numpy
import glob
import joblib
import pandas as pd
import constants
from multiprocessing import Pool, cpu_count

results_folder = '/mnt/data/Birdman/full/results/warbler_grid08_bp1-6_wl256_th2'
model_path = '/mnt/data/Birdman/models/features_petrels_bp1-6_wl256_th2_model.pkl'
model = joblib.load(model_path)


def predict(path):
    df = pd.read_csv(path, index_col=None)
    X = df[constants.selected_features_names]
    X = X.fillna(0)
    y_prob = model.predict_proba(X.values)
    df['stormpetrel_proba'] = y_prob[:,1]
    return df[['sound.files', 'selec', 'start', 'end', 'stormpetrel_proba']]


if __name__ == '__main__':
    results_paths = glob.glob(results_folder + '/*.csv')
    with Pool(cpu_count()) as pool:
        results = pool.map(predict, results_paths)
        df = pd.concat(results)
        df.to_csv(os.path.basename(results_folder) + '_results.csv', index=False)