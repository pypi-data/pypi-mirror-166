import os
import requests
import make_zip as mz

api_url_test= "http://34.168.0.37:8778/demo"

def demo(key, main_name, func):
  main_pyfilename = mz.make_zip(key, main_name, func)
  
  values = {"key": key, "modelname": main_pyfilename}
  res = requests.post(api_url_test, files = {'file': open("./aif.zip",'rb', )}, data=values)  
  if res.status_code == 200 or res.status_code == 201: 
    print("success")
    return
  print(res.status_code)  
  print(res.text)