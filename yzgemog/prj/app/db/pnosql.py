# -*- coding: utf-8 -*-
from pymongo import MongoClient



#conn = Connection(host='localhost', port=27017)
#goods = conn["goods"]
#spgoods = goods["spgoods"]

#连接mongo数据库
class nosql:    
    def __init__(self,host, port, db):#主机地址，端口，数据库名称
        self.conn = MongoClient(host= host, port=port)
        self.db = self.conn[db]#连接指定数据库
        
    def insertspgoods(self, spinfolist):
        #待修改
        self.db.spgoods_4.insert(spinfolist)

     #查询商品资料，x为商品代码，查询指定数据库,spgoods集合，find_one只找头一条数据
     #可以把这个单独写，写的更加复杂
    def getthespgood(self, x):
        #待修改
        print  x["comp"]
        col ="spgoods_"+ x["comp"]
        spdata = self.db[col].find_one(x)
        return spdata
    # 上传商品资料
    def updatespgood(self, spinfo):
        col = "spgoods_"+spinfo["comp"]
        self.db[col].update({"_id": spinfo["_id"]}, spinfo, True)
        return True

    def updateTheSpinfo(self,spinfo):
        col = "spgoods_"+spinfo["comp"]
        self.db[col].update({"_id": spinfo["_id"]},{"$set":spinfo}, True)


    def insertcabinets(self, cabinetinfolist):
        self.db.cabinets.insert(cabinetinfolist)
        
        
    def getthehjdata(self, x):
        hjdata = {}
        
        hjdata["shelfType"] = (['a','a','a','a','a'])
        hjdata["emptyHeight"] = 0
        hjdata["geom"] = [[980,280],[980,230],[980,210],[980,210],[980,210]]
        hjdata["width"] = 980
        
        hjdata = self.db.cabinets.find_one(x)       
        return hjdata
    
    def getallhjdata(self):        
        result = []
        hjdata = self.db.cabinets.find()
        for i in hjdata:
            result.append(i)        
        return result
    
    def setthehjdata(self, hjdata):
        """hjdata:json"""
        _id = hjdata["_id"]        
        self.db.cabinets.update({"_id":_id}, hjdata, True)
        
    def delthehjdata(self, x):
        try:
            self.db.cabinets.remove(x)
            return True
        except:
            return False
        
        
        
    def insertTKs(self, TKinfolist):
        self.db.TKs.insert(TKinfolist)
        
    def updateTK(self, key, setvalue):
        self.db.TKs.update(key, {"$set":setvalue})
        
    def gettheTKdata(self, x):
        TKdata = self.db.TKs.find_one(x)
        return TKdata
    
    def insertlz(self, lzinfolist):
        self.db.lz.insert(lzinfolist)
        
    def getthelzdata(self, x):       
        result = self.db.lz.find_one(x)       
        return result
    
    def setthelzdata(self, lzdata):
        """hjdata:json"""
        code = lzdata["code"]        
        self.db.lz.update({"code":code}, lzdata, True)
        
    def inserthj(self, hjinfolist):
        self.db.hj.insert(hjinfolist)
        
    def gethjinfo(self, x):
        result = self.db.hj.find_one(x)
        return result
    
    def sethjinfo(self, hjinfo):
        _id = hjinfo["_id"]
        self.db.hj.update({"_id":_id}, hjinfo, True)
    
    
conn = nosql('localhost', 27017, 'goods')

if __name__=='__main__':
    nosqlcon = nosql('localhost', 27017, 'goods')
    print str(nosqlcon.getthespgood({"_id":"33bfcfb0-e162-11e3-861e-b888e3dd9ca1"}))
