import pandas as pd


def correcter_rate(pred, groundtruth):
    n = len(groundtruth)
    gt = groundtruth[["Travel_mode_verification", "Satisfaction_verification"]]
    pred = pred[["Travel_mode_verification", "Satisfaction_verification"]][:n]

    correct_pred = sum(
        pred["Travel_mode_verification"] == gt["Travel_mode_verification"]
    ) + sum(pred["Satisfaction_verification"] == gt["Satisfaction_verification"])
    total = n * 2

    return correct_pred / total
