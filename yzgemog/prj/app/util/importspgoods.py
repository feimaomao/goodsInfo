# -*- coding: utf-8 -*-

#D:\fmapp\VCM\data\mongodb\bin>mongoexport -d goods -c spgoods --csv -f spcode,spname,spformat,height,width,thickness,barcode  -o spgoods.data

from pymongo import MongoClient
import uuid, json

import csv

conn = MongoClient(host='localhost', port=27017)
db = conn["goods"]

def upsertspgood(spinfo):           
    db.spgoods.update({"spcode":spinfo["spcode"]}, spinfo, upsert=True)    
    return True
    
def deletespgood(spinfo):
    db.spgoods.remove({"spcode":spinfo["spcode"]})

reader = csv.reader(file('spgoods.data', 'rb'))
i = 0
for line in reader:
    try:                  #去除表头
        spinfo = {}         
        spinfo["_id"] = str(uuid.uuid1())
        spinfo["spcode"] = line[0]
        spinfo["spname"] = line[1]
        spinfo["spformat"] = line[2]
        spinfo["height"] = int(line[3])
        spinfo["width"] = int(line[4])
        spinfo["thickness"] = int(line[5])
        spinfo["barcode"] = line[6]
        i = i + 1
        print i
        deletespgood(spinfo)
        upsertspgood(spinfo)
    except:
        print spinfo["spcode"]