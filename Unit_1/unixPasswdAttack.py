import crypt

'''
UNIX 口令破解机
'''
def testPass(cryptPass):
    salt=cryptPass[0:2]
    dictFile=open('dictionary.txt','r')
    for word in dictFile.readlines():
        word=word.strip('\n')
        cryptWord=crypt.crypt(word,salt)
        print("Now check cryptWord is {}".format(cryptWord))
        if(cryptWord==cryptPass):
            print("[+] Found Password: {} ".format(word))
            return
    print("Sorry,Password not found :(")
    return

def main():
    passFile=open('passwords.txt')
    for line in passFile.readlines():
        if ":" in line:
            user=line.split(':')[0]
            cryptPass=line.split(':')[1].strip(' ')
            print("[*] Cracking Password For: {}".format(user))
            testPass(cryptPass)
    return

if __name__ == '__main__':
    main()