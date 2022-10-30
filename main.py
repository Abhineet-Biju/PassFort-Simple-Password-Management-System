from tkinter import*
from tkinter import ttk
from tkinter import filedialog
import sqlite3
import hashlib
from functools import partial
from turtle import down
import webbrowser
from cryptography.fernet import Fernet
import shutil
import os

#initializing global variable for the menubar
control_var = True

# Creating Database
with sqlite3.connect("pass_vault.db") as db:
    cursor = db.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS masterpassword(
    id INTEGER PRIMARY KEY,
    password TEXT NOT NULL);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS cryptographykey(
    id INTEGER PRIMARY KEY,
    key TEXT NOT NULL);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS vault(
    id INTEGER PRIMARY KEY,
    platform TEXT NOT NULL,
    email TEXT NOT NULL,
    username TEXT NOT NULL,
    password TEXT NOT NULL);
""")

# Creating window for recieving entries from user
def add_entry():
    window =Toplevel()
    window.config(bg=BG)
    window.title("Add Entry")
    window.geometry("250x213")

    lbl1 = Label(window, text="Platform", anchor=CENTER, bg=BG, fg=FG)
    lbl1.pack()

    entry1 = Entry(window, width=20)
    entry1.pack()
    entry1.focus()

    lbl2 = Label(window, text="E-mail", anchor=CENTER, bg=BG, fg=FG)
    lbl2.pack()

    entry2 = Entry(window, width=20)
    entry2.pack()

    lbl3= Label(window, text="Username", anchor=CENTER, bg=BG, fg=FG)
    lbl3.pack()

    entry3 = Entry(window, width=20)
    entry3.pack()

    lbl4= Label(window, text="Password", anchor=CENTER, bg=BG, fg=FG)
    lbl4.pack()

    entry4 = Entry(window, width=20)
    entry4.pack()

    def Submit():
        global platform, email, username, password
        cursor.execute("SELECT * FROM cryptographykey")
        key = cursor.fetchmany()[0]
        #creating cryptography fernet obj
        fernetobj = Fernet(key[1])

        platform = fernetobj.encrypt(bytes(entry1.get(), 'utf8'))
        email = fernetobj.encrypt(bytes(entry2.get(), 'utf8'))
        username = fernetobj.encrypt(bytes(entry3.get(), 'utf8'))
        password = fernetobj.encrypt(bytes(entry4.get(), 'utf8'))

        insert_fields = """INSERT INTO vault(platform, email, username, password)
        VALUES(?, ?, ?, ?)"""
        cursor.execute(insert_fields, (platform, email, username, password))
        db.commit()

        manager_window()
    
    btn = Button(window, image=submit_img, height=35, width=91, bd=0, activebackground=BG, command=Submit)
    btn.pack(pady=8)
    window.bind('<Return>', lambda event: Submit())
        
    mainloop()

#defining menubar function
def menuBar():
    global control_var
    if control_var:
        importbtn.place(x=685,y=35)
        exportbtn.place(x=685,y=55)
        abtbtn.place(x=685,y=75)
        control_var = False
    else:
        importbtn.place_forget()
        exportbtn.place_forget()
        abtbtn.place_forget()
        control_var = True


#function to display import warning
def import_warning():
    global wrng_win
    wrng_win = Toplevel(bg=BG)
    wrng_win.geometry('250x300')
    wrng_win.title('Import')
    wrng_win.resizable(False, False)

    lbl1 = Label(wrng_win, text='WARNING!', font='Helvetica 15 bold', bg=BG, fg='red')
    lbl1.pack(anchor=CENTER)
    warning_txt = """Importing will lead to the permanent 
loss of your current saved information.

Make sure you have saved/exported 
your current passwords.

