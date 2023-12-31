import pandas as pd
from data import load_for_trust_rate
import argparse


def correcter_rate(pred, groundtruth):
    n = len(groundtruth)
    gt = groundtruth[["Travel_mode_verification", "Satisfaction_verification"]]
    pred = pred[["Travel_mode_verification", "Satisfaction_verification"]][:n].replace(
        to_replace={"Correct": True, "Not Correct": False}
    )

    correct_pred = sum(
        pred["Travel_mode_verification"] == gt["Travel_mode_verification"]
    ) + sum(pred["Satisfaction_verification"] == gt["Satisfaction_verification"])
    total = n * 2

    return correct_pred / total


def main(args):
    correction, gt = load_for_trust_rate(
        args.GT_PATH, args.CORRECTION_PATH, labeled_lines=args.labeled_lines
    )
    print(f" Trust rate: {correcter_rate(correction,gt)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--GT_PATH",
        default="../data/configs/fashionpedia.yaml",
        type=str,
        help="Path for the data file 1",
    )
    parser.add_argument(
        "--CORRECTION_PATH",
        default="no_technique_specified",
        type=str,
        help="Path for the data file 1",
    )
    parser.add_argument(
        "--labeled_lines",
        default="25",
        type=int,
        help="number of hand verified lines",
    )

    args = parser.parse_args()

    main(args)
