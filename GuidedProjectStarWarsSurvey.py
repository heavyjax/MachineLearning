
# coding: utf-8

# In[10]:

import pandas as pd
from numpy import nan
import matplotlib.pyplot as plt
get_ipython().magic('matplotlib inline')

star_wars = pd.read_csv("star_wars.csv", encoding="ISO-8859-1")
column_list = star_wars.columns.values

#Find rows where value is not NaN
respondentidisnotnull = star_wars['RespondentID'].notnull()
star_wars = star_wars[respondentidisnotnull]

#Converting "Yes/No" columns to True/False
yes_no = {
    "Yes":True,
    "No": False
}
star_wars['Have you seen any of the 6 films in the Star Wars franchise?'] = star_wars['Have you seen any of the 6 films in the Star Wars franchise?'].map(yes_no)
star_wars['Do you consider yourself to be a fan of the Star Wars film franchise?'] = star_wars['Do you consider yourself to be a fan of the Star Wars film franchise?'].map(yes_no)

Episode1 = {
    "Star Wars: Episode I  The Phantom Menace": True,
    nan: False
}
star_wars['Which of the following Star Wars films have you seen? Please select all that apply.'] = star_wars['Which of the following Star Wars films have you seen? Please select all that apply.'].map(Episode1)

Episode2 = {
    "Star Wars: Episode II  Attack of the Clones": True,
    nan: False
}
star_wars['Unnamed: 4'] = star_wars['Unnamed: 4'].map(Episode2)

Episode3 = {
    "Star Wars: Episode III  Revenge of the Sith": True,
    nan: False
}
star_wars['Unnamed: 5'] = star_wars['Unnamed: 5'].map(Episode3)

Episode4 = {
    "Star Wars: Episode IV  A New Hope": True,
    nan: False
}
star_wars['Unnamed: 6'] = star_wars['Unnamed: 6'].map(Episode4)

Episode5 = {
    "Star Wars: Episode V The Empire Strikes Back": True,
    nan: False
}
star_wars['Unnamed: 7'] = star_wars['Unnamed: 7'].map(Episode5)

Episode6 = {
    "Star Wars: Episode VI Return of the Jedi": True,
    nan: False
}
star_wars['Unnamed: 8'] = star_wars['Unnamed: 8'].map(Episode6)

#Rename columns
star_wars = star_wars.rename(columns={
    "Which of the following Star Wars films have you seen? Please select all that apply.": "seen_1",
    "Unnamed: 4":"seen_2",
    "Unnamed: 5":"seen_3",
    "Unnamed: 6":"seen_4",
    "Unnamed: 7":"seen_5",
    "Unnamed: 8":"seen_6"    
})

#Converting columns to float type
star_wars[star_wars.columns[9:15]] = star_wars[star_wars.columns[9:15]].astype(float)

#Rename columns
star_wars = star_wars.rename(columns={
    "Please rank the Star Wars films in order of preference with 1 being your favorite film in the franchise and 6 being your least favorite film.": "ranking_1",
    "Unnamed: 10":"ranking_2",
    "Unnamed: 11":"ranking_3",
    "Unnamed: 12":"ranking_4",
    "Unnamed: 13":"ranking_5",
    "Unnamed: 14":"ranking_6"    
})

#Plotting ranks
ranking_list = ['ranking_1','ranking_2','ranking_3','ranking_4','ranking_5','ranking_6']
star_wars[ranking_list].mean().plot.bar()

#Plotting sum
seeing_list = ['seen_1', 'seen_2', 'seen_3', 'seen_4', 'seen_5', 'seen_6']
star_wars[seeing_list].sum().plot.bar()

#Split the dataset into 2 subsets
males = star_wars[star_wars["Gender"] == "Male"]
females = star_wars[star_wars["Gender"] == "Female"]

#Plotting rank and sum splitted by gender
males[ranking_list].mean().plot.bar()
females[ranking_list].mean().plot.bar()
males[seeing_list].mean().plot.bar()
females[ranking_list].mean().plot.bar()