*UPON NEXT RESTART, A NEW
MASTERPASSWORD WILL HAVE TO 
BE SET"""
    lbl2 = Label(wrng_win, text=warning_txt, font='Helvetica 10 bold', bg=BG, fg='red')
    lbl2.pack(anchor=NW)

    #creating final import button
    import_btn = Button(wrng_win, text='Import', font='Helvetica 13 bold', bg=BG, fg='grey', activebackground=BG, activeforeground='grey', 
                        relief=SUNKEN, width=7)

    def import_btnBind():
        if var.get() == 1:
            import_btn.config(relief=RAISED, fg='red', activeforeground='red', command=import_bckup)            
        else:
            import_btn.config(relief=SUNKEN, fg='grey', activeforeground='grey', command=None)


    #creating confirmation checkbox
    var = IntVar()
    checkbox = Checkbutton(wrng_win, text='  I have saved my current \n passwords in a safe location',
                           bg=BG, fg=FG, activebackground=BG, activeforeground=FG, selectcolor=BG, variable=var, command=import_btnBind)
    checkbox.pack(anchor=S,pady=13)

    import_btn.pack(anchor=S,pady=5)

#fucntion to import backup
def import_bckup():
    path = filedialog.askopenfilename()
    shutil.copyfile(path, 'pass_vault.db')  
    wrng_win.destroy()
    manager_window()

#function to create backup
def export_bckup():
    shutil.copyfile('pass_vault.db', 'backup.db')
    con = sqlite3.connect('backup.db')
    c = con.cursor()
    delete = "DELETE FROM masterpassword"
    c.execute(delete)
    con.commit()
    path = filedialog.askdirectory()
    shutil.move('backup.db', path)

#function to  diplay the about window
def abt_info():
    version = 1.0
    abt_win = Toplevel(bg=BG)
    abt_win.title("About")
    abt_win.geometry('300x213')
    #abt_win.resizable(False,False)

    #creating variables for storing required text 
    txt1 = """PassFort - Simple Password
