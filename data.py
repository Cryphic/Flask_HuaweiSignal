#!/usr/bin/python3
from huawei_lte_api.Client import Client
from huawei_lte_api.Connection import Connection
import requests
import json
import re
from datetime import datetime

with Connection('http://admin:{PASSWORD}@192.168.1.1/') as connection:
    client = Client(connection) 
    signal_info = client.device.signal()
    rsrq = re.sub(r'[A-z]', '', signal_info['rsrq'])
    rsrp = re.sub(r'[A-z]', '', signal_info['rsrp'])
    sinr = re.sub(r'[A-z]', '' , signal_info['sinr'])
    data = {'rsrq': rsrq, 'rsrp' : rsrp, 'sinr' : sinr}
    msg = json.dumps(data)
    vastaus = requests.post('http://localhost:5000/lisaadata', data=msg)
    print(msg)


  
