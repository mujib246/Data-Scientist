# -*- coding: utf-8 -*-
"""Automobile.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1IStuAUklmTDbbxGjViAEPfHJavwbN_4S
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import preprocessing
import re as re

losses = pd.read_csv('automobile-losses.csv')
risk = pd.read_csv('automobile-risk.csv')
spec = pd.read_csv('automobile-spec.csv')

losses.head()

risk.head()

spec.head()

"""# 1. JOIN 3 Tables using ID as key"""

join1 = pd.merge(losses, risk, how='outer', on ='ID')

join1.head()

fulljoin = pd.merge(spec, join1, how='outer', on='ID')

fulljoin.head()

""" # 2. Quick-look (dimension, data type, head/tail, summary statistics, etc) """

fulljoin.shape

fulljoin.info()

fulljoin.head()

fulljoin.describe()

""" # 3. Entify missing value. If any, how will you handle it?"""

fulljoin.isnull().sum()

fulljoin['num-of-doors'].fillna(fulljoin['num-of-doors'].mode()[0], inplace=True)

fulljoin['bore'].fillna(fulljoin['bore'].mean(), inplace=True)

fulljoin['stroke'].fillna(fulljoin['stroke'].mean(), inplace=True)

fulljoin['peak-rpm'].fillna(fulljoin['peak-rpm'].mean(), inplace=True)

fulljoin['price'].fillna(fulljoin['price'].mean(), inplace=True)

fulljoin['normalized-losses'].fillna(fulljoin['normalized-losses'].mean(), inplace=True)

fulljoin['horsepower'].fillna(fulljoin['normalized-losses'].mean(), inplace=True)

fulljoin.isnull().sum()

"""# 4.  Perform visualization using at least 5 difference visualization technique (barplot, scatter

## Scatterplot
"""

f=plt.figure(figsize=(20,8))

f.add_subplot(1,2,1)
horse_price= plt.scatter(fulljoin['horsepower'],fulljoin['price'])
plt.title('horsepower vs price ')
plt.xlabel('horsepower')
plt.ylabel('price($)')

f.add_subplot(1,2,2)
horse_price= plt.scatter(fulljoin['horsepower'],fulljoin['price'])
plt.title('city-mpg vs highway-mpg ')
plt.xlabel('city-mpg')
plt.ylabel('highway-mpg')
plt.show()

"""## Histogram"""

f=plt.figure(figsize=(16,8))

f.add_subplot(2,2,1)
histo_engine= plt.hist(fulljoin['engine-size'],
         facecolor='peru', 
         edgecolor='blue', 
         bins=10)
plt.xlabel('engine size')
plt.ylabel('count')

f.add_subplot(2,2,2)
histo_price = plt.hist(fulljoin['city-mpg'], 
         facecolor='peru', 
         edgecolor='blue', 
         bins=10)
plt.xlabel('horsepower')
plt.ylabel('count')

f.add_subplot(2,2,3)
histo_price = plt.hist(fulljoin['highway-mpg'], 
         facecolor='peru', 
         edgecolor='blue', 
         bins=10)
plt.xlabel('highway-mpg')
plt.ylabel('count')

f.add_subplot(2,2,4)
histo_peakrpm = plt.hist(fulljoin['peak-rpm'], 
         facecolor='peru', 
         edgecolor='blue', 
         bins=10)
plt.xlabel('peak-rpm')
plt.ylabel('count')

plt.show()

"""## Barplot"""

f=plt.figure(figsize=(17,8))

f.add_subplot(2,2,1)
barplot_make = fulljoin['cylinder'].value_counts().plot(kind='bar');
plt.xlabel('cylinder')
plt.ylabel('count')

f.add_subplot(2,2,2)
barplot_make = fulljoin['drive-wheel'].value_counts().plot(kind='bar');
plt.xlabel('drive-wheel')
plt.ylabel('count')

f.add_subplot(2,2,3)
barplot_make = fulljoin['body-style'].value_counts().plot(kind='bar');
plt.xlabel('body-style')
plt.ylabel('count')

f.add_subplot(2,2,4)
barplot_make = fulljoin['make'].value_counts().plot(kind='bar');
plt.xlabel('make')
plt.ylabel('count')

"""## Boxplot"""

f=plt.figure(figsize=(17,8))

f.add_subplot(1,2,1)
sns.boxplot(data = fulljoin, x = 'stroke', color = 'cyan', orient = "h").set_title('Boxplot - Stroke')

f.add_subplot(1,2,2)
sns.boxplot(data = fulljoin, x = 'bore', color = 'red', orient = "h").set_title('Boxplot - Bore')

f=plt.figure(figsize=(20,13))
f.add_subplot(3,1,1)
g = sns.boxplot(y=fulljoin["horsepower"], x=fulljoin['make'])
f.add_subplot(3,1,2)
g = sns.boxplot(y=fulljoin["horsepower"], x=fulljoin['aspiration'])
f.add_subplot(3,1,3)
g = sns.boxplot(y=fulljoin["horsepower"], x=fulljoin['body-style'])
plt.xticks(rotation=60)

"""## Stackplot"""

x = fulljoin['make']

y = np.vstack([fulljoin['horsepower'],
               fulljoin['city-mpg']])

plt.figure(figsize=(25,12))
# Labels for each stack
labels = ['horsepower', 
          'city-mpg', 
          ]

# Colors for each stack
colors = ['sandybrown', 
          'tomato', 
          'skyblue']

#  Similar to pandas df.plot.area()
plt.stackplot(x, y, 
              labels=labels,
              colors=colors, 
              edgecolor='black')

# Plots legend to the upperleft of Figure
plt.legend(loc=2)

plt.show()

"""## Correlation"""

#create correlation with hitmap

#create correlation
corr = fulljoin.corr(method = 'pearson')

#convert correlation to numpy array
mask = np.array(corr)

#to mask the repetitive value for each pair
mask[np.tril_indices_from(mask)] = False
fig, ax = plt.subplots(figsize = (15,12))
fig.set_size_inches(30,15)
sns.heatmap(corr, mask = mask, vmax = 0.9, square = True, annot = True)

"""# PART 2

# 1.  Car brand with highest price
"""

carbrand= fulljoin.groupby('make')
higgest_price = carbrand['price'].max()
higgest_price.head(3)

"""# 2. Maximum horsepower for car with 6 cylinder engine """

six_cylinder = fulljoin[fulljoin.cylinder == 'six']
max_cylinder = six_cylinder['horsepower'].max()
max_cylinder

"""# 3. Average peak-rpm for ‘turbo’ style aspiration car """

turbo_style = fulljoin[fulljoin.aspiration == 'turbo']
avg_turbo = turbo_style['peak-rpm'].mean()
avg_turbo

"""# 4. Average price based on body-style"""

bodystyle = fulljoin.groupby('body-style')
avg_price = bodystyle['price'].mean()
avg_price

"""# 5. Average price based on body-style only for Honda car (make=Honda)"""

onlyhonda = fulljoin[fulljoin.make == 'honda']
bodystyle = onlyhonda.groupby('body-style')
avg_price_honda = bodystyle['price'].mean()
avg_price_honda