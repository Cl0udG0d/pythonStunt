import hashlib


'''
*Nix 口令破解机
    SHA-512算法
cryptString 为 /etc/shadow文件中的一行待解密字符串
'''

cryptString=":"

'''
testPass(cryptPass)函数
功能:
    传入 cryptPass 待解密密码
    print 破解结果
算法:穷举法
'''
def testPass(cryptPass):
    return

def main():
    test="root"
    print(hashlib.sha512(test.encode("utf-8")).hexdigest())
    user,cryptPass=cryptString.split(":")[0],cryptString.split(":")[1]
    print("[*] Cracking Password For: {}".format(user))
    testPass(cryptPass)
    return

if __name__ == '__main__':
    main()