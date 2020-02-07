from django.shortcuts import render, redirect
from .models import Admission, Admin
import mysql.connector
import pickle
import numpy as np
import pandas as pd
from django.http import JsonResponse
from datetime import timedelta  
from sklearn.preprocessing import LabelEncoder
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from sklearn.linear_model import LinearRegression
import json
from time import gmtime, strftime, localtime
import random

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
p = {}
i = 0
for alll in all_patient:
  p[alll] = i



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

def generateJSON(pid):
    mydbs = mysql.connector.connect(
      host="localhost",
      user="root",
      passwd=""
    )
    mycursor = mydbs.cursor()
    mycursor.execute("USE hospice")
    mycursor.execute("SELECT genderId, isCritical FROM `admission` WHERE IPNo = '" + pid + "'")
    data = list(mycursor.fetchone())
    
    mycursor.execute("SELECT IPNo FROM `admission` WHERE genderId = '" + str(data[0]) + "' AND isCritical = '" + str(data[1]) + "' LIMIT 10")
    data = list(mycursor.fetchall())
    print(data)
    patient = list(p[0] for p in data)
    datediff = []
    for p in patient:
      mycursor.execute("SELECT dateDiff from `admission` WHERE  IPNo = '" + p + "' ")
      datediff.append(mycursor.fetchone())
    datediff = list(p[0] for p in datediff)
    print(datediff)
    name = []
    for p in patient:
      mycursor.execute("SELECT name from `admission` WHERE  IPNo = '" + p + "' ")
      name.append(mycursor.fetchone())
    name = list(p[0].split()[0] for p in name)
    print(name)
    mydbs.commit()
    mydbs.close()
    return patient, datediff, name


def dataFetchFromSQL(idd):

    mydbs = mysql.connector.connect(
      host="localhost",
      user="root",
      passwd=""
    )

    mycursor = mydbs.cursor()
    mycursor.execute("USE hospice")
    mycursor.execute("SELECT * FROM `admission` WHERE IPNo = '" + idd + "'")
    data = mycursor.fetchone()

    mycursor.execute("SELECT * FROM `gender` WHERE id = '" + str(data[1]) + "'")
    gender = mycursor.fetchone()[1]

    mycursor.execute("SELECT * FROM `disease` WHERE id = '" + str(data[2]) + "'")
    disease = mycursor.fetchone()[1]

    mycursor.execute("SELECT * FROM `previousdisease` WHERE id = '" + str(data[3]) +"'")
    p_disease = mycursor.fetchone()[1]

    if(data[4] == 0):
        is_critical = "normal"
    else:
        is_critical = "critical"

    mycursor.execute("SELECT * FROM `bloodgroup` WHERE id = '" + str(data[5]) +"'")
    b_group = mycursor.fetchone()[1]
    mydbs.commit()
    mydbs.close()

    return [is_critical, disease, gender, b_group, p_disease], data[6].date(), data[6].date(), str(data[13]), str(data[14]), str(data[15]), disease, gender


def data_entry(addmissionDate, disease, p_disease, condition, bloodGroup, name, gender, address, email, mobile):
  mydbs = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd=""
  )
  
  
  flag = True
  ip = "IP-"
  fno = 0
  bno = 0
  while(flag):
    fno = random.randint(10, 100000)
    bno = random.randint(10, 1000000)
    if(ip + str(fno) + "-" + str(bno) not in all_patient):
      flag = False
    print(ip + str(fno) + "-" + str(bno))
    ip = ip + str(fno) + "-" + str(bno)


  mycursor = mydbs.cursor()
  mycursor.execute("USE hospice")
  #addmissionDate = DateTime(addmissionDate) 
  command = """ INSERT INTO admission (genderId, diseaseId, previousDiseaseId, isCritical, bloodGroupId, admissionDate, IPNo, name, email, phone) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """
 
  mycursor.execute(command, (int(gender), int(disease), int(p_disease), int(condition), int(bloodGroup), addmissionDate, ip, name, email, int(mobile)))
  mydbs.commit()
  mydbs.close()


