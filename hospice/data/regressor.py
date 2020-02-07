# -*- coding: utf-8 -*-
"""
Created on Mon Dec 30 12:35:07 2019

@author: Wasim sayyed
"""
import pandas as pd

data = pd.read_csv("final_hospice_data.csv")
data.loc[data['IsCritical'] == 0 , "IsCritical"]  = "normal"
data.loc[data['IsCritical'] == 1 , "IsCritical"]  = "critical"
X = data.iloc[:, [5, 7, 8, 9, 10]].values
y = data.iloc[:, 12].values

from sklearn.preprocessing import LabelEncoder
Encoder1 = LabelEncoder()
Encoder2 = LabelEncoder()
Encoder3 = LabelEncoder()
Encoder4 = LabelEncoder()
Encoder5 = LabelEncoder()
X[:, 0] = Encoder1.fit_transform(X[:, 0])
X[:, 1] = Encoder2.fit_transform(X[:, 1])
X[:, 2] = Encoder3.fit_transform(X[:, 2])
X[:, 3] = Encoder4.fit_transform(X[:, 3])
X[:, 4] = Encoder5.fit_transform(X[:, 4])

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

from sklearn.linear_model import LinearRegression
regressor = LinearRegression()
regressor.fit(X_train, y_train)





