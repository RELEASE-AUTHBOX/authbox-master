import requests,json
headers={'content-type':'application/json'}
payload=json.dumps({'name':'Apple AirPods','data':{'color':'white','generation':'3rd','price':135}})
requestUrl='https://127.0.0.1/users/1/'
r=requests.put(requestUrl,data=payload,headers=headers)
print(r.content)