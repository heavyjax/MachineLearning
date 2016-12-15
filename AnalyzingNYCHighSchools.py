
# coding: utf-8

# # Read in the data

# In[5]:

import pandas
import numpy
import re

data_files = [
    "ap_2010.csv",
    "class_size.csv",
    "demographics.csv",
    "graduation.csv",
    "hs_directory.csv",
    "sat_results.csv"
]

data = {}

for f in data_files:
    d = pandas.read_csv("schools/{0}".format(f))
    data[f.replace(".csv", "")] = d


# # Read in the surveys

# In[6]:

all_survey = pandas.read_csv("schools/survey_all.txt", delimiter="\t", encoding='windows-1252')
d75_survey = pandas.read_csv("schools/survey_d75.txt", delimiter="\t", encoding='windows-1252')
survey = pandas.concat([all_survey, d75_survey], axis=0)

survey["DBN"] = survey["dbn"]

survey_fields = [
    "DBN", 
    "rr_s", 
    "rr_t", 
    "rr_p", 
    "N_s", 
    "N_t", 
    "N_p", 
    "saf_p_11", 
    "com_p_11", 
    "eng_p_11", 
    "aca_p_11", 
    "saf_t_11", 
    "com_t_11", 
    "eng_t_10", 
    "aca_t_11", 
    "saf_s_11", 
    "com_s_11", 
    "eng_s_11", 
    "aca_s_11", 
    "saf_tot_11", 
    "com_tot_11", 
    "eng_tot_11", 
    "aca_tot_11",
]
survey = survey.loc[:,survey_fields]
data["survey"] = survey


# # Add DBN columns

# In[7]:

data["hs_directory"]["DBN"] = data["hs_directory"]["dbn"]

def pad_csd(num):
    string_representation = str(num)
    if len(string_representation) > 1:
        return string_representation
    else:
        return "0" + string_representation
    
data["class_size"]["padded_csd"] = data["class_size"]["CSD"].apply(pad_csd)
data["class_size"]["DBN"] = data["class_size"]["padded_csd"] + data["class_size"]["SCHOOL CODE"]


# # Convert columns to numeric

# In[8]:

cols = ['SAT Math Avg. Score', 'SAT Critical Reading Avg. Score', 'SAT Writing Avg. Score']
for c in cols:
    data["sat_results"][c] = pandas.to_numeric(data["sat_results"][c], errors="coerce")

data['sat_results']['sat_score'] = data['sat_results'][cols[0]] + data['sat_results'][cols[1]] + data['sat_results'][cols[2]]

def find_lat(loc):
    coords = re.findall("\(.+, .+\)", loc)
    lat = coords[0].split(",")[0].replace("(", "")
    return lat

def find_lon(loc):
    coords = re.findall("\(.+, .+\)", loc)
    lon = coords[0].split(",")[1].replace(")", "").strip()
    return lon

data["hs_directory"]["lat"] = data["hs_directory"]["Location 1"].apply(find_lat)
data["hs_directory"]["lon"] = data["hs_directory"]["Location 1"].apply(find_lon)

data["hs_directory"]["lat"] = pandas.to_numeric(data["hs_directory"]["lat"], errors="coerce")
data["hs_directory"]["lon"] = pandas.to_numeric(data["hs_directory"]["lon"], errors="coerce")


# # Condense datasets

# In[9]:

class_size = data["class_size"]
class_size = class_size[class_size["GRADE "] == "09-12"]
class_size = class_size[class_size["PROGRAM TYPE"] == "GEN ED"]

class_size = class_size.groupby("DBN").agg(numpy.mean)
class_size.reset_index(inplace=True)
data["class_size"] = class_size

data["demographics"] = data["demographics"][data["demographics"]["schoolyear"] == 20112012]

data["graduation"] = data["graduation"][data["graduation"]["Cohort"] == "2006"]
data["graduation"] = data["graduation"][data["graduation"]["Demographic"] == "Total Cohort"]


# # Convert AP scores to numeric

# In[10]:

cols = ['AP Test Takers ', 'Total Exams Taken', 'Number of Exams with scores 3 4 or 5']

for col in cols:
    data["ap_2010"][col] = pandas.to_numeric(data["ap_2010"][col], errors="coerce")


# # Combine the datasets

# In[11]:

combined = data["sat_results"]

