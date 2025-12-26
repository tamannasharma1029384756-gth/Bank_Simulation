from tkinter import Tk,Label,Frame,Button,Entry,messagebox,simpledialog,filedialog
            #from pkg tkinter importing entry--->frame window
import time             #import time module
import TableCreator
TableCreator.create()
import sqlite3
import Generator
import Emailhandler
from datetime import datetime
import re 
from PIL import Image,ImageTk
import os

root=Tk()               #this code make top level window
root.state("zoomed")            #to make full screen visibility of window
root.resizable(width=False,height=False)            #disabiling resizable property 
root.configure(bg="powder blue")            #code for setting background color
title=Label(root,text="🤝Welcome to Digital Banking System",
            font=('arial',40,'bold',"underline"),bg="powder blue")  
             #code to make label on root window and making title and formating it 
title.pack()            #packing label to top-center of window

curdate=time.strftime("📅%d-%b-%Y ⏳%r")            #var for current date and time
date=Label(root,text=curdate, 
           font=('arial',20,'bold'),bg="powder blue",fg="navy blue") 
            #code for setting date & time and formating it
date.pack(pady=15)              #packing label to top-center of window and vertical padding with 15pixel

img=Image.open("logo.jfif").resize((150,130))
imgtk=ImageTk.PhotoImage(img,master=root)

lbl_img=Label(root,image=imgtk)
lbl_img.place(relx=0,rely=0)

img2=Image.open("logo2.png").resize((150,130))
imgtk2=ImageTk.PhotoImage(img2,master=root)

lbl_img2=Label(root,image=imgtk2)
lbl_img2.place(relx=0.9,rely=0)


def update_time():                     #update time label to running clock 
    curdate=time.strftime("📅%d-%b-%Y ⏳%r")        #logic to fetch date&time of system 
    date.configure(text=curdate)            #througt text we are showing date&time
    date.after(1000,update_time)            #every 1000mili sec time will update
update_time()           #calling update_time function
def main_screen():
    def newuser_click():
        frm.destroy()             #function destroying the existing frm 
        newuser_screen()      #will call new fun and will b visible on same frm place 


    def existuser_click():
        frm.destroy()             #function destroying the existing frm 
        existuser_screen()          #code of function for exist user screen


    frm=Frame(root,highlightbackground='black',highlightthickness=2)        #created frame and drop it on root window
    frm.configure(bg="pink")                    #configuring frame with backgrnd color-pink
    frm.place(relx=0,rely=.19,relwidth=1,relheight=.73)         #placing the frame by defining relx and rely

    newuser_btn=Button(frm,text="New user \nCreate Account",
                       font=('arial',15,'bold'),
                       fg="black",
                       bg="powder blue",
                       width=14,
                       activebackground="purple",
                       activeforeground="white",
                       command=newuser_click)     
             #new user account creation button code on frame
    newuser_btn.place(relx=.3,rely=.3)                  #placing the button on frame by defining relx and rely

    existuser_btn=Button(frm,text="Existing user \nSign In",
                       font=('arial',15,'bold'),
                       fg="black",
                       bg="powder blue",
                       width=14,
                       activebackground="purple",
                       activeforeground="white",
                       command=existuser_click)   
             #Existing user account sign in button code on frame
    existuser_btn.place(relx=.5,rely=.3)                  #placing the button on frame by defining relx and rely
main_screen()                              #calling main_screen function

