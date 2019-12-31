from django.shortcuts import render
from .models import Admission
import mysql.connector
import pickle
import numpy as np
import pandas as pd
from django.http import JsonResponse
from datetime import timedelta  
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression
import json

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd=""
)

main = mydb.cursor()
main.execute("USE hospice")
main.execute("SELECT `IPNo` FROM `admission`")
all_patient = list(main.fetchall())
all_patient = list(p[0] for p in all_patient)
# print(json.dumps(all_patient))



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

data = pd.read_csv('data/final_hospice_data.csv')
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

def dataFetchFromSQL(idd):
    mycursor = mydb.cursor()
    #ipno = input("Enter IPNo of Patient: ")
    mycursor.execute("USE hospice")
    mycursor.execute("SELECT * FROM `admission` WHERE IPNo = '" + idd +"'")
    data = mycursor.fetchone()
    
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


# Create your views here.
def hospices(request):
    # print(ip.ipno)
    IPNo = None
    data = {"ip": all_patient, "submit": "none"}
    if request.method=='POST':
        IPNo = request.POST['PId']

        data, date = dataFetchFromSQL(IPNo)
        data = np.asarray(data).reshape(1, -1)

        data[:, 0] = labelencoder0.transform(data[:, 0])
        data[:, 1] = labelencoder1.transform(data[:, 1])
        data[:, 2] = labelencoder2.transform(data[:, 2])
        data[:, 3] = labelencoder3.transform(data[:, 3])
        data[:, 4] = labelencoder4.transform(data[:, 4])

        data = data.astype('int')
        #print(data)
        file = open('data/regressor.pkl', "rb")
        regressor = pickle.load(file)
        file.close()

        file = open('data/regresor_lab.pkl', "rb")
        regressor_lab = pickle.load(file)
        file.close()
        
        price = regressor.predict(data)[0].round(2)
        price_lab = regressor_lab.predict(data)[0].round(2)
        total = (abs(price) + abs(price_lab)).round(2)

        #print(price)
        data = scaler.transform(data)
        #print(data)

        file = open('data/abc.pkl', "rb")
        classs = pickle.load(file)
        file.close()

        op = classs.predict(data)
        #print(type(date))
        if(len(day(op)) == 2):
            start = date + timedelta(days = day(op)[0])
            end = date + timedelta(days = day(op)[1])
            data = {"ip": all_patient, "IPNo": IPNo, "total": total, "price_lab": abs(price_lab), "price": abs(price), "date": day(op), "submit": "block", "start": str(start.strftime("%d/%m/%Y")), "end": str(end.strftime("%d/%m/%Y"))}
            # print("hello", type(start))
            return render(request, 'hospiceweb/basic.html', data)
        else:
            start = date + timedelta(days = day(op)[0])
            data = {"ip": all_patient, "IPNo": IPNo, "total": total, "price_lab": abs(price_lab), "price": abs(price), "date": day(op), "submit": "block", "start": str(start.strftime("%d/%m/%Y")), "end": "NaN"}
            return render(request, 'hospiceweb/basic.html', data)
    else:
        return render(request, 'hospiceweb/basic.html', data)



def search(request):
    if request.is_ajax():
        queryset = Admission.objects.filter(ipno__contains=request.GET.get('search', None))
        lst = []        
        for i in queryset:
            lst.append(i.ipno)
        data = {
            'list': lst,
        }
        #print(len(lst))
        return JsonResponse(data)
    else:
      return render(request, 'hospiceweb/basic.html')














# def search(request):

#   if request.method == 'GET':
#     search_text = request.GET['search_text']
#   else:
#     search_text = ''
#   IP=IP-294001
#   ip = Admission.objects.filter(ipno__contains=search_text)
#   print(ip)
#   return render(request,'hospiceweb/basic.html')
#   return render(request,'hospiceweb/search',{'ip':ip})
#   return JsonResponse(ip)

# def autocomplete(request):
#     if request.is_ajax():
#         queryset = Admission.objects.filter(ipno__startswith=request.GET.get('search', None))
#         list = []        
#         for i in queryset:
#             list.append(i.ipno)
#         data = {
#             'list': list,
#         }
#         return JsonResponse(data)