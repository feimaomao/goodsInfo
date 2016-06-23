# -*- coding: utf-8 -*-

import sqlalchemy

import uuid

import pnosql

class Confsql:
    #def __init__(self,mchost="127.0.0.1:11211",sqlstr=""):
    #def __init__(self,mchost="127.0.0.1:11211",sqlstr=""):
    def __init__(self,dbstr="postgresql+psycopg2://postgres:root@localhost:5432/Usermodel"):
        
        self.engine = sqlalchemy.create_engine(dbstr, echo=True)
        self.metadata = sqlalchemy.MetaData()
        self.metadata.bind = self.engine  
        
        
        

    def checkExist(self,sqlstr): #数据库表中是否能查出sqlstr语句
        s = sqlstr
        result = self.engine.execute(sqlstr)
        rows = result.fetchall()        
        result.close()        
        
        
        
        if len(rows)>0:
            return 1
        else:
            return 0
        

    def runquery(self,sqlstr):
        s = sqlstr
        result = self.engine.execute(sqlstr)
        rows = result.fetchall()        
        result.close()        
        
        
        
        
        return rows#!/usr/bin/env python
    
    def runsp(self,sqlstr):        
        s = sqlstr
        result = self.engine.execute(sqlstr)
        rows = result.fetchall()        
        result.close()
        
        result  = []
        for row in rows:
            x = {}
            x["barcode"] = row[0]
            x["spcode"] = row[1]
            x["spname"] = row[2]
            x["spformat"] = row[3]
            x["height"] = row[4]
            x["width"] = row[5]
            x["thickness"] = row[6]
            
            x["comp"] = 'youke'
            x["parentcomp"] = 'yz'
            x["_id"] = str(uuid.uuid1())
            
            result.append(x)
    
        return result
    
    def runhj_kd(self,sqlstr):
        s = sqlstr
        result = self.engine.execute(sqlstr)
        rows = result.fetchall()        
        result.close()
        
        result  = []
        for row in rows:
            x = {}
            x["cabinetcode"] = row[0]
            x["cabinetname"] = row[1]
            x["cabinettype"] = row[2]
            width = row[3]
            x["width"] = width
            x["shelftype"] = row[4].split(",")
            try:
                shelfheight = [int(y) for y in row[5].split(",")]
            except:
                shelfheight = [200 for y in x["shelftype"]]
            shelfwidth = [int(width) for y in x["shelftype"]]
            x["shelfheight"] = shelfheight
            x["shelfwidth"] = shelfwidth
            x["geom"] = zip(shelfwidth, shelfheight)
            
            try:
                x["shelfdepth"] = [int(y) for y in row[6].split(",")]
            except:
                x["shelfdepth"]=[]
                
            x["flag"] = row[7]
            
            x["emptyheight"] = 0
            
            x["comp"] = 'youke'
            x["parentcomp"] = 'yz'
            x["_id"] = str(uuid.uuid1())
            
            result.append(x)
    
        return result
    
    def runlz(self,sqlstr):
        s = sqlstr
        result = self.engine.execute(sqlstr)
        rows = result.fetchall()        
        result.close()
        
        result  = []
        for row in rows:
            x = {}
            x["lzcode"] = row[0]
            x["lzname"] = row[1]
            x["lz_l"] = row[2]
            x["lz_w"] = row[3]
            x["lz_hh"] = row[4]
            x["lz_hl"] = row[5]
            x["lz_hc"] = row[6]
            x["lz_hw"] = row[7]
            x["lz_tl"] = row[8]
            x["lz_dl"] = row[9]
            x["note"] = row[10]
            x["comp"] = 'youke'
            x["parentcomp"] = 'yz'
            x["_id"] = str(uuid.uuid1())
            
            result.append(x)
    
        return result
    
    def runlz1(self,sqlstr):
        s = sqlstr
        result = self.engine.execute(sqlstr)
        rows = result.fetchall()        
        result.close()
        
        result  = []
        for row in rows:
            x = {}
            x["code"] = row[0]
            x["name"] = row[1]
            x["l"] = row[2]
            x["w"] = row[3]
            x["hh"] = row[4]
            x["hl"] = row[5]
            x["hc"] = row[6]
            x["hw"] = row[7]
            x["tl"] = row[8]
            x["dl"] = row[9]
            x["note"] = row[10]
            x["comp"] = 'youke'
            x["parentcomp"] = 'yz'
            x["_id"] = str(uuid.uuid1())
            
            result.append(x)
    
        return result
    
    def runhj(self):
        s = "select hjcode, hjname, lzcode, width from kdhj "
        result = self.engine.execute(s)
        rows = result.fetchall()        
        result.close()
        
        hjdata = []
        
        for row in rows:
            x = {}
            x["_id"] = str(uuid.uuid1())
            x["comp"] = 'yk'
            x["parent"] = 'yz'            
            x["code"] = row[0]
            x["name"] = row[1]
            x["lzcode"] = row[2]
            x["w"] = row[3]
            x["hjcbs"] = []
            ss = "select hjcode, cb_type, cb_hd, cb_sd, cb_jd, cb_hole_x, cb_xc, cb_xh, note from kdcb where hjcode =" + " '" + row[0] + "'"
            result = self.engine.execute(ss)
            lines = result.fetchall()        
            result.close()
            for line in lines:
                y = {}
                y["hjcode"] = line[0]
                y["type"] = line[1]
                y["l"] = line[2]
                y["s"] = line[3]
                y["t"] = line[4]
                y["hole_x"] = line[5]
                y["xc"] = line[6]
                y["xh"] = line[7]
                y["note"] = line[8]
                x["hjcbs"].append(y)
            
            hjdata.append(x)
            
        return hjdata

con = Confsql()

if __name__=='__main__':
    con=Confsql()
    nosqlcon = pnosql.nosql('localhost', 27017, 'goods')
    
    sql="select barcode, spcode, spname, spformat, height, width, thickness from kdsp"
    results = con.runsp(sql)
    nosqlcon.insertspgoods(results)
    
    print "spgoods"
    
    sql = 'select cabinetcode, cabinetname, cabinettype, width, shelftype, shelfheight, shelfdepth, flag from kdcabinet'
    results = con.runhj_kd(sql)    
    nosqlcon.insertcabinets(results)
    
    print "cabinets"
    
    sql = 'select lzcode, lzname, lz_l, lz_w, lz_hh, lz_hl, lz_hc, lz_hw, lz_tl, lz_dl, note from kdlz'
    results = con.runlz1(sql)    
    nosqlcon.insertlz(results)
    
    print "lz"
    
    results = con.runhj()
    nosqlcon.inserthj(results)
    
    
    print 'hj'

