import  hashlib
##
def sha1(str):
    return  hashlib.sha1(str).hexdigest()