import Function
import ipsec_fun
import requests
import json
import cred
import csv
import pprint as pp
from dict2xml import dict2xml
import xmltodict

def p(v):
    print('*' * 70, '\n' )
    pp.pprint(v)
    print('\n', '*' * 70)


with open('File\info.csv', newline='') as csvinfo:
    
    reader=csv.DictReader(csvinfo)
    for info in reader:
   
        print(info)
        location_t='template'
        template='Remote_Network_Template'
        standar_tunnel='INET-C3024001-Karachi_Pri'
        old_rn_name='INET-C3024001-Karachi'
        site=info['site']
        city=info['city']
        function=info['function']
        rn_name=f'{function}-{site}-{city}'
        roll=['Pri','Sec']
        
        for i in range (len(roll)):        
            new_id=f'{site}-{roll[i]}@essity.com'
             
            new_tunnel=f'{function}-{site}-{city}_{roll[i]}'
            ipsec_fun.create_prisma_ipsec_tunnel(standar_tunnel,location_t,template,new_tunnel,new_id)
        
        ###check if the rn exist before.
        data=Function.get_rn(rn_name)
        if data['response']['result']==None:
                print ("Remote network doesn't exist, create RN.")
                data=Function.get_rn(old_rn_name)
                a=ipsec_fun.create_prisma_rn(data,info)
                
        else:
            p('RN already exists')
    

