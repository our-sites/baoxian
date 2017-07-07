#!/usr/bin/env python
# -*- coding:utf-8 -*
import os
import sys
app_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(app_root, 'lib'))
from bottle import *
import requests
from time import time, sleep
from random import random
import simplejson as json
import urllib
from io import BytesIO
import pyexcel as pe
import unicodecsv as csv
import re
#import sae
import MySQLdb.cursors
import MySQLdb

reload(sys)
sys.setdefaultencoding('utf-8')

app = Bottle()


@app.route('/static/<path:path>')
def server_static(path):
    return static_file(path, root='static')


class QQGroups(object):
    """QQ Groups Spider"""

    def __init__(self):
        super(QQGroups, self).__init__()
        self.session = requests.Session()
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:53.0) Gecko/20100101 Firefox/53.0',
            'Referer': 'http://ui.ptlogin2.qq.com/cgi-bin/login?appid=715030901&daid=73&pt_no_auth=1&s_url=http%3A%2F%2Fqqun.qq.com%2Fgroup%2Findex.html%3Fkeyword%3Dtencent',
        }
        self.session.headers.update(headers)
        self.js_ver = '10196'
        global Mysql_conf, My_cxn, My_cur
        Mysql_conf = {
            'host': '172.16.13.165',
            'user': 'mha_user',
            'passwd': 'gc895316',
            'db': 'bx_caiji',
            'charset': 'utf8',
            'init_command': 'set autocommit=0',
            'cursorclass': MySQLdb.cursors.DictCursor
        }
        My_cxn = MySQLdb.connect(**Mysql_conf)
        My_cur = My_cxn.cursor()

    def getQRCode(self):
        try:
            url = 'http://ui.ptlogin2.qq.com/cgi-bin/login?appid=715030901&daid=73&pt_no_auth=1&s_url=http%3A%2F%2Fqqun.qq.com%2Fgroup%2Findex.html%3Fkeyword%3Dtencent'
            self.session.get(url, timeout=200)
            try:
                pattern = r'ptuiV\("(\d+)"\);'
                self.js_ver = re.search(pattern, resp.content).group(1)
            except:
                pass
            url = 'http://ptlogin2.qq.com/ptqrshow?appid=715030901&e=2&l=M&s=3&d=72&v=4&t=%.17f&daid=73' % (
                random())
            resp = self.session.get(url, timeout=200)
            response.set_header('Content-Type', 'image/png')
            response.add_header('Cache-Control', 'no-cache, no-store')
            response.add_header('Pragma', 'no-cache')
        except:
            resp = None
        return resp

    def qrLogin(self):
        u1 = 'http%3A%2F%2Fqqun.qq.com%2Fgroup%2Findex.html%3Fkeyword%3Dtencent'
        login_sig = self.session.cookies.get_dict().get('pt_login_sig', '')
        qrsig = self.session.cookies.get_dict().get('qrsig', '')
        url = 'http://ptlogin2.qq.com/ptqrlogin?u1=%s&ptqrtoken=%s&ptredirect=1&h=1&t=1&g=1&from_ui=1&ptlang=2052&action=0-0-%d&js_ver=%s&js_type=1&login_sig=%s&pt_uistyle=40&aid=715030901&daid=73&' % (
            u1,
            self.hash33(qrsig),
            time() * 1000,
            self.js_ver,
            login_sig
        )
        try:
            errorMsg = ''
            resp = self.session.get(url, timeout=200)
            result = resp.content
            if '二维码未失效' in result:
                status = 0
            elif '二维码认证中' in result:
                status = 1
            elif '登录成功' in result:
                status = 2
            elif '二维码已失效' in result:
                status = 3
            else:
                status = 4
                errorMsg = str(result.text)
        except:
            status = -1
            try:
                errorMsg = resp.status_code
            except:
                pass
        loginResult = {
            'status': status,
            'time': time(),
            'errorMsg': errorMsg,
        }
        resp = json.dumps(loginResult)
        response.set_header('Content-Type', 'application/json; charset=UTF-8')
        response.add_header('Cache-Control', 'no-cache; must-revalidate')
        response.add_header('Expires', '-1')
        return resp

    def hash33(self, t):
        e = 0
        for i in xrange(0, len(t)):
            e += (e << 5) + ord(t[i])
        t = (e & 2147483647)
        return str(t)

    def genbkn(self, skey):
        b = 5381
        for i in xrange(0, len(skey)):
            b += (b << 5) + ord(skey[i])
        bkn = (b & 2147483647)
        return str(bkn)

    ###将采集到的数据插入数据库###
    def insert_data(self, item, data, My_cxn, My_cur):
        try:
            My_cxn.ping()
        except:
            My_cxn = MySQLdb.connect(**Mysql_conf)
            My_cur = My_cxn.cursor()
        SQL = """INSERT INTO qq_qun_caiji.qq_qun(gc,gname, gmemnum,gowner,gIntro,gClass,gClass2,gClassText,gBitMap,gFlag,gLevel,gMaxMem,gTags,province,province_id,city,city_id,area,area_name)
                                      VALUES(%s,'%s',%s,%s,'%s',%s,'%s','%s',%s,%s,%s,%s,'%s','%s',%s,'%s',%s,'%s','%s')"""
        try:
            My_cur.execute(SQL % (item.get('gc',0), item.get('gName','').strip(), item.get('gMemNum',0), item.get('gOwner',0),item.get('gIntro','').strip(), item.get('gClass',0),
                                  item.get('gClass2','').strip(),item.get('gClassText','').strip(),item.get('gBitMap',0),item.get('gFlag',0),item.get('gLevel',0),item.get('gMaxMem',200),item.get('gTags','').strip(),
                                  data.get('province',''),data.get('province_id',0),data.get('city',''),data.get('city_id',''),data.get('area',''),data.get('area_name','')))
        except Exception,e:
            print e,'~~~~~~~~~'
            return False
        else :
            My_cxn.commit()
            return True

    ###检测QQ群号是否已经采集过,防止重复采集###
    def check_gc(self, gc, My_cxn, My_cur):
        try:
            My_cxn.ping()
        except:
            My_cxn = MySQLdb.connect(**Mysql_conf)
            My_cur = My_cxn.cursor()
        SQL = "SELECT gc FROM qq_qun_caiji.qq_qun WHERE gc=%s"
        My_cur.execute(SQL % gc)
        result = My_cur.fetchall()
        if result:
            return True
        else:
            return False

    ###已采过的小区群进行标记###
    def update_data(self, data, My_cxn, My_cur,m):
        try:
            My_cxn.ping()
        except:
            My_cxn = MySQLdb.connect(**Mysql_conf)
            My_cur = My_cxn.cursor()
        SQL = "UPDATE bx_toubao_caiji SET mark=mark+%d WHERE id=%s"
        My_cur.execute(SQL %(m,data.get('id',0)))
        My_cxn.commit()

    ###获取相关小区对应的QQ群信息###
    def get_data(self,st,pn,kw,skey,data):
        data['area_name'] = str(data['area_name'])
        groups = [(u'群名称', u'群号', u'群人数', u'群主', u'群简介')]
        n = 0
        try:
            for page in xrange(0, pn):
                url = 'http://qqun.qq.com/cgi-bin/qun_search/search_group?k=%s&t=&c=1&p=%s&n=8&st=%s&d=1&r=%.17f&bkn=%s&s=3&v=0' % (
                    urllib.quote(data['area_name']), page, st, random(), self.genbkn(skey)
                )
                resp = self.session.get(url, timeout=200)
                result = resp.json()
                gList = result.get('gList')
                for item in gList:
                    gc = item['gc']
                    if self.check_gc(gc, My_cxn, My_cur):
                        continue
                    if self.insert_data(item, data, My_cxn, My_cur) :
                        n+=1
                sleep(2.5)
        except Exception, e:
            return groups,n
            #if len(groups) == 0:
            #    redirect('/qqun')
        else :
            return groups,n

    def qqunSearch(self, request):
        fromdata=request.forms
        st = fromdata.get('st',4)
        pn = int(fromdata.get('pn', 25))
        ft = fromdata.get('ft', 'xls')
        kw = fromdata.get('kw','').strip()
        skey = self.session.cookies.get_dict().get('skey', '')
        groups = [(u'群名称', u'群号', u'群人数', u'群主', u'群简介')]
        if len(kw) < 15 :
            try:
                My_cxn.ping()
            except:
                My_cxn = MySQLdb.connect(**Mysql_conf)
                My_cur = My_cxn.cursor()
            SQL = "SELECT id,area_name,province,province_id,city,city_id,area FROM bx_caiji.bx_toubao_caiji WHERE mark<3 LIMIT 200"
            My_cur.execute(SQL)
            result = My_cur.fetchall()
            for data in result :
                groups,n = self.get_data(st, pn, kw, skey, data)
                if n :
                    self.update_data(data, My_cxn, My_cur,4)
                else :
                    self.update_data(data, My_cxn, My_cur,1)
                sleep(1.5)

            f = BytesIO()
            if ft == 'xls':
                sheet = pe.Sheet(groups)
                f = sheet.save_to_memory('xls', f)
                response.set_header('Content-Type', 'application/vnd.ms-excel')
                filename = kw.replace(' ', '_') + '.xls'
                response.add_header('Content-Disposition',
                                    'attachment; filename="%s"'%(filename))
                return f.getvalue()
        else :
            print  kw,type(kw)
            data={'area_name':kw}
            groups=self.get_data(st,pn,kw,skey,data)
            f = BytesIO()
            if ft == 'xls':
                sheet = pe.Sheet(groups)
                f = sheet.save_to_memory('xls', f)
                response.set_header('Content-Type', 'application/vnd.ms-excel')
                filename = kw.replace(' ', '_') + '.xls'
                response.add_header('Content-Disposition',
                                    'attachment; filename="%s"'%(filename))
                return f.getvalue()

q = QQGroups()

@app.route('/')
def home():
    redirect('/qqun')

@app.route('/qqun', method='ANY')
@view('qqun')
def qqun():
    if request.method == 'GET':
        response.set_header('Content-Type', 'text/html; charset=UTF-8')
        response.add_header('Cache-Control', 'no-cache')
        return
    elif request.method == 'POST':
        return q.qqunSearch(request)

@app.route('/getqrcode')
def getQRCode():
    return q.getQRCode()

@app.route('/qrlogin')
def qrLogin():
    return q.qrLogin()

### Local ###
run(app, server='paste', host='0.0.0.0', port=8080, debug=True, reloader=True)
#run(app, host='localhost', port=8080, debug=True, reloader=True)

### SAE ###
# debug(True)
#application = sae.create_wsgi_app(app)
