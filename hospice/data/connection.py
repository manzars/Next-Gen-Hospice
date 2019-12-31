# -*- coding: utf-8 -*-
"""
Created on Thu Dec 26 11:44:10 2019

@author: Faizan Shaikh
"""
import mysql.connector
import pickle
import numpy as np
import pandas as pd

data = pd.read_csv('final_hospice_data.csv')
data.loc[data['IsCritical'] == 0 , "IsCritical"]  = "normal"
data.loc[data['IsCritical'] == 1 , "IsCritical"]  = "critical"
X = data.iloc[:, [5,7,8,9,10]].values
y = data.iloc[:, 6].values

y = y.astype('str')
for i in range(data.shape[0]):
  y[i] = rangeMakerOutput(int(y[i]))

from sklearn.preprocessing import LabelEncoder
labelencoder0 = LabelEncoder()
labelencoder1 = LabelEncoder()
labelencoder2 = LabelEncoder()
labelencoder3 = LabelEncoder()
labelencoder4 = LabelEncoder()
X[:, 0] = labelencoder0.fit_transform(X[:, 0])
X[:, 1] = labelencoder1.fit_transform(X[:, 1])
X[:, 2] = labelencoder2.fit_transform(X[:, 2])
X[:, 3] = labelencoder3.fit_transform(X[:, 3])
X[:, 4] = labelencoder4.fit_transform(X[:, 4])

labelencoder_y = LabelEncoder()
y[:] = labelencoder_y.fit_transform(y[:])

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 1/4, random_state = 0)

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd=""
)

def day(op):
  if(op.item() == '0'):
    output = [0, 2]
  elif(op.item() == '1'):
    output =  [3, 5]
  elif(op.item() == '2'):
    output =  [6, 8]
  elif(op.item() == '3'):
    output =  [9, 11]
  elif(op.item() == '4'):
    output =  [12, 14]
  elif(op.item() == '5'):
    output =  [15, 19]
  elif(op.item() == '6'):
    output =  [20, 24]
  elif(op.item() == '7'):
    output =  [25, 31]
  elif(op.item() == '8'):
    output =  [32, 47]
  else:
    output =  [48]
  return output
p = None
def dataFetchFromSQL():
    mycursor = mydb.cursor()
    ipno = input("Enter IPNo of Patient: ")
    mycursor.execute("USE hospice")
    mycursor.execute("SELECT * FROM `admission` WHERE IPNo = '" + ipno +"'")
    data = mycursor.fetchone()
    p = data
    mycursor.execute("SELECT * FROM `gender` WHERE id = '" + str(data[1]) +"'")
    gender = mycursor.fetchone()[1]
    
    mycursor.execute("SELECT * FROM `disease` WHERE id = '" + str(data[2]) +"'")
    disease = mycursor.fetchone()[1]
    
    mycursor.execute("SELECT * FROM `previousdisease` WHERE id = '" + str(data[3]) +"'")
    p_disease = mycursor.fetchone()[1]
    
    if(data[4] == 0):
        is_critical = "normal"
    else:
        is_critical = "critical"
    
    #is_critical = data[4]
    
    mycursor.execute("SELECT * FROM `bloodgroup` WHERE id = '" + str(data[5]) +"'")
    b_group = mycursor.fetchone()[1]
    return [is_critical, disease, gender, b_group, p_disease], data[6].date()


data, date = dataFetchFromSQL()
data = np.asarray(data).reshape(1, -1)

data[:, 0] = labelencoder0.transform(data[:, 0])
data[:, 1] = labelencoder1.transform(data[:, 1])
data[:, 2] = labelencoder2.transform(data[:, 2])
data[:, 3] = labelencoder3.transform(data[:, 3])
data[:, 4] = labelencoder4.transform(data[:, 4])

data = data.astype('int')
data = scaler.transform(data)
print(data)

file = open('abc.pkl', "rb")
classs = pickle.load(file)
file.close()

op = classs.predict(data)

print(f'\nExpected date of recovery of patient is {day(op)} days')
print(str(date + timedelta(days = day(op)[0])) + " to " str(date + timedelta(days = day(op)[1])))
    
    
    
    # mycursor.execute("SELECT * FROM `admission` WHERE genderId = '1' AND diseaseId = '1' AND previousDiseaseId = '1' AND isCritical = '1' AND bloodGroupId = '1'")

