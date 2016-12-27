import pandas as pd
import codecs
import sqlite3

df = pd.read_csv('/Users/heavyjax/GoogleDrive/MachineLearning/Dataquest/GuidedProjectPreparingDataForSQLite/data/academy_awards.csv', encoding = 'ISO-8859-1')
#print(df.columns.values)
#print(df.head())

#Series.str Return first 4 digits from Year columns
df['Year'] = df['Year'].str[0:4]
df['Year'] = df['Year'].astype('int64')
#print(df['Nominee'])
later_than_2000 = df[df['Year'] > 2000]
award_categories = ['Actor -- Leading Role', 'Actor -- Supporting Role', 'Actress -- Leading Role', 'Actress -- Supporting Role']
#df.isin() return all rows in a column that match any of the values in a list of strings
nominations = later_than_2000['Category'].isin(award_categories)
later_than_2000 = later_than_2000[nominations]

#Set the correct encoding to Nominee column
def encode(string):
    return codecs.encode(string)

later_than_2000['Nominee'] = later_than_2000['Nominee'].apply(encode)
replace_dict = {'YES':1, 'NO':0}
later_than_2000['Won?'] = later_than_2000['Won?'].map(replace_dict)
later_than_2000['Won'] = later_than_2000['Won?']
dropping_columns = ['Won?', 'Unnamed: 5', 'Unnamed: 6', 'Unnamed: 7', 'Unnamed: 8', 'Unnamed: 9', 'Unnamed: 10']
final_nominations = later_than_2000.drop(dropping_columns, axis = 1)

#Series.str.rstrip() - Remove '} symbols from the end of value in Additional Info column'
#For alternative approach we can use the regular expressions to extract values in '{ }' brackets
additional_info_one = final_nominations['Additional Info'].str.rstrip("'}")

#Series.str.split() - Split values to {' in Additional Info column
additional_info_two = additional_info_one.str.split(" {'")
movie_names = additional_info_two.str[0]
characters = additional_info_two.str[1]
final_nominations['Movie'] = movie_names
final_nominations['Character'] = characters
final_nominations = final_nominations.drop('Additional Info', axis = 1)

#Export cleaned DataFrame final_nominations to SQLite
conn = sqlite3.connect('/Users/heavyjax/GoogleDrive/MachineLearning/Dataquest/GuidedProjectPreparingDataForSQLite/data/nominations.db')
final_nominations.to_sql('nominations', conn, index = False)

#Exploring the nominations.db
select_connection = sqlite3.connect('/Users/heavyjax/GoogleDrive/MachineLearning/Dataquest/GuidedProjectPreparingDataForSQLite/data/nominations.db')
query_result = select_connection.execute('select * from nominations limit 10').fetchall()
select_connection.close()
print(query_result)