def newuser_screen():
    def back():
        frm.destroy()
        main_screen()
    def reset_click():
        e_name.delete(0,"end")
        e_email.delete(0,"end")
        e_mob.delete(0,"end")
        e_adhar.delete(0,"end")
        e_name.focus()

    def createacn_db():
        name=e_name.get()
        email=e_email.get()
        mob=e_mob.get()
        adhar=e_adhar.get()
        if len(name)==0 or len(email)==0 or len(mob)==0 or len(adhar)==0:
            messagebox.showwarning("New user", "Empty fields are not allowed")
            return
        match=re.fullmatch(r"[a-zA-Z0-9_.]+@[a-zA-Z]+\.[a-zA-Z]+",email)
        if match==None:
            messagebox.showwarning("New user", "Invalid Email")
            return

        match=re.fullmatch(r"[6-9][0-9]{9}",mob)
        if match==None:
            messagebox.showwarning("New user", "Invalid Mobile Number")
            return

        match=re.fullmatch(r"^[2-9][0-9]{11}$",adhar)
        if match==None:
            messagebox.showwarning("New user", "Invalid Adhar Number")
            return

        bal=0
        opendate=datetime.now()
        pwd=Generator.generate_pass()
        query='''insert into accounts values(?,?,?,?,?,?,?,?)'''
        conobj=sqlite3.connect(database="mybank.sqlite")
        curobj=conobj.cursor()
        curobj.execute(query,(None,name,pwd,mob,email,adhar,bal,opendate))
        conobj.commit()
        conobj.close()

        
        conobj=sqlite3.connect(database="mybank.sqlite")
        curobj=conobj.cursor()
        query='''select max(acn) from accounts'''
        curobj.execute(query)
        tup=curobj.fetchone()
        conobj.close()
        Emailhandler.send_credentials(email,name,tup[0],pwd)

        messagebox.showinfo("Account creation","Your Account is opened \nwe have mailed your credentials to given email")

    frm=Frame(root,highlightbackground='black',highlightthickness=2)        #created frame and drop it on root window
    frm.configure(bg="pink")                    #configuring frame with backgrnd color-pink
    frm.place(relx=0,rely=.19,relwidth=1,relheight=.73) 

    back_btn=Button(frm,text="Back",bg="powder blue",font=('arial',15,'bold'),bd=5,command=back)   #back button on next screen after clicking newuser_btn
    back_btn.place(relx=0,rely=0)                                #placing the button on frame by defining relx and rely

    lbl_name=Label(frm,text="Name",font=("arial",18,'bold'),width=7,bg='purple',fg='white')  #name label on newuser next screen
    lbl_name.place(relx=.1,rely=.2)                               #placing the button on frame

    e_name=Entry(frm,font=("arial",20,'bold'),bd=5)
    e_name.place(relx=.2,rely=.2)
    e_name.focus()

    lbl_email=Label(frm,text="📧Email",font=("arial",18,'bold'),width=7,bg='purple',fg='white')  #email label on newuser next screen
    lbl_email.place(relx=.1,rely=.3)                             #placing the button on frame

    e_email=Entry(frm,font=("arial",20,'bold'),bd=5)
    e_email.place(relx=.2,rely=.3)

    lbl_mob=Label(frm,text="📱Mob",font=("arial",18,'bold'),width=7,bg='purple',fg='white')  #Mob label on newuser next screen
    lbl_mob.place(relx=.5,rely=.2)                              #placing the button on frame

    e_mob=Entry(frm,font=("arial",20,'bold'),bd=5)
    e_mob.place(relx=.6,rely=.2)                                 #placing the button on frame

    lbl_adhar=Label(frm,text="Adhar",font=("arial",18,'bold'),width=7,bg='purple',fg='white')  #Mob label on newuser next screen
    lbl_adhar.place(relx=.5,rely=.3)                              #placing the button on frame

    e_adhar=Entry(frm,font=("arial",20,'bold'),bd=5)
    e_adhar.place(relx=.6,rely=.3)                                 #placing the button on frame


    submit_btn=Button(frm,text="Submit",bg="powder blue",font=('arial',15,'bold'),bd=5,command=createacn_db)   #back button on next screen after clicking newuser_btn
    submit_btn.place(relx=.4,rely=.45)                                #placing the button on frame by defining relx and rely


    reset_btn=Button(frm,text="Reset",bg="powder blue",font=('arial',15,'bold'),bd=5,command=reset_click)   #back button on next screen after clicking newuser_btn
    reset_btn.place(relx=.5,rely=.45)                                #placing the button on frame by defining relx and rely

