import random


n=random.randint(5,10)
chr_list=[]
for i in range(ord('A'),ord('Z')+1):
    char=chr(i)
    chr_list.append(char)


if n%2!=0:
    for i in range(n):
        m=i
        if(i>((n+1)/2)-1):
            m=n-1-i
        for j in range(int((n+1)/2-m-1)):
            print(" ",end="")
        for j in range(m*2+1):
            print(chr_list[i],end="")
        print("\n")
if n%2==0:
    for i in range(n):
        m=i
        if(i>(n/2)):
            m=n-1-i
        for j in range(int((n)/2-m-1)):
            print(" ",end="")
        if m==n/2:
            m-=1
        for j in range(m*2+1):
            print(chr_list[i],end="")
        print("\n")
