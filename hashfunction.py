import struct

roundConstants = ['428a2f98', '71374491', 'b5c0fbcf', 'e9b5dba5', '3956c25b', '59f111f1', '923f82a4', 'ab1c5ed5','d807aa98', '12835b01', '243185be', '550c7dc3', '72be5d74', '80deb1fe', '9bdc06a7', 'c19bf174','e49b69c1', 'efbe4786', '0fc19dc6', '240ca1cc', '2de92c6f', '4a7484aa', '5cb0a9dc', '76f988da','983e5152', 'a831c66d', 'b00327c8', 'bf597fc7', 'c6e00bf3', 'd5a79147', '06ca6351', '14292967','27b70a85', '2e1b2138', '4d2c6dfc', '53380d13', '650a7354', '766a0abb', '81c2c92e', '92722c85','a2bfe8a1', 'a81a664b', 'c24b8b70', 'c76c51a3', 'd192e819', 'd6990624', 'f40e3585', '106aa070','19a4c116', '1e376c08', '2748774c', '34b0bcb5', '391c0cb3', '4ed8aa4a', '5b9cca4f', '682e6ff3','748f82ee', '78a5636f', '84c87814', '8cc70208', '90befffa', 'a4506ceb', 'bef9a3f7', 'c67178f2']
    
def strToBin(string): #turns string to binary
    binary = ""
    for x in string:
        binary = binary + (format(ord(x), 'b'))
    return binary


def rightRotate(string, num):
    output_list = []
    list1 = list(str(string))
    num = num % len(list1)
    # Will add values from n to the new list
    for item in range(len(list1) - num, len(list1)):
        output_list.append(list1[item])
        
    # n to the end of new list    
    for item in range(0, len(list1) - num): 
        output_list.append(list1[item])

    return "".join(output_list)


def rightShift(string,num):
    for x in range(num):
        string = "0" + string

    string = string[0:32]
    return string


def chunkloop(chunk,hash1,hash2,hash3,hash4,hash5,hash6,hash7,hash8):
    #splits chunk into 16 32 bit segments
    words = []
    for x in range(16):
        words.append(chunk[32*x:32*x+32])

    #add 48 more empty words
    for x in range(48):
        words.append('00000000000000000000000000000000')

    #apply an algorithm to these zeroed words
    for i in range(16,64):
        s0 = int(rightRotate(words[i - 15], 7),2) ^ int(rightRotate(words[i - 15], 18),2) ^ int(rightShift(words[i - 15], 3),2)
        s1 = int(rightRotate(words[i- 2], 17),2) ^ int(rightRotate(words[i- 2],19),2) ^ int(rightShift(words[i- 2],10),2)
        added = int(words[i-16],2) + s0 + int(words[i-7],2) + s1
        stringed = str(bin(added))[2:]
        truncated = stringed[0:32]
        words[i] = truncated

    #Compresion, modifiying a-h
    a = int(hash1,16)
    b = int(hash2,16)
    c = int(hash3,16)
    d = int(hash4,16)
    e = int(hash5,16)
    f = int(hash6,16)
    g = int(hash7,16)
    h = int(hash8,16)
    for i in range(0,64):
        #messes around with values
        s1 = int(str(bin(int(rightRotate(e,6),16) ^ int(rightRotate(e,11),16) ^ int(rightRotate(e,25),16)))[2:34],2)
        temp0 = int(str(e + f)[0:32]) ^ abs(int(str(~e + g)[0:32]))
        temp1 = h + s1 + temp0 + int(roundConstants[i],16) + int(words[i],2)
        s0 = int(rightRotate(a,2),16) ^ int(rightRotate(a,13),16) ^ int(rightRotate(a,22),16)
        major = a + b ^ c + d ^ e + f
        temp2 = int(str(bin(s0 + major))[2:34],2)
        h = g
        g = f
        f = e
        e = d + temp1
        d = c
        c = b
        b = a
        a = int(str(bin(temp1 + temp2))[0:32],2)
    #hex values
    hash1 = '{:x}'.format(int(str(bin(int(hash1,16) + a))[2:34],2))
    hash2 = '{:x}'.format(int(str(bin(int(hash1,16) + b))[2:34],2))
    hash3 = '{:x}'.format(int(str(bin(int(hash1,16) + c))[2:34],2))
    hash4 = '{:x}'.format(int(str(bin(int(hash1,16) + d))[2:34],2))
    hash5 = '{:x}'.format(int(str(bin(int(hash1,16) + e))[2:34],2))
    hash6 = '{:x}'.format(int(str(bin(int(hash1,16) + f))[2:34],2))
    hash7 = '{:x}'.format(int(str(bin(int(hash1,16) + g))[2:34],2))
    hash8 = '{:x}'.format(int(str(bin(int(hash1,16) + h))[2:34],2))
    #returns the hex hash values so they can be used in the next chunckloop
    return [hash1,hash2,hash3,hash4,hash5,hash6,hash7,hash8]

def BHASH68(string):
    #check if string
    if type(string) != str:
        return "please use a string as paramater"

    #Convert string to binary
    binary = strToBin(string)

    #defines
    binlen = len(binary)
    #preset hash values
    hash1 = "6a09e667"
    hash2 = "bb67ae85"
    hash3 = "3c6ef372"
    hash4 = "a54ff53a"
    hash5 = "510e527f"
    hash6 = "9b05688c"
    hash7 = "1f83d9ab"
    hash8 = "5be0cd19"

    
    #append 1
    binary += "1"
    
    #Make a multiple of 512 - 64
    length = len(binary)
    while (length + 64) % 512 != 0:
        binary += "0"
        length = len(binary)
        
    #Big endian
    bigEndianList = (struct.pack('>I', binlen)) #this fuction returns a list
    bigEndianInt = 0
    for x in bigEndianList:
        bigEndianInt += x #so we combine it to a single int
    bigEndianBin = "{0:b}".format(bigEndianInt) #transform it to binary
    bigEndianLen = len(str(bigEndianBin))
    bigEndian = str(bigEndianBin) #then a string
    while bigEndianLen % 64 != 0: #and pad it with 0's untill it is 64 bits
        bigEndian = "0" + bigEndian
        bigEndianLen = len(str(bigEndian))
    binary += bigEndian

    #split up into 512 bit chunks
    chunks = []
    loops = len(binary) // 512
    for x in range(loops):
        chunks.append(binary[512*x:512*x+512])

    #Chunkloop performed on 512 bit increments
    for chunk in chunks:
        newhashes = chunkloop(chunk,hash1,hash2,hash3,hash4,hash5,hash6,hash7,hash8)
        hash1 = newhashes[0]
        hash2 = newhashes[1]
        hash3 = newhashes[2]
        hash4 = newhashes[3]
        hash5 = newhashes[4]
        hash6 = newhashes[5]
        hash7 = newhashes[6]
        hash8 = newhashes[7]
    #return final hash
    return hash1+hash2+hash3+hash4+hash5+hash6+hash7+hash8
    

while True:
    userinput = input("Enter what you want hashed: ")
    print(BHASH68(userinput))
    print("\n\n\n\n\n\n")
