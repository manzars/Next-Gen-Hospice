# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 16:41:48 2019

@author: Wasim sayyed
"""

import pandas as pd
import numpy as np

data = pd.read_csv('final_hospice_data.csv')

data.loc[data['IsCritical'] == 0 , "IsCritical"]  = "normal"
data.loc[data['IsCritical'] == 1 , "IsCritical"]  = "critical"

X = data.iloc[:, [5,7,8,9,10]].values
y = data.iloc[:, 6].values

def days(x):
  if(op.item() == '0'):
    output = "0 to 2"
  elif(op.item() == '1'):
    output =  "3 to 5"
  elif(op.item() == '2'):
    output =  "6 to 8"
  elif(op.item() == '3'):
    output =  "9 to 11"
  elif(op.item() == '4'):
    output =  "12 to 14"
  elif(op.item() == '5'):
    output =  "15 to 19"
  elif(op.item() == '6'):
    output =  "20 to 24"
  elif(op.item() == '7'):
    output =  "25 to 31"
  elif(op.item() == '8'):
    output =  "32 to 47"
  else:
    output =  "More than 47 Days"
  return output

def rangeMakerOutput(number):
  if(0 <= number <= 2):
        return 'A'
  elif(3 <= number <= 5):
        return 'B'
  elif(6 <= number <= 8):
        return 'C'
  elif(9 <= number <= 11):
        return 'D'
  elif(12 <= number <= 14):
        return 'E'
  elif(15 <= number <= 19):
        return 'F'
  elif(20 <= number <= 24):
        return 'G'
  elif(25 <= number <= 31):
        return 'H'
  elif(32 <= number <= 47):
        return 'I'
  else:
        return 'J'

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

from sklearn.ensemble import RandomForestClassifier
classifier = RandomForestClassifier(n_estimators = 10, criterion = 'entropy', random_state = 0)
classifier.fit(X_train, y_train)

y_pred = classifier.predict(X_test)
from sklearn.metrics import accuracy_score
accuracy = accuracy_score(y_test, y_pred)
str((accuracy *100).round(2)) + " %"


#-----------------------------------------------------------------------


flag = True
while(flag):
  print("Choose your gender\n1. Male\n2. Female")
  inn = int(input())
  if(inn == 1):
    gender = 'M'
    flag = False
  elif(inn == 2):
    gender = 'F'
    flag = False
  else:
    print('Wrong Gender.....Enter Again')
    
flag = True
while(flag):
  print("Choose your Disease\n1. fever	\n2. cbc\n3. maleria\n4. Pneumonia\n5. abdomen pain\n6. Pseudomonas aeruginosa\n7. dengue fever\n8. Influenza\n9. Tuberculosis\n10. Adhesive Pericapsulitis")
  inn = int(input())
  if(inn == 1):
    disease = 'fever'
    flag = False
  elif(inn == 2):
    disease = 'cbc'
    flag = False
  elif(inn == 3):
    disease = 'maleria'
    flag = False
  elif(inn == 4):
    disease = 'Pneumonia'
    flag = False
  elif(inn == 5):
    disease = 'abdomen pain'
    flag = False
  elif(inn == 6):
    disease = 'Pseudomonas aeruginosa'
    flag = False
  elif(inn == 7):
    disease = 'dengue fever'
    flag = False
  elif(inn == 8):
    disease = 'Influenza'
    flag = False
  elif(inn == 9):
    disease = 'Tuberculosis'
    flag = False
  elif(inn == 10):
    disease = 'Adhesive Pericapsulitis'
    flag = False
  else:
    print('Wrong Disease.....Enter Again')
    
flag = True
while(flag):
  print("Choose your Condition\n1. Critical - 1\n2. Normal - 0")
  inn = int(input())
  if(inn == 1):
    condition = "critical"
    flag = False
  elif(inn == 0):
    condition = "normal"
    flag = False
  else:
    print('Wrong Condition.....Enter Again')
    

flag = True
while(flag):
  print("Choose your Previous Disease\n1. fever	\n2. dengue fever\n3. Infulenza\n4. maleria\n5. Tuberculosis\n6. none")
  inn = int(input())
  if(inn == 1):
    p_disease = 'fever'
    flag = False
  elif(inn == 2):
    p_disease = 'dengue fever'
    flag = False
  elif(inn == 3):
    p_disease = 'Influenza'
    flag = False
  elif(inn == 4):
    p_disease = 'maleria'
    flag = False
  elif(inn == 5):
    p_disease = 'Tuberculosis'
    flag = False
  elif(inn == 6):
    p_disease = 'none'
    flag = False
  else:
    print('Wrong Previous Disease.....Enter Again')


flag = True
while(flag):
  print("Choose your Blood Group\n1. A+\n2. A-\n3. B+\n4. B-\n5. O+\n6. O-\n7. AB+\n8. AB-")
  inn = int(input())
  if(inn == 1):
    bgroup = 'A+'
    flag = False
  elif(inn == 2):
    bgroup = 'A-'
    flag = False
  elif(inn == 3):
    bgroup = 'B+'
    flag = False
  elif(inn == 4):
    bgroup = 'B-'
    flag = False
  elif(inn == 5):
    bgroup = 'O+'
    flag = False
  elif(inn == 6):
    bgroup = 'O-'
    flag = False
  elif(inn == 7):
    bgroup = 'AB+'
    flag = False
  elif(inn == 8):
    bgroup = 'AB-'
    flag = False
  else:
    print('Wrong Blood Group.....Enter Again')
    
tupp = [condition, disease, gender, bgroup, p_disease]
tupp = np.asarray(tupp).reshape(1, -1)

tupp[:, 0] = labelencoder0.transform(tupp[:, 0])
tupp[:, 1] = labelencoder1.transform(tupp[:, 1])
tupp[:, 2] = labelencoder2.transform(tupp[:, 2])
tupp[:, 3] = labelencoder3.transform(tupp[:, 3])
tupp[:, 4] = labelencoder4.transform(tupp[:, 4])

tupp = tupp.astype('int')
tupp = scaler.transform(tupp)
print(tupp)

op = classifier.predict(tupp)


print(f'\nExpected date of recovery of patient is {days(op)} days')

"""
file = open('label1.pkl', "wb")
pickle.dump(labelencoder0, file)
file = open('label2.pkl', "wb")
pickle.dump(labelencoder1, file)
file = open('label3.pkl', "wb")
pickle.dump(labelencoder2, file)
file = open('label4.pkl', "wb")
pickle.dump(labelencoder3, file)
file = open('label5.pkl', "wb")
pickle.dump(labelencoder4, file)

file = open('scaler.pkl', "wb")
pickle.dump(scaler, file)

file = open('abc.pkl', "rb")
classs = pickle.dump(classifier, file)
"""