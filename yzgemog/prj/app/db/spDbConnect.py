#coding:utf-8
import pnosql,psql

# def uploadSpgood(id,barcode,comp,depart,spinfo,height,operator,spcode,spformat,thickness,spname,upload ,width):
#     return pnosql.conn.updatespgood(spinfo)

def getSpinfo(item,value,depart,comp):
    result = pnosql.conn.getthespgood({item: value, "depart":depart, "comp": comp})
    if result:
        return result
    else:
        return False


# def getDepartidBySearch(depart,comp):
#     departFatherid = psql.con.runquery('select "departFather_id" from auth_department where id =%s and company_id=%s' % (depart, comp))
#     if len(departFatherid) == 0 and departFatherid[0][0]==None:
#         return False
#     else:
#         return departFatherid[0][0]


def Search(nextitem, nextvalue, departid, comp, rule):
    if rule == "searchByDepartFather":
        depart = psql.con.runquery('select "departFather_id" from auth_department where id =%s and company_id=%s' % (departid, comp))
        if len(depart) == 0:
            depart = False
        else:
            depart =  depart[0][0]
            if depart:
                depart = str(depart)
        item = nextitem
        value = nextvalue
    return item,value, depart, comp, rule
    # nextitem, nextvalue, nextdepartid, nextcomp, nextrule


def getTopDepart(topDepart,comp):
    isTopDepart = psql.con.runquery('select "departFather_id" from auth_department where id =%s and company_id=%s' % (topDepart, comp))
    if len(isTopDepart):
        isTopDepart = isTopDepart[0][0]
        if isTopDepart:
            return getTopDepart(isTopDepart,comp)
    return str(topDepart)


if __name__ == "__main__":
    topDepart = getTopDepart(11,2)
    print topDepart
#     print getSpinfo("spcode","222222",103,2)


# if __name__ == "__main__":
#     print getDepartidBySearch(108,2)
#     print getDepartidBySearch(109, 2)
#     print getSpinfo("spcode","222222",103,2