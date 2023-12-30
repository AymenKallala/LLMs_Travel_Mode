def prompt(
    input, travel_mode=None, reason=None, satisfaction=None, technique="in_context"
):
    if technique == "zero_shot":
        return """Your goal is to retrieve the travel mode, the satisfaction (satisfied,dissatisfied or neutral) and the reason of the satisfaction, from this tweet:
            {}


            ONLY ANSWER WITH THE JSON OUTPUT FORMAT.your answer has to get the following fields with the same structure. I wrote you a description of each one :
                        {{"travel_mode" : Travel mode detected (can be N/A),"satisfaction" : Satisfaction detected (satisfied,dissatisfied or neutral),"reason": reason towards the satisfaction detected}}
            Be careful to use DOUBLE QUOTES to denote the keys. """.format(
            input
        )
    if technique == "in_context":
        return """Your goal is to retrieve the travel mode, the satisfaction (satisfied,dissatisfied or neutral) and the reason of the satisfaction, from a tweet.


            ### Examples:

            Tweet : " Jesus, I've been waiting at this train station for an hour, they do not seem to be rushing to solve the left package issue... I hate NYC transit"
            {{"travel_mode" : "train", "satisfaction" : "dissatisfied", "reason": "left package"}}
                
            Tweet: "My computer died 3 hours ago"
            {{"travel_mode" : "N/A", "satisfaction" : "N/A", "reason": "N/A"}}
               
            Tweet: "My Uber driver is so sweet, he let me plug my phone to the Bluetooth and play my own playlist"
            {{"travel_mode" : "uber", "satisfaction" : "satisfied", "reason": "The uber is sweet and let custom music playing"}}
               
            Tweet: "I am currently seating in the back of the bus, there's an horrifc smell coming out the person next to me...."
            {{"travel_mode" : "bus", "satisfaction" : "dissatisfied", "reason": "horrific smell"}}

            ### Now give me the output for this tweet :
            {}


            ONLY ANSWER WITH THE JSON OUTPUT FORMAT
            Be careful to use DOUBLE QUOTES to denote the keys. """.format(
            input
        )
    if technique == "COT":
        return """Your goal is to retrieve the travel mode, the satisfaction (satisfied,dissatisfied or neutral) and the reason of the satisfaction, from a tweet.


            ### Examples:

            Tweet : " Jesus, I've been waiting at this train station for an hour, they do not seem to be rushing to solve the left package issue... I hate NYC transit"
               
                In this tweet, the user mentionned the train, it is obviously the travel mode. They also mentionned a long waiting time with an injuction "Jesus" which refers to a non satisfaction and also gives the reason : long waiting time because of a left package issue.
            
                {{"travel_mode" : "Train", "satisfaction" : "dissatisfied", "reason": "left package"}}
                
            Tweet: "My computer died 3 hours ago"
               
                In this tweet, no mention of any travel mode is done. So we cannot determine any.

                {{"travel_mode" : "N/A", "satisfaction" : "N/A", "reason": "N/A"}}
               
            Tweet: "My Uber driver is so sweet, he let me plug my phone to the Bluetooth and play my own playlist"
               
               In this tweet, the user mention specifically that they are in a uber and that the driver is sweet enough to let pick the music

            {{"travel_mode" : "uber", "satisfaction" : "satisfied", "reason": "The uber is sweet and let custom music playing"}}
               
            Tweet: "I am currently seating in the back of the bus, there's an horrifc smell coming out the person next to me...."
               
               In this tweet, the bus is specifically mentioned. Besides, the term horrific smell let us know that the user is not satisfied and that it is the reason why.

            {{"travel_mode" : "bus", "satisfaction" : "dissatisfied", "reason": "horrific smell"}}

            ### Now give me the output for this tweet :
            {}


            ONLY ANSWER WITH THE JSON OUTPUT FORMAT
            Be careful to use DOUBLE QUOTES to denote the keys. """.format(
            input
        )

    if technique == "analogical":
        return """Your goal is to retrieve the travel mode, the satisfaction (satisfied,dissatisfied or neutral) and the reason of the satisfaction, from a tweet.

                When presenting a given tweet, recall three relevant tweets as example. The relevant tweets should be distinct from each other and
                from the initial one (e.g., involving different modes and reasons of satisfaction). For each example answer to the questions.Afterward, proceed to detect the travel mode in the initial tweet, the satisfaction regarding it and the reason.
               
                ONLY ANSWER WITH a JSON OUTPUT FORMAT. your answer has to get the following fields with the same structure. I wrote you a description of each one :
                
               {{"example_1" : Recall a first example of tweet that is relevant to the initial tweet,
               {{"tweet" : Write the first tweet example,
               "travel_mode_1": This is the travel mode for the first  example,
               "satisfaction_1": This is the satisfaction towards the travel mode for the first  example,
               "reason_1": This is the reason of the satisfaction for the first  example,}}
               "example_2" : Recall a second example of tweet that is relevant to the initial tweet,
               {{"tweet" : Write the second tweet example,
               "travel_mode_2": This is the travel mode for the second example,
               "satisfaction_2": This is the satisfaction towards the travel mode for the second example",
               "reason_2": This is the reason of the satisfaction for the second example,}}
               "example_3": Recall a third example of tweet that is relevant to the initial tweet,
               {{"tweet" : Write the third tweet example,
               "travel_mode_3": This is the travel mode for the third example,
               "satisfaction_3": This is the satisfaction towards the travel mode for the third example,
               "reason_3": This is the reason of the satisfaction for the third example,}}
               "travel_mode": This is the travel mode for the initial tweet, return 'N/A' if non applicable,
               "satisfaction": This is the satisfaction towards the travel mode for the initial tweet, return 'N/A' if non applicable,
               "reason": This is the reason of the satisfaction for the initial tweet, you can be exhaustive here. Return 'N/A' if non applicable
               }}
               Be careful to use DOUBLE QUOTES to denote the keys.
               
               ### Generate examples
               For each of the example you recall, detect the travel mode, the satisfaction and the reason. You will incorporate them in the final output.

                ### Now answer for this tweet :
                {}
     
               """.format(
            input
        )
    if technique == "self_verification":
        prompt = """I will give you a tweet and statements regarding it.

                Your goal is to answer the following questions:
                    Q1: Is STATEMENT 1 correct ? It is possible that the tweet does not mention any travel mode, in which case the right statement would be 'Nan' or 'nan' or 'NaN'.
                    Q2: Is STATEMENT 2 correct ? It is possible that the text does not mention any satisfaction, in which case the right statement would be 'Nan' or 'nan' or 'NaN'.
                    Q3: Is STATEMENT 3 correct ? It is possible that the text does not mention any reason, in which case the right statement would be 'Nan' or 'nan' or 'NaN'.
                
                
                #Examples

                    ##Example 1:
                        tweet: "remember when you could not get cell service in the subway... damn"
                        STATEMENT 1: The travel mode detected in the tweet is "subway".
                        STATEMENT 2: The user's satisfaction towards the travel mode is "dissatisfied".
                        STATEMENT 3: The reason of satisfaction is "could not get cell service".

                        Answer:
                            {{"Travel_mode_verification" : "Correct","Satisfaction_verification" : "Correct","Reason_verification": "Correct"}}

                    ##Example 2:
                        tweet: "can you tell the 96st station to move one of their train to the tracks beyond their stations, so this one can pull over"
                        STATEMENT 1: The travel mode detected in the tweet is "train".
                        STATEMENT 2: The user's satisfaction towards the travel mode is "neutral".
                        STATEMENT 3: The reason of satisfaction is "request for train to move to clear tracks".

                        Answer:
                            {{"Travel_mode_verification" : "Correct","Satisfaction_verification" : "Not Correct","Reason_verification": "Correct"}}

                    ##Example 3:
                        tweet: "just noticed the mta (?) installed stee bollards next to the new elevator. more steel bollards please https: and and t.co and fycdzlvyl4"
                        STATEMENT 1: The travel mode detected in the tweet is "mta".
                        STATEMENT 2: The user's satisfaction towards the travel mode is "satisfied".
                        STATEMENT 3: The reason of satisfaction is "installed steel bollards next to the new elevator".

                        Answer:
                            {{"Travel_mode_verification" : "Not Correct","Satisfaction_verification" : "Correct","Reason_verification": "Correct"}}
                    ##Example 4:
                        tweet: "too bad the mta has done nothing to increase service on 4th ave. we need to reconnect the city and it is transit. that is the only way we grow in a sane way."
                        STATEMENT 1: The travel mode detected in the tweet is "transit".
                        STATEMENT 2: The user's satisfaction towards the travel mode is "dissatisfied".
                        STATEMENT 3: The reason of satisfaction is "lack of increased service on 4th ave".

                        'transit' is not a travel mode! Hence STATEMENT 1 is Not Correct.

                        Answer:
                            {{"Travel_mode_verification" : "Not Correct","Satisfaction_verification" : "Correct","Reason_verification": "Correct"}}



                #Now answer for this tweet:
                
                    tweet:{}
                    STATEMENT 1: The travel mode detected in the tweet is "{}".
                    STATEMENT 2: The user's satisfaction towards the travel mode is "{}".
                    STATEMENT 3: The reason of satisfaction is "{}".
                    

                    ONLY ANSWER WITH "Correct" or "Not Correct".
                    ONLY ANSWER WITH a JSON OUTPUT FORMAT.your answer has to get the following fields with the same structure. I wrote you a description of each one :
                        {{"Travel_mode_verification" : "Answer to Q1","Satisfaction_verification" : "Answer to Q2","Reason_verification": "Answer to Q3"}}
                    Be careful to use DOUBLE QUOTES to denote the keys and values.

                """.format(
            input, travel_mode, satisfaction, reason
        )

        return prompt
