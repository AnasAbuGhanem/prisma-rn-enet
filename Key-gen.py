import requests
import json
from getpass import getpass
import xmltodict


user="sehaani01"
password = getpass(prompt='Input your password: ') # the default prompt is 'Password: 

url_security='https://panorama.ngninfra.net/api/?type=keygen'
params={'type':'keygen','user':user,'password':password}
get_key=requests.get(url_security, params=params, verify=False)

data=xmltodict.parse(get_key.content)
api_key=data['response']['result']['key']
print('The new API key is: ', api_key)
