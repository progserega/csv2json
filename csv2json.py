#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
import json
import sys

def grad2dec(grad_min_sec,delim1,delim2,delim3):
  minutes=0
  sec=0
  if len(grad_min_sec.split(delim1)) == 0:
    return 0
  grad_str=grad_min_sec.split(delim1)[0].replace(' ','')
#print("grad_str=%s"%grad_str)
  grad=int(grad_str)

  if len(grad_min_sec.split(delim1)) > 1:
    min_sec=""
    # склеиваем оставшиеся значения массива (актуально, если delim1==delim2==delim3 или как-то ещё)
    min_sec_list=grad_min_sec.split(delim1)[1:]
    for item in min_sec_list:
      min_sec+=item+delim1

    if len(min_sec.split(delim2)) > 0:
      minutes=float(min_sec.split(delim2)[0])

      if len(min_sec.split(delim2)) > 1:
        seconds=""
        seconds_list=min_sec.split(delim2)[1:]
        # склеиваем оставшиеся значения массива (актуально, если delim1==delim2==delim3 или как-то ещё)
        for item in seconds_list:
          seconds+=item+delim2
        if delim3 in seconds:
          sec = float(seconds.split(delim3)[0].replace(' ',''))
        else:
          sec = float(seconds.replace(' ',''))

  dec=grad+minutes/60+sec/3600
  return dec

def get_data(file_name):
  data={}
  data["type"]="FeatureCollection"
  data["features"]=[]
  f=open(file_name,"r")

  item={}
  item["type"]="Feature"
  geometry={}
  geometry["type"]="MultiPolygon"
  coordinates=[]
  latlon=[]
  first_latlon=[]

  for line in f.readlines():
#   print("line=",line)
#   print("len(line)=",len(line))
    if len(line) <= 2:
      continue
    param=line.split("|")
    index_in_poly=param[0].strip('"')
    full_index=param[1].strip('"')
    lat_grad=param[2].strip('"')
    lon_grad=param[3].strip('"')
    if lat_grad == "" or lon_grad == "":
      # закончился полигон:
      # зацикливаем полигон:
      coordinates.append(first_latlon)
      first_latlon=[]
      polygons=[]
      parts=[]
      parts.append(coordinates)
      polygons.append(parts)
      geometry["coordinates"]=polygons
      item["geometry"]=geometry
      properties={}
      properties["district"]="неизвестно"
      properties["cad_num"]="неизвестно"
      item["properties"]=properties
      data["features"].append(item)

      item={}
      item["type"]="Feature"
      geometry={}
      geometry["type"]="MultiPolygon"
      coordinates=[]
      latlon=[]

#return data
      continue

    delim1=u"°"
    delim2=u"'"
    delim3=u"\""

    lat=grad2dec(lat_grad+"\"",delim1,delim2,delim3)
    lon=grad2dec(lon_grad+"\"",delim1,delim2,delim3)

#   print("param=",param)
    latlon=[]
    latlon.append(lon)
    latlon.append(lat)
    if len(coordinates)==0:
      first_latlon.append(lon)
      first_latlon.append(lat)
    coordinates.append(latlon)

  f.close()
  return data

if len(sys.argv) < 2:
	print("Необходим один параметр - имя файла!")
	print("Выход")
	raise SystemExit(1)

#print(sys.argv)

data=get_data(sys.argv[1])

print(json.dumps(data, sort_keys=True,indent=4, separators=(',', ': ')))
