# -*- coding: utf-8 -*-

import json, time

from flask import Blueprint, request
from flask import render_template

from db import pnosql, imginterface, redissql


tk = Blueprint('tk', __name__, template_folder='templates', static_url_path='/tk/static', static_folder='static')

@tk.route("/insertTKs", methods=["POST"])
def insertTKs():
    TKinfolist = json.loads(request.form['TKinfolist'])  
    pnosql.conn.insertTKs(TKinfolist)    
    return json.dumps({'tag':'yes'})

@tk.route("/updateTK", methods=["POST"])
def updateTK():
    key  = json.loads(request.form['key'])
    print str(key)
    setvalue = json.loads(request.form['setvalue'])
    print str(setvalue)
    pnosql.conn.updateTK(key, setvalue)    
    return json.dumps({'tag':'yes'})
@tk.route("/gettheTKdata", methods=["POST"])
def gettheTKdata():
    company = request.form["company"]
    item = request.form["item"]
    value = request.form["value"]
    result = pnosql.conn.gettheTKdata({item:value})    
    return json.dumps(result)