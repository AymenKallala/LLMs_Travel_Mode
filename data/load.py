import pandas as pd


def load(file_path_1, file_path_2, start=None, end=None):
    first_data = pd.read_csv(file_path_1, usecols=["GLOBAL_ID", "processed_txt"])[
        start:end
    ].set_index("GLOBAL_ID")
    second_data = pd.read_csv(file_path_2, usecols=["GLOBAL_ID", "processed_txt"])[
        start:end
    ].set_index("GLOBAL_ID")
    data = pd.concat([first_data, second_data], ignore_index=False, axis=0)
    return data


def load_for_correction(file_path, start=0, end=2000):
    data = pd.read_csv(file_path)
    dataset = data[["tweet", "Travel Mode", "Satisfaction", "Reason"]][start:end]
    groundtruth = data[
        ["Travel Mode Correction Groundtruth", "Satisfaction Correction Groundtruth"]
    ][start:end].rename(
        columns={
            "Travel Mode Correction Groundtruth": "Travel_mode_verification",
            "Satisfaction Correction Groundtruth": "Satisfaction_verification",
        }
    )
    return dataset, groundtruth
