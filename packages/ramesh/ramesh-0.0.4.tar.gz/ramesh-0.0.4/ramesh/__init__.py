import csv
import pickle
import os

def all():
    p=("diamond","ramgenrator","csvhelper","BBF","ramgui","i_sort","b_sort"
       ,"s_sort","b_search","position","mergesort","lineasearch")
    for i in p:
        print(i)
class csvhelper:
    global o,create,show,exit,sum2,delete,append,update,search
    def create():
        with open("B.csv",'w',newline='')as f:
            s=csv.writer(f)
            s.writerow(["names","roll","marks"])
            a=[]
            while True:
                a1=input("enter name:")
                a2=input("enter rollno:")
                a3=input("enter marks:")
                sp=[a1,a2,a3]
                a.append(sp)
                ch=input("do you want to enter more(y/n)")
                if ch=='n'or ch=='N':
                    break
            s.writerows(a)
    o=("""
Type 1 for create
Type 2 for show
Type 3 for exit
Type 4 for count row
Type 5 for search
Type 6 for delete
Type 7 for append on old file
Type 8 for update old content
""")

    def show():
        with open("B.csv",'r')as f:
            a=csv.reader(f)
##        print(f"""names\t rollno   marks""")
            for r in a:
                print(f"{r[0]}    {r[1]}   {r[2]}")
    def sum2():
        with open("B.csv",'r')as f:
            a=csv.reader(f)
            c=0
            for r in a:
                c+=1
            print(c-1)
    def delete():
        h=open("B.csv","r")
        h1=open("temo.csv","w",newline='')
        a=csv.reader(h)
        s=csv.writer(h1)
        found=False
        lo=input("enter roll no to delete:")
        for i in a:
            if i[1]==lo:
                del i[0],i[1]
                found=True
            else:
                s.writerows([i])
        if(found==False):
            print("Roll no not found")
        else:
            print("Deleted sucessfully")
        h.close()
        h1.close()
        os.remove("B.csv")
        os.rename("temo.csv","B.csv")
        h.close()
    def append():
        with open("B.csv",'a',newline='')as f:
            s=csv.writer(f)
##        s.writerow(["names","roll","marks"])
            a=[]
            while True:
                a1=input("enter name:")
                a2=input("enter rollno:")
                a3=input("enter marks:")
                sp=[a1,a2,a3]
                a.append(sp)
                ch=input("do you want to enter more(y/n)")
                if ch=='n'or ch=='N':
                    break
            s.writerows(a)
    def search():
        h=open("B.csv","r")
        a=csv.reader(h)
        found=False
        lo=input("enter roll no to search:")
        for i in a:
            if i[1]==lo:
                print(i[0],'\t',i[2])
                found=True
        if(found==False):
            print("Roll no not found")
        else:
            print("search sucessfully")
        h.close()
    def update():
        h=open('B.csv','r')
        a=csv.reader(h)
        l=[]
        r=input("enter roll no:")
        found=False
        for i in a:
            if i[1]==r:
                found=True
                i[1]=r
                i[0]=input('new name')
                i[2]=input("new marks")
                l.append([i[0],i[1],i[2]])
        h.close()
        if found==False:
            print("student not found")
        else:
            h=open('B.csv','w+',newline='')
            s=csv.writer(h)
            s.writerows(l)
            h.seek(0)
            a=csv.reader(h)
            for i in a:
                print(i)
            h.close()
    def main():
        print(o)
        while True:
            m=int(input("enter task you want to do"))
            if m==1:
                create()
            elif m==2:
                show()
            elif m==3:
                break
            elif m==5:
                search()
            elif m==4:
                sum2()
            elif m==6:
                delete()
            elif m==7:
                append()
            elif m==8:
                update()
            else:
                break        
def show():
     h=open("t.dat","rb+")
     a={}
     print("names\trollno\tmarks")
     while True:
           try:
              a= pickle.load(h)
              print(a['name'],'\t',a['roll'],'\t',a['marks'])
           except EOFError:
              break
    
def create():
    h=open("t.dat","wb")
    b={}
    while True:
         b['name']=input("enter name")
         b['roll']=input("enter rollno")
         b['marks']=input("enter marks")
         pickle.dump(b,h)
         ch=input("want more to enter (y/n)")
         if ch=='n'or ch=='N':
              break
         b={}
    h.close()
def append():
    h=open("t.dat","ab+")
    b={}
    n=int(input("enter no of data you want to add"))
    for i in range(n):
        b['name']=input("enter name")
        b['roll']=input("enter rollno")
        b['marks']=input("enter marks")
        pickle.dump(b,h)
        b={}
    h.close()
def search():
     h=open("t.dat","rb")
     a={}
     found=False
     lo=input("enter roll no to search:")
     try:
          while True:
               a=pickle.load(h)
               if (a['roll']==lo):
                    print(a['name'],'\t',a['marks']) 
                    found=True
     except EOFError:
          if(found==False):
               print("Roll no not found")
          else:
               print("search sucessfully")
          h.close()

     





def delete():
     h=open("t.dat","rb")
     h1=open("tem.dat","wb")
     a={}
     found=False
     lo=input("enter roll no to delete:")
     while True:
           try:
              a=pickle.load(h)
              if lo==a['roll']:
                       found=True
              else:
                   pickle.dump(a,h1)
           except EOFError:
               break
     if found==False:
          print("record not found")
     else:
          print("record found and deleted")
     h.close()
     h1.close()
     os.remove("t.dat")
     os.rename("tem.dat","t.dat")
     h.close()
