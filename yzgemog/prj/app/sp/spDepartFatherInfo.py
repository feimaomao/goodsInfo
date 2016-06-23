#coding:utf-8
from db.spDbConnect import getSpinfo,Search,getTopDepart
import uuid
from db import pnosql

def getSpinfoBySearch(item,value,departid,comp, rule, origindepart, origincomp):
    nextitem, nextvalue, nextdepartid, nextcomp, nextrule = Search(item, value, departid, comp, rule)
    if nextdepartid:
        spinfo= getSpinfo(nextitem, nextvalue, nextdepartid, nextcomp)
        if spinfo:
            spinfo = copyspinfo(spinfo,origindepart, origincomp)
        else:
            spinfo = getSpinfoBySearch(nextitem, nextvalue, nextdepartid, nextcomp, nextrule,origindepart,origincomp)
        return spinfo
    else:
        return False


def copyspinfo(spinfo,fromdepart, fromcomp):
    spinfo["operator"] = spinfo["depart"]
    spinfo["depart"] = str(fromdepart)
    spinfo["_id"] = str(uuid.uuid1())
    spinfo["upload"] = 0
    spinfo["comp"] = str(fromcomp)
    pnosql.conn.updatespgood(spinfo)
    return spinfo


def setTopDepartSpinfo(spinfo,item,value,depart,comp):
    # spinfo={"depart":,"comp":,"operator":,"upload":,"width":,"height":,"thickness":,"spformat":,"spcode":,"spname":,"barcode":,"_id"}
    topDepart = getTopDepart(depart,comp)
    if topDepart:
        topDepartSpinfo = getSpinfo(item,value,topDepart,comp)
        if not topDepartSpinfo:
            spinfo = copyspinfo(spinfo,topDepart,comp)
            # spinfo ={'depart': , 'spname': u'', 'comp':, 'barcode': u'', 'upload':,'thickness': , 'height': , 'spcode': u'', 'width': , 'operator': '', 'spformat': u'', '_id': ''}
            return spinfo
    return False


if __name__ == "__main__":
    spinfo = {
        "_id": "cbaa37f0-25fe-11e6-85a5-005056c00008",
        "barcode": "6934665087677",
        "comp": "2",
        "depart": "101",
        "height": 233,
        "operator": "101",
        "spcode": "02134141111212",
        "spformat": "",
        "spname": "C活性乳酸菌饮品原味Test",
        "thickness": 80,
        "upload": True,
        "width": 80,
    }
    item = "spcode"
    value = "02134141111212"
    depart = "126"
    comp ="2"
    print 111,getSpinfoBySearch(item,value,"126","2", "searchByDepartFather","126","2")

# if __name__ == "__main__":
#     print getSpinfoBySearch("barcode","6934665087677",126,2,"searchByDepartFather",126,2)
#     print getSpinfoBySearch("spcode","222222",125,2)
