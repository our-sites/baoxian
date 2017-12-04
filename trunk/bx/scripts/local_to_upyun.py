#coding:utf-8
# write  by  zhou

import os
import os
import upyun
import time

up = upyun.UpYun('manman-1234', 'mm123456', 'mm123456', timeout=30,
                                        endpoint=upyun.ED_AUTO)
with open("./static/imgs/default-user.png","rb") as f :
    result = up.put("/static/imgs/default-user.png", f.read(), checksum=False)
    print result
