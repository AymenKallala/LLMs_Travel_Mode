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


def load_for_verification(file_path):
    data = pd.read_csv(file_path)
    dataset = data[["tweet", "Travel Mode", "Satisfaction", "Reason"]]
    return dataset


def load_for_trust_rate(gt_file_path, correction_file_path, labeled_lines):
    correction = pd.read_csv(correction_file_path)
    groundtruth = pd.read_excel(gt_file_path)[:labeled_lines][
        ["Travel Mode Correction Groundtruth", "Satisfaction Correction Groundtruth"]
    ].rename(
        columns={
            "Travel Mode Correction Groundtruth": "Travel_mode_verification",
            "Satisfaction Correction Groundtruth": "Satisfaction_verification",
        }
    )

    return correction, groundtruth
