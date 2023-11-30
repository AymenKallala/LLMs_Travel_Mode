import pandas as pd
import os
import openai
from collections import defaultdict
from tqdm import tqdm
import time

from .utils import prompt,parse_gpt_output,process_output

openai.api_key = os.environ["OPENAI_KEY"]


class OpenAI_Tweet_Analyzer():
    def __init__(self,model_name,max_tokens,temperature,prompt_technique):
        self.model_name = model_name
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.prompt_technique = prompt_technique

    
    def predict(self,tweet,travel_mode=None,satisfaction = None,reason = None):

        prompt_string = prompt(input = tweet,travel_mode=travel_mode,satisfaction=satisfaction,reason=reason,technique = self.prompt_technique)




        if self.prompt_technique == 'analogical':
        
            answer = """{"travel_mode":"API Problem","satisfaction":"API Problem","reason":"API Problem","example_1" :{"tweet":"API Problem","travel_mode_1":"API Problem","satisfaction_1":"API Problem","reason_1":"API Problem"},"example_2":{"tweet":"API Problem","travel_mode_2":"API Problem","satisfaction_2":"API Problem","reason_2":"API Problem"},"example_3":{"tweet":"API Problem","travel_mode_3":"API Problem","satisfaction_3":"API Problem","reason_3":"API Problem"}}}"""
        if self.prompt_technique == 'COT' or 'in_context':
            answer = '{"travel_mode":"API Problem","satisfaction":"API Problem","reason":"API Problem"}'
        else:
            answer = 'None'
        
        try:
            completion = openai.ChatCompletion.create(model=self.model_name,
                                            messages = [{"role": "user",
                                                        "content" : prompt_string}],
                                            max_tokens = self.max_tokens,
                                            temperature = self.temperature
                                                        )
            answer = completion["choices"][0].message.content
        except:
            print("OpenAI API did not work")
        finally:
            return parse_gpt_output(answer,self.prompt_technique)


    
def predict_dataset(analyzer,dataset,sleep = True):
    output_dict = defaultdict(defaultdict)

    for global_id in tqdm(dataset,total = len(dataset)):
        tweet = dataset[global_id]['processed_txt']

        answer = analyzer.predict(tweet)
        output_dict[global_id]["tweet"] = tweet
        output_dict[global_id]["output"] = answer
        if sleep:
            time.sleep(20)

    return process_output(output_dict,technique=analyzer.prompt_technique)

def verify_dataset(analyzer,dataset,sleep = False):
    output_dict = defaultdict()

    for global_id in tqdm(dataset,total = len(dataset)):
        tweet = dataset[global_id]['tweet']
        travel_mode = dataset[global_id]['Travel Mode']
        satisfaction = dataset[global_id]['Satisfaction']
        reason = dataset[global_id]['Reason']

        answer = analyzer.predict(tweet,travel_mode=travel_mode,satisfaction=satisfaction,reason=reason)

        output_dict[global_id]= answer
        if sleep:
            time.sleep(20)

    return process_output(output_dict,technique=analyzer.prompt_technique)
    
        