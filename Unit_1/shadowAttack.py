import hashlib,math


def rstr_sha512(text: bytes) -> bytes:
    sha512 = hashlib.sha512()
    sha512.update(text)
    return sha512.digest()

def _extend(source: bytes, size_ref: int) -> bytes :
    extended = b""
    for i in range(math.floor(size_ref/64)):
        extended += source
    extended += source[:size_ref % 64]
    return extended

def _sha512crypt_intermediate(password: bytes,salt: bytes) -> bytes:
    #digest_a = rstr_sha512(password + salt)
    digest_b = rstr_sha512(password + salt + password)
    digest_b_extended = _extend(digest_b,len(password))
    intermediate_input = password + salt + digest_b_extended
    passwd_len = len(password)
    while passwd_len!=0:
        if passwd_len&1 == 1:
            intermediate_input += digest_b
        else:
            intermediate_input += password
        passwd_len >>= 1
    return rstr_sha512(intermediate_input)

def _sha512crypt(password :bytes,salt :bytes,rounds :int) -> bytes:
    digest_a = _sha512crypt_intermediate(password, salt)
    p = _extend(rstr_sha512(password*len(password)),len(password))
    s = _extend(rstr_sha512(salt*(16+digest_a[0])),len(salt))
    digest = digest_a
    for i in range(rounds):
        c_input = b""
        if i&1 :
            c_input += p
        else:
            c_input += digest
        if i % 3:
            c_input += s
        if i % 7:
            c_input += p
        if i & 1:
            c_input += digest
        else:
            c_input += p
        digest = rstr_sha512(c_input)
    return digest

def sha512crypt(password :bytes,salt :bytes, rounds=5000) -> str:
    salt = salt[:16] # max 16 bytes for salt
    input = _sha512crypt(password, salt, rounds)
    tab = "./0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    order = [ 42, 21, 0,  1,  43, 22, 23, 2,  44, 45, 24, 3,
              4,  46, 25, 26, 5,  47, 48, 27, 6, 7,  49, 28,
              29, 8,  50, 51, 30, 9, 10, 52, 31, 32, 11, 53,
              54, 33, 12, 13, 55, 34, 35, 14, 56, 57, 36, 15,
              16, 58, 37, 38, 17, 59, 60, 39, 18, 19, 61, 40,
              41, 20, 62, 63]
    output = ""
    for i in range(0,len(input),3):
        # special case for the end of the input
        if i+1 >= len(order): # i == 63
            char_1 = input[order[i+0]] & 0b00111111
            char_2 = (input[order[i+0]] & 0b11000000) >> 6
            output += tab[char_1] + tab[char_2]
        else:
            char_1 = input[order[i+0]] & 0b00111111
            char_2 = (((input[order[i+0]] & 0b11000000) >> 6) |
                       (input[order[i+1]] & 0b00001111) << 2)
            char_3 = (
                ((input[order[i+1]] & 0b11110000) >> 4) | 
                    (input[order[i+2]] & 0b00000011) << 4)
            char_4 = (input[order[i+2]] & 0b11111100) >> 2
            output += tab[char_1] + tab[char_2] + tab[char_3] + tab[char_4]
    if rounds!=5000:
        return "$6$rounds={}${}${}".format(rounds,salt.decode("utf-8"),output)
    else:
        return "$6${}${}".format(salt.decode("utf-8"),output)

def testPass(cryptPass):
    salt,shadowPass=cryptPass.split('$')[2],cryptPass.split('$')[3]
    dictFile=open('dictionary.txt','r')
    for word in dictFile.readlines():
        word=word.strip()
        # print(word)
        tempPassWord=sha512crypt(bytes(word, encoding = "utf8"), bytes(salt, encoding = "utf8"), 5000)
        # print("temppassword is {}".format(tempPassWord))
        # print("shadowpassword is {}".format(shadowPass))
        if cryptPass==tempPassWord:
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

if __name__ == "__main__":
    #  与crypt.crypt("123456","$6$123456") 运算结果一致
    # print(sha512crypt(b"123",b"DhlRUwqV",5000))
    main()
