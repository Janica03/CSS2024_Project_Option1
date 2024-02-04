# -*- coding: utf-8 -*-
"""
Created on Fri Feb  2 11:29:25 2024

@author: Janica van Wyk
"""

import pandas as pd
# import numpy as np
from itertools import chain
# import plotly.express as px
from ydata_profiling import ProfileReport

# Load data

pd.set_option('display.max_columns',None)

df = pd.read_csv("movie_dataset.csv", index_col=0)
print(df.info())
print(df.describe())

# Remove spaces and brackets in column names

df.columns = df.columns.str.replace(" ", "_")
df.columns = df.columns.str.replace("(", "")
df.columns = df.columns.str.replace(")", "")
print(df)

# Remove duplicates, if there are any

df.drop_duplicates(inplace = True)

# Numerical dataset with the original NANs, for the numerical analysis (Question 12)

df_num = df[["Year", "Runtime_Minutes", "Rating", "Votes", "Revenue_Millions", "Metascore"]].copy()

# NANs
# All NANs are replaced with the mean, as this will not influence the average of those columns, neither min or max values, if any of these stats are of interest. Additionally, these movies still form part of the database, if some of the other info in the other columns is studied.

x_rev = df["Revenue_Millions"].mean()

df["Revenue_Millions"].fillna(x_rev, inplace = True)

x_met = df["Metascore"].mean()

df["Metascore"].fillna(x_met, inplace = True)

"""Questions"""
"""1."""

high_rated_rank = df.Rating.argmax() + 1        # account for 0 indexing

print("\n1. The highest rated movie is:", df.Title[high_rated_rank])

"""2."""

avg_rev = df.Revenue_Millions.mean()

print("\n2. The average revenue of all the movies is:", round(avg_rev,0), "million")

"""3."""

avg_rev_15_17 = df[(df["Year"] > 2014) & (df["Year"] < 2018)].Revenue_Millions.mean()

print("\n3. The average revenue of movies from 2015 and 2017 is:", round(avg_rev_15_17,0), "million")

"""4."""

num_year_2016 = df[df["Year"] == 2016].Year.count()

print("\n4. The number of movies released in 2016 is:", num_year_2016)

"""5."""

num_cn = df[df["Director"] == "Christopher Nolan"].Title.count()

print("\n5. The number of movies directed by Christopher Nolan is:", num_cn)

"""6."""

num_8 = df[df["Rating"] >= 8.0].Rating.count()

print("\n6. The number of movies having a rating of at least 8.0 is:", num_8)

"""7."""

median_cn = df[df["Director"] == "Christopher Nolan"].Rating.median()

print("\n7. The median rating of movies directed by Christopher Nolan is:", median_cn)

"""8."""

year_min = df["Year"].min()
year_max = df["Year"].max()

year_avg_rating = []

for year in range(year_min, year_max+1):
    avg_rating = df[df["Year"] == year].Rating.mean()
    year_avg_rating.append(avg_rating)
    
high_rate_year = year_avg_rating.index(max(year_avg_rating)) + year_min

print("\n8. The year with the highest average rating is:", high_rate_year)

"""9."""

per_inc = abs( df[df["Year"] == 2006].Title.count() - df[df["Year"] == 2016].Title.count() ) / ( df[df["Year"] == 2006].Title.count() ) * 100

print("\n9. The percentage increase in number of movies made between 2006 and 2016 is:", per_inc, "%")

"""10."""
actors = []

for i in df.index:
    actors = df["Actors"].str.split(", ")

actors_df = pd.DataFrame(list(chain(*actors)))
actors_df.columns = ["Actor"]
actors_df["Count"] = pd.Series([1 for x in range(len(actors_df.index))])

a = actors_df.groupby("Actor").count()
a.reset_index(inplace = True)

print("\n10. The most common actor in all the movies is:", a.Actor[a.Count.argmax()])

"""11."""

genres = []

for i in df.index:
    genres = df["Genre"].str.split(",")

genres_df = pd.DataFrame(list(chain(*genres)))
genres_df.columns = ["Genre"]
# genres_df["Count"] = pd.Series([1 for x in range(len(actors_df.index))])

b = genres_df.groupby("Genre").count()
b.reset_index(inplace = True)

print("\n11. The amount of unique genres in the dataset is:", b.Genre.count())

"""12."""
# For this analyses the original data was used, since replacing the NANs with the mean values can influence some of the trends.

profile = ProfileReport(df_num, title="Profiling Report")

profile.to_file("your_report.html")

# Q. 12's answers obtained from analyzing the report.

