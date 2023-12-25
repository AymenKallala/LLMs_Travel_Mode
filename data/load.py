import pandas as pd


def load(file_path, start = None, end = None,type='prediction'):
        
        data = pd.read_csv(file_path)[start:end]
        return data

def load_for_correction(file_path,start=0,end=2000):
    data = pd.read_csv(file_path)
    dataset = data[['tweet', 'Travel Mode', 'Satisfaction', 'Reason']][start:end]
    groundtruth = data[['Travel Mode Correction Groundtruth', 'Satisfaction Correction Groundtruth']][start:end].rename(columns={"Travel Mode Correction Groundtruth":'Travel_mode_verification',"Satisfaction Correction Groundtruth": "Satisfaction_verification"})
    return dataset,groundtruth

