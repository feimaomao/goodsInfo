# -*- coding: utf-8 -*-
import requests, json

def resizeimg(spcode,depart,comp,height,width,thickness):
    p = {"spcode":spcode,"height":height,"width":width,"thickness":thickness}
    cookie = {"depart":str(depart),"comp":str(comp)}
    r = requests.post("http://127.0.0.1:5003/resizeimg", data=p,cookies=cookie)

    result = r.json()
    return result
#   return r.json()

if __name__ == "__main__":
    print resizeimg("21241211",103,2)

