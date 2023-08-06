from scipy import stats
from xgboost import XGBRegressor
import numpy as np
import pandas as pd


def verify_ml_dataset(dataset):
    # check for null values in pandas dataframe
    DATA_IMBALANCE_THRESHOLD = 0.1
    TOO_MANY_ZEROES_THRESHOLD = 0.1
    FEATURE_IMPORTANCE_THRESHOLD = 0.01

    checks = {"null_values": "",
              "too_many_zeroes": "",
              "label": "",
              "outliers": "",
              "data_imbalance": "",
              "data_format": "",
              "low_importance_features": "",
              "data_normalization": "",
              "string_features": ""
              }
    Y = pd.DataFrame()

    # check for null values in pandas dataframe
    if dataset.isnull().values.any():
        checks["null_values"] = "error"
    else:
        checks["null_values"] = "ok"

    # check for label config
    for column in dataset.columns:
        if 'label' in column:
            Y[column] = dataset[column]
            dataset.drop(column, axis=1, inplace=True)
    if Y.empty:
        checks["label"] = "error"
    else:
        checks["label"] = "ok"

    # check for string columns in pandas dataframe
    if (dataset.dtypes == object).sum() > 0:
        checks["string_features"] = "error"
    else:
        checks["string_features"] = "ok"

    # check for too many zeroes in pandas dataframe
    count = 0
    for column_name in dataset.columns:
        column = dataset[column_name]
        count += (column == 0).sum()
        if count > len(dataset)*TOO_MANY_ZEROES_THRESHOLD:
            checks["too_many_zeroes"] = "warning"

    # Check for outliers
    if checks['string_features'] == "ok":
        z_scores = stats.zscore(dataset)
        abs_z_scores = np.abs(z_scores)
        # Select data points with a z-scores above or below 3
        filtered_entries = (abs_z_scores < 3).all(axis=1)
        if len(filtered_entries) > 0:
            checks["outliers"] = "warning"
        else:
            checks["outliers"] = "ok"

    # Check for data imbalance
    if checks['label'] == 'ok':
        try:
            values = Y.value_counts()
            if values[0]*DATA_IMBALANCE_THRESHOLD > values[1] or values[1]*DATA_IMBALANCE_THRESHOLD > values[0]:
                checks["data_imbalance"] = "warning"
            else:
                checks["data_imbalance"] = "ok"
        except:
            labels = []
            for column_name in Y.columns:
                if 'label' in column_name:
                    labels.append(dataset[column_name][1])
            labels.sort()
            if labels[0]*DATA_IMBALANCE_THRESHOLD > labels[-1] or labels[-1]*DATA_IMBALANCE_THRESHOLD > labels[0]:
                checks["data_imbalance"] = "warning"
            else:
                checks["data_imbalance"] = "ok"

    # check for feature importance
    if checks['string_features'] == "ok":
        xgb = XGBRegressor()
        xgb.fit(dataset, Y)
        importance = xgb.feature_importances_
        for score in importance:
            if score < FEATURE_IMPORTANCE_THRESHOLD:
                checks["low_importance_features"] = "warning"
                break
        else:
            checks["low_importance_features"] = "ok"

    # Data normalization
    if checks['string_features'] == "ok":
        for val in dataset.min():
            if val < -1:
                checks["data_normalization"] = "warning"
                break
        else:
            checks["data_normalization"] = "ok"
        for val in dataset.max():
            if val > 1:
                checks["data_normalization"] = "warning"
                break
        else:
            checks["data_normalization"] = "ok"

    return checks
