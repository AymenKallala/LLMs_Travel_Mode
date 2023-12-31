# Large Language Models for Travel Mode Tweets Analysis

This restitutes my work during the Fall 2023 semester in which our objective was to extract relevant information from unlabeled tweets. We focused on details such as travel mode, satisfaction, and reasons to analyze travel patterns. After exploring various prompting methods, including Plain In Context Learning, Chain of Thoughts, and Analogical Prompting, I found that the simplest prompts produced the most robust results when using the gpt3.5 turbo model for prediction.

 
Another challenge I encountered was assessing the results when using Large Language Models on unlabeled data. To address this, I used a "verifier" LLM to self-check the results predicted by my"labeler" LLM. After hand verifying a few predictions myself, I designed a trust rate to assess the reliability of my verifiers. However, my analysis revealed a low trust rate in almost every cases, indicating that further reflection is needed to ensure the reliability of the correction used to compute the performance of our labeler.

# Setup the environment and your OpenAI key
```
pip install requirements.txt
```
To run succesfully the code, you will also need a valid OpenAI API token to save in the `OPENAI_KEY` variable environment.
# LLMs

I focused with one large language model to conduct my experience:
1. GPT-3.5-turbo-1106

# Dataset

The exploration work was carried out by experimenting on a custom dataset of tweets related to the NYC MTA. Example :

# Prompts
## Baseline
The baseline model consisted in simply asking gpt3.5 to retrieve the travel mode, the satisfaction and the reason of it in a straightforward fashion, without any additional details.
 
## In context Learning
This technique consists in applying a detailed prompt
engineering format to let the model learn from inference only.
As for instance in the *Input-Output* format of a query, where
one show the model examples of demonstration before asking
it to predict on a new input.

![alt-text-1](images/IL-example.png "In Context Learning demonstration")

In my work, this transcripted in showing the model a few exemplars of _expected outputs_ given certain tweets before asking it to solve for the tweet of interest.

## Chain of Thougts

Is a specific In-Context learning format: It consists in specifying a series of intermediate reasoning steps to the model that leads to solve a problem in hand. 
![alt-text-1](images/COT-example.png "Chain of Thoughts demonstration")


## Analogical Prompting

Techniques such as In-Context Learning or CoT have been proved to work pretty well but still present the drawback of needing handwritten exemplars to be inputed to the model. This can represent a significant amount of time in the case of CoT for instance. This technique aims to allow models to generate themselves the exemplars, and hence to obviate the need for labeling or retrieving exemplars. Based on the idea that modern LLMs possess a broad range of problem-solving knowledge acquired during training. Explicitly prompting them to recall or generate relevant problems and solutions in context aids LLMs to perform in-context learning to solve new problems.

Below is an example of prompting.

![alt-text-1](images/A-example.png "Analogical Prompting demonstration")


# Commands
## Prediction
For prediction, you will need the 2 csv files where initial tweets are stored. It was (processed_0_999.csv) and (processed_1000_1999.csv) in my case.
```
python prediction.py --data_path_1 <FILE_PATH_1> --data_path_2 <FILE_PATH_2> --technique zero_shot
 
 ```
 - `data_path_1` (and 2): The tweets file (csv containing a `GLOBAL_ID` and a `processed_txt` column.).
- `technique`: the prompt engineering technique to use. Can be `zero_shot`, `in_context`, `COT` or `analogical`.

This will save two output files, one csv and one excel. The csv will be useful to compute the verification later on.

## Verification
To conduct a self-verification step, you need to be provided with the csv file of predicted data.
```
python verification.py --data_path results/0_1999_In_Context_Learning.csv --sleep False

```
- `data_path` : The prediction file (csv containing a `tweet`, `travel_mode`, `satisfaction` and `reason` columns.
- `technique`: the prompt engineering technique to use. Can be `zero_shot`, `in_context`, `COT` or `analogical`.

This will also output the verifications in two files, a csv and an excel one. The csv file will be needed to compute the trust rate.

## Trust Rate
To compute the trust rate of your verifications, you need to be provided with a csv file of verified data (computedi in last step). You also need to correct by hand a few lines of the initial predictions file (needed to compute the trustworthiness of the correction). You will retain the number of line that you corrected yourself as the `labeled_lines` parameter below.
```
python verification.py  --VERIFIER_PATH <verification_to_test> --GT_PATH <predictions verified by hand> --labeled_lines <INT>
```
- `labeled_lines` is the number of lines that you hand-labeled. Mandatory for the algorith to distinguish groundtruth corrections from predicted corrections and compute a `trust_rate`.

# Results

| Method    | Travel Mode | Satisfaction| Reason| Trust Rate |
| -------- | ------- | --------|--------|--------|
| Baseline (zero-shot)| 79%| 53% | 82%|  72% |
| Plain In-Context Learning| 84%| 43%| 74%| 71% |
| COT| 80%| 44% |  68%|  68% | 
| Analogical Prompting| 77.5%|  41% | 54%|  66% |

# Challenge with models evaluation

We are conducting information retrieval on *unlabeled data*. Therefore, no groundtruth labels are available. In order to evaluate our models, one solution is to perform *self-verification*. Strictly speaking, asking another LLM wether the answers provided along with the relevant tweet are correct or not. But how can we trust this _corrector_ ?

To that end, I self-checked by hand approximatively 100 predictions per method. Then, for each self-verification performed, I compared the verification with the ones I self-verified to compute a *trust_rate*.