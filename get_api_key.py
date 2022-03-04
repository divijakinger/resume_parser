import requests

url = "https://auth.emsicloud.com/connect/token"

payload = "client_id=3vjr348ekdkyu6s7&client_secret=rXxiEP0P&grant_type=client_credentials&scope=emsi_open"
headers = {'Content-Type': 'application/x-www-form-urlencoded'}

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)