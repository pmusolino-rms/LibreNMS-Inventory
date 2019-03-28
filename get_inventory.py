#!/usr/bin/env python

import requests
import os
import json
import sys
import csv
import pandas
import datetime
import bs4
from IPython.core.display import display, HTML
from pivottablejs import pivot_ui
from pprint import pprint
from secrets import token

API_HOST="librenms-api.example.com"
API_ROOT="/api"
API_VERSION="/v0"
API_URI="https://" + API_HOST + API_ROOT + API_VERSION
CA_BUNDLE='./bundle.trust.crt'
CSV_FILE='/tmp/dev.csv'
DATE = datetime.datetime.now()
HTML_FILE='/opt/librenms/html/device_inventory.html'
NMS_DEVICE_URL=API_HOST + "/device/device="
RANCID="rancid-host.example.com/repo/src/master/configs/"
if __name__ == '__main__':
    devices_list = []
    device_dict = {}
    headers = { 
        'X-Auth-Token': token
        }
    devices_uri=API_URI + "/devices"
    r = requests.get(devices_uri, headers=headers,verify=False)
    if (r.ok):
        json_device_list = r.json()
    else:
        print("Unable to fetch data")
        sys.exit(1)

    for i in json_device_list['devices']:
        device_dict['sysName'] = i['sysName']
        device_dict['ip'] = i['ip']
        device_dict['sysDescr'] = i['sysDescr']
        device_dict['os'] = i['os']
        device_dict['version'] = i['version']
        device_dict['location'] = i['location']
        device_dict['hardware'] = i['hardware']
        device_dict['hostname'] = i['hostname']
        device_dict['features'] = i['features']
        device_dict['serial'] = i['serial']
        device_dict['nms'] = "https://" + NMS_DEVICE_URL + str(i['device_id'])
        device_dict['rancid'] = "http://" + RANCID + i['hostname']
        devices_list.append(dict(device_dict))

with open(CSV_FILE, 'w') as csvfile:
    writer = csv.DictWriter(csvfile,delimiter=',',fieldnames=devices_list[0].keys())
    writer.writeheader()
    writer.writerows(devices_list)

df = pandas.read_csv(CSV_FILE)
pivot_ui(df,outfile_path=HTML_FILE,rows=['sysName','hostname','ip','hardware','os','version','features','serial','location','nms','rancid'])
with open(HTML_FILE) as myfile:
        txt = myfile.read()
            soup = bs4.BeautifulSoup(txt, features="html.parser")

            soup.head.append("Last Edit: " + DATE.strftime("%Y-%m-%d %H:%M"))
            with open(HTML_FILE, "w") as outfile:
                    outfile.write(str(soup))
