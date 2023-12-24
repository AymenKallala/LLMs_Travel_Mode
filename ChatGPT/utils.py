import json
import pandas as pd
import re


def prompt(
    input, travel_mode=None, reason=None, satisfaction=None, technique="in_context"
):
    if technique == "in_context":
        return """Your goal is to retrieve the travel mode, the satisfaction (satisfied,dissatisfied or neutral) and the reason of the satisfaction, from a tweet.


            ### Examples:

            Tweet : " Jesus, I've been waiting at this train station for an hour, they do not seem to be rushing to solve the left package issue... I hate NYC transit"
            ["travel_mode" : "train", "satisfaction" : "dissatisfied", "reason": "left package"]
                
            Tweet: "My computer died 3 hours ago"
            ["travel_mode" : "N/A", "satisfaction" : "N/A", "reason": "N/A"]
               
            Tweet: "My Uber driver is so sweet, he let me plug my phone to the Bluetooth and play my own playlist"
            ["travel_mode" : "uber", "satisfaction" : "satisfied", "reason": "The uber is sweet and let custom music playing"]
               
            Tweet: "I am currently seating in the back of the bus, there's an horrifc smell coming out the person next to me...."
            ["travel_mode" : "bus", "satisfaction" : "dissatisfied", "reason": "horrific smell"]

            ### Now give me the output for this tweet :
            {}


            ONLY ANSWER WITH THE JSON OUTPUT FORMAT """.format(
            input
        )
    if technique == "COT":
        return """Your goal is to retrieve the travel mode, the satisfaction (satisfied,dissatisfied or neutral) and the reason of the satisfaction, from a tweet.


            ### Examples:

            Tweet : " Jesus, I've been waiting at this train station for an hour, they do not seem to be rushing to solve the left package issue... I hate NYC transit"
               
                In this tweet, the user mentionned the train, it is obviously the travel mode. They also mentionned a long waiting time with an injuction "Jesus" which refers to a non satisfaction and also gives the reason : long waiting time because of a left package issue.
            
                ["travel_mode" : "Train", "satisfaction" : "dissatisfied", "reason": "left package"]
                
            Tweet: "My computer died 3 hours ago"
               
                In this tweet, no mention of any travel mode is done. So we cannot determine any.

                ["travel_mode" : "N/A", "satisfaction" : "N/A", "reason": "N/A"]
               
            Tweet: "My Uber driver is so sweet, he let me plug my phone to the Bluetooth and play my own playlist"
               
               In this tweet, the user mention specifically that they are in a uber and that the driver is sweet enough to let pick the music

            ["travel_mode" : "uber", "satisfaction" : "satisfied", "reason": "The uber is sweet and let custom music playing"]
               
            Tweet: "I am currently seating in the back of the bus, there's an horrifc smell coming out the person next to me...."
               
               In this tweet, the bus is specifically mentioned. Besides, the term horrific smell let us know that the user is not satisfied and that it is the reason why.

            ["travel_mode" : "bus", "satisfaction" : "dissatisfied", "reason": "horrific smell"]

            ### Now give me the output for this tweet :
            {}


            ONLY ANSWER WITH THE JSON OUTPUT FORMAT """.format(
            input
        )

    if technique == "analogical":
        return """Your goal is to retrieve the travel mode, the satisfaction (satisfied,dissatisfied or neutral) and the reason of the satisfaction, from a tweet.

                When presenting a given tweet, recall three relevant tweets as example. The relevant tweets should be distinct from each other and
                from the initial one (e.g., involving different modes and reasons of satisfaction). For each example answer to the questions.Afterward, proceed to detect the travel mode in the initial tweet, the satisfaction regarding it and the reason.
               
                ONLY ANSWER WITH a JSON OUTPUT FORMAT. your answer has to get the following fields with the same structure. I wrote you a description of each one :
                
               ["example_1" : Recall a first example of tweet that is relevant to the initial tweet,
               ("tweet" : Write the first tweet example,
               "travel_mode_1": This is the travel mode for the first  example,
               "satisfaction_1": This is the satisfaction towards the travel mode for the first  example,
               "reason_1": This is the reason of the satisfaction for the first  example,)
               "example_2" : Recall a second example of tweet that is relevant to the initial tweet,
               ("tweet" : Write the second tweet example,
               "travel_mode_2": This is the travel mode for the second example,
               "satisfaction_2": This is the satisfaction towards the travel mode for the second example",
               "reason_2": This is the reason of the satisfaction for the second example,)
               "example_3": Recall a third example of tweet that is relevant to the initial tweet,
               ("tweet" : Write the third tweet example,
               "travel_mode_3": This is the travel mode for the third example,
               "satisfaction_3": This is the satisfaction towards the travel mode for the third example,
               "reason_3": This is the reason of the satisfaction for the third example,)
               "travel_mode": This is the travel mode for the initial tweet, return 'N/A' if non applicable,
               "satisfaction": This is the satisfaction towards the travel mode for the initial tweet, return 'N/A' if non applicable,
               "reason": This is the reason of the satisfaction for the initial tweet, you can be exhaustive here. Return 'N/A' if non applicable
               ]
               
               ### Generate examples
               For each of the example you recall, detect the travel mode, the satisfaction and the reason. You will incorporate them in the final output.

                ### Now answer for this tweet :
                {}
     
               """.format(
            input
        )
    if technique == "self_verification":
        return """ In this tweet: {}

            Your goal is to verify the following statements:

            STATEMENT 1: The travel mode detected in the tweet is "{}".
            STATEMENT 2: The user's satisfaction towards the travel mode is "{}".
            STATEMENT 3: The reason of satisfaction is "{}".
            
            Answer the following questions: 
                Q1: Is STATEMENT 1 correct ? It is possible that the tweet does not mention any travel mode, in which case the right statement would be 'Nan' or 'nan' or 'NaN'.
                Q2: Is STATEMENT 2 correct ? It is possible that the text does not mention any satisfaction, in which case the right statement would be 'Nan' or 'nan' or 'NaN'.
                Q3: Is STATEMENT 3 correct ? It is possible that the text does not mention any reason, in which case the right statement would be 'Nan' or 'nan' or 'NaN'.

            ONLY ANSWER WITH True or False.
            ONLY ANSWER WITH a JSON OUTPUT FORMAT.your answer has to get the following fields with the same structure. I wrote you a description of each one :
                [   "Travel_mode_verification" : Answer to Q1,
                    "Satisfaction_verification" : Answer to Q2,
                    "Reason_satisfaction": Answer to Q3,
                ]

        """.format(
            input, travel_mode, satisfaction, reason
        )


def process_text(input):
    pattern = r"json"
    pattern_2 = r"```"
    pattern_3 = "\n"
    regexed = re.sub(pattern, "", input)
    regexed = re.sub(pattern_2, "", regexed)
    regexed = re.sub(pattern_3, "", regexed)
    return regexed


def parse_gpt_output(output, technique):
    string = process_text(output).strip()
    try:
        string = json.loads(string)
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
        return x["Travel_mode_verification"]
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

def tm_verification(x):
    try:
        return x["reason"]
    except:
        return "Error"
def satisfaction_verification(x):
    try:
        return x["Satisfaction_verification"]
    except:
        return "Error"
def reason_verification(x):
    try:
        return x["Reason_satisfaction"]
    except:
        return "Error"


def process_output(output_dict, technique="in_context"):
    if technique == "in_context" or technique == "COT":
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
        output_df = pd.DataFrame.from_dict(
            output_dict, orient="index"
        )
        output_df["Travel_mode_verification"] = output_df["Travel_mode_verification"].apply(lambda x: tm_verification(x))
        output_df["Satisfaction_verification"] = output_df["Satisfaction_verification"].apply(lambda x: satisfaction_verification(x))
        output_df["Reason_verification"] = output_df["Reason_verification"].apply(lambda x: reason_verification(x))

        return output_df[["Travel_mode_verification", "Satisfaction_verification", "Reason_verification"]]
