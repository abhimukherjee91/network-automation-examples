import NSX_Edge_Interface_backend as nsx
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

master = Tk()
master.title("NSX Edge Interface Details")
master.geometry('500x200')
x = Label(master, text='Welcome to NSX-V Interface Details Program',font=("Arial", 11)).grid(row=0, column=0)
a = Label(master, text='NSX Manager IP').grid(row=4,column = 0)
b = Label(master, text='Username').grid(row=5,column = 0)
c = Label(master, text='Password').grid(row=6,column = 0)
a1 = Entry(master)
a1.grid(row = 4,column = 1)
b1 = Entry(master)
b1.grid(row = 5,column = 1)
c1 = Entry(master, show= "*")
c1.grid(row = 6,column = 1)

def when_clicked():
    nsx_manager_ip = a1.get()
    username = b1.get()
    password = c1.get()
    if nsx_manager_ip != "\n" or username != "\n" or password != "\n" :
        try:
            nsx.get_nsx_edge_interface(nsx_manager_ip,username,password)
            messagebox.showinfo("Sucess!!", "Operation Completed")
        except:
            messagebox.showerror("Error!!", "Error: Please validate you inputs. For more info, please refer Logfile")

ttk.Button(master ,text="Execute",command=when_clicked).grid(row=7,column=0)

master.mainloop()






