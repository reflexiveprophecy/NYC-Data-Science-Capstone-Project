import requests
url = 'https://gimmeproxy.com/api/getProxy'
proxies = {
    "http": '159.224.176.205:53281', 
    "https": '159.224.176.205:53281'
}
response = requests.get(url,proxies=proxies)
print(response.json())