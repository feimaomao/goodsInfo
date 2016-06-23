# -*- coding: utf-8 -*-

from flask import Flask,request

app = Flask(__name__)

from sp.sp import sp
from cabinet.cabinet import cabinet
from lzhj.lzhj import lzhj
from tk.tk import tk
import requests

app.register_blueprint(sp, url_prefix='/gemo')
app.register_blueprint(cabinet, url_prefix='/gemo')
app.register_blueprint(lzhj, url_prefix='/gemo')
app.register_blueprint(tk, url_prefix='/gemo')


if __name__ == '__main__':
    app.run(debug=True, port=5002)