def update():
     h=open("t.dat","rb+")
     a={}
     found=False
     lo=input("enter roll no to delete:")
     try:
          while True:
               po=h.tell()
               a=pickle.load(h)
               if (a['roll']==lo):
                    a['name']=input("enter new name ")
                    a['marks']=input("enter new marks ")
                    h.seek(po)
                    pickle.dump(a,h)
                    found=True
     except EOFError:
          if(found==False):
               print("Roll no not found")
          else:
               print("update sucessfully")
          h.close()


d=(
"""operation in binary file given by:-\n
Type 1 for create new
Type 2 for show file
Type 3 for append in old file
Type 4 for delete
Type 5 for update records
Type 6 for search
Type 7 for any other number for exit
Type 8 for calculation
""")

def exiti():
     exit()


def calcu():
     print("you can do calculation\nBy enter your operater and opertion")
     a=eval(input("enetr your operator and operation"))
     print(a)

def BBF():
    print(d)
    while True:
        n=int(input("you want to perfrom operation"))
        if n==1:
             create()
        elif n==2:
             show()
        elif n==3:
             append()
        elif n==4:
             delete()
        elif n==7:
             print("Tab on  yes for exit ")
             exiti()
        elif n==5:
             update()
        elif n==6:
             search()
        elif n==8:
             calcu()
               
        else:
            break



    

def diamond(a,v):
    "arg=number of rows and which word"
    for i in range(0,a):
        for j in range(0,a-1-i):
            print(end=" ")
        for s in range(0,i+1):
            print(v,end=" ")
        print()
    for i in range(a-1,0,-1):
        for j in range(a,i,-1):
            print(end=" ")
        for s in range(0,i):
            print(v,end=" ")
        print()
    
def ramgenrator(p,q):
    from random import randint
    p1=list(p)
    m=[]
    while p1:
        c=randint(0,len(p1)-1)
        o=p1[c]
        if o not in m:
            m.append(o)
            if len(m)==q:
                break
    return m
#selection sort
def s_sort(a):
    for i in range(len(a)):
        for j in range(i+1,len(a)):
            if a[i]>a[j]:
                a[i],a[j]=a[j],a[i]
    return a
def i_sort(a):
    v=a[1]
    b=len(a)
    for i in range(b):
        k=a[i]
        j=i-1
        while j>=0 and a[j]>k:
            a[j+1]=a[j]
            j=j-1
        a[j+1]=k
    return a


##binary sort

def b_sort(a):
    x=0
    v=False
    while x<len(a) and v==False:
        v=True
        for j in range(len(a)-1-x):
            if a[j]>a[j+1]:
                a[j],a[j+1]=a[j+1],a[j]
                v=False
        x+=1
    return a


#mergeSort
def mergesort(a,s):
    b=[]
    w=len(a+s)//2+4
    try:
        for i in range(w):
            if a[0]>s[0]:
                b.append(s.pop(0))
            else:
                b.append(a.pop(0))
    except IndexError:
        pass
    b+=a
    b+=s
    return b

def linearsearch(o,p):
    w=0
    b=len(o)
    while w<b:
        m=(w+b)//2
        if o[m]==p:
            return (m+1,True)
        elif o[m]<=p:
            w=m-1
        else:
            b=m+1
            break
    return False

def position(l,b):
    global a
    for i in range(len(l)):
        if l[i]==b:
            print("position",i+1)
            return True
    else:
        return False
def b_search(a,b,c,d):
    if c>=d:
        return False
    m=int((c+d//2))
    if a[m]==b:
        return m
    elif a[m]<b:
        return (b_search(a,b,c+1,d))
    else:
        return (b_search(a,b,c,m-1))
from tkinter import *
import random
def ramgui(text,title,bgi,size,speed,pdx,pdy):
    "arguments = text,title,bgi,size,speed,pdx,pdy"
    global lable,l4,a4
    a4=Tk()
    a4.title("project amul page 37")
    a4.geometry("1024x768")
    a4.configure(bg=bgi)
##    t2=("""Amul is best, Amul is an Indian state gvernment
##    cooperative under the ownership of Gujarat Cooperative
##    Milk Marketing Federation, Ministry of Cooperation,
##    gvernment of Gujarat based at Anand in Gujarat.
##    Formed in 1946, it is a cooperative brand managed
##    (GCMMF), which today is jointly controlled by 46
##    lakh (4.6 million) milk producers in Gujarat
##    and the apex body of 13 district milk unions,
##    spread across 15,000 villages of Gujarat. Amul
##    Give India's White Revolution, which made
##    country the worlds largest producer of milk
##    and milk products and \nTHANKING YOU FOR WATCHING
##        """)#text,title,padd,y-x,size
    
    l4=Label(a4, bg='#ffffff')
    l4.place(x=pdx, y=pdy)
    def lable():
        color = '#'+("%06x" % random.randint(0, 0xFFFFFF))
        l4.config(text=text, bg="black",fg=(color),font=f"lucida {size} bold")
        a4.after(speed, lable)
    lable()
    color = '#'+("%06x" % random.randint(0, 0xFFFFFF))
    f4=Frame(width=300,height=80,borderwidth=12,bg=color)
    Label(f4, text=title,bg="lightgreen",fg="red",
          font="lucida 34 bold",anchor='n').pack()
    f4.pack(side=TOP)
    def o():
        import time
        time.sleep(6)
    Button(a4,text="stop",fg="red",bg="white",font="lucida 13 bold",
            command=o).pack(side=BOTTOM)
    a4.mainloop()
























        
