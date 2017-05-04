#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
import json
import sys

def get_data(file_name):
  data={}
  data["type"]="FeatureCollection"
  data["features"]=[]
  f=open(file_name,"r")
  for line in f.readlines():
#    print("line=",line)
    param=line.split("|")
    cad_num=param[0].strip()
    district=param[1].strip()
    lon=param[2].strip()
    lat=param[3].strip()
    if lat == "" or lon == "":
      continue

#   print("param=",param)
    item={}
    item["type"]="Feature"
    geometry={}
    geometry["type"]="Point"
    coordinates=[]
    coordinates.append(lon)
    coordinates.append(lat)
    geometry["coordinates"]=coordinates
    item["geometry"]=geometry

    properties={}
    properties["district"]=district
    properties["cad_num"]=cad_num
    item["properties"]=properties

    data["features"].append(item)
  f.close()
  return data

if len(sys.argv) < 2:
	print("Необходим один параметр - имя файла!")
	print("Выход")
	raise SystemExit(1)

#print(sys.argv)

data=get_data(sys.argv[1])

print(json.dumps(data, sort_keys=True,indent=4, separators=(',', ': ')))
