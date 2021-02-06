import zipfile
import optparse
from threading import Thread


def extractFile(zFile,password):
    try:
        # print(password)
        zFile.extractall(pwd=password.encode(encoding='utf-8', errors = 'strict'))
        print("[+] Found password {}".format(password))
    except Exception as e:
        pass

def main():
    parser=optparse.OptionParser("参数说明 -f <压缩包文件名> -d <密码txt文件名>")
    parser.add_option('-f',dest='zname',type='string',help='压缩包文件名')
    parser.add_option('-d',dest='dname',type='string',help='密码文件名')
    (options,args)=parser.parse_args()
    if (options.zname==None) or (options.dname==None):
        print(parser.usage)
        exit(0)
    zname,dname=options.zname,options.dname
    zFile=zipfile.ZipFile(zname)
    passFile=open(dname)
    for line in passFile.readlines():
        password=line.strip()
        t=Thread(target=extractFile,args=(zFile,password))
        t.start()

    return

if __name__ == '__main__':
    main()