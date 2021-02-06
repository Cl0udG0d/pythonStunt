import hashlib


'''
testPass(cryptPass)函数
功能:
    传入 cryptPass 待解密密码
    print 破解结果
算法:穷举法
'''
def testPass(cryptPass):
    salt,shadowPass=cryptPass.split('$')[2],cryptPass.split('$')[3]
    dictFile=open('dictionary.txt','r')
    for word in dictFile.readlines():
        word=word.strip()
        # print(word)
        hash=hashlib.sha512(salt.encode('utf-8'))
        hash.update(word.encode('utf-8'))
        # print(hash.hexdigest())
        if shadowPass==hash.hexdigest():
            print("[+] Found Password {}".format(word))
            return
    print("[-] Password Not Found ")
    return


def main():
    passFile=open('passwords.txt')
    for line in passFile.readlines():
        if ":" in line:
            user=line.split(':')[0]
            cryptPass=line.split(':')[1].strip(' ')
            print("[*] Now cracking Password For :{}".format(user))
            testPass(cryptPass)

if __name__ == '__main__':
    main()