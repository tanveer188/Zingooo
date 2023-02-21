from django.shortcuts import render,HttpResponse
from datetime import datetime
from datetime import date
def convert24(time):
    # Parse the time string into a datetime object
    t = datetime.strptime(time, '%I:%M %p')
    # Format the datetime object into a 24-hour time string
    return t.strftime('%H:%M:%S')
 

# Create your views here.
def login(request):
  return render(request,"login.html")
    #return render(request,'login.html')
  
def submit(request):
  if(request.method == 'POST'):
    import requests
    requests.packages.urllib3.disable_warnings() 
    import json
    import re
    from bs4 import BeautifulSoup
    email = request.POST.get('email')
    password = request.POST.get('password')
    url = 'https://erp.meu.edu.in/j_security_check'
    myobj = {'j_username': email,'j_password': password}
    try:
      response = requests.post(url, data = myobj,verify=False)
    except:
      context = {
          "id" : "Internal Server Error",
          }
      return render(request,"login.html",context)
    soup = BeautifulSoup(response.content,'html5lib')
    table = soup.find("title")
    #table = ["Student Home"]
    try:
      for i in table:
        if(i == "Student Home"):
          apiurl = 'https://erp.meu.edu.in/getSubjectOnChangeWithSemId1.json?termId=0'
          #apiurl = "http://127.0.0.1:8000/static/att.html"
          timtableapi = "https://erp.meu.edu.in/getTodaysScheduleForStudentLoggedIn.json?date=Feb%2017,2023"
          #timtableapi = "http://127.0.0.1:8000/static/stdtimtable.html"
          subject,present,absent,total,percentage,howPerce75,SkipClasses,arr,arr2 = 0,0,0,0,0,0,0,[],[]
          content = []
          timetable = []
          todayAttArr = []
          with requests.Session() as s:
            #make request to erp.meu to login
            s.post(url, data = myobj,verify=False)
            #fetching all th atendence data from mandsaur university
            x = s.get(apiurl,verify=False)
            z = s.get(timtableapi,verify=False)
            #converting into a json object 
            y = x.json()
            z = z.json()
            z = z[0]["timetable"]
            for value in z:
              subShortName = value["subShortName"]
              time = value["startTimeHHMMA"]
              startTimeHM = value["startTimeHM"]
              timetabletemp = {
                "subShortName":subShortName,
                "time":time.replace("AM","").replace("PM",""),
                "startTimeHM":startTimeHM,
                "todayatt":"",
              }
              timetable.append(timetabletemp)
            timetable.sort(key = lambda x: datetime.strptime(x["startTimeHM"], "%X"))
            #working on individual subject
            for i in y:
              Worry = True
              todayAttArrTemp = 0
              #cleearing arr and arr 2
              #arr is used to retrive and format attendance date wise
              arr.clear()
              #arr2 is used to retrive and fetch the next lecture date
              arr2.clear()
              #requesting python for todats date in format 2021-02-10
              todayDatetime =datetime.now().strftime("%Y-%m-%d")
              #storing subject name and present and absent of student
              subject = i["subject"]
              subjectCategory = i["subjectCategory"]
              present = int(i["presentCount"])
              absent = int(i["absentCount"])
              #total days 
              total = absent + present
              #when total become zero then python make an error to resolve it a if statment to check wheater total is zero or not 
              if total != 0 and subjectCategory != "VOCATIONAL_SUBJECT":
                #calculating percentage
                percentage = int((present/total)*100)
                #if percantage is greater than 75 then calculating how many classes you can skip and making howto75 0
                if percentage > 75 :
                  howPerce75 = 0
                  for j in range(0,120):
                    SkipClasses = ((present)/(total+j))*100
                    if SkipClasses < 75 :
                      SkipClasses = j-1
                      break
                #if percentage is not geater than 75 then calculating how many days it takes to make it 75 and making skipable clases 0
                else:
                  SkipClasses = 0
                  for j in range(0,120):
                    howPerce75 = ((present+j)/(total+j))*100
                    if howPerce75 > 75 :
                      howPerce75 = j
                      break
                #if total is equal to zero then making percentage 0 and how to 75 0
              elif subjectCategory == "VOCATIONAL_SUBJECT":
                Worry = False
                percentage = 0
                howPerce75 = "No need to worry"
                SkipClasses = "No need to worry"
              else:
                percentage = 0
                howPerce75 = 0
              #formating all the attandance of all the date string
              arr = re.split(";| |,",i["studentAttendanceData"].replace("^^^"," "))
              #formating the next class date 
              arr2 = re.split(" ",(i["nextLectDate"].replace(",","")))
              #to solve the error when zero item in attendance or when zero clases have happen make a condition to avoid error of arr overloading index
              if(len(arr) > 1):
                #formatting the last date we get in arr1 to datetime object
                lastclassTime = datetime.strftime(datetime.strptime(arr[len(arr)-8]+"/"+arr[len(arr)-11]+"/"+arr[len(arr)-10],"%Y/%b/%d"),"%Y-%m-%d")
                #STarting the process to check wheater attence is taking or not than checking if taken then persent or absent 
                #STEP1- chacking is attendance is taking by comparing dates of today and attendance data
                if todayDatetime == lastclassTime:
                  todayAtt = arr[len(arr)-3]
                  todayAttSub = subject
                  todayAttTime = arr[len(arr)-7]+" "+arr[len(arr)-6]#START_IME
                  todayAttArrTemp = {
                "todayAtt":todayAtt,
                "subject":todayAttSub,
                "todayAttTime":todayAttTime,
                  }
                #STEP2- CHecking it is a special class or not if it is special if it is not  then no next class date is provided in api
                elif arr2[0] != "-":
                #similar to previous one formating the nextclass 
                  nextclassTime = datetime.strftime(datetime.strptime(arr2[-1]+"/"+arr2[0]+"/"+arr2[1],"%Y/%B/%d"),"%Y-%m-%d")
                #STEP3- there is three condinion when attendance is not taken
                #1. some time left for class
                  if(nextclassTime == todayDatetime):
                    todayAtt = 'N/A'
                    todayAttSub = subject
                    todayAttTime = i["nextLectTime"]
                    todayAttArrTemp = {
                "todayAtt":todayAtt,
                "subject":todayAttSub,
                "todayAttTime":todayAttTime,
                      }
                  #2. today have no classes wrt to subject
                  else:
                     todayAtt = 'N/A'
                  #3.it is a special class then there is n0o shedule 
              else:
                todayAtt = "NO SHEDULE"
              # print(arr[len(arr)-11],arr[len(arr)-10],arr[len(arr)-8],arr[len(arr)-5],arr[len(arr)-4])
              contextTemp = {
                "subject":subject,
                "present":present,
                "absent":absent,
                "total":total,
                "percentage":percentage,
                "howPerce75":howPerce75,
                "SkipClasses":SkipClasses,
                "border": percentage*3.6,
                "Worry":Worry,
                "height":0,
                "totalAtt":[],
              }
              if(str(todayAttArrTemp) != "0"):
                todayAttArr.append(todayAttArrTemp)
              for index in range(0,len(arr)-1,11):
                Date =str(arr[index+1])+"/"+str(arr[index+0])+"/"+str(arr[index+3])#date month
                Aorp = arr[index+8]#A_OR_P
                contextmin = {
                  "Date":Date,
                  "Aorp":Aorp,
                }
                # Stime = arr[index+4],arr[index+5]#START_IME
                # contextTemp["totalAtt"].append(Stime)
                # Etime =arr[index+6],arr[index+7]#END_TIME
                # contextTemp["totalAtt"].append(Etime)
                contextTemp["totalAtt"].append(contextmin)
              contextTemp["height"] = (((len(contextTemp["totalAtt"])+1)*2.57864375)+10.849625)*16
              content.append(contextTemp)
  
          todayAttArr.sort(key = lambda x: convert24(x["todayAttTime"]))
          print(len(timetable),len(todayAttArr))
          try:
            for index in range(0,len(todayAttArr)):
              timetable[index]["todayatt"] = todayAttArr[index]["todayAtt"]
              context = {
            "timetable": timetable,
            "content" : content
                 }
          except:
            context = {
              "content":content
            }
  
          return render(request,'Attandance.html',context)
        else:
          context = {
            "id" : "Incorrect Email or password"}
          return render(request,'login.html',context)
    except:
      context = {
        "id" : "Server Error try again later"}
      return render(request,'login.html',context)
    else:
      context = {
        "id" : "Incorrect Email or password"}
      return render(request,'login.html',context)
  else:
    return render(request,'login.html')
    # except:
    #   context = {
    #       "id" : "Unexpected error has occus try again later"}
    #   return render(request,'login.html',context)
    
  