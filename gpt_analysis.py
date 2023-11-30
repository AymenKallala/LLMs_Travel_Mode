
from ChatGPT.model import OpenAI_Tweet_Analyzer,predict_dataset
from data.load import load_data

first_data = load_data(1000,1999)


model = OpenAI_Tweet_Analyzer(model_name="gpt-3.5-turbo-1106",max_tokens = 300,temperature=0.7,prompt_technique="in_context")
output_df_COT = predict_dataset(model,first_data,sleep=False)
output_df_COT.to_excel('./results/1000_1999_in_context.xlsx')



model = OpenAI_Tweet_Analyzer(model_name="gpt-3.5-turbo-1106",max_tokens = 1000,temperature=0.7,prompt_technique="analogical")
output_df_analogical = predict_dataset(model,first_data,sleep=False)
output_df_analogical.to_excel('./results/1000_1999_Analog.xlsx')

