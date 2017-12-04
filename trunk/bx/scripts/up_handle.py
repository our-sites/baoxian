#coding:utf-8
# write  by  zhou
import urllib2
import json
import urllib
import pyquery
import  MySQLdb

data = '''3558|pro_imgs/perspro_08.jpg
3559|pro_imgs/perspro_04.jpg
3560|pro_imgs/perspro_05.jpg
3561|pro_imgs/1509522180210_20171101155720_盛朗康顺.jpg
3562|pro_imgs/1482317675386000229.jpg
3563|pro_imgs/1493368161878005908.png
3564|pro_imgs/嘉运产品.JPG
3569|pro_imgs/1511031623297561.jpg
3577|pro_imgs/1.png
3578|pro_imgs/011501185nc8.PNG
3579|pro_imgs/27175354k8h4.JPG
3580|pro_imgs/1308081027105790.jpg
3581|pro_imgs/1610311345445001.jpg
3582|pro_imgs/1704171551336501.jpg'''
data = [i.split("|") for i in data.split("\n")]
conn = MySQLdb.connect(host="118.89.220.36", port=3306, user="bx_user",
                       passwd="gc895316", charset="utf8", db="bx_abc")
cursor = conn.cursor()

for pid,img in data :
    img = "/media/" + img
    cursor.execute("update bx_product set img=%s where pid = %s ",(img,int(pid)))
    conn.commit()
    print pid,img







