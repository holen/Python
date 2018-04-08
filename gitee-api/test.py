import requests  
  
r = requests.get('http://127.0.0.1:5000/client/login')  
print(r.text)
print(r.history)

print(r.url)

login_uri = r.url.split('?')[0] + '?user=liuchunming&pw=12345'  
r2 = requests.get(login_uri)
print(r2.text)
print(r2.history)
  
r = requests.get('http://127.0.0.1:5000/testlogin',params={'token': r2.text})  
print(r.text)
