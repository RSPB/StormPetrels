from comet_ml import Experiment

import os
import glob
import warnings
import plotutils
import xgboost as xg
import pandas as pd
from sklearn import model_selection
from sklearn.metrics import f1_score, precision_score, recall_score, confusion_matrix, accuracy_score

warnings.filterwarnings(module='sklearn*', action='ignore', category=DeprecationWarning)

selected_features = (
    ('petrel', 'presence of storm petrel'),
    ('sound.files', 'name of the file'),
    ('meanfreq', 'mean frequency (in kHz)'),
    ('sd', 'standard deviation of frequency'),
    ('freq.Q75', 'third quantile (in kHz)'),
    ('freq.IQR', 'interquantile range (in kHz)'),
    ('skew', 'skewness - asymmetry of the spectrum'),
    ('kurt', 'kurtosis - peakedness of the spectrum'),
    ('sp.ent', 'spectral entropy'),
    ('sfm', 'spectral flatness'),
    ('meanfun', 'average of fundamental frequency'),
    ('maxfun', 'maximum fundamental frequency'),
    ('meandom', 'average of dominant frequency'),
    ('dfrange', 'range of dominant frequency'),
    ('modindx', 'modulation index'),
    ('meanpeakf', 'mean peak frequency'))


if __name__ == '__main__':
    feature_paths = glob.glob('/mnt/data/Birdman/samples/features/feature*.csv')
    for path in feature_paths:
        experiment = Experiment(api_key="4PdGdUZmGf6P8QsMa5F2zB4Ui",
                                project_name="storm petrels",
                                workspace="tracewsl")

        features = pd.read_csv(path, index_col=None)

        selected_features_names = [name for name, desc in selected_features]
        features = features[selected_features_names]

        split_idx = 1200
        noise_only_df, df = features.iloc[:split_idx], features.iloc[split_idx:]
        df = df.drop(['sound.files'], axis=1)
        y = df.pop('petrel')
        X = df.values

        X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size=0.25, random_state=42)

        hyperparams = {
            'n_estimators': [100, 200],
            'learning_rate': [0.1],
            'gamma': [0.0, 0.5],
            'max_depth': [2,3,4],
            'min_child_weight': [1,2,3],
            'subsample': [1.0, 0.8],
            'reg_alpha': [0.0, 0.1],
            'reg_lambda': [1,2]
        }

        clf = model_selection.GridSearchCV(estimator=xg.XGBClassifier(objective='binary:logistic', n_jobs=-1),
                                           param_grid=hyperparams,
                                           cv=4)

        fit_params = clf.fit(X_train, y_train)
        estimator = fit_params.best_estimator_
        test_pred = estimator.predict(X_test)

        metrics = {
            'accuracy': accuracy_score(y_true=y_test, y_pred=test_pred),
            'precision': precision_score(y_true=y_test, y_pred=test_pred),
            'recall': recall_score(y_true=y_test, y_pred=test_pred),
            'f1-score': f1_score(y_true=y_test, y_pred=test_pred),
        }
        cm = confusion_matrix(y_true=y_test, y_pred=test_pred)

        experiment.log_parameter('name', os.path.basename(path))
        experiment.log_multiple_params(fit_params.best_params_)
        experiment.log_multiple_metrics(metrics)

        cmf_fig = plotutils.print_confusion_matrix(confusion_matrix=cm,
                                                   class_names=['noise', 'petrels'],
                                                   figsize=(12,12))

        experiment.log_figure('Confusion matrix', cmf_fig)

