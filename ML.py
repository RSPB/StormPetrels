from comet_ml import Experiment

import os
import glob
import warnings
import plotutils
import joblib
import xgboost as xg
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import model_selection
from sklearn.metrics import f1_score, precision_score, recall_score, confusion_matrix, accuracy_score

warnings.filterwarnings(module='sklearn*', action='ignore', category=DeprecationWarning)

feature_paths = glob.glob('/mnt/data/Birdman/samples/features/feature*.csv')

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


def main(feature_paths):
    for path in feature_paths:
        train(path)


def train(path):
    name = os.path.splitext(os.path.basename(path))[0]
    print('Processing: ', name)
    features = pd.read_csv(path, index_col=None)
    selected_features_names = [name for name, desc in selected_features]
    features = features[selected_features_names]
    split_idx = 1200
    features = features.drop(['sound.files'], axis=1)
    noise_only_df, df = features.iloc[:split_idx], features.iloc[split_idx:]
    y = df.pop('petrel')
    X = df.values
    y_noise = noise_only_df.pop('petrel')
    X_noise = noise_only_df.values
    X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)
    hyperparams = {
        'n_estimators': [100, 300, 500, 1000],
        'learning_rate': [0.1],
        'gamma': [0.0, 0.5],
        'max_depth': [2, 3, 4],
        'min_child_weight': [1, 2],
        'subsample': [1.0, 0.8],
        'reg_alpha': [0.0, 0.1],
        'reg_lambda': [1, 2, 3]
    }
    #
    # hyperparams = {
    #     'n_estimators': [100],
    #     'learning_rate': [0.1],
    #     'gamma': [0.0],
    #     'max_depth': [2],
    #     'min_child_weight': [1],
    #     'subsample': [1.0],
    #     'reg_alpha': [0.0],
    #     'reg_lambda': [1]
    # }

    clf = model_selection.GridSearchCV(estimator=xg.XGBClassifier(objective='binary:logistic', n_jobs=-1),
                                       param_grid=hyperparams,
                                       cv=4)
    fit_params = clf.fit(X_train, y_train)
    estimator = fit_params.best_estimator_
    joblib.dump(estimator, name + '_model.pkl')

    test_pred = estimator.predict(X_test)
    metrics = calculate_metrics(test_pred, y_test)

    noise_pred = estimator.predict(X_noise)
    noise_detection_accuracy = accuracy_score(y_noise, noise_pred)

    experiment = Experiment(api_key="4PdGdUZmGf6P8QsMa5F2zB4Ui",
                            project_name="storm petrels",
                            workspace="tracewsl")
    experiment.set_name(name)
    experiment.log_parameter('name', name)
    experiment.log_multiple_params(fit_params.best_params_)
    experiment.log_multiple_metrics(metrics)
    experiment.log_metric('Noise detection accuracy', noise_detection_accuracy)
    experiment.log_figure('Confusion matrix', get_confusion_matrix_figure(test_pred, y_test))
    experiment.log_figure('Feature importnace', get_feature_importance_figure(estimator, list(df.columns.values)))


def get_feature_importance_figure(estimator, feature_names):
    fig, ax = plt.subplots(figsize=(12, 8))
    y_pos = range(len(feature_names))
    plt.barh(y_pos, estimator.feature_importances_)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(feature_names, fontsize=14)
    return fig


def get_confusion_matrix_figure(test_pred, y_test):
    cm = confusion_matrix(y_true=y_test, y_pred=test_pred)
    cmf_fig = plotutils.print_confusion_matrix(confusion_matrix=cm,
                                               class_names=['noise', 'petrels'],
                                               figsize=(12, 12))
    return cmf_fig


def calculate_metrics(y_prediction, y_true):
    metrics = {
        'accuracy': accuracy_score(y_true=y_true, y_pred=y_prediction),
        'precision': precision_score(y_true=y_true, y_pred=y_prediction),
        'recall': recall_score(y_true=y_true, y_pred=y_prediction),
        'f1-score': f1_score(y_true=y_true, y_pred=y_prediction),
    }
    return metrics


if __name__ == '__main__':
    main(feature_paths)
