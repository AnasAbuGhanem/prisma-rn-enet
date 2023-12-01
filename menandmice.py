import cred
import json
import requests
import Function
from requests.auth import HTTPBasicAuth
import pprint as pp
##
user=f"ecdomain\{cred.user}"
pas='ESSpassE20!$2023!2'
#auth=HTTPBasicAuth(user,cred.password)
auth=HTTPBasicAuth(user,pas)
def p(v):
    print('*' * 70, '\n' )
    pp.pprint(v)
    print('\n', '*' * 70)

def get_ip():

    ref='10.255.2.0/24'
    #'/Ranges/25915'#25705
    url=f'https://ipam.app.essity.com/mmws/api/Ranges/'
    response=requests.get(url=url+ref,  verify=False, auth=auth).json()
    ip=response['result']['range']['childRanges'][-1]['name']
    ip=ip[0:-3]

    a=ip_address(ip)
    return a

def check_ip(ip):
    
    url=f'https://ipam.app.essity.com/mmws/api/Ranges/'
    response=requests.get(url=url+ip,  verify=False, auth=auth).json()
    return response

def add_ip(ip,descrip):
    data=json.dumps(
        {
        'range': {
                    'name': ip,
                    'customProperties':
                              {'Title': descrip}           
                }
         }
                    )
    url=f'https://ipam.app.essity.com/mmws/api/Ranges'
    res_post=requests.post(url=url,  data=data,verify=False, auth=auth).json()
    return res_post

def ip_address(ip):
    
    if ip[-3]=='.':
        okt=int(ip[-2:]) +2
        peer_ip_pr=ip[:-2]+str(okt )
        loc_ip_pri=ip[:-2]+str(okt +1)
        peer_ip_sec=ip[:-2]+str(okt +2)
        loc_ip_sec=ip[:-2]+str(okt +3)
        
        adress=[peer_ip_pr,loc_ip_pri,peer_ip_sec,loc_ip_sec]
        return adress
    elif ip[-2]=='.':
        okt=int(ip[-1:]) +2
        peer_ip_pr=ip[:-2]+str(okt )
        loc_ip_pri=ip[:-1]+str(okt +1)
        peer_ip_sec=ip[:-1]+str(okt +2)
        loc_ip_sec=ip[:-1]+str(okt +3)
        
        adress=[peer_ip_pr,loc_ip_pri,peer_ip_sec,loc_ip_sec]
        return adress
    else:
        okt=int(ip[-3:]) +2
        peer_ip_pr=ip[:-3]+str(okt )
        loc_ip_pri=ip[:-3]+str(okt +1)
        peer_ip_sec=ip[:-3]+str(okt +2)
        loc_ip_sec=ip[:-3]+str(okt +3)
        
        adress=[peer_ip_pr,loc_ip_pri,peer_ip_sec,loc_ip_sec]
        return adress
