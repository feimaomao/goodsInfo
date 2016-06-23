# -*- coding: utf-8 -*-

import json, uuid

from flask import Blueprint, request
from flask import render_template

from db import pnosql, imginterface, redissql

cabinet = Blueprint('cabinet', __name__, template_folder='templates', static_url_path='/cabinet/static', static_folder='static')

@cabinet.route("/singlehj")
def singlehj():
    return render_template('cabinet/singlehj.html')


@cabinet.route("/queryhjdata")
def queryhjdata():
    return render_template('cabinet/insult_kdcabinet.html')


@cabinet.route("/getallhjdata", methods=["POST"])
def getallhjdata():
    comp = request.form["comp"]    
    result = pnosql.conn.getallhjdata()    
    
    return json.dumps(result)

@cabinet.route("/getthehjdata", methods=["POST"])
def getthehjdata():
    comp = request.form["comp"]
    item = request.form["item"]
    value = request.form["value"]    
    result = pnosql.conn.getthehjdata({item:value})    
    return json.dumps(result)

@cabinet.route("/delthehjdata", methods=["POST"])
def delthehjdata():
    comp = request.form["comp"]
    item = request.form["item"]
    value = request.form["value"]    
    result = pnosql.conn.delthehjdata({item:value})
    
    if result:
        return "删除数据成功"
    else:
        return "数据库删除数据失败"


@cabinet.route("/setthehjdata", methods=["POST"])
def setthehjdata():
    x = {}
    x["cabinetcode"] = request.form["cabinetcode"]
    x["cabinetname"] = request.form["cabinetname"]
    x["cabinettype"] = request.form["cabinettype"]
    width = request.form["width"]
    x["width"] = int(width)
    x["shelftype"] = request.form["shelftype"].split(",")
    try:
        shelfheight = [int(y) for y in request.form["shelfheight"].split(",")]
    except:
        shelfheight = [200 for y in x["shelftype"]]
    shelfwidth = [int(width) for y in x["shelftype"]]
    x["shelfheight"] = shelfheight
    x["shelfwidth"] = shelfwidth
    x["geom"] = zip(shelfwidth, shelfheight)
    
    try:
        x["shelfdepth"] = [int(y) for y in request.form["shelfdepth"].split(",")]
    except:
        x["shelfdepth"]=[]
        
    x["flag"] = 0    
    x["emptyheight"] = 0
    
    x["comp"] = request.form["comp"]
    x["parentcomp"] = request.form["parentcomp"]
    
    x["_id"] = request.form["hjuuid"]    
    if x["_id"] == '':
        x["_id"] = str(uuid.uuid1())
        
    try:
        result = pnosql.conn.setthehjdata(x)
        x["tag"] = "保存数据成功"
    except:        
        x["tag"] = "保存数据失败"   
    
    return json.dumps(x)

if __name__=='__main__':
    pass

