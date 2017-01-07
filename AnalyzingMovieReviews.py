import pandas as pd
import matplotlib.pyplot as plt
import numpy
from scipy.stats import pearsonr, linregress

#Read dataset
movies = pd.read_csv("/Users/heavyjax/GoogleDrive/MachineLearning/Data/data-master/fandango/fandango_score_comparison.csv")
print(movies.columns.values)

#Make histograms
plt.hist(movies["Fandango_Stars"])
plt.show()
plt.hist(movies["Metacritic_norm_round"])
plt.show()

#Get mean, meadian, std
mean_fandango = movies["Fandango_Stars"].mean()
mean_metacritic = movies["Metacritic_norm_round"].mean()
median_fandango = numpy.median(movies["Fandango_Stars"])
median_metacritic = numpy.median(movies["Metacritic_norm_round"])
std_fandango = movies["Fandango_Stars"].std()
std_metacritic = movies["Metacritic_norm_round"].std()

#Make scatterplot
plt.scatter(movies["Metacritic_norm_round"], movies["Fandango_Stars"])
plt.show()

#Find the differences between ratings
movies["fm_diff"] = movies["Metacritic_norm_round"] - movies["Fandango_Stars"]
fm_diff = numpy.absolute(movies["fm_diff"])

#Sort the difference to find outliers (largest differences)
movies.sort_values("fm_diff", inplace=True, ascending=True)
print(movies["FILM"].head())

#Find correlation
r_value = pearsonr(movies["Metacritic_norm_round"], movies["Fandango_Stars"])

#Build linear regression
slope, intercept, r_value, p_value, stderr_slope = linregress(movies["Metacritic_norm_round"], movies["Fandango_Stars"])

#Predict what a movie that got a 3.0, 1.0, 5.0 in Metacritic would get on Fandango
pred_3 = slope * 3 + intercept
pred_1 = slope * 1 + intercept
pred_5 = slope * 5 + intercept

metacritics_ratings = [1.0, 5.0]
fandango_predictions_ratings = [pred_1, pred_5]

#Make scatterplot
plt.plot(metacritics_ratings, fandango_predictions_ratings)
plt.xlim(1,5)
plt.show()
