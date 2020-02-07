# -*- coding: utf-8 -*-
"""
Created on Tue Dec 31 11:09:58 2019

@author: Wasim sayyed
"""

import pandas as pd
import sqlalchemy
from sqlalchemy import event
import numpy as np

data = pd.read_csv('HospiceDummyData.csv')
male = data.loc[data[' Gender'] == ' M']
female = data.loc[data[' Gender'] == ' F']

data_new = pd.read_csv('final_hospice_data.csv')
data_new.drop(columns = ['Unnamed: 0', 'Unnamed: 0.1'], axis = 0, inplace = True)
data_new['Name'] = None
data_new['Email'] = None
data_new['Phone'] = None

for i in range(data_new.shape[0]):
    if(data_new['Gender'][i] == 'M'):
        data_new['Name'][i] = male.loc[male.index[i]]['Name']
        data_new['Email'][i] = male.loc[male.index[i]][' Email']
        data_new['Phone'][i] = male.loc[male.index[i]][' Phone']
    else:
        data_new['Name'][i] = female.loc[female.index[i]]['Name']
        data_new['Email'][i] = female.loc[female.index[i]][' Email']
        data_new['Phone'][i] = female.loc[female.index[i]][' Phone']
    print(female.loc[female.index[i]]['Name'])
    
data_new.to_csv("final_hospice_data.csv")

data_new.loc[data_new['Gender'] == "M" , "Gender"]  = "1"
data_new.loc[data_new['Gender'] == "F" , "Gender"]  = "2"

#assigning Disease ids as per foreign key
data_new.loc[data_new['Disease'] == "fever" , "Disease"]  = "1"
data_new.loc[data_new['Disease'] == "cbc" , "Disease"]  = "4"
data_new.loc[data_new['Disease'] == "maleria" , "Disease"]  = "6"
data_new.loc[data_new['Disease'] == "Pneumonia" , "Disease"]  = "7"
data_new.loc[data_new['Disease'] == "abdomen pain" , "Disease"]  = "2"
data_new.loc[data_new['Disease'] == "Pseudomonas aeruginosa" , "Disease"]  = "14"
data_new.loc[data_new['Disease'] == "dengue fever" , "Disease"]  = "3"
data_new.loc[data_new['Disease'] == "Influenza" , "Disease"]  = "13"
data_new.loc[data_new['Disease'] == "Tuberculosis" , "Disease"]  = "15"
data_new.loc[data_new['Disease'] == "Adhesive Pericapsulitis" , "Disease"]  = "5"
data_new.loc[data_new['Disease'] == "Klebsiella" , "Disease"]  = "12"
data_new.loc[data_new['Disease'] == "Cardiac arrhythmias" , "Disease"]  = "8"
data_new.loc[data_new['Disease'] == "Mycobacterium abscessus" , "Disease"]  = "11"
data_new.loc[data_new['Disease'] == "Congestive heart failure" , "Disease"]  = "9"
data_new.loc[data_new['Disease'] == "Norovirus" , "Disease"]  = "10"

#assigning Previous disease ids as per foreign key
data_new.loc[data_new['PreviousDisease'] == "fever" , "PreviousDisease"]  = "1"
data_new.loc[data_new['PreviousDisease'] == "maleria" , "PreviousDisease"]  = "6"
data_new.loc[data_new['PreviousDisease'] == "dengue fever" , "PreviousDisease"]  = "3"
data_new.loc[data_new['PreviousDisease'] == "Influenza" , "PreviousDisease"]  = "13"
data_new.loc[data_new['PreviousDisease'] == "Tuberculosis" , "PreviousDisease"]  = "15"
data_new.loc[data_new['PreviousDisease'] == "none" , "PreviousDisease"]  = "16"

#assigning blood group ids as per foreign key
data_new.loc[data_new['BloodGroup'] == "O+" , "BloodGroup"]  = "1"
data_new.loc[data_new['BloodGroup'] == "O-" , "BloodGroup"]  = "2"
data_new.loc[data_new['BloodGroup'] == "A+" , "BloodGroup"]  = "3"
data_new.loc[data_new['BloodGroup'] == "A-" , "BloodGroup"]  = "4"
data_new.loc[data_new['BloodGroup'] == "B+" , "BloodGroup"]  = "5"
data_new.loc[data_new['BloodGroup'] == "B-" , "BloodGroup"]  = "6"
data_new.loc[data_new['BloodGroup'] == "AB+" , "BloodGroup"]  = "7"
data_new.loc[data_new['BloodGroup'] == "AB-" , "BloodGroup"]  = "8"    


data_new.rename(columns={
        "AdmissionId": "id",
        "Gender": "genderId",
        "BloodGroup": "bloodGroupId",
        "AdmissionDate": "admissionDate",
        "DischargeDate": "dischargeDate",
        "IsCritical": "isCritical",
        "Disease": "diseaseId",
        "PreviousDisease": "previousDiseaseId",
        "MedBill": "medBill",
        "LabBill": "labBill",
        "TotalBill": "totalBill",
        "Name": "name",
        "Phone": "phone",
        "Email": "email",
        }, inplace = True)

#connecting Database with python script
engine = sqlalchemy.create_engine('mysql+pymysql://root:@localhost:3306/hospice')

def add_own_encoders(conn, cursor, query, *args):
    cursor.connection.encoders[np.int64] = lambda value, encoders: int(value)

event.listen(engine, "before_cursor_execute", add_own_encoders)

#forwarding data from here to database
data_new.to_sql(
        name = "admission",
        con = engine,
        index = False,
        if_exists = "append"
        )