def forgot_screen():
    def back():
        frm.destroy()
        existuser_screen()

    def send_otp():
        gen_otp=Generator.generate_otp()
        acn=e_acn.get()
        adhar=e_adhar.get()

        conobj=sqlite3.connect(database="mybank.sqlite")
        curobj=conobj.cursor()
        query='''select name,email,password from accounts where acn=? and adhar=?'''
        curobj.execute(query,(acn,adhar))
        tup=curobj.fetchone()
        conobj.close()
        if tup==None:
            messagebox.showerror("Forgot Password","Record not found")
        else:
            Emailhandler.send_otp(tup[1],tup[0],gen_otp )
            user_otp=simpledialog.askinteger("Password Recovery","Enter OTP")
            if gen_otp==user_otp:
                messagebox.showinfo("Password Recovery","Your Password ={tup[2]}")
            else:
                messagebox.showerror("Password Recovery",'Invalid OTP')

    frm=Frame(root,highlightbackground='black',highlightthickness=2)        #created frame and drop it on root window
    frm.configure(bg="pink")                    #configuring frame with backgrnd color-pink
    frm.place(relx=0,rely=.19,relwidth=1,relheight=.73)
    
    back_btn=Button(frm,text="Back",bg="powder blue",font=('arial',15,'bold'),bd=5,command=back)   #back button on next screen after clicking newuser_btn
    back_btn.place(relx=0,rely=0)                                #placing the button on frame by defining relx and rely

    lbl_acn=Label(frm,text="👤ACN",font=("arial",18,'bold'),width=7,bg='purple',fg='white')  #acn label on existuser next screen
    lbl_acn.place(relx=.3,rely=.2)                               #placing the button on frame

    e_acn=Entry(frm,font=("arial",20,'bold'),bd=5)              #code for creating enter box of acn
    e_acn.place(relx=.4,rely=.2)                                #code for placing the entry box of acn
    e_acn.focus()                                           #focus-cursor for writting will start from here

    lbl_adhar=Label(frm,text="Adhar",font=("arial",18,'bold'),width=7,bg='purple',fg='white')  #pass label on existuser next screen
    lbl_adhar.place(relx=.3,rely=.3)                             #placing the label on frame

    e_adhar=Entry(frm,font=("arial",20,'bold'),bd=5,show='*')                #code for creating enter box of pass
    e_adhar.place(relx=.4,rely=.3)                                   #code for plcing the entry box of pass

    otp_btn=Button(frm,text="Send OTP",width=8,bg="powder blue",font=('arial',15,'bold'),bd=5,command=send_otp)   #submit button on next screen  
    otp_btn.place(relx=.45,rely=.45)                                #placing the button on frame by defining relx and rely

    reset_btn=Button(frm,text="Reset",width=8,bg="powder blue",font=('arial',15,'bold'),bd=5)   #reset password button on next screen 
    reset_btn.place(relx=.55,rely=.45)                                #placing the button on frame by defining relx and rely

