import pandas as pd


def load(file_path, start = None, end = None,verification=False):
    if verification:
        data = pd.read_excel(file_path,usecols=['tweet', 'Travel Mode', 'Satisfaction', 'Reason'])[start:end]
    else:
        data = pd.read_csv(file_path)[start:end]

    return data
