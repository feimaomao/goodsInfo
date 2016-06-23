# -*- coding: utf-8 -*-
from flask import Blueprint, request
from flask import render_template
import uuid
import json
from db.spDbConnect import getSpinfo
from spDepartFatherInfo import getSpinfoBySearch
from db import pnosql
from db import imginterface
import copy
from db.spDbConnect import getTopDepart
from spDepartFatherInfo import setTopDepartSpinfo
import requests
sp = Blueprint('sp', __name__, template_folder='templates', static_url_path='/sp/static', static_folder='static')



#设置商品外形尺寸和图像 保存页面
@sp.route("/singlesp")
def singlesp():
    return render_template('sp/singlesp.html')


#批量上传商品资料页面
@sp.route("/importspinfo")
def importspinfo():
    return render_template('sp/importspinfo.html')


#批量上传商品图片页面
@sp.route("/jfupload")
def jfupload():
    return render_template('sp/jfupload.html')

#获取商品信息
@sp.route("/gettheSpdata", methods=["POST"])
def gettheSpdata():
    item = request.form["item"]
    value = request.form["value"]
    depart = request.cookies.get('depart')
    comp= request.cookies.get('comp')
    result = getSpinfo(item,value,depart,comp)
    #判断图片是否存在，如果不存在，就去查找，然后进行设置
    if not result:
        result = getSpinfoBySearch(item,value,depart,comp,"searchByDepartFather",depart,comp)
    return json.dumps(result)


#上传商品资料
@sp.route("/settheSpdata", methods=["POST"])
def settheSpdata():
    spinfo = {}
    spinfo["depart"] = request.cookies.get('depart')
    spinfo["comp"] = request.cookies.get('comp')
    spinfo["spcode"] = request.form["spcode"]
    spinfo["spname"] = request.form["spname"]
    spinfo["spformat"] = request.form["spformat"]
    spinfo["width"] = int(request.form["spwidth"])
    spinfo["height"] = int(request.form["spheight"])
    spinfo["thickness"] = int(request.form["spthickness"])
    spinfo["barcode"] = request.form["spbar"]
    spinfo["upload"] = 1
    # spinfo["_id"] = request.form["spuuid"]
    # if spinfo["_id"] == '':

        #判断是否是本单位或者是顶级单位   进行修改
    is_spinfo =getSpinfo("spcode", spinfo["spcode"], spinfo["depart"], spinfo["comp"])
    if is_spinfo:
        spinfo["_id"] = is_spinfo["_id"]
        spinfo["operator"] = is_spinfo["operator"]
    else:
        spinfo["_id"] = str(uuid.uuid1())
        spinfo["operator"] = request.cookies.get('depart')  # 当上传了商品图片之后才修改这个
    #判断是否是本单位
    if spinfo["operator"] == spinfo["depart"]:
        spinfo["imgPath"] = imginterface.resizeimg(spinfo["spcode"], spinfo["depart"], spinfo["comp"], spinfo["height"],spinfo["width"], spinfo["thickness"])
    else:
        topDepart = getTopDepart(spinfo["depart"], spinfo["comp"])
        if topDepart == spinfo["depart"]:
            spinfo["imgPath"] = imginterface.resizeimg(spinfo["spcode"], spinfo["operator"], spinfo["comp"],spinfo["height"], spinfo["width"], spinfo["thickness"])

    result = pnosql.conn.updatespgood(spinfo)
    spinfoOriginal = copy.deepcopy(spinfo)
    if result:
        spinfo["tag"] = "上传数据成功"
        topDepartSpinfo = setTopDepartSpinfo(spinfoOriginal, "spcode", spinfo["spcode"], spinfo["depart"],spinfo["comp"])
        #获取顶级单位，顶级单位有没有，没有就上传商品信息，有判断operator是否是本单位之后更新
    else:
        spinfo["tag"] = "上传数据失败"
    return json.dumps(spinfo)


#批量上传商品资料
@sp.route("/setSpdatas", methods=["POST"])
def setSpdatas():
    spdatas = json.loads(request.form["spdatas"])
    depart = request.cookies.get('depart')
    comp= request.cookies.get('comp')
    upload = 1
    spformat = ""
    for spinfo in spdatas:
        #spdatas=[{},{},{}....]
        # spinfo={"width":,"height":,"thickness":,"barcode":,"spcode":,"spname":}
        spinfo["width"] = int(spinfo["width"])
        spinfo["height"] = int(spinfo["height"])
        spinfo["thickness"] = int(spinfo["thickness"])
        spinfo["depart"] =depart
        spinfo["comp"] =comp
        spinfo["upload"] =upload
        spinfo["spformat"] =spformat

        is_spinfo=getSpinfo("spcode",spinfo["spcode"],depart,comp)
        if is_spinfo:
            spinfo["_id"] = is_spinfo["_id"]
            spinfo["operator"] = is_spinfo["operator"]
        else:
            spinfo["_id"] = str(uuid.uuid1())
            spinfo["operator"] = request.cookies.get('depart')  # 当上传了商品图片之后才修改这个
        #判断是否可以修改图片
        if spinfo["operator"] == spinfo["depart"]:
            spinfo["imgPath"] = imginterface.resizeimg(spinfo["spcode"], spinfo["depart"], spinfo["comp"],
                                                       spinfo["height"], spinfo["width"], spinfo["thickness"])
        else:
            topDepart = getTopDepart(spinfo["depart"], spinfo["comp"])
            if topDepart == spinfo["depart"]:
                spinfo["imgPath"] = imginterface.resizeimg(spinfo["spcode"], spinfo["operator"], spinfo["comp"],spinfo["height"], spinfo["width"], spinfo["thickness"])
        result = pnosql.conn.updatespgood(spinfo)
        spinfoOriginal = copy.deepcopy(spinfo)
        if result:
            spinfo["tag"] = "上传数据成功"
            topDepartSpinfo = setTopDepartSpinfo(spinfoOriginal, "spcode", spinfo["spcode"], spinfo["depart"],
                                                 spinfo["comp"])
            # 获取顶级单位，顶级单位有没有，没有就上传商品信息，有判断operator是否是本单位之后更新
        else:
            spinfo["tag"] = "上传数据失败"
    return json.dumps(spdatas)


#上传商品资料，暂时无法使用
@sp.route("/setlan", methods=["POST", "GET"])
def setlan():
    code = request.args.get('code')
    width = request.args.get('width')
    height = request.args.get('height')
    content = request.args.get('content')
    html = render_template('sp/setlan.html', code=code,
                                           width=width,
                                           height=height,
                                           content=content)
    return html


@sp.route("/updateSpinfo", methods=["POST", "GET"])
def updateSpinfo():
    spinfo ={}
    data = json.loads(request.data)
    spinfo["_id"] = data["_id"]
    spinfo["operator"] = data["operator"]
    spinfo["comp"] = data["comp"]
    spinfo["imgPath"] = data["imgPath"]
    print spinfo
    result = pnosql.conn.updateTheSpinfo(spinfo)
    return json.dumps(result)

# {'operator': u'111', 'comp': u'1', '_id': u'2a5ef500-33a7-11e6-8a2c-005056c00008',
#  'imgPath': [{u'0': u'/1/111/upload/0/014059.jpg'}, {u'r': u'/1/111/upload/r/014059.jpg'},
#              {u'c': None}, {u'd': None}, {u'b': None}, {u'imgDir': u'D:/img'}]}