def welcome_screen(acn=None):  
    def logout():
        frm.destroy()
        main_screen()
        
    def check_screen():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg="white")                   #configuring frame with backgrnd color-pink
        ifrm.place(relx=.2,rely=.1,relwidth=.7,relheight=.8) 

        title_lbl=Label(ifrm,text='This is Check Details Screen',
                        font=('arial',20,'bold'),bg="white",fg="Red")
        title_lbl.pack()
        conobj=sqlite3.connect(database="mybank.sqlite")
        curobj=conobj.cursor()
        query='''select acn,bal,adhar,email,opndate from accounts where acn=?'''
        curobj.execute(query,(acn,))
        tup=curobj.fetchone()
        conobj.close()
        details=f'''
Account No = {tup[0]}\n
Account Bal = {tup[1]}\n
Account Adhar = {tup[2]}\n
Account Email = {tup[3]}\n
Account Opndate = {tup[4]}\n 
'''

        lbl_details=Label(ifrm,text=details,justify="left",anchor="w",bg='white',fg='Red',font=('arial',17,"bold"))
        lbl_details.place(relx=.05,rely=.15)
    def update_screen():
        def update_db():
            name=e_name.get()
            email=e_email.get()
            mob=e_mob.get()
            pwd=e_pass.get()
            conobj=sqlite3.connect(database="mybank.sqlite")
            curobj=conobj.cursor()
            query='''update accounts set name=?,email=?,mob=?,password=? where acn=?'''
            curobj.execute(query,(name,email,mob,pwd,acn))
            conobj.commit() 
            conobj.close()
            messagebox.showinfo("update screen","Details Updated Successfully")
            welcome_screen(acn)
        
        conobj=sqlite3.connect(database="mybank.sqlite")
        curobj=conobj.cursor()
        query='''select name,email,mob,password from accounts where acn=?'''
        curobj.execute(query,(acn,))
        tup=curobj.fetchone()
        conobj.close()

        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg="white")                   #configuring frame with backgrnd color-pink
        ifrm.place(relx=.2,rely=.1,relwidth=.7,relheight=.8) 

        title_lbl=Label(ifrm,text='This is Update Details Screen',
                        font=('arial',20,'bold'),bg="white",fg="Red")
        title_lbl.pack()

        lbl_name=Label(ifrm,text="Name",font=("arial",15,'bold'),width=7,bg='purple',fg='white')  #name label on newuser next screen
        lbl_name.place(relx=.1,rely=.2)                               #placing the button on frame

        e_name=Entry(ifrm,font=("arial",15,'bold'),bd=5)
        e_name.place(relx=.2,rely=.2)
        e_name.focus()

        lbl_pass=Label(ifrm,text="Pass",font=("arial",15,'bold'),width=7,bg='purple',fg='white')  #email label on newuser next screen
        lbl_pass.place(relx=.1,rely=.3)                             #placing the button on frame

        e_pass=Entry(ifrm,font=("arial",15,'bold'),bd=5)
        e_pass.place(relx=.2,rely=.3)

        lbl_mob=Label(ifrm,text="📱Mob",font=("arial",15,'bold'),width=7,bg='purple',fg='white')  #Mob label on newuser next screen
        lbl_mob.place(relx=.5,rely=.2)                              #placing the button on frame

        e_mob=Entry(ifrm,font=("arial",15,'bold'),bd=5)
        e_mob.place(relx=.6,rely=.2)                                 #placing the button on frame

        lbl_email=Label(ifrm,text="📧Email",font=("arial",15,'bold'),width=7,bg='purple',fg='white')  #Mob label on newuser next screen
        lbl_email.place(relx=.5,rely=.3)                              #placing the button on frame

        e_email=Entry(ifrm,font=("arial",15,'bold'),bd=5)
        e_email.place(relx=.6,rely=.3)                              #placing the button on frame

        e_name.insert(0,tup[0])
        e_mob.insert(0,tup[1])
        e_pass.insert(0,tup[3])
        e_email.insert(0,tup[2])

        submit_btn=Button(ifrm,text="Submit",bg="powder blue",font=('arial',15,'bold'),bd=5,command=update_db)   #back button on next screen after clicking newuser_btn
        submit_btn.place(relx=.4,rely=.45)                                #placing the button on frame by defining relx and rely


    def deposite_screen():
        def deposit_db():
            amt=float(e_amt.get())

            conobj=sqlite3.connect(database="mybank.sqlite")
            curobj=conobj.cursor()
            query='''update accounts set bal=bal+? where acn=?'''
            curobj.execute(query,(amt,acn))
            conobj.commit()
            conobj.close()
            messagebox.showinfo('Deposite screen','Amount Deposited Successfully')
            e_amt.delete(0,"end")
            e_amt.focus()


        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg="white")                   #configuring frame with backgrnd color-pink
        ifrm.place(relx=.2,rely=.1,relwidth=.7,relheight=.8) 

        title_lbl=Label(ifrm,text='This is Deposite Amount Screen',
                        font=('arial',20,'bold'),bg="white",fg="Red")
        title_lbl.pack()

        lbl_amt=Label(ifrm,text="Amount",font=("arial",15,'bold'),width=7,bg='purple',fg='white')  #Mob label on newuser next screen
        lbl_amt.place(relx=.25,rely=.3)                              #placing the button on frame

        e_amt=Entry(ifrm,font=("arial",15,'bold'),bd=5)
        e_amt.place(relx=.4,rely=.3)                              #placing the button on frame

        submit_btn=Button(ifrm,text="Submit",bg="powder blue",font=('arial',15,'bold'),bd=5,command=deposit_db)   #back button on next screen after clicking newuser_btn
        submit_btn.place(relx=.4,rely=.45)                                #placing the button on frame by defining relx and rely


    def withdraw_screen():
        def withdraw_db():
            amt=float(e_amt.get())
            conobj=sqlite3.connect(database="mybank.sqlite")
            curobj=conobj.cursor()
            query='''select bal,email,name from accounts where acn=?'''
            curobj.execute(query,(acn,))
            tup=curobj.fetchone()
            conobj.close()
            
            if tup[0]>amt:
                gen_otp=Generator.generate_otp()
                Emailhandler.send_otp_withdraw(tup[1],tup[2],gen_otp,amt)
                user_otp=simpledialog.askinteger("Withdraw OtP","OTP")
                if gen_otp==user_otp:
                    conobj=sqlite3.connect(database="mybank.sqlite")
                    curobj=conobj.cursor()
                    query='''update accounts set bal=bal-? where acn=?'''
                    curobj.execute(query,(amt,acn))
                    conobj.commit()
                    conobj.close()
                    messagebox.showinfo('Withdraw screen',f'{amt} Amount withdrawn Successfully')
                    e_amt.delete(0,"end")
                    e_amt.focus()
                else:
                    messagebox.showerror("withdraw screen","Invalid OTP")
                    submit_btn.configure(text="resent otp")
            else:
                messagebox.showwarning("withdraw screen",f"Insufficient bal:{tup[0]}")

        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg="white")                   #configuring frame with backgrnd color-pink
        ifrm.place(relx=.2,rely=.1,relwidth=.7,relheight=.8) 

        title_lbl=Label(ifrm,text='This is Withdraw Amount Screen',
                        font=('arial',20,'bold'),bg="white",fg="Red")
        title_lbl.pack()

        lbl_amt=Label(ifrm,text="Amount",font=("arial",15,'bold'),width=7,bg='purple',fg='white')  #Mob label on newuser next screen
        lbl_amt.place(relx=.25,rely=.3)                              #placing the button on frame

        e_amt=Entry(ifrm,font=("arial",15,'bold'),bd=5)
        e_amt.place(relx=.4,rely=.3)                              #placing the button on frame

        submit_btn=Button(ifrm,text="Submit",bg="powder blue",font=('arial',15,'bold'),bd=5,command=withdraw_db)   #back button on next screen after clicking newuser_btn
        submit_btn.place(relx=.4,rely=.45)                                #placing the button on frame by defining relx and rely


    def transfer_screen():
        def transfer_db():
            to_acn=int(e_to.get())
            amt=float(e_amt.get())
            conobj=sqlite3.connect(database="mybank.sqlite")
            curobj=conobj.cursor()
            query='''select * from accounts where acn=?'''
            curobj.execute(query,(to_acn,))
            tup=curobj.fetchone()
            conobj.close()

            if tup==None:
                messagebox.showerror("Transfer screen","Invalid to ACN")
                return

            conobj=sqlite3.connect(database="mybank.sqlite")
            curobj=conobj.cursor()
            query='''select bal,email,name from accounts where acn=?'''
            curobj.execute(query,(acn,))
            tup=curobj.fetchone()
            conobj.close()

            if tup[0]>amt:
                gen_otp=Generator.generate_otp()
                Emailhandler.send_otp_transfer(tup[1],tup[2],gen_otp,amt,to_acn)
                user_otp=simpledialog.askinteger("Transfer OtP","OTP")
                if gen_otp==user_otp:
                    conobj=sqlite3.connect(database="mybank.sqlite")
                    curobj=conobj.cursor()
                    query1='''update accounts set bal=bal-? where acn=?'''
                    query2='''update accounts set bal=bal+? where acn=?'''
                    
                    curobj.execute(query1,(amt,acn))
                    curobj.execute(query2,(amt,to_acn))

                    conobj.commit()
                    conobj.close()
                    messagebox.showinfo('Transfer screen',f'{amt} Amount Tranferred Successfully')
                    e_amt.delete(0,"end")
                    e_amt.focus()
                else:
                    messagebox.showerror("Transfer screen","Invalid OTP")
                    submit_btn.configure(text="resent otp")
            else:
                messagebox.showwarning("Transfer screen",f"Insufficient bal:{tup[0]}")


        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg="white")                   #configuring frame with backgrnd color-pink
        ifrm.place(relx=.2,rely=.1,relwidth=.7,relheight=.8) 

        title_lbl=Label(ifrm,text='This is Transfer Amount Screen',
                        font=('arial',20,'bold'),bg="white",fg="Red")
        title_lbl.pack()

        lbl_to=Label(ifrm,text="To ACN",font=("arial",15,'bold'),width=7,bg='purple',fg='white')  #Mob label on newuser next screen
        lbl_to.place(relx=.25,rely=.2)                              #placing the button on frame

        e_to=Entry(ifrm,font=("arial",15,'bold'),bd=5)
        e_to.place(relx=.4,rely=.2)                              #placing the button on frame
        e_to.focus()

        lbl_amt=Label(ifrm,text="Amount",font=("arial",15,'bold'),width=7,bg='purple',fg='white')  #Mob label on newuser next screen
        lbl_amt.place(relx=.25,rely=.35)                              #placing the button on frame

        e_amt=Entry(ifrm,font=("arial",15,'bold'),bd=5)
        e_amt.place(relx=.4,rely=.35)                              #placing the button on frame

        submit_btn=Button(ifrm,text="Transfer",bg="powder blue",font=('arial',15,'bold'),bd=5,command=transfer_db)   #back button on next screen after clicking newuser_btn
        submit_btn.place(relx=.4,rely=.5)                                #placing the button on frame by defining relx and rely



    conobj=sqlite3.connect(database="mybank.sqlite")
    curobj=conobj.cursor()
    query='''select name from accounts where acn=?'''
    curobj.execute(query,(acn,))
    tup=curobj.fetchone()
    conobj.close()

    frm=Frame(root,highlightbackground='black',highlightthickness=2)        #created frame and drop it on root window
    frm.configure(bg="pink")                    #configuring frame with backgrnd color-pink
    frm.place(relx=0,rely=.19,relwidth=1,relheight=.73) 
    
    logout_btn=Button(frm,text="Logout",bg="powder blue",font=('arial',15,'bold'),bd=5,command=logout)   #back button on next screen after clicking newuser_btn
    logout_btn.place(relx=0.93,rely=0)                                #placing the button on frame by defining relx and rely

    lbl_welcome=Label(frm,text=f"Hello👋 {tup[0]},Welcome to the Dashboard",font=("arial",18,'bold'),bg='White',fg='Red')  #pass label on existuser next screen
    lbl_welcome.place(relx=0.001,rely=0.0)                             #placing the label on frame

    def update_pic():
        name=filedialog.askopenfilename()
        os.rename(name,f"{acn}.jpg")
        img_profile=Image.open(f"{acn}.jpg").resize((150,130))
        imgtk_profile=ImageTk.PhotoImage(img_profile,master=root)
        lbl_img_profile=Label(frm,image=imgtk_profile)
        lbl_img_profile.place(relx=.001,rely=0.08)
        lbl_img_profile.image=imgtk_profile

    if os.path.exists(f"{acn}.jpg"):
        img_profile=Image.open(f"{acn}.jpg").resize((150,130))
    else:
        img_profile=Image.open("profile.png").resize((150,130))
        
    imgtk_profile=ImageTk.PhotoImage(img_profile,master=root)

    lbl_img_profile=Label(frm,image=imgtk_profile)
    lbl_img_profile.place(relx=.001,rely=0.08)
    lbl_img_profile.image=imgtk_profile

    
    pic_btn=Button(frm,text="Update Picture📸",bg="light yellow",width=15,font=('arial',13,'bold'),bd=5,command=update_pic)   #back button on next screen after clicking newuser_btn
    pic_btn.place(relx=0.001,rely=.35)

    check_btn=Button(frm,text="Check Details",bg="light yellow",width=15,font=('arial',13,'bold'),bd=5,command=check_screen)   #back button on next screen after clicking newuser_btn
    check_btn.place(relx=0.001,rely=.45)                                #placing the button on frame by defining relx and rely

    update_btn=Button(frm,text="Update Details",bg="light yellow",width=15,font=('arial',13,'bold'),bd=5,command=update_screen)   #back button on next screen after clicking newuser_btn
    update_btn.place(relx=0.001,rely=.55)                                #placing the button on frame by defining relx and rely

    deposite_btn=Button(frm,text="Deposite Amount",bg="light yellow",width=15,font=('arial',13,'bold'),bd=5,command=deposite_screen)   #back button on next screen after clicking newuser_btn
    deposite_btn.place(relx=0.001,rely=.65)                                #placing the button on frame by defining relx and rely
    
    withdraw_btn=Button(frm,text="Withdraw Amount",bg="light yellow",width=15,font=('arial',13,'bold'),bd=5,command=withdraw_screen)   #back button on next screen after clicking newuser_btn
    withdraw_btn.place(relx=0.001,rely=.75)                                #placing the button on frame by defining relx and rely
 
    transfer_btn=Button(frm,text="Transfer Amount",bg="light yellow",width=15,font=('arial',13,'bold'),bd=5,command=transfer_screen)   #back button on next screen after clicking newuser_btn
    transfer_btn.place(relx=0.001,rely=.85)                                #placing the button on frame by defining relx and rely


