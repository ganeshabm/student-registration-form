from tkinter import messagebox
import mysql.connector
from tkinter import *
from PIL import Image,ImageTk
def mainRoot():
    conn = mysql.connector.connect(host="localhost", user="root", password="root")
    '''
    if (conn):
        print("connection established")
    else:
        print("Connection error")
    '''
    db = conn.cursor(buffered=True)
    db.execute("use demoregistration")
    Rootwindow=rootwindow(conn,db)

class rootwindow:
    def __init__(self,conn,db):
        self.db=db
        self.conn=conn
        self.showuser()
    def showuser(self):
        self.root=Tk()
        self.displayuser=self.root
        self.logininfovallabels=['Userid','Password','User Name','Phone',' ']
        self.logininfoval=[]
        self.userid=[]
        self.k=0
        self.displayuser.geometry("550x500+500+100")
        self.img1 = Image.open("./logo.jpg")
        self.img1 = self.img1.resize((550, 50), Image.LANCZOS)
        self.img1 = ImageTk.PhotoImage(self.img1)
        self.img = Label(self.root, image=self.img1).grid(row=0,columnspan=5)
        self.db.execute("select * from logininfo where userid!='root'")
        for i in self.db:
            #print("values:",i)
            self.logininfoval.insert(self.k,i)
            self.k+=1
        for i in range(len(self.logininfovallabels)):
            self.toplabel = Entry(self.root, width=18, fg='blue', bg='yellow',
                                  font=('Times New Roman', 8, 'bold'))
            self.toplabel.grid(row=1, column=i)
            self.toplabel.insert(END, self.logininfovallabels[i])
        #print(len(self.logininfoval))
        total_rows=len(self.logininfoval)
        for i in range(total_rows):
            for j in range(5):
                if j==4:
                    self.userid.insert(i,self.logininfoval[i][0])
                    #print(self.userid)
                    self.e = Button(self.root, text="Delete", fg='blue',font=('Times New Roman', 8),command=lambda:self.deleteuser(self.userid[i]))
                    self.e.grid(row=i + 2, column=j)
                    #self.e.bind('<Button-1>',lambda:self.deleteuser(self.logininfoval[i][0]))

                    #self.e.insert(END,"Delete")
                else:
                    self.e = Entry(self.root, width=17, fg='blue',
                                   font=('Times New Roman', 8))
                    self.e.grid(row=i + 2, column=j)
                    self.e.insert(END,str(self.logininfoval[i][j]))
        self.logininfoval = list()
        self.displayuser.mainloop()

    def deleteuser(self,userid):
        #print("userid:",str(userid))
        self.db.execute("delete from logininfo where userid='"+userid+"'")
        self.db.execute("delete from applicationdetails where loginid='"+userid+"'")
        messagebox.showinfo("Information","'"+userid+"' deleted successfully")
        self.conn.commit()
        self.displayuser.destroy()
        self.showuser()
        #self.displayuser.deiconify()

if __name__=="__main__":
    mainRoot()