def data(request):
  if not request.user.is_authenticated:
      return redirect('signin')

  if request.method == 'POST':
    name = request.POST['name']
    mobile = request.POST['mobile']
    address = request.POST['address']
    gender = request.POST['gender']
    disease = request.POST['disease']
    p_disease = request.POST['previousDisease']
    bloodgroup = request.POST['bloodGroup']
    condition = request.POST['condition']
    addmission_date = request.POST['admissionDate']
    addmission_date = addmission_date + " " + str(strftime("%H:%M:%S", localtime()))
    email = request.POST['email']
    data_entry(addmission_date, disease, p_disease, condition, bloodgroup, name, gender, address, email, mobile)
    print(addmission_date + " " + str(strftime("%H:%M:%S", localtime())))




    return render(request, 'hospiceweb/data1.html', {})
  else:
    return render(request, 'hospiceweb/data1.html')

def hospices(request):

    mydbs = mysql.connector.connect(
      host="localhost",
      user="root",
      passwd=""
    )

    main = mydbs.cursor()
    main.execute("USE hospice")
    main.execute("SELECT `IPNo` FROM `admission`")
    all_patient = list(main.fetchall())
    mydbs.commit()
    mydbs.close()
    all_patient = list(p[0] for p in all_patient)
    p = {}
    i = 0
    for alll in all_patient:
      p[alll] = i
    if not request.user.is_authenticated:
      return redirect('signin')
    IPNo = None
    data = {"ip": all_patient, "submit": "none", "p": p, "patient": "undefined", "datediff": "undefined", "chart_name": "undefined"}
    if request.method == 'POST':
        IPNo = request.POST['PId']
        patient, datediff, chart_name = generateJSON(IPNo)

        data, admissionDate, date, name, email, phone, disease, gender = dataFetchFromSQL(IPNo)
        data = np.asarray(data).reshape(1, -1)

        data[:, 0] = labelencoder0.transform(data[:, 0])
        data[:, 1] = labelencoder1.transform(data[:, 1])
        data[:, 2] = labelencoder2.transform(data[:, 2])
        data[:, 3] = labelencoder3.transform(data[:, 3])
        data[:, 4] = labelencoder4.transform(data[:, 4])

        data = data.astype('int')
        file = open('data/regressor.pkl', "rb")
        regressor = pickle.load(file)
        file.close()

        file = open('data/regresor_lab.pkl', "rb")
        regressor_lab = pickle.load(file)
        file.close()
        
        price = regressor.predict(data)[0].round(2)
        price_lab = regressor_lab.predict(data)[0].round(2)
        total = (abs(price) + abs(price_lab)).round(2)
        data = scaler.transform(data)
        file = open('data/classifier.pkl', "rb")
        classs = pickle.load(file)
        file.close()

        if(gender=='M'):
          gender = "Male"
        else:
          gender = "Female"

        op = classs.predict(data)
        if(len(day(op)) == 2):
            start = date + timedelta(days = day(op)[0])
            end = date + timedelta(days = day(op)[1])
            data = {"admissionDate": str(admissionDate.strftime("%d %b %Y")), "gender": gender, "name": name, "phone": phone, "email": email, "disease": disease, "ip": all_patient, "IPNo": IPNo, "total": total, "price_lab": abs(price_lab), "price": abs(price), "date": day(op), "submit": "block", "start": str(start.strftime("%d %b %Y")), "end": str(end.strftime("%d %b %Y")), "p": p, "patient": patient, "datediff": datediff, "chart_name": chart_name}
            return render(request, 'hospiceweb/basic.html', data)
        else:
            start = date + timedelta(days = day(op)[0])

            data = {"admissionDate": str(admissionDate.strftime("%d %b %Y")), "gender": gender, "name": name, "phone": phone, "email": email, "disease": disease, "ip": all_patient, "IPNo": IPNo, "total": total, "price_lab": abs(price_lab), "price": abs(price), "date": day(op), "submit": "block", "start": str(start.strftime("%d %b %Y")), "end": "NaN", "p": p, "patient": patient, "datediff": datediff, "chart_name": chart_name}
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
      return JsonResponse(data)
  else:
    return render(request, 'hospiceweb/basic.html')


def signin(request):
  if request.user.is_authenticated:
      return redirect('hospice')
  if(request.method == 'POST'):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    try:
      if user is not None:
        login(request, user)
        return redirect("hospice")
      else:
        messages.success(request, ('Error - logging in - Please try again'))
        return redirect("signin")
    except:
      return render(request, 'hospiceweb/signin1.html')
  else:
    return render(request, 'hospiceweb/signin1.html')




def log_out(request):
  if not request.user.is_authenticated:
      return redirect('signin')
  data = {"name": request.user.username}
  logout(request)
  return render(request, 'hospiceweb/logout.html', data)