def existuser_screen():
    def back():
        frm.destroy()
        main_screen()

    def fp_click():
        frm.destroy()
        forgot_screen()
    
    def reset_click():
        e_acn.delete(0,"end")
        e_pass.delete(0,"end")
        e_acn.focus()

    def submit_click():
        acn=e_acn.get()
        pwd=e_pass.get()

        conobj=sqlite3.connect(database="mybank.sqlite")
        curobj=conobj.cursor()
        query='''select * from accounts where acn=? and password=?'''
        curobj.execute(query,(acn,pwd))
        tup=curobj.fetchone()
        conobj.close()
        if tup==None:
            messagebox.showerror("Login","Invalid Credentials")
        else:
            acn=tup[0]
            frm.destroy() 
            welcome_screen(acn)

    frm=Frame(root,highlightbackground='black',highlightthickness=2)        #created frame and drop it on root window
    frm.configure(bg="pink")                    #configuring frame with backgrnd color-pink
    frm.place(relx=0,rely=.19,relwidth=1,relheight=.73) 

    back_btn=Button(frm,text="Back",bg="powder blue",font=('arial',15,'bold'),bd=5,command=back)   #back button on next screen after clicking newuser_btn
    back_btn.place(relx=0,rely=0)                                #placing the button on frame by defining relx and rely

    lbl_acn=Label(frm,text="👤ACN",font=("arial",18,'bold'),width=7,bg='purple',fg='white')  #acn label on existuser next screen
    lbl_acn.place(relx=.3,rely=.2)                               #placing the button on frame

    e_acn=Entry(frm,font=("arial",20,'bold'),bd=5)              #code for creating enter box of acn
    e_acn.place(relx=.4,rely=.2)                                #code for placing the entry box of acn
    e_acn.focus()                                           #focus-cursor for writting will start from here

    lbl_pass=Label(frm,text="🔑Pass",font=("arial",18,'bold'),width=7,bg='purple',fg='white')  #pass label on existuser next screen
    lbl_pass.place(relx=.3,rely=.3)                             #placing the label on frame

    e_pass=Entry(frm,font=("arial",20,'bold'),bd=5,show='*')                #code for creating enter box of pass
    e_pass.place(relx=.4,rely=.3)                                   #code for plcing the entry box of pass

    submit_btn=Button(frm,text="Submit",width=8,bg="powder blue",font=('arial',15,'bold'),bd=5,command=submit_click)   #submit button on next screen  
    submit_btn.place(relx=.45,rely=.45)                                #placing the button on frame by defining relx and rely

    reset_btn=Button(frm,text="Reset",width=8,bg="powder blue",font=('arial',15,'bold'),bd=5,command=reset_click)   #reset password button on next screen 
    reset_btn.place(relx=.55,rely=.45)                                #placing the button on frame by defining relx and rely

    fp_btn=Button(frm,text="Forgot Password",width=15,bg="powder blue",font=('arial',15,'bold'),bd=5,command=fp_click)   #reset password button on next screen 
    fp_btn.place(relx=.47,rely=.55)                                #placing the button on frame by defining relx and rely

footer=Label(root,text="Developed by-Tamanna Sharma \n📱xxxxxxx487",
            font=('arial',15,'bold'),bg="powder blue")  
                #code to make label on frame and formating it 
footer.pack(side="bottom")                  #packing label to the center bottom of the page

root.mainloop()                      #making window visible
