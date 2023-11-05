from tkinter import *
import registrationLogin
from tkinter import filedialog
import  mysql.connector
from PIL import ImageTk, Image
import re
import os
import shutil
from time import *

def mainWindow(param):
    conn = mysql.connector.connect(host="localhost", user="root", password="root")
    '''
    if (conn):
        print("connection established")
    else:
        print("Connection error")
    '''
    db = conn.cursor(buffered=True)
    db.execute("use demoregistration")
    global loginidva
    loginidva = param
    if loginidva!="":
        root=Tk()
        registerapply=Registerapply(root,db,conn)
    else:
        registrationLogin.main()

class Registerapply:
    def __init__(self,root,db,conn):
        self.db=db
        self.conn=conn
        self.root=root
        self.k=0
        self.applicationval=list()
        self.applicationshow=None
        self.addphotopath=None
        self.addsupportedphotopath=None
        self.root.geometry("450x500+500+100")
        self.root.title("Apply For Application")

        #-----------------------------------------
        self.frame2 = Frame(self.root, pady=0, padx=0)
        self.frame2.grid(row=1, sticky="w")
        self.frame3 = Frame(self.root, pady=0, padx=0)
        self.frame3.grid(row=0,columnspan=2)
        self.frame = Frame(self.root, pady=0, padx=70)
        self.frame.grid(row=2, sticky="ew")
        self.frame1 = Frame(self.root,pady=10)
        self.frame1.grid(row=3, column=0, sticky="ew")

        self.img1 = Image.open("./logo.jpg")
        self.img1 = self.img1.resize((450, 50), Image.LANCZOS)
        self.img1 = ImageTk.PhotoImage(self.img1)
        self.img = Label(self.frame3, image=self.img1).grid(row=0)

        self.applicationlabel=Label(self.frame3,text="Application Form",font=('Times New Roman', 20),fg="green")
        self.applicationlabel.grid(row=1)
        self.loginlabel=Label(self.frame2,text="Login ID:",pady=0,padx=0,font=('Times New Roman', 10))
        self.loginlabel.grid(row=0,column=0,sticky="ew")
        self.loginlabelval = Label(self.frame2, text=loginidva,pady=2,fg="red",font=('Times New Roman', 10))
        self.loginlabelval.grid(row=0, column=1, sticky="ew")
        self.namelabel = Label(self.frame, text="Enter Your Name:", padx=10, pady=10,font=('Times New Roman', 10))
        self.namelabel.grid(row=0, column=0, sticky="ew")
        self.agelabel = Label(self.frame, text="Enter Your Age:", padx=10, pady=10,font=('Times New Roman', 10))
        self.agelabel.grid(row=1, column=0, sticky="ew")
        self.phonelabel = Label(self.frame, text="Enter Your phone Number:", padx=10, pady=10,font=('Times New Roman', 10))
        self.phonelabel.grid(row=2, column=0, sticky="ew")
        self.gmaillabel = Label(self.frame, text="Enter Your Gmail:", padx=10, pady=10,font=('Times New Roman', 10))
        self.gmaillabel.grid(row=3, column=0, sticky="ew")
        self.addphotolabel = Label(self.frame, text="Add photo:", padx=10, pady=10,font=('Times New Roman', 10))
        self.addphotolabel.grid(row=4, column=0, sticky="ew")
        self.addsupportingphotolabel = Label(self.frame, text="Add Supporting photo:", padx=10, pady=10,font=('Times New Roman', 10))
        self.addsupportingphotolabel.grid(row=5, column=0, sticky="ew")
        self.errorlabel = Label(self.frame1, text="", padx=0, pady=0, fg="red",font=('Times New Roman', 10))
        self.errorlabel.grid(row=5, column=0, sticky="ew")
        self.nameentry = Entry(self.frame,font=('Times New Roman', 10))
        self.nameentry.grid(row=0, column=1, sticky="ew")
        self.ageentry = Entry(self.frame,font=('Times New Roman', 10))
        self.ageentry.grid(row=1, column=1, sticky="ew")
        self.phoneentry = Entry(self.frame,font=('Times New Roman', 10))
        self.phoneentry.grid(row=2, column=1, sticky="ew")
        self.gmailentry = Entry(self.frame,font=('Times New Roman', 10))
        self.gmailentry.grid(row=3, column=1, sticky="ew")
        self.photolabel=Label(self.frame,font=('Times New Roman', 10))
        self.photolabel.grid(row=4,column=1,sticky="e")
        self.addphoto=Button(self.frame,text="Add photo",command=self.addphoto,font=('Times New Roman', 10))
        self.addphoto.grid(row=4, column=1, sticky="w")
        self.photosupportinglabel=Label(self.frame,font=('Times New Roman', 10))
        self.photosupportinglabel.grid(row=5,column=1,sticky="e")
        self.addsupportingphoto=Button(self.frame,text="Add photo",command=self.addsupportingphotofun,font=('Times New Roman', 10))
        self.addsupportingphoto.grid(row=5, column=1, sticky="w")
        self.submitregister = Button(self.frame, text="Submit",font=('Times New Roman', 10), bg="#808080", fg="Black", justify="center", pady=5,
                                     padx=20,command=self.submitapplication)
        self.submitregister.grid(row=6, column=1, sticky="e")
        self.viewapplibtn = Button(self.frame,font=('Times New Roman', 10), text="View Application", padx=10, pady=5,activebackground="green",bg="green",fg="white",state="active",command=self.showapplication)
        self.viewapplibtn.grid(row=6, column=0, sticky="ew")

        self.db.execute("create table if not exists applicationdetails(name varchar(50),age int,gmail varchar(50),photo varchar(256),supporting_photo varchar(256),application_id int auto_increment primary key,phonenumber varchar(30),loginid varchar(56))")
        self.db.execute("select * from applicationdetails where loginid='"+loginidva+"'")
        '''
        for i in self.db:
            print("val:"+str(i))
        '''
        if self.db.rowcount == 0:
            self.viewapplibtn['state']='disabled'
        else:
            self.submitregister['state'] = 'disabled'
        self.root.mainloop()
    def showapplication(self):
            self.applicationshow=Toplevel()
            self.applicationshow.title(loginidva+" Applications")
            loginidarr=loginidva.split('@')
            loginidval=str(loginidarr[0])
            self.applicationshow.geometry("770x500+350+100")
            self.db.execute("select * from applicationdetails where loginid='"+loginidva+"'")
            for i in self.db:
                self.applicationval.insert(self.k,i)
                self.k+=1
            #print("application values:",self.applicationval)
            total_rows = len(self.applicationval)
            #total_columns = len(self.applicationval[0])
            self.applicationvallabels=['NAME','AGE','GMAIL','PHOTO','S_PHOTO','APP_ID','PH_NO']
            for i in range(len(self.applicationvallabels)):
                self.toplabel=Entry(self.applicationshow, width=18, fg='blue',bg='yellow',
                               font=('Arial', 8, 'bold'))
                self.toplabel.grid(row=0, column=i)
                self.toplabel.insert(END,self.applicationvallabels[i])
            for i in range(total_rows):
                for j in range(7):
                    if(j==3):
                        if not self.applicationval[i][j]=="None":
                            try:
                                self.imagepath1="C:\\Users\\User\\Desktop\\pythonregisterphotos\\"+loginidval+"\\primaryphoto\\"+self.applicationval[i][j]
                                self.img = Image.open(self.imagepath1)
                                self.img = self.img.resize((65, 35), Image.LANCZOS)
                                self.img = ImageTk.PhotoImage(self.img)
                                self.l =Button(self.applicationshow, width=19, image=self.img)
                                self.l.grid(row=i+1, column=j,sticky="ew")
                                self.l.config(image=self.img)
                                #'self.l' + str(i) + ' = ' + str(Label(self.applicationshow, width=19, image=self.img).grid(row=i + 1, column=j, sticky="ew"))
                            except FileNotFoundError:
                                self.e = Entry(self.applicationshow, width=17, fg='blue',
                                               font=('Arial', 8))
                                self.e.grid(row=i + 1, column=j)
                                self.e.insert(END, "Path Not Found")
                        else:
                            self.e = Entry(self.applicationshow, width=17, fg='blue',
                                           font=('Arial', 8))
                            self.e.grid(row=i + 1, column=j)
                            self.e.insert(END, "No Photo")
                    elif(j==4):
                        #print("self.applicationval[i][j]:"+str(self.applicationval[i][j]))
                        if not self.applicationval[i][j] == "None":
                            try:
                                self.imagepath2="C:\\Users\\User\\Desktop\\pythonregisterphotos\\"+loginidval+"\\supportedphoto\\"+self.applicationval[i][j]
                                self.supportinimg = Image.open(self.imagepath2)
                                self.supportinimg = self.supportinimg.resize((65, 35), Image.LANCZOS)
                                self.supportinimg = ImageTk.PhotoImage(self.supportinimg)
                                self.l1=Button(self.applicationshow,width=19,image=self.supportinimg)
                                self.l1.grid(row=i+1, column=j,sticky="ew")
                                self.l1.config(image=self.supportinimg)
                                #'self.l1' + str(i) + ' = ' + str(Label(self.applicationshow, width=19, image=self.supportinimg).grid(row=i + 1, column=j, sticky="ew"))
                            except FileNotFoundError:
                                self.e = Entry(self.applicationshow, width=17, fg='blue',
                                               font=('Arial', 8))
                                self.e.grid(row=i + 1, column=j)
                                self.e.insert(END, "Path Not Found")
                        else:
                            self.e = Entry(self.applicationshow, width=17, fg='blue',
                                           font=('Arial', 8))
                            self.e.grid(row=i + 1, column=j)
                            self.e.insert(END, "No Photo")
                    else:
                        self.e = Entry(self.applicationshow, width=17, fg='blue',
                                       font=('Arial', 8))
                        self.e.grid(row=i+1, column=j)
                        self.e.insert(END, self.applicationval[i][j])
            self.applicationval=list()
            self.applicationshow.mainloop()
    def submitapplication(self):
        #print("submitapplication called")
        self.regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        self.reg = re.compile("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$")
        self.regphone = re.compile(r"([0-9]){10,10}")
        self.regage=re.compile("^[0-9]{1,2}$")
        self.regname = re.compile("^[A-Za-z._ ]+$")
        #print("value1:"+self.nameentry.get() == "" or self.ageentry.get() == "" or self.phoneentry.get() == "" or self.gmailentry.get() == "" or self.addphotopath==None)
        if self.nameentry.get() =="" or self.ageentry.get()=="" or self.phoneentry.get()=="" or self.gmailentry.get()=="" or self.addphotopath==None:
            self.errorlabel.config(text="Please enter all the fields")
        elif re.fullmatch(self.regname, self.nameentry.get()) == None:
            self.errorlabel.config(text="Name Only Contains Alphabet")
        elif re.fullmatch(self.regage, self.ageentry.get()) == None:
            self.errorlabel.config(text="invalid age")
        elif re.fullmatch(self.regphone, self.phoneentry.get()) == None:
            self.errorlabel.config(text="Phone number only Contains numbers and it has 10 digit")
        elif re.fullmatch(self.regex, self.gmailentry.get()) == None:
            self.errorlabel.config(text="Enter valid email", font=('Arial', 10))
        else:
            self.errorlabel.config(text="")
            #print("concatenate:"+str(self.addphotopath)+","+str(self.addsupportedphotopath))
            loginidarr=loginidva.split('@')
            loginidval=str(loginidarr[0])
            #print("loginidval"+str(loginidval))
            path="C:\\Users\\User\\Desktop\\pythonregisterphotos"
            if not os.path.exists(path):
                os.mkdir(path)
            path1="C:\\Users\\User\\Desktop\\pythonregisterphotos\\"+loginidval
            path2="C:\\Users\\User\\Desktop\\pythonregisterphotos\\"+loginidval+"\\primaryphoto"
            path3="C:\\Users\\User\\Desktop\\pythonregisterphotos\\"+loginidval+"\\supportedphoto"
            if not os.path.exists(path1):
                os.mkdir(path1)
            if not os.path.exists(path2):
                os.mkdir(path2)
            if not os.path.exists(path3):
                os.mkdir(path3)
            #print("path:"+self.addphotopath)
            #print("path:"+str(self.addphotopath))
            if not self.addphotopath==None:
                shutil.copy(self.addphotopath,path2)
                self.addphotopatharr=self.addphotopath.split('/')
                self.addphotopath=self.addphotopatharr[-1]
                #print("addphoto:"+str(self.addphotopath))
            if not self.addsupportedphotopath==None:
                shutil.copy(self.addsupportedphotopath,path3)
                self.addsupportedphotopatharr=self.addsupportedphotopath.split('/')
                self.addsupportedphotopath=self.addsupportedphotopatharr[-1]
            self.db.execute("insert into applicationdetails(name,age,phonenumber,gmail,photo,supporting_photo,loginid) values('"+self.nameentry.get()+"','"+self.ageentry.get()+"','"+self.phoneentry.get()+"','"+self.gmailentry.get()+"','"+str(self.addphotopath)+"','"+str(self.addsupportedphotopath)+"','"+loginidva+"')")
            self.errorlabel.config(text="Application submitted")
            self.submitregister['state'] = 'disabled'
            self.viewapplibtn['state'] = 'active'
            self.conn.commit()

    def addphotospath(self):
        filename = filedialog.askopenfilename(title='open')
        #print("filname:" + filename)
        return filename
    def addphotopath1(self):
        filename = filedialog.askopenfilename(title='open')
        #print("filname:" + filename)
        return filename
    def addphoto(self):
        #img=Image.open("D:/Users/Dharuni/Documents/ganeshadocs/2ndsem.JPEG")
        self.addphotopath=self.addphotospath()
        #print("path"+self.addphotopath)
        self.img =Image.open(self.addphotopath)
        self.img = self.img.resize((50, 60), Image.LANCZOS)
        self.img=ImageTk.PhotoImage(self.img)
        self.photolabel.config(image=self.img)

    def addsupportingphotofun(self):
        self.addsupportedphotopath=self.addphotospath()
        #print("path"+self.addsupportedphotopath)
        self.supportinimg =Image.open(self.addsupportedphotopath)
        self.supportinimg = self.supportinimg.resize((50, 60), Image.LANCZOS)
        self.supportinimg=ImageTk.PhotoImage(self.supportinimg)
        self.photosupportinglabel.config(image=self.supportinimg)

if __name__ == '__main__':
    mainWindow("")