combined = combined.merge(data["ap_2010"], on="DBN", how="left")
combined = combined.merge(data["graduation"], on="DBN", how="left")

to_merge = ["class_size", "demographics", "survey", "hs_directory"]

for m in to_merge:
    combined = combined.merge(data[m], on="DBN", how="inner")

combined = combined.fillna(combined.mean())
combined = combined.fillna(0)


# # Add a school district column for mapping

# In[12]:

def get_first_two_chars(dbn):
    return dbn[0:2]

combined["school_dist"] = combined["DBN"].apply(get_first_two_chars)


# # Find correlations

# In[13]:

correlations = combined.corr()
correlations = correlations["sat_score"]
#print(correlations)


# In[14]:

corr_fields = [
    "DBN", 
    "rr_s", 
    "rr_t", 
    "rr_p", 
    "N_s", 
    "N_t", 
    "N_p", 
    "saf_p_11", 
    "com_p_11", 
    "eng_p_11", 
    "aca_p_11", 
    "saf_t_11", 
    "com_t_11", 
    "eng_t_10", 
    "aca_t_11", 
    "saf_s_11", 
    "com_s_11", 
    "eng_s_11", 
    "aca_s_11", 
    "saf_tot_11", 
    "com_tot_11", 
    "eng_tot_11", 
    "aca_tot_11",
    "sat_score",
]

survey_fields_df = combined[corr_fields]
survey_fields_df = survey_fields_df.corr()
survey_fields_df = survey_fields_df['sat_score']
#print(survey_fields_df)


# In[15]:

import matplotlib.pyplot as plt
#%matplotlib inline
#combined.plot(x='saf_s_11', y='sat_score', kind='scatter', title='saf_s_11 vs. sat_score', figsize=(5,10))
school_dist = combined.groupby('school_dist')
school_dist = school_dist.agg(numpy.mean)
school_dist.reset_index(inplace = True)


from mpl_toolkits.basemap import Basemap
m = Basemap(
    projection='merc', 
    llcrnrlat=40.496044, 
    urcrnrlat=40.915256, 
    llcrnrlon=-74.255735, 
    urcrnrlon=-73.700272,
    resolution='i'
)

m.drawmapboundary(fill_color='#85A6D9')
m.drawcoastlines(color='#6D5F47', linewidth=.4)
m.drawrivers(color='#6D5F47', linewidth=.4)

longitudes = school_dist["lon"].tolist()
latitudes = school_dist["lat"].tolist()
m.scatter(longitudes, latitudes, s=50, zorder=2, latlon=True, c=school_dist["saf_s_11"], cmap="summer")
plt.show()


# In[16]:

race_list = ['white_per','asian_per','black_per','hispanic_per','sat_score']
correlations = combined[race_list].corr()
correlations = correlations['sat_score']
#correlations.plot.bar()

#combined.plot(x='hispanic_per', y='sat_score', kind='scatter', title='hispanic_per vs. sat_score', figsize=(5,10))

#print(combined[combined['hispanic_per'] > 95]['SCHOOL NAME'])
hispanic_per_less_10 = combined['hispanic_per'] < 10
sat_score_less_1800 = combined['sat_score'] > 1800
#print(combined[hispanic_per_less_10 & sat_score_less_1800]['SCHOOL NAME'])


# In[21]:

sex_list = ['male_per','female_per','sat_score']
#%matplotlib inline
correlation = combined[sex_list].corr()
correlation = correlation['sat_score']
print(correlation)
#correlation.plot.bar()
#combined.plot(x='female_per', y='sat_score', kind='scatter', title='saf_s_11 vs. sat_score', figsize=(5,10))
female_per_over_60 = combined['female_per'] > 60
sat_score_over_1700 = combined['sat_score'] > 1700
print(combined[female_per_over_60 & sat_score_over_1700]['SCHOOL NAME'])


# In[25]:

#col_list = ['AP Test Takers ','total_enrollment']
#print(combined[col_list].dtypes)
combined['ap_per'] = combined['AP Test Takers '] + combined['total_enrollment']
col_list = ['ap_per','sat_score']
correlation = combined[col_list].corr()
print(correlation['sat_score'])
combined.plot(x='ap_per', y='sat_score', kind='scatter', title='saf_s_11 vs. sat_score', figsize=(5,10))

