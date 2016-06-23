# -*- coding: utf-8 -*-

import uuid
import json, time

from flask import Blueprint, request
from flask import render_template

from db import pnosql, imginterface, redissql


lzhj = Blueprint('lzhj', __name__, template_folder='templates', static_url_path='/lzhj/static', static_folder='static')


@lzhj.route("/setlz")
def setlz():
    return render_template('lzhj/setlz.html')

@lzhj.route("/getlzinfo", methods=["POST"])
def getlzinfo():
    item = request.form["item"]
    value = request.form["value"]
    comp = request.form["comp"]
    parentcomp = request.form["parentcomp"]    
    result = pnosql.conn.getthelzdata({item:value})
    print str(result)
    if result != None:
        del result["_id"]            #若_id 是mongo给的，不能序列化
        return json.dumps(result)
    else:
        return json.dumps({})

@lzhj.route("/setlzinfo", methods=["POST"])
def setlzinfo():
    lzinfo = json.loads(request.form["lzinfo"])
    comp = request.form["comp"]
    parentcomp = request.form["parentcomp"]
    lzinfo["comp"] = comp
    lzinfo["parentcomp"] = parentcomp
    lzinfo["_id"] = str(uuid.uuid1())
    result = pnosql.conn.setthelzdata(lzinfo)  
    return 'sucesss'


@lzhj.route("/gethj", methods=['POST', 'GET'])
def gethj():    
    hjcode = request.args.get('hjcode', '')    
    return render_template('lzhj/gethj.html', hjcode=hjcode)

@lzhj.route("/sethj")
def sethj():
    return render_template('lzhj/sethj.html')


@lzhj.route("/gethjinfo", methods=["POST"])
def gethjinfo():
    item = request.form["item"]
    value = request.form["value"]
    comp = request.form["comp"]
    parentcomp = request.form["parentcomp"]    
    hjinfo = pnosql.conn.gethjinfo({item:value})
    
    if hjinfo != None :
        lzcode = hjinfo["lzcode"]
        lzinfo = pnosql.conn.getthelzdata({"code":lzcode})       
        hj = {
            "code":hjinfo["code"],
            "name":hjinfo["name"],
            "w"   :hjinfo["w"],
            "lz1" :lzinfo,
            "lz2" :lzinfo,
            "hjcbs":hjinfo["hjcbs"]
        }    
        return json.dumps(hj)    
    else:        
        return "nodata"
    

@lzhj.route("/savehjinfo", methods=["POST"])
def savehjinfo():
    hjinfostr= request.form["hjinfo"]
    hjinfo = json.loads(hjinfostr)
    
    comp = request.form["comp"]
    parentcomp = request.form["parentcomp"]
    hjinfo2 = pnosql.conn.gethjinfo({"code":hjinfo["code"]})
    if hjinfo2 != None:
        _id = hjinfo2["_id"]
    else:
        _id = str(uuid.uuid1())
    pnosql.conn.sethjinfo({"_id":_id,"code":hjinfo["code"], "name":hjinfo["name"], "lzcode":hjinfo["lz1"]["code"], "w":hjinfo["w"], "hjcbs":hjinfo["hjcbs"], 'comp':comp, 'parentcomp':parentcomp})    
    
    savetocabinet(hjinfo)
    return 'sucesss'

def savetocabinet(hjinfo):
    cabinetcode = hjinfo["code"]
    cabinettype = hjinfo["name"]
    width = hjinfo["w"]
    shelftype = []
    shelfheight = []
    shelfdepth = []
    cbs = hjinfo["hjcbs"]
    
    length = len(cbs)
    
    for i in range(0, length):
        shelftype.append(cbs[i]["type"])
        shelfdepth.append(str(cbs[i]["s"]))
        if i == 0 :
            shelfheight.append(str(cbs[i]["xh"]))
        else:
            if (cbs[i]["type"] == "a" or cbs[i]["type"] == "as"):
                shelfheight.append(str(cbs[i]["xh"]))
            else:
                if (cbs[i-1]["type"] == "a" or cbs[i-1]["type"] == "as") :
                    shelfheight.pop()
                    shelfheight.append(str(int(cbs[i-1]["xh"]/2)))
                    shelfheight.append(str(int(cbs[i-1]["xh"]/2)))
                elif (cbs[i-1]["type"] == "b" or cbs[i-1]["type"] == "bs") :
                    shelfheight.append(str(int(cbs[i-1]["xh"])))
                else:
                    shelfheight.append(str(int(hjinfo["lz1"]["l"]/length)))
    
    x = shelfheight.pop()
    shelfheight.append(str(int(x)+200))
    
    result = pnosql.conn.getthehjdata({"cabinetcode":cabinetcode})
    
    thehjdata = {}
    thehjdata["cabinetcode"] = cabinetcode
    thehjdata["cabienttype"] = cabinettype
    thehjdata["width"] = int(width)
    thehjdata["shelftype"] = shelftype
    thehjdata["shelfheight"] = [int(x) for x in shelfheight]
    thehjdata["shelfdepth"] = [int(x) for x in shelfdepth]
    thehjdata["shelfwidth"] = [int(width) for y in shelftype]
    
    thehjdata["geom"] = zip(thehjdata["shelfwidth"], thehjdata["shelfheight"])
    
    if result != None:
        thehjdata["_id"] = result["_id"]
        thehjdata["comp"] = result["comp"]
        thehjdata["parentcomp"] = result["parentcomp"]
        thehjdata["flag"] = 0
        thehjdata["emptyheight"] = 0
    else:
        thehjdata["_id"] = str(uuid.uuid1())
        thehjdata["comp"] = 'yk'
        thehjdata["parentcomp"] = 'yz'
        thehjdata["flag"] = 0
        thehjdata["emptyheight"] = 0
    
    pnosql.conn.setthehjdata(thehjdata)
    

@lzhj.route("/getshelfmax", methods=['POST', 'GET'])   
def getshelfmax():
    hjcode = request.form["cabinetcode"]
    
    data = {}
    #data["shelfmax"] = theFmWebSql.getshelfmax(hjcode)
    data["shelfmax"] = "0"
    
    return json.dumps(data)

@lzhj.route("/gethjimg", methods=["POST"])    
def gethjimg():
    item = request.form["item"]
    value = request.form["value"]
    comp = request.form["comp"]
    parentcomp = request.form["parentcomp"]    
    imgname = yzimg.gethjimg(value)
    
    if imgname != None :
        return imgname 
    else:        
        return "noimg"
