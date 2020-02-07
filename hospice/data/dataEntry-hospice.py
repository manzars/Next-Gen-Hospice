import pandas
import numpy as np

#appendind Days i;e difference of discharge date and admission date
data = pandas.read_excel('hospice-data.xlsv')
data['dateDiff'] = data['DischargeDate'] - data['AdmissionDate']
data['dateDiff']=data['dateDiff']/np.timedelta64(1,'D')
data['dateDiff'] = data['dateDiff'].round(0).astype(int)

#Appending Disease
diseaseList = ['fever', 'abdomen pain', 'dengue fever',  'cbc',  'Adhesive Pericapsulitis',  'maleria',  'Pneumonia',  'Cardiac arrhythmias',  'Congestive heart failure',  'Norovirus',  'Mycobacterium abscessus',  'Klebsiella',  'Influenza',  'Pseudomonas aeruginosa',  'Tuberculosis']

data['Disease'] = 