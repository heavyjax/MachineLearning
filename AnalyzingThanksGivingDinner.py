
# coding: utf-8

# In[2]:

import pandas
data = pandas.read_csv('thanksgiving.csv', encoding = 'Latin-1')
#print(data.head())


# In[3]:

#print(data.columns)


# In[3]:

is_celebrate_count = data['Do you celebrate Thanksgiving?'].value_counts()
#print(is_celebrate_count)
is_celebrate = data['Do you celebrate Thanksgiving?'] == 'Yes'
data = data[is_celebrate]
#print(data.shape)


# In[4]:

dish_counter = data['What is typically the main dish at your Thanksgiving dinner?'].value_counts()
#print(dish_counter)
is_tofurkey = data['What is typically the main dish at your Thanksgiving dinner?'] == 'Tofurkey'
#print(data['Do you typically have gravy?'][is_tofurkey])


# In[5]:

apple_isnull = data['Which type of pie is typically served at your Thanksgiving dinner? Please select all that apply. - Apple'].isnull()
pumpkin_isnull = data['Which type of pie is typically served at your Thanksgiving dinner? Please select all that apply. - Pumpkin'].isnull()
pecan_isnull = data['Which type of pie is typically served at your Thanksgiving dinner? Please select all that apply. - Pecan'].isnull()
ate_pies = apple_isnull & pumpkin_isnull & pecan_isnull
#print(ate_pies)


# In[6]:

def convert_age(string):
    if pandas.isnull(string):
        return None
    else:
        string = string.replace('+','')
        string = string.split(' ')
    return int(string[0])

data['int_age'] = data['Age'].apply(convert_age)
print(data['int_age'].describe())


# In[9]:

def convert_income_string_to_int(string):
    if pandas.isnull(string):
        return None
    else:
        string = string.split(' ')
        if string[0] == 'Prefer':
            return None
        string[0] = string[0].replace('$','')
        string[0] = string[0].replace(',','')
        return int(string[0])
data['int_income'] = data['How much total combined money did all members of your HOUSEHOLD earn last year?'].apply(convert_income_string_to_int)
print(data['int_income'].describe())
        
    


# In[13]:

less_than_50k = data['int_income'] < 50000
result50 = data['How far will you travel for Thanksgiving?'][less_than_50k].value_counts()
#print(result50)
less_than_150k = data['int_income'] < 150000
result150 = data['How far will you travel for Thanksgiving?'][less_than_150k].value_counts()
#print(result150)


# In[14]:

result = data.pivot_table(index = 'Have you ever tried to meet up with hometown friends on Thanksgiving night?', columns = 'Have you ever attended a "Friendsgiving?"', values = 'int_age')
print(result)

