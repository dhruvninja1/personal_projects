import math
import random
choose = input("E or D")
msg = input("Enter message: ")
ord1, ord2, ord3, ord4, ord5 = map(int, input("Enter order: ").split())
order = [ord1, ord2, ord3, ord4, ord5]
abc =   "abcdefghijklmnopqrstuvwxyz"
abcCaps = abc.upper()
print(abcCaps)
code = ["QWERTYUIOPASDFGHJKLZXCVBNM", 
        "POIUYTREWQASDFGHJKLMZNXBCV", 
        "LAKSJDHFGQPWOEIRUTYMZNXBCV", 
        "ZXCVBNMLKJHGDFSAQWTERYUPOI", 
        "SADHFGJLKPOQWIREUTYNBVMZCX"]



if choose == "E":
    for x in range(0, 5):
        for y in range(0, 26):
            msg = msg.replace(abc[y], code[order[x]-1][y])
            print(msg)
        msg = msg.lower()
        print(" ")
if choose == "D":
    for x in range(4, -1, -1):
        msg = msg.upper()
        for y in range(0, 26):
            msg = msg.replace(code[order[x]-1][y], abc[y])
            print(msg)
        print(" ")





print(f"Final: {msg}")
     
     
     
     
     


