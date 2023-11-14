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

    
    def predict(self,tweet):

        prompt_string = prompt(input = tweet,technique = self.prompt_technique)




        answer = '{"travel_mode":"API Problem","satisfaction":"API Problem","reason":"API Problem"}'
        
        try:
            completion = openai.ChatCompletion.create(model=self.model_name,
                                            messages = [{"role": "user",
                                                        "content" : prompt_string}],
                                            max_tokens = self.max_tokens,
                                            #response_format = {"type":"json_object"},
                                            temperature = self.temperature
                                                        )
            answer = completion["choices"][0].message.content
        except:
            print("OpenAI API did not work")
        finally:
            return parse_gpt_output(answer)


    
def predict_dataset(analyzer,dataset):
    output_dict = defaultdict(defaultdict)

    for global_id in tqdm(dataset,total = len(dataset)):
        tweet = dataset[global_id]['processed_txt']

        answer = analyzer.predict(tweet)
        output_dict[global_id]["tweet"] = tweet
        output_dict[global_id]["output"] = answer
        time.sleep(20)

    return process_output(output_dict,technique=analyzer.prompt_technique)
    
        