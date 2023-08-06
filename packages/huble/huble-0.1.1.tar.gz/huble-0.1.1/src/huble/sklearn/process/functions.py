from re import sub
from sklearn import preprocessing
import pandas as pd


def normalize(params):
    preprocessing.normalize(**params)


def drop_duplicates(data_frame=None, subset=None, keep="first"):
    #TODO : Add support for ignore index
    data_frame.drop_duplicates(subset=subset, keep=keep)

