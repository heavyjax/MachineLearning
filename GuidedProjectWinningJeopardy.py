import pandas as pd
from scipy.stats import chisquare
import numpy as np

#Read dataset
df = pd.read_csv('/Users/heavyjax/GoogleDrive/MachineLearning/Dataquest/GuidedProjectWinningJeopardy/data/JEOPARDY_CSV.csv')

#Rename columns
df = df.rename(columns = {
" Air Date":"Air Date",
" Round":"Round",
" Category":"Category",
" Value":"Value",
" Question":"Question",
" Answer":"Answer"
})

# clean_answer_question  function which replace clean_chars and transform text to lowercase
def clean_answer_question(text):
    clean_text = text
    clean_chars = [",", ".", "'", ";", ":", "$", "(", ")", "\""]
    for i in clean_chars:
        clean_text = clean_text.replace(i, '')
    return clean_text.lower()

# clean_value function converts value column into int
def clean_value(text):
    clean_text = clean_answer_question(text)
    try:
        int_value = int(clean_text)
    except Exception:
        int_value = 0
    return int_value

#Function clean_row count probability of how often the answer is deducible from the question
def clean_row(row):
    match_count = 0
    split_answer = row["clean_answer"].split(" ")
    split_question = row["clean_question"].split(" ")
    for i in split_answer:
        if i == "the":
            split_answer.remove("the")
    if len(split_answer) == 0:
        return 0
    else:
        for j in split_answer:
            if j in split_question:
                match_count += 1
        return match_count / len(split_answer)

df["clean_question"] = df["Question"].apply(clean_answer_question)
df["clean_answer"] = df["Answer"].apply(clean_answer_question)
df["clean_value"] = df["Value"].apply(clean_value)
# Transform air date column to datatime type
df["Air Date"] = pd.to_datetime(df["Air Date"])
df["answer_in_question"] = df.apply(clean_row, axis = 1)

question_overlap = []
terms_used = set()
#Iterate over dataframe
for index, row in df.iterrows():
    split_question = row["clean_question"].split(" ")
    #Remove all elements of list which len > 6
    split_question = [j for j in split_question if len(j) > 5]
    match_count = 0
    for k in split_question:
        if k in terms_used:
            match_count += 1
    for l in split_question:
        terms_used.add(l)
    if len(split_question) > 0:
        match_count = match_count / len(split_question)
    question_overlap.append(match_count)
df["question_overlap"] = question_overlap

def define_high_low_values(row):
    value = 0
    if row["clean_value"] > 800:
        value = 1
    return value

df["high_value"] = df.apply(define_high_low_values, axis = 1)

def count_high_low_values(word):
    low_count = 0
    high_count = 0
    for index, row in df.iterrows():
        split_question = row["clean_question"].split(" ")
        if word in split_question:
            if df["high_value"].any() == 1:
                high_count += 1
            else:
                low_count += 1
    return high_count, low_count

observed_expected = []
comparison_terms = list(terms_used)
comparison_terms = comparison_terms[0:6]

for i in comparison_terms:
    observed_expected.append(count_high_low_values(i))

high_value_count = df[df["high_value"] == 1].shape[0]
low_value_count = df[df["high_value"] == 0].shape[0]

chi_squared = []
for obs in observed_expected:
    total = sum(obs)
    total_prop = total / df.shape[0]
    high_value_exp = total_prop * high_value_count
    low_value_exp = total_prop * low_value_count

    observed = np.array([obs[0], obs[1]])
    expected = np.array([high_value_exp, low_value_exp])
    chi_squared.append(chisquare(observed, expected))
print(chi_squared)
