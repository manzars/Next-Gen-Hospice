# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 13:39:53 2019

@author: Wasim sayyed
"""
#importing Libraries
import pandas
import numpy as np
import sqlalchemy

#reading CSV
data = pandas.read_excel('hospice-data.xlsv')

#calculating number of days
data['dateDiff'] = data['DischargeDate'] - data['AdmissionDate']
data['dateDiff'] = data['dateDiff']/np.timedelta64(1, 'D')
data['dateDiff'] = data['dateDiff'].round(0).astype(int)

#Adding Disease to database
data.loc[(data['dateDiff'] <= 1) & (data['dateDiff'] >= 0), "Disease"]  = "fever"
data.loc[(data['dateDiff'] <= 2) & (data['dateDiff'] >= 2), "Disease"]  = "cbc"
data.loc[(data['dateDiff'] <= 4) & (data['dateDiff'] >= 3), "Disease"]  = "maleria"
data.loc[(data['dateDiff'] <= 5) & (data['dateDiff'] >= 5), "Disease"]  = "Pneumonia"
data.loc[(data['dateDiff'] <= 6) & (data['dateDiff'] >= 6), "Disease"]  = "abdomen pain"
data.loc[(data['dateDiff'] <= 8) & (data['dateDiff'] >= 7), "Disease"]  = "Pseudomonas aeruginosa"
data.loc[(data['dateDiff'] <= 11) & (data['dateDiff'] >= 9), "Disease"]  = "dengue fever"
data.loc[(data['dateDiff'] <= 14) & (data['dateDiff'] >= 12), "Disease"]  = "Influenza"
data.loc[(data['dateDiff'] <= 19) & (data['dateDiff'] >= 15), "Disease"]  = "Tuberculosis"
data.loc[(data['dateDiff'] <= 21) & (data['dateDiff'] >= 20), "Disease"]  = "Adhesive Pericapsulitis"
data.loc[(data['dateDiff'] <= 24) & (data['dateDiff'] >= 22), "Disease"]  = "Klebsiella"
data.loc[(data['dateDiff'] <= 31) & (data['dateDiff'] >= 25), "Disease"]  = "Cardiac arrhythmias"
data.loc[(data['dateDiff'] <= 40) & (data['dateDiff'] >= 33), "Disease"]  = "Mycobacterium abscessus"
data.loc[(data['dateDiff'] <= 47) & (data['dateDiff'] >= 41), "Disease"]  = "Congestive heart failure"
data.loc[(data['dateDiff'] <= 999) & (data['dateDiff'] >= 48), "Disease"]  = "Norovirus"

#adding Gender to database
data['Gender'] = np.random.choice(["M", "F"], data.shape[0])


#adding Gender to database
data['IsCritical'] = np.random.choice([0, 1], data.shape[0])

#adding blood group to database
data['BloodGroup'] = np.random.choice(["O+", "O-", "A+", "A-", "B+", "B-", "AB+", "AB-"], data.shape[0])

#adding Previous disease to database
data['PreviousDisease'] = np.random.choice(["fever", "dengue fever", "Influenza", "maleria", "Tuberculosis", "none", "none", "none", "none"], data.shape[0])

#making copy of newly created csv file for training purpose
data.to_csv("final_hospice_data.csv")

#assigning gender ids as per foreign key
data.loc[data['Gender'] == "M" , "Gender"]  = "1"
data.loc[data['Gender'] == "F" , "Gender"]  = "2"

#assigning Disease ids as per foreign key
data.loc[data['Disease'] == "fever" , "Disease"]  = "1"
data.loc[data['Disease'] == "cbc" , "Disease"]  = "4"
data.loc[data['Disease'] == "maleria" , "Disease"]  = "6"
data.loc[data['Disease'] == "Pneumonia" , "Disease"]  = "7"
data.loc[data['Disease'] == "abdomen pain" , "Disease"]  = "2"
data.loc[data['Disease'] == "Pseudomonas aeruginosa" , "Disease"]  = "14"
data.loc[data['Disease'] == "dengue fever" , "Disease"]  = "3"
data.loc[data['Disease'] == "Influenza" , "Disease"]  = "13"
data.loc[data['Disease'] == "Tuberculosis" , "Disease"]  = "15"
data.loc[data['Disease'] == "Adhesive Pericapsulitis" , "Disease"]  = "5"
data.loc[data['Disease'] == "Klebsiella" , "Disease"]  = "12"
data.loc[data['Disease'] == "Cardiac arrhythmias" , "Disease"]  = "8"
data.loc[data['Disease'] == "Mycobacterium abscessus" , "Disease"]  = "11"
data.loc[data['Disease'] == "Congestive heart failure" , "Disease"]  = "9"
data.loc[data['Disease'] == "Norovirus" , "Disease"]  = "10"

#assigning Previous disease ids as per foreign key
data.loc[data['PreviousDisease'] == "fever" , "PreviousDisease"]  = "1"
data.loc[data['PreviousDisease'] == "maleria" , "PreviousDisease"]  = "6"
data.loc[data['PreviousDisease'] == "dengue fever" , "PreviousDisease"]  = "3"
data.loc[data['PreviousDisease'] == "Influenza" , "PreviousDisease"]  = "13"
data.loc[data['PreviousDisease'] == "Tuberculosis" , "PreviousDisease"]  = "15"
data.loc[data['PreviousDisease'] == "none" , "PreviousDisease"]  = "16"

#assigning blood group ids as per foreign key
data.loc[data['BloodGroup'] == "O+" , "BloodGroup"]  = "1"
data.loc[data['BloodGroup'] == "O-" , "BloodGroup"]  = "2"
data.loc[data['BloodGroup'] == "A+" , "BloodGroup"]  = "3"
data.loc[data['BloodGroup'] == "A-" , "BloodGroup"]  = "4"
data.loc[data['BloodGroup'] == "B+" , "BloodGroup"]  = "5"
data.loc[data['BloodGroup'] == "B-" , "BloodGroup"]  = "6"
data.loc[data['BloodGroup'] == "AB+" , "BloodGroup"]  = "7"
data.loc[data['BloodGroup'] == "AB-" , "BloodGroup"]  = "8"

#Renaming columns name as per the tables in database
data.rename(columns={
        "AdmissionId": "id",
        "Gender": "genderId",
        "BloodGroup": "bloodGroupId",
        "AdmissionDate": "admissionDate",
        "DischargeDate": "dischargeDate",
        "IsCritical": "isCritical",
        "Disease": "diseaseId",
        "PreviousDisease": "previousDiseaseId"
        }, inplace = True)

#connecting Database with python script
engine = sqlalchemy.create_engine('mysql+pymysql://root:@localhost:3306/hospice')

#forwarding data from here to database
data.to_sql(
        name = "admission",
        con = engine,
        index = False,
        if_exists = "append"
        )

