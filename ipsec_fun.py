import json
import cred
import pprint as pp
import requests 
from dict2xml import dict2xml
import xmltodict
import menandmice
import Function
import openpyxl
from openpyxl import workbook, load_workbook
headers={'X-PAN-KEY':cred.key}

def p(v):
    print('*' * 70, '\n' )
    pp.pprint(v)
    print('\n', '*' * 70)
    
def create_prisma_ipsec_tunnel(standar_tunnel,location_t,template,new_tunnel,new_id):
    IPsec_tunnel=Function.get_tunnel(new_tunnel,location_t,template)
    if '@status' in IPsec_tunnel:
        print(f'{new_tunnel} is already exist in {template}')
        
    else:
        old_ipsec=Function.get_tunnel(standar_tunnel,location_t,template)
        tunnel_body=old_ipsec['result']['entry'][0]
        ip_crypto_p=tunnel_body['auto-key']['ipsec-crypto-profile']
        del tunnel_body['@location']
        del tunnel_body['@template']
        del tunnel_body['tunnel-monitor']
        tunnel_body['@name']=new_tunnel
        tunnel_body['auto-key']['ike-gateway']['entry'][0]['@name']=new_tunnel
        #work with ike gw
        old_ike_gw=Function.get_ike_gw(standar_tunnel,location_t,template)
        ike_body=old_ike_gw['result']['entry'][0]
        if '@location' in ike_body: del ike_body['@location']
        if '@template' in ike_body: del ike_body['@template']
        ike_body['@name']=new_tunnel
        ike_body['local-id']['id']=new_id
        ike_body['peer-id']['id']=new_id
        #Add ike gw
        add_ike=Function.add_ike_gw(ike_body,location_t,template)
        print('IKE gateway add respons')
        p(add_ike)
        create_ipsec=Function.create_ipsec_tunnel(tunnel_body,location_t,template)
        print('IPsec tunnel add respons')
        p(create_ipsec)



def create_prisma_rn(data,info):
    #ip=info['subnet']
    site=info['site']
    city=info['city']
    roll=['Pri','Sec']
    function=info['function']
    pri_tunnel=f'{function}-{site}-{city}_{roll[0]}'
    sec_tunnel=f'{function}-{site}-{city}_{roll[1]}'
    rn_name=f'{function}-{site}-{city}'
    rn_data=data['response']['result']['entry']
    address=menandmice.get_ip()
    #change the name valute to the new RN
    del rn_data['@name']
    del rn_data['@id']
    rn_data['bgp-peer']['peer-ip-address']=address[2]
    rn_data['bgp-peer']['local-ip-address']=address[3]
    rn_data['ipsec-tunnel']=pri_tunnel
    rn_data['protocol']['bgp']['peer-ip-address']=address[0]
    rn_data['protocol']['bgp']['local-ip-address']=address[1]
    rn_data['region']=info['region']
    rn_data['secondary-ipsec-tunnel']=sec_tunnel
    rn_data['spn-name']=info['spn']
    xpath_post=f"/config/devices/entry[@name='localhost.localdomain']/plugins/cloud_services/multi-tenant/tenants/entry[@name='eNET']/remote-networks/onboarding/entry[@name='{rn_name}']"
    xml_data = dict2xml(rn_data)
    element_value=xml_data
    fw_post=f'https://panorama.ngninfra.net/api/?type=config&action=set&xpath={xpath_post}&element={element_value}'
    create_rn=requests.post(fw_post,verify=False, headers=headers)
    p(create_rn.content)
    
    data=xmltodict.parse(create_rn.content)
    
    if data['response']['@status']=='success':
        #add the subnet to mictro
        ip_pri=address[0]+'/31'
        ip_sec=address[2]+'/31'
        check_pri=menandmice.check_ip(ip_pri)
        if 'error' in check_pri:
            add_pri_address = menandmice.add_ip(ip_pri,pri_tunnel)
            p(add_pri_address)
        else:
            print('Subnet alraedy exists in Men&Mice')
            p(check_pri)
            
        check_sec=menandmice.check_ip(ip_sec)
        if 'error' in check_sec:
            add_sec_address = menandmice.add_ip(ip_sec,sec_tunnel)
            p(add_sec_address)
        else:
            print('Subnet alraedy exists in Men&Mice')
            p(check_sec)    

    # uppdate the exel file
    for i in range (len(roll)):   
        if roll[i]=='Pri':
            new_id=f'{site}-{roll[i]}@essity.com' 
            new_row=['NEW' , ' ',site, city, info['region'], roll[i],
                    info['prisma-ip'], new_id, ip_pri,
                    address[0], address[1], '65525', address[1],
                    '64998', address[0]] 
            add_to_exel(new_row)
        else:
            new_id=f'{site}-{roll[i]}@essity.com' 
            new_row=['NEW' ,' ', site, city, info['region'], roll[i],
                     info['prisma-ip'], new_id, ip_sec,
                    address[2], address[3], '65525', address[3],
                    '64998', address[2] ]
            add_to_exel(new_row)
    
        
def add_to_exel(new_row):
    file_name='File\Prisma eNet Remote Networks details.xlsx'
    sheet = "Config eNet"
    wb=load_workbook(file_name)
    ws=wb[sheet]

    ws.append(new_row)
    wb.save(file_name)
    p('Added to Exel file')