Management System"""
    txt2 = f"Build: version {version} (stable)"
    txt3 = "Developed and Maintained by:"
    name = "Abhineet Biju"
    txt5 = "My Social Media (Links):"
    linkedin = "https://linkedin.com/in/abhineet-biju-528a62227"

    #defining function to open a link
    def callback(url):
        webbrowser.open_new(url)
    
    #creating labels holding the text
    lbl1 = Label(abt_win,text=txt1,font='Helvetica 15 bold',bg=BG,fg='white')
    lbl2 = Label(abt_win,text=txt2,font='Helvetica 8 bold',bg=BG,fg=FG)
    lbl3 = Label(abt_win,text=txt3,font='Helvetica 13 bold',bg=BG,fg='white')
    lbl4 = Label(abt_win,text=name,font='Helvetica 11 bold',bg=BG,fg=FG)
    lbl5 = Label(abt_win,text=txt5,font='Helvetica 13 bold',bg=BG,fg='white')
    lbl6 = Label(abt_win,text="LinkedIn",font='Helvetica 11 bold underline',bg=BG,fg='#0200FF')
    lbl6.bind("<Button-1>",lambda e: callback(linkedin))
    

    #placing the labels on the window
    lbl1.pack(anchor=CENTER)
    lbl2.pack(anchor=CENTER)
    lbl3.pack(anchor=CENTER,pady=(15,1))
    lbl4.pack(anchor=CENTER)
    lbl5.pack(anchor=CENTER,pady=(15,1))
    lbl6.pack(anchor=CENTER)




# Window initialization
root = Tk()
root.title("PassFort-Simple Password Management System")
BG = "#444444"
FG = "#bcbcbc"
red_FG = "#f44336"
root.config(bg=BG)
root.iconbitmap(default=r"resources ignored\App Logo\App Logo Type 2.ico")


# Defining button images
set_img = PhotoImage(file="resources ignored\Button\Products\Set button\Set Type 4 5% 4.png")
submit_img = PhotoImage(file="resources ignored\Button\Products\Submit Button\Submit final 7%.png")
add_img = PhotoImage(file=r"resources ignored\Button\Products\Add Button\addbtn style2 7%.png")
del_img = PhotoImage(file="resources ignored\Button\Products\Delete Button\delete  button final 6%.png")

# Hashing data
def hash_password(input):
    hash = hashlib.md5(input)
    hash = hash.hexdigest()
    return hash

# First time window
def first_time_window():
    root.geometry("300x150")
    root.resizable(False, False)

    lbl1 = Label(root, text="Set Master Password",height=2, anchor=CENTER, bg=BG, fg=FG)
    lbl1.pack()

    entry = Entry(root, width=20)
    entry.pack()
    entry.focus()

    lbl2 = Label(root, text="Re-enter password",height=2, bg=BG, fg=FG)
    lbl2.pack()

    entry2 = Entry(root, width=20)
    entry2.pack()

    btn = Button(root, image=set_img, height=30, width=85, bd=0, activebackground=BG)
    btn.pack(pady=5)
    root.bind('<Return>', lambda event: set_password())
    
    # Adding masterpassword to database
    def set_password():
        if entry.get() == entry2.get():
            hashed_password = hash_password(entry.get().encode("utf-8"))
            insert_password = """INSERT INTO masterpassword(password)
            VALUES(?) """
            cursor.execute(insert_password, [(hashed_password)])
            db.commit()

            manager_window()
        else:
            lbl1.config(text="Passwords do not match!", fg=red_FG)

    btn.config(command=set_password)
    
    #Creating cryptography key
    key = Fernet.generate_key()
    str_key = str(key, 'utf8')
    insert_key = """INSERT INTO cryptographykey(key)
    VALUES(?) """
    cursor.execute(insert_key, [(str_key)])
    db.commit()
    

#Login Window
def login_window():
    try:
        os.remove('backup.db')
    except:
        pass
    root.geometry("300x117")

    lbl1 = Label(root, text="Enter Master Password",height=2, anchor=CENTER,  bg=BG, fg=FG)
    lbl1.pack()

    entry = Entry(root, width=20)
    entry.pack()
    entry.focus()

    btn = Button(root, image=submit_img, height=37, width=91, bd=0, activebackground=BG)
    btn.pack(pady=12)

    #lbl2 = Label(root,anchor=S,  bg=BG, fg=FG)
    #lbl2.pack()

    def get_master_password():
        check_hashed_password = hash_password(entry.get().encode("utf-8"))
        cursor.execute("SELECT * FROM masterpassword WHERE id= 1 AND password= ?", [(check_hashed_password)])
        return cursor.fetchall()


    def verify_password():
        match = get_master_password()

        if match:
            print("Correct Password")
            manager_window()
        else:
            entry.delete(0, 'end')
            lbl1.config(text="Wrong Password!", fg=red_FG)

    btn.config(command=verify_password)    
    root.bind('<Return>', lambda event: verify_password())



# Main pasword manager window
def manager_window():
    for widget in root.winfo_children():
        widget.destroy()
    root.geometry("775x500")
    
    # Function for removing info from database
    def delete_entry(input):
        cursor.execute("DELETE FROM vault WHERE id=? ", (input, ))
        db.commit()

        manager_window()

    #creating frames and canvases for adding scrollbar
    #creating main frame
    main_frame = Frame(root, bg=BG)
    main_frame.pack(fill=BOTH, expand=1)

    #creating canvas
    canvas = Canvas(main_frame, bg=BG, highlightthickness=1, highlightbackground=BG)
    canvas.pack(side=LEFT, fill=BOTH, expand=1)

    #adding scrollbar to the frame
    scrlbar = ttk.Scrollbar(main_frame, style="arrowless.Vertical.TScrollbar", orient=VERTICAL, command=canvas.yview)
    scrlbar.pack(side=RIGHT, fill=Y)
    
    #confguring the canvas
    canvas.configure(yscrollcommand=scrlbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

    #creating second frame
    sec_frame = Frame(canvas, bg=BG)

    #adding second frame to new window in canvas
    canvas.create_window((0,0), window=sec_frame, anchor='nw')


    # Button to add entry
    btn = Button(root, bg=BG, fg=FG, command=add_entry, image=add_img, height=45, width=100, bd=0, activebackground=BG)
    btn.place(x=338, y=3)
    
    #menubar button
    dark_FG = '#6E6E6E'

    mnu = Button(root, text='options',font='Helvetica 13 underline', command=menuBar, 
                 bg=BG, fg=FG, activebackground=BG, activeforeground=dark_FG, relief='sunken', borderwidth=0)
    mnu.place(x=685, y=10)

    #defining menubar sub-buttons
    global exportbtn, importbtn, abtbtn
    importbtn = Button(root, text='import',font='Helvetica 10 underline', command=import_warning,
                       bg=BG, activebackground=BG, activeforeground=dark_FG, fg=FG, relief='sunken', width=7, borderwidth=0)

    exportbtn = Button(root, text='export',font='Helvetica 10 underline', command=export_bckup, 
                       bg=BG, fg=FG, activebackground=BG, activeforeground=dark_FG, relief='sunken', width=7, borderwidth=0)

    abtbtn = Button(root, text='about',font='Helvetica 10 underline', command=abt_info,
                    bg=BG, activebackground=BG, activeforeground=dark_FG, fg=FG, relief='sunken', width=7, borderwidth=0)

                       

    # Creating labels
    pad_x = 60
    pad_y = 50
    lbl1 = Label(sec_frame, text="Platform", bg=BG, fg=FG)
    lbl1.grid(column=0, row=2, padx=pad_x, pady=pad_y)
    lbl1 = Label(sec_frame, text="E-mail", bg=BG, fg=FG)
    lbl1.grid(column=1, row=2, padx=pad_x, pady=pad_y)
    lbl1 = Label(sec_frame, text="Username", bg=BG, fg=FG)
    lbl1.grid(column=2, row=2, padx=pad_x, pady=pad_y)
    lbl1 = Label(sec_frame, text="Password", bg=BG, fg=FG)
    lbl1.grid(column=3, row=2, padx=pad_x, pady=pad_y)

    # Displaying info from database
    cursor.execute("SELECT * FROM vault")
    if cursor.fetchall():
        i = 0
        while True:
            cursor.execute("SELECT * FROM cryptographykey")
            key = cursor.fetchmany()[0]
            #creating cryptography fernet obj
            fernetobj = Fernet(key[1])

            cursor.execute("SELECT * FROM vault")
            array = cursor.fetchall()

            lbl = Label(sec_frame, text=fernetobj.decrypt(array[i][1]), bg=BG, fg=FG)
            lbl.grid(column=0, row=i+3)
            lbl = Label(sec_frame, text=fernetobj.decrypt(array[i][2]), bg=BG, fg=FG)
            lbl.grid(column=1, row=i+3)
            lbl = Label(sec_frame, text=fernetobj.decrypt(array[i][3]), bg=BG, fg=FG)
            lbl.grid(column=2, row=i+3)
            lbl = Label(sec_frame, text=fernetobj.decrypt(array[i][4]), bg=BG, fg=FG)
            lbl.grid(column=3, row=i+3)

            del_btn = Button(sec_frame, relief=FLAT, image=del_img, command = partial(delete_entry, array[i][0]),
                         activebackground=BG, bd=0, height=25, width=57)
            del_btn.grid(column=4, row=i+3)

            i += 1

            cursor.execute("SELECT * FROM vault")
            if len(cursor.fetchall()) <= i:
                break







   


cursor.execute("SELECT * FROM masterpassword")
if cursor.fetchall():
    login_window()
    #export_bckup()
else:
    first_time_window()

#root.resizable(False, False)
mainloop()