import json
import re

import pandas as pd


def process_text(input):
    pattern = r"json"
    pattern_2 = r"```"
    pattern_3 = "\n"
    regexed = re.sub(pattern, "", input)
    regexed = re.sub(pattern_2, "", regexed)
    regexed = re.sub(pattern_3, "", regexed)
    return regexed


def parse_gpt_output(output):
    string = process_text(output).strip()
    # print("string outputted by the model: ", string)
    try:
        string = json.loads(string)
        # print("Correct string")

    except:
        print("An error occured with json formatting of the LLM output")
    finally:
        return string


def handle_error_apply(x, key1, key2):
    try:
        return x[key1][key2]
    except:
        return "Error"


def travel_mode(x):
    try:
        return x["travel_mode"]
    except:
        return "Error"


def satisfaction(x):
    try:
        return x["satisfaction"]
    except:
        return "Error"


def reason(x):
    try:
        return x["reason"]
    except:
        return "Error"


def process_output(output_dict, technique="in_context"):
    if technique == "in_context" or technique == "COT" or technique == "zero_shot":
        output_df = pd.DataFrame.from_dict(output_dict, orient="index")
        output_df["Travel Mode"] = output_df["output"].apply(lambda x: travel_mode(x))
        output_df["Satisfaction"] = output_df["output"].apply(lambda x: satisfaction(x))
        output_df["Reason"] = output_df["output"].apply(lambda x: reason(x))

        return output_df[["tweet", "Travel Mode", "Satisfaction", "Reason"]]

    if technique == "analogical":
        output_df = pd.DataFrame.from_dict(output_dict, orient="index")

        output_df["Travel Mode"] = output_df["output"].apply(lambda x: travel_mode(x))
        output_df["Satisfaction"] = output_df["output"].apply(lambda x: satisfaction(x))
        output_df["Reason"] = output_df["output"].apply(lambda x: reason(x))
        output_df["Example 1"] = output_df["output"].apply(
            lambda x: handle_error_apply(x, "example_1", "tweet")
        )
        output_df["Travel Mode 1"] = output_df["output"].apply(
            lambda x: handle_error_apply(x, "example_1", "travel_mode_1")
        )
        output_df["Satisfaction 1"] = output_df["output"].apply(
            lambda x: handle_error_apply(x, "example_1", "satisfaction_1")
        )
        output_df["Reason 1"] = output_df["output"].apply(
            lambda x: handle_error_apply(x, "example_1", "reason_1")
        )
        output_df["Example 2"] = output_df["output"].apply(
            lambda x: handle_error_apply(x, "example_2", "tweet")
        )
        output_df["Travel Mode 2"] = output_df["output"].apply(
            lambda x: handle_error_apply(x, "example_2", "travel_mode_2")
        )
        output_df["Satisfaction 2"] = output_df["output"].apply(
            lambda x: handle_error_apply(x, "example_2", "satisfaction_2")
        )
        output_df["Reason 2"] = output_df["output"].apply(
            lambda x: handle_error_apply(x, "example_2", "reason_2")
        )
        output_df["Example 3"] = output_df["output"].apply(
            lambda x: handle_error_apply(x, "example_3", "tweet")
        )
        output_df["Travel Mode 3"] = output_df["output"].apply(
            lambda x: handle_error_apply(x, "example_3", "travel_mode_3")
        )
        output_df["Satisfaction 3"] = output_df["output"].apply(
            lambda x: handle_error_apply(x, "example_3", "satisfaction_3")
        )
        output_df["Reason 3"] = output_df["output"].apply(
            lambda x: handle_error_apply(x, "example_3", "reason_3")
        )

        return output_df[
            [
                "tweet",
                "Travel Mode",
                "Satisfaction",
                "Reason",
                "Example 1",
                "Travel Mode 1",
                "Satisfaction 1",
                "Reason 1",
                "Example 2",
                "Travel Mode 2",
                "Satisfaction 2",
                "Reason 2",
                "Example 3",
                "Travel Mode 3",
                "Satisfaction 3",
                "Reason 3",
            ]
        ]

    if technique == "self_verification":
        try:
            output_df = pd.DataFrame.from_dict(output_dict, orient="index")
            return output_df
        except:
            return output_dict
