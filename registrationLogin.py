from tkinter import *
import  mysql.connector
import re,time
import registrationapply,rootwindow
from PIL import Image,ImageTk

conn = mysql.connector.connect(host="localhost", user="root", password="root")
'''
if (conn):
    print("connection established")
else:
    print("Connection error")
'''
db = conn.cursor(buffered=True)
db.execute("use demoregistration")
def dbconnect():
    dbconn=db
    #db.connect("create database if not exists demoregistration")
    dbconn.execute("use demoregistration")
    dbconn.execute("show tables")
    '''
    # lst=db.fetchall()
    # print(lst)
    for i in db:
        print("tables: " + str(i))
    dbconn.execute('select * from logininfo')
    for j in db:
        print("before insert " + str(j))
    '''
    dbconn.execute("create table if not exists logininfo(userid varchar(100) primary key,password varchar(100),username varchar(30),phone varchar(30))")
    dbconn.execute("select * from logininfo where userid='root'")
    if dbconn.rowcount==0:
        dbconn.execute("insert into logininfo(userid,password) values('root','root')")
    conn.commit()

def main():
    root = Tk()
    window1 = Window1(root,db,conn)

class Window1:
    def __init__(self,root,db,conn):
        self.registerwindow=root
        self.loginwindow=None
        self.db=db
        self.conn=conn
        self.registerwindow.title("Registration For Login")
        self.registerwindow.geometry("450x500+500+100")
        self.registerwindow.configure(borderwidth="10", relief="sunken")
        self.registerwindow.columnconfigure(0, weight=1)
        self.registerwindow.resizable(0,0)

        #-----------------------------------------------#
        self.frame0=Frame(self.registerwindow,padx=0,pady=0)
        self.frame0.grid(row=0,columnspan=2)
        self.frame = Frame(self.registerwindow, pady=0, padx=70)
        self.frame.grid(row=1, sticky="ew")
        self.frame1 = Frame(self.registerwindow, padx=70,pady=0)
        self.frame1.grid(row=2,column=0, sticky="ew")

        self.img1 = Image.open("./logo.jpg")
        self.img1 = self.img1.resize((430, 50), Image.LANCZOS)
        self.img1 = ImageTk.PhotoImage(self.img1)
        self.img = Label(self.frame0, image=self.img1).grid(row=0)
        self.signuplabel = Label(self.frame0, text="SignUp Form",fg="Green",padx=65, pady=10,justify="center",font=('Times New Roman', 20))
        self.signuplabel.grid(row=1)

        self.gmaillabel = Label(self.frame, text="Enter Your Gmail:", padx=10, pady=10,font=('Times New Roman', 12))
        self.gmaillabel.grid(row=0, column=0, sticky="ew")
        self.namelabel = Label(self.frame, text="Enter Your name:", padx=10, pady=10,font=('Times New Roman', 12))
        self.namelabel.grid(row=1, column=0, sticky="ew")
        self.phonelabel = Label(self.frame, text="Enter Your phone:", padx=10, pady=10,font=('Times New Roman', 12))
        self.phonelabel.grid(row=2, column=0, sticky="ew")
        self.passwordlabel = Label(self.frame, text="Password:", padx=10, pady=10,font=('Times New Roman', 12))
        self.passwordlabel.grid(row=3, column=0, sticky="ew")
        self.reenterpasswordlabel = Label(self.frame, text="Re-Enter Password:", padx=10, pady=10,font=('Times New Roman', 12))
        self.reenterpasswordlabel.grid(row=4, column=0,sticky="ew")
        self.errorlabel =Label(self.frame1, text="", padx=0, pady=0, fg="red",font=('Times New Roman', 12))
        self.errorlabel.grid(row=5, column=0, sticky="ew")
        self.gmailentry = Entry(self.frame,font=('Times New Roman', 12))
        self.gmailentry.grid(row=0, column=1, sticky="ew")
        self.nameentry = Entry(self.frame,font=('Times New Roman', 12))
        self.nameentry.grid(row=1, column=1, sticky="ew")
        self.phoneentry = Entry(self.frame,font=('Times New Roman', 12))
        self.phoneentry.grid(row=2, column=1, sticky="ew")
        self.passwordentry =Entry(self.frame, show="*",font=('Times New Roman', 12))
        self.passwordentry.grid(row=3, column=1, sticky="ew")
        self.reenterpasswordentry =Entry(self.frame,font=('Times New Roman', 12))
        self.reenterpasswordentry.grid(row=4, column=1, sticky="ew")
        self.submitregister =Button(self.frame, text="Register", bg="#808080", fg="Black", justify="center", pady=5,padx=20,command=self.submitbutval,font=('Times New Roman', 12))
        self.submitregister.grid(row=5, column=1, sticky="e")
        self.loginbutton=Button(self.frame,text="Go to Login Page",padx=10,pady=5,bg="green",fg="white",command=self.loginwindowshow,font=('Times New Roman', 12))
        self.loginbutton.grid(row=5,column=0,sticky="ew")

        self.registerwindow.mainloop()
        #self.nextbutton=Button(self.registerwindow,text="next",command=self.loginwindowshow).place(x=50,y=20)
    def submitbutval(self):
        self.regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        self.reg = re.compile("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$")
        self.regphone=re.compile(r"([0-9]){10,10}")
        self.regname=re.compile("^[A-Za-z._ ]+$")


        if self.passwordentry.get() == "" or self.reenterpasswordentry.get() == "" or self.gmailentry.get() == "" or self.nameentry.get() == "" or self.phoneentry.get() == "":
            self.errorlabel.config(text="Please enter all fields", font=('Arial', 10))
        elif re.fullmatch(self.regex, self.gmailentry.get()) == None:
            self.errorlabel.config(text="Enter valid email", font=('Arial', 10))
        elif re.fullmatch(self.regname, self.nameentry.get()) == None:
            self.errorlabel.config(text="Name Only Contains Alphabet")
        elif re.fullmatch(self.regphone,self.phoneentry.get()) == None:
            self.errorlabel.config(text="Phone number only Contains numbers and it has 10 digit")
        elif (self.passwordentry.get() != self.reenterpasswordentry.get()):
            self.errorlabel.config(text="Password and Confirm Password must be same", font=('Arial', 7))
        elif re.fullmatch(self.reg, self.passwordentry.get()) == None:
            self.errorlabel.config(text="Password does not meet crieteria", font=('Arial', 8))
        else:
            try:
                self.db.execute("insert into logininfo(userid,password,username,phone) values('" + str(self.gmailentry.get()) + "','" + str(self.passwordentry.get()) + "','"+str(self.nameentry.get())+"','"+self.phoneentry.get()+"')")
                self.conn.commit()
                self.errorlabel.config(text="")
            except mysql.connector.errors.IntegrityError:
                self.errorlabel.config(text="Email already exist")
            else:
                self.loginwindowshow()
            '''
            finally:
                print("this will always Execute")
                self.db.execute('select * from logininfo')
                for j in self.db:
                    print("after insert " + str(j))
            '''


    def loginwindowshow(self):
        if not self.loginwindow:
            #self.registerwindow.withdraw()
            self.loginwindow=Toplevel()
            self.loginwindow.title("Restaurant login")
            self.loginwindow.geometry("450x500+500+100")
            self.loginwindow.resizable(0,0)
            #-------------------------------------------------#
            self.regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
            self.reg = re.compile("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$")
            self.regphone = re.compile(r"([0-9]){10,10}")
            self.regname = re.compile("^[A-Za-z._ ]+$")

            self.img2 = Label(self.loginwindow, image=self.img1).place(x=0,y=0)

            self.registerwindowshowbtn=Button(self.loginwindow,text="Register",fg="white",bg="green",command=self.registerwindowshow,font=('Times New Roman', 12))
            self.registerwindowshowbtn.place(x=40,y=200)
            self.loginlabel=Label(self.loginwindow,text="Login To Your Account",font=('Times New Roman', 20),fg="green").place(x=70,y=65)
            self.loginlabelname=Label(self.loginwindow,text="Enter User Name:",font=('Times New Roman', 10)).place(x=40,y=120)
            self.loginname=Entry(self.loginwindow,width=35,font=('Times New Roman', 10))
            #self.loginname.insert(0,'Enter User Id')
            self.loginname.place(x=155,y=120)
            #self.loginname.bind('<Button-1>',self.clearnametext)
            self.loginlabelpassword=Label(self.loginwindow,text="Enter Password:",font=('Times New Roman', 10)).place(x=40,y=160)
            self.loginpassword=Entry(self.loginwindow,width=35,font=('Times New Roman', 10))
            #self.loginpassword.insert(0,'Enter Password to Login')
            self.loginpassword.place(x=155,y=160)
            #self.loginpassword.bind('<Button-1>',self.clearpasswordtext)

            self.loginerrorlabel=Label(self.loginwindow,fg="red",font=('Times New Roman', 10))
            self.loginerrorlabel.place(x=40,y=250)

            self.submitloginbutton=Button(self.loginwindow,text="Login to your Account",bg="green",fg="white",command=self.loginaccount,font=('Times New Roman', 12))
            self.submitloginbutton.place(x=240,y=200)

            self.loginwindow.mainloop()
            #self.nextbutton = Button(self.loginwindow, text="Back",command=self.registerwindowshow).place(x=50, y=20)
        else:
            #pass
            #self.registerwindow.withdraw()
            self.loginwindow.deiconify()
    def registerwindowshow(self):
        self.loginwindow.withdraw()
        #self.registerwindow.deiconify()

    def loginid(self):
        return self.loginname.get()

    def clearnametext(self,*args):
        self.loginname.delete(0,'end')
    def clearpasswordtext(self,*args):
        self.loginpassword.delete(0,'end')
    def loginaccount(self):
        if self.loginname.get() =="" or self.loginpassword.get() == "" or self.loginname.get() =="Enter User Id" or self.loginpassword.get() == "Enter Password to Login" :
            self.loginerrorlabel.config(text="Enter all Fields")
        else:
            #self.db.execute("select * from logininfo where userid='"+self.loginname.get()+"' and password='"+self.loginpassword.get()+"'")
            self.db.execute("select * from logininfo where userid='"+self.loginname.get()+"'")
            if self.db.rowcount == 0:
                self.loginerrorlabel.config(text="user id not found")
            elif self.db.rowcount != 0:
                #print(self.loginname.get(),self.loginpassword.get())
                self.db.execute("select * from logininfo where userid='" + str(self.loginname.get()) + "' and password='" + str(self.loginpassword.get()) + "'")
                if self.db.rowcount == 0:
                    self.loginerrorlabel.config(text="Enter Credentials Are Not Found")
                    self.forgotbutton = Button(self.loginwindow, text="Forgot Password", bg="red", fg="white",command=self.forgotpaasword,font=('Times New Roman', 12))
                    self.forgotbutton.place(x=240, y=190)
                elif str(self.loginname.get())=="root" and str(self.loginpassword.get())=="root":
                    self.loginwindow.destroy()
                    self.registerwindow.destroy()
                    rootwindow.mainRoot()
                else:
                    #registrationapply.loginid(self.loginname.get())
                    self.loginnameval=self.loginname.get()
                    self.loginwindow.destroy()
                    self.registerwindow.destroy()
                    registrationapply.mainWindow(self.loginnameval)
                    # for i in self.db:
                    #    print("values:"+str(i))
                self.conn.commit()
    def forgotpaasword(self):
        self.loginwindow.withdraw()
        self.forgotpasswordview=Toplevel()
        self.forgotpasswordview.geometry("450x500+500+100")
        self.forgotpasswordview.title("Forgot Password")
        self.forgotpasswordview.resizable(0, 0)

        self.forgotFrame = Frame(self.forgotpasswordview)
        self.forgotFrame.grid(row=0, column=0,pady=0, padx=70)
        self.forgotFrame1 = Frame(self.forgotpasswordview)
        self.forgotFrame1.grid(row=1, column=0,pady=0, padx=70)
        self.gmaillabel = Label(self.forgotFrame, text="Your Gmail:", padx=10, pady=10,font=('Times New Roman', 10))
        self.gmaillabel.grid(row=0, column=0, sticky="ew")
        self.phonelabel = Label(self.forgotFrame, text="Enter Your phone:", padx=10, pady=10,font=('Times New Roman', 10))
        self.phonelabel.grid(row=1, column=0, sticky="ew")
        self.getotp = Button(self.forgotFrame, text="Get Otp",command=self.getotp,font=('Times New Roman', 10))
        self.getotp.grid(row=2, column=1,sticky="e")

        self.gmailentry = Entry(self.forgotFrame,font=('Times New Roman', 10))
        self.gmailentry.insert(END,self.loginname.get())
        self.gmailentry.config(state="disabled")
        self.gmailentry.grid(row=0, column=1, sticky="ew")
        self.phoneentry = Entry(self.forgotFrame,font=('Times New Roman', 10))
        self.phoneentry.grid(row=1, column=1, sticky="ew")
        self.errorlabel=Label(self.forgotFrame1,fg="red",anchor="w",font=('Times New Roman', 10))
        self.errorlabel.grid(row=0,column=0,sticky="ew")
        self.forgotpasswordview.mainloop()
    def getotp(self):
        self.db.execute("select * from logininfo where userid='"+self.gmailentry.get()+"'")
        lst=db.fetchall()
        #print("loginid",lst[0][0])
        if self.phoneentry.get()=="":
            self.errorlabel.config(text="Input all Fields")
        elif re.fullmatch(self.regphone, self.phoneentry.get()) == None:
            self.errorlabel.config(text="Phone Number only contains letters and 10 Digits")
        else:
            if lst[0][3]==self.phoneentry.get():
                self.errorlabel.config(text="")
                self.otpentry = Entry(self.forgotFrame,width=15,font=('Times New Roman', 10))
                self.otpentry.grid(row=2, column=0,padx=20, sticky="ew")
                self.otpentry.insert(END,"Enter OTP")
                self.otpentry.bind('<Button>',self.cleartext)
                self.forgotFrame.bind('<Button>',self.addtext)
                self.getotp.config(text="Submit",command=self.submitotp)
            else:
                self.errorlabel.config(text="Entered phone numbered is not in the database")
    def cleartext(self,event):
        if self.otpentry.get()=="Enter OTP":
            self.otpentry.delete(0, 'end')
    def addtext(self,event):
        if self.otpentry.get()=="":
            self.otpentry.insert(END, 'Enter OTP')
        if self.repasswordentry.get()=="":
            self.repasswordentry.insert(END, 'Re-Enter Password')
        if self.passwordentry.get() == "":
            self.passwordentry.insert(END, 'Enter Password')
    def submitotp(self):
        if self.otpentry.get()=="782946":
            self.errorlabel.config(text="")
            self.passwordentry = Entry(self.forgotFrame, width=15,font=('Times New Roman', 10))
            self.passwordentry.grid(row=3, column=0, sticky="ew",columnspan=2,padx=20,pady=5)
            self.passwordentry.insert(END,"Enter Password")
            self.passwordentry.bind('<Button>', self.clearpasswordtext)
            self.repasswordentry = Entry(self.forgotFrame, width=15,font=('Times New Roman', 10))
            self.repasswordentry.grid(row=4, column=0, pady=5,padx=20 ,sticky="ew",columnspan=2)
            self.repasswordentry.insert(END, "Re-Enter Password")
            self.repasswordentry.bind('<Button>', self.clearrepasswordtext)
            self.updatepasswordbtn=Button(self.forgotFrame,font=('Times New Roman', 10),text="Update Password",bg="green",fg="white",command=self.updatepassword)
            self.updatepasswordbtn.grid(row=5,column=1,sticky="ew")
        else:
            self.errorlabel.config(text="Entered OTP Is Wrong")

    def clearpasswordtext(self,event):
        if self.passwordentry.get()=="Enter Password":
            self.passwordentry.delete(0, 'end')
        if self.repasswordentry.get()=="":
            self.repasswordentry.insert(END, 'Re-Enter Password')
    def clearrepasswordtext(self,event):
        if self.repasswordentry.get()=="Re-Enter Password":
            self.repasswordentry.delete(0, 'end')
        if self.passwordentry.get()=="":
            self.passwordentry.insert(END, 'Enter Password')
    def updatepassword(self):
        #print("update password called")
        if self.passwordentry.get()=="" and self.repasswordentry=="":
            self.errorlabel.config(text="Enter All Fields")
        elif self.passwordentry.get()!=self.repasswordentry.get():
            self.errorlabel.config(text="Password and Confirm Password must be same")
        elif re.fullmatch(self.reg, self.passwordentry.get()) == None:
            self.errorlabel.config(text="Password does not meet crieteria")
        else:
            self.errorlabel.config(text="Password Updated redirecting to Login Page")
            self.db.execute("update logininfo set password='"+str(self.passwordentry.get())+"' where userid='"+self.loginname.get()+"'")
            self.conn.commit();
            time.sleep(3)
            self.loginname.delete(0, 'end')
            self.loginpassword.delete(0, 'end')
            self.loginerrorlabel.config(text="")
            self.forgotbutton.place_forget()
            self.forgotpasswordview.withdraw()
            self.loginwindow.deiconify()

if __name__ == "__main__":
    dbconnect()
    main()
