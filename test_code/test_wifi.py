import urllib.request
def connect(host='http://ia.ic.polyu.edu.hk'):
    try:
        urllib.request.urlopen(host) #Python 3.x
        return True
    except:
        return False
# test
if connect():
    print("ok")
else:
    print("fail")