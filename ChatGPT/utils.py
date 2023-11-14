import json
import pandas as pd


def prompt(input,technique = 'in_context') :
    
    if technique == 'in_context':
  
        return("""Your goal is to retrieve the travel mode, the satisfaction (it has to be True or False) and the reason of the satisfaction, from a tweet.


            ### Examples:

            Tweet : " Jesus, I've been waiting at this train station for an hour, they do not seem to be rushing to solve the left package issue... I hate NYC transit"
            ["travel_mode" : "Train", "satisfaction" : "False", "reason": "left package"]
                
            Tweet: "My computer died 3 hours ago"
            ["travel_mode" : "N/A", "satisfaction" : "N/A", "reason": "N/A"]

            ### Now give me the output for this tweet :
            {}


            ONLY ANSWER WITH THE JSON OUTPUT FORMAT """.format(input))
    
    if technique == 'analogical':
        return("""Your goal is to retrieve the travel mode, the satisfaction (it has to be True or False) and the reason of the satisfaction, from a tweet.

                When presenting a given tweet, recall three relevant tweets as example. The relevant tweets should be distinct from each other and
                from the initial one (e.g., involving different modes and reasons of satisfaction). For each example answer to the questions.Afterward, proceed to detect the travel mode in the initial tweet, the satisfaction regarding it and the reason.
               
               ### Generate examples
               For each of the example you recall, detect the travel mode, the satisfaction and the reason. You will incorporate them in the final output.

                ### Now give the output for this tweet :
                {}

                ### Response:
                ONLY ANSWER WITH THE JSON OUTPUT FORMAT.your answer has to get the following fields. I wrote you description of each one :
                
               ("example_1" : Recall a first example of tweet that is relevant to the initial tweet,
               "travel_mode1": This is the travel mode for the first  example,
               "satisfaction1": This is the satisfaction towards the travel mode for the first  example,
               "reason1": This is the reason of the satisfaction for the first  example,
               "example_2" : Recall a second example of tweet that is relevant to the initial tweet,
               "travel_mode2": This is the travel mode for the second example,
               "satisfaction2": This is the satisfaction towards the travel mode for the second example",
               "reason2": This is the reason of the satisfaction for the second example,
               "example_3": Recall a third example of tweet that is relevant to the initial tweet,
               "travel_mode3": This is the travel mode for the third example,
               "satisfaction3": This is the satisfaction towards the travel mode for the third example,
               "reason3": This is the reason of the satisfaction for the third example,
               "example_1": This is the travel mode for the initial tweet, return 'N/A' if non applicable,
               "travel_mode1": This is the satisfaction towards the travel mode for the initial tweet, return 'N/A' if non applicable,
               "satisfaction1": This is the reason of the satisfaction for the initial tweet, you can be exhaustive here. Return 'N/A' if non applicable
               )""".format(input))

def parse_gpt_output(output):
    string = output.strip()
    try:
        string = json.loads(string)
    except :
        print("An error occured with formatting")
    finally:
        return string

def process_output(output_dict,technique = 'in_context'):

    if technique == 'in_contex':
        output_df = pd.DataFrame.from_dict(output_dict,orient='index')
        output_df["Travel Mode"] = output_df["output"].apply(lambda x: x["travel_mode"])
        output_df["Satisfaction"] = output_df["output"].apply(lambda x: x["satisfaction"])
        output_df["Reason"] = output_df["output"].apply(lambda x: x["reason"])

        return output_df[["tweet","Travel Mode","Satisfaction","Reason"]]
    
    if technique == 'analogical':
        pass