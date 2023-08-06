import requests
from make_zip import make_zip

api_url_test= "https://grade-bridge-test.aifactory.space/grade"
api_url = "https://grade-bridge.aifactory.space/grade"

def submit(key, submit_file_path):
  values = {"key": key}
  res = requests.post(api_url, files = {'file': open(submit_file_path,'rb', )}, data=values)  
  if res.status_code == 200 or res.status_code == 201: 
    print("success")
    return
  print(res.status_code)  
  print(res.text)

def submit_test(key, main_name, func):
  main_pyfilename = make_zip(key, main_name, func)
  
  values = {"key": key, "modelname": main_pyfilename}
  res = requests.post(api_url_test, files = {'file': open("./aif.zip",'rb', )}, data=values)  
  if res.status_code == 200 or res.status_code == 201: 
    print("success")
    return
  print(res.status_code)  
  print(res.text)

