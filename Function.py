import json
import cred
import pprint as pp
import requests 
from dict2xml import dict2xml
import xmltodict
import menandmice
headers={'X-PAN-KEY':cred.key}
def p(v):
    print('*' * 70, '\n' )
    pp.pprint(v)
    print('\n', '*' * 70)

def get_ike_gw(ike_name,location_t,template):
    url="https://panorama.ngninfra.net/restapi/v10.1/Network/IKEGatewayNetworkProfiles"
    query={"name": ike_name,'location':location_t,location_t:template }
    ike_gw_respons=requests.get(url, params=query, verify=False, headers=headers).json()
    return ike_gw_respons

def get_tunnel(tunnel_name,location_t,template):
    url="https://panorama.ngninfra.net/restapi/v10.1/Network/IPSecTunnels"
    query={"name": tunnel_name,'location':location_t,location_t:template }
    respons=requests.get(url, params=query, verify=False, headers=headers).json()
    return respons

def create_ipsec_tunnel(data,location_t,template):
    body = json.dumps(
                {
                "entry":
                data
                    
                }                )
            
    tunnel_name=data['@name']
    url="https://panorama.ngninfra.net/restapi/v10.1/Network/IPSecTunnels"
    query={"name": tunnel_name,'location':location_t,location_t:template }
    post_ipsec_tunnel=requests.post(url,params=query,data=body, verify=False, headers=headers).json()
    return post_ipsec_tunnel

def add_ike_gw(data,location_t,to_template):
    body = json.dumps(
                {
                "entry":
                data
                    
                }                )
            
    ike_name=data['@name']
    location_ike_gw={"name": ike_name,'location':location_t,location_t:to_template }
    url_ike_gw='https://panorama.ngninfra.net/restapi/v10.1/Network/IKEGatewayNetworkProfiles'
    post_ike_gw=requests.post(url_ike_gw,params=location_ike_gw,data=body, verify=False, headers=headers).json()
    return post_ike_gw

def get_tunnel_interface(tunnel_interfece_name,location_t,template):
    url="https://panorama.ngninfra.net/restapi/v10.1/Network/TunnelInterfaces"
    query={"name": tunnel_interfece_name,'location':location_t,location_t:template }
    respons=requests.get(url, params=query, verify=False, headers=headers).json()
    return respons

def create_tunnel_interface(name,tl_if_name,location_t,to_template):
    
    body = json.dumps(
            {
                "entry":
                {
                    "@name": tl_if_name,
                    "comment":name
                }
            }
        )
   
    query={"name": tl_if_name,'location':location_t,location_t:to_template }
    url_tl_if='https://panorama.ngninfra.net/restapi/v10.1/Network/TunnelInterfaces'
    response=requests.post(url_tl_if,params=query,data=body, verify=False, headers=headers).json()


    return response


def get_ipsec_crypto_p(cry_p_name,location_t,template):
    url='https://panorama.ngninfra.net/restapi/v10.1/Network/IPSecCryptoNetworkProfiles'
    query={"name": cry_p_name,'location':location_t,location_t:template }
    respons=requests.get(url, params=query, verify=False, headers=headers).json()
    return respons
def get_ike_crypto_p(ike_p_name,location_t,template):
    url='https://panorama.ngninfra.net/restapi/v10.1/Network/IKECryptoNetworkProfiles'
    query={"name": ike_p_name,'location':location_t,location_t:template }
    respons=requests.get(url, params=query, verify=False, headers=headers).json()
    return respons
def create_ike_crypto(ike_p,location_t,to_template):
    data=ike_p['result']['entry'][0]
    if '@location' in data: del data['@location']
    if '@template' in data: del data['@template']
    
    body = json.dumps(
            {
                "entry":
                
                    data
                
            }
        )

    location_crypto={"name": data['@name'],'location':location_t,location_t:to_template}
    url='https://panorama.ngninfra.net/restapi/v10.1/Network/IKECryptoNetworkProfiles'
    post_crypto=requests.post(url,params=location_crypto,data=body, verify=False, headers=headers).json()
    return post_crypto
def create_ipsec_crypto(ipsec_p,location_t,to_template):
    data=ipsec_p['result']['entry'][0]
    if '@location' in data: del data['@location']
    if '@template' in data: del data['@template']
    
    body = json.dumps(
            {
                "entry":
                
                    data
                
            }
        )

    location_crypto={"name": data['@name'],'location':location_t,location_t:to_template}
    url='https://panorama.ngninfra.net/restapi/v10.1/Network/IPSecCryptoNetworkProfiles'
    post_crypto=requests.post(url,params=location_crypto,data=body, verify=False, headers=headers).json()
    return post_crypto

def get_spn(loc):
    xpath_value=f"/config/devices/entry[@name='localhost.localdomain']/plugins/cloud_services/multi-tenant/tenants/entry[@name='eNET']/remote-networks/agg-bandwidth/region/entry[@name='{loc}']/spn-name-list"

    fw=f'https://panorama.ngninfra.net/api/?type=config&action=get&xpath={xpath_value}' 

    a=requests.get(fw,verify=False, headers=headers)
    a.content
    data=xmltodict.parse(a.content)
    if data['response']['result']==None:
        print ("Didn't finde any spn for given region. Please check the region")
        
    else:
        spn=data['response']['result']['spn-name-list']['member']
        return spn
def get_region():
    xpath_value="/config/devices/entry[@name='localhost.localdomain']/plugins/cloud_services/multi-tenant/tenants/entry[@name='eNET']/remote-networks/agg-bandwidth/region"

    fw=f'https://panorama.ngninfra.net/api/?type=config&action=get&xpath={xpath_value}' 

    a=requests.get(fw,verify=False, headers=headers)
    a.content
    data=xmltodict.parse(a.content)
    region=data['response']['result']['region']['entry']
    p(region)
    return region

def get_rn(name):
    xpath_get=f"/config/devices/entry[@name='localhost.localdomain']/plugins/cloud_services/multi-tenant/tenants/entry[@name='eNET']/remote-networks/onboarding/entry[@name='{name}']"
    url_get=f'https://panorama.ngninfra.net/api/?type=config&action=get&xpath={xpath_get}' 
    get_data=requests.get(url_get,verify=False, headers=headers)
    data=xmltodict.parse(get_data.content)
    return data

