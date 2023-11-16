import requests
import json

user="sehaani01"
password = getpass(prompt='Input your password: ') # the default prompt is 'Password: 

url_security='https://panorama.ngninfra.net/api/?type=keygen'
params={'type':'keygen','user':user,'password':password}
get_key=requests.get(url_security, params=params, verify=False)