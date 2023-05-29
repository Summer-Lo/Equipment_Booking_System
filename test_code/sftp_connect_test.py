import pysftp

#sftp server info
sHostName = '158.132.153.195'		
sUserName = 'pad'
sPassWord = '42004200'			
sPort = 22
cnopts = pysftp.CnOpts()
cnopts.hostkeys = None 
connect = False

with pysftp.Connection(host=sHostName,username=sUserName,password=sPassWord,port=sPort,cnopts=cnopts) as sftp:
    connect = True

if connect:
    print("sftp connection ok!")
else:
    print("sftp connection failed!")
