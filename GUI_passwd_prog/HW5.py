"""
Input: No input is required for the HW.
Output: GUI of a password generating and encrypted account & password notebook.
Please put lecture_module.py under the same directory with this file.(HW5.py)
There will be .txt files put under the same direcotry, which name is as the string in login_info['Group']. (The name we enter in the Group entry box)

Password generating steps:
    1. Enter Group/Keyphrase/Seed: Group will be the filename and Keyphrase & Seed will be the checkers for future retrieve.
    2. Press "Edit" button.
    3. Enter Accnt/Userid: Account should be the name of target website/database/system, Userid is the desired account name.
    4. Press "Generate" button.
    5. NOW YOU HAVE YOUR PASSWORD GENERATED!!! Don"t forget to press "Save" button for future retrieve.

Retrieve for ccount/password steps:
    1. Enter Group/Keyphrase/Seed: Each information should match the infomation we entered in the password generationg procedure.
    2. Press "Use" button.
    3. NOW YOU HAVE YOUR ACCOUNTS and PASSWORDS!!! Do not share your username and password with anyone. Except in the case of a shared account :) 
"""

## Include files
import tkinter as tk
from tkinter import *
from tkinter.messagebox import *
from lecture_module import *

## Define of fiels and accntf, dictionary entries of acc_info and login_info
fields = ['Group', 'Keyphrase', 'Seed']
accntf = ['Accnt','Userid','Password']
## Record acc_info and login_info through functions
acc_info = {}
login_info = {}


## Not only destroy the root, but also stop the Python execution
def quit():
    root.destroy()
    exit()

## Generate password if enough information is entered, or a pop-up window will show
def generate_password_display(accntinfo,logininfo):
    ## A pop-up window to remind user to enter full information 
    if not (acc_info[accntf[0]].get() and acc_info[accntf[1]].get()):
        tk.messagebox.showinfo("ERROR","Can't generate password, please provide Accnt/Userid")
    else:
        password = generate_password(accntinfo,logininfo)
        acc_info[accntf[2]] = password

## Save account and password, also has a pop-up window for ACK
def save_file_and_notice(acc_info,login_info):
    save_file(acc_info,login_info)
    tk.messagebox.showinfo("NOTICE","Account information stored successfully!!!")

## Generate the "Use Accounts" GUI
def use_acnt_table():
    err,acc = read_file(login_info)
    ## Another pop-up window to remind user to enter full information 
    if err == 1 or not login_info[fields[2]].get():
        tk.messagebox.showinfo("ERROR","Invalid infomation, check your Group/Keyphrase/Seed")
    elif err == 2:
        tk.messagebox.showinfo("ERROR","Wrong infomation, check if your Group/Keyphrase/Seed are correct")
    else:
        root_uat = tk.Tk()
        root_uat.title('Use Accounts')
        dup_list = {}
        for i,ival in enumerate(acc):
            ## Do not display duplicate output if 3 infomations of a row is the same as the other row
            if not (acc[i][accntf[0]],acc[i][accntf[1]],acc[i][accntf[2]]) in dup_list:
                dup_list[(acc[i][accntf[0]],acc[i][accntf[1]],acc[i][accntf[2]])] = 1

                lbl = tk.Label(root_uat, text=str(acc[i][accntf[0]]))
                lbl.grid(row=i, column=0, sticky="w") 
                e = tk.Entry(root_uat)
                e.grid(row=i, column=1, sticky="w")
                f = tk.Entry(root_uat)
                f.grid(row=i, column=2, sticky="w")
                
                e.delete(0, END)
                e.insert(0, acc[i][accntf[1]])
                f.delete(0, END)
                f.insert(0, acc[i][accntf[2]])
        
        tk.Button(root_uat, text='Quit', command=root_uat.destroy).grid(row=len(acc), column=2,sticky="e", pady=4) 
        root_uat.mainloop()
    
## Generate the "New Account" GUI
def new_acnt_table():
    ## Again, a pop-up window to remind user to enter full information 
    if not (login_info[fields[0]].get() and login_info[fields[1]].get() and login_info[fields[2]].get()):
        tk.messagebox.showinfo("ERROR","Please provide Group/Keyphrase/Seed")
    else:
        root_nat = tk.Tk()
        root_nat.title('New Account')
        lbl_0 = tk.Label(root_nat, text="Accnt:")
        lbl_1 = tk.Label(root_nat, text="Userid")
        lbl_2 = tk.Label(root_nat, text="Password:")
        lbl_0.grid(row=0, column=0, sticky="w") 
        lbl_1.grid(row=1, column=0, sticky="w")
        lbl_2.grid(row=2, column=0, sticky="w")
        e0 = tk.Entry(root_nat)
        e1 = tk.Entry(root_nat)
        e2 = tk.Entry(root_nat)
        e0.grid(row=0, column=1, sticky="e")
        e1.grid(row=1, column=1, sticky="e")
        e2.grid(row=2, column=1, sticky="e")
        acc_info[accntf[0]] = e0
        acc_info[accntf[1]] = e1
        acc_info[accntf[2]] = e2
        
        tk.Button(root_nat, text='Save', command=lambda: save_file_and_notice(acc_info,login_info)).grid(row=3, column=0,sticky="w", pady=4)
        tk.Button(root_nat, text='Generate',  command=lambda: generate_password_display(acc_info,login_info)).grid(row=3, column=1,sticky="w", pady=4)
        tk.Button(root_nat, text='Quit', command=root_nat.destroy).grid(row=3, column=2,sticky="e", pady=4) 
        root_nat.mainloop()

## Generate the "Passwword Program" GUI
def main_table(fields,root):
    root.title('Password Program')
    lbl_0 = tk.Label(root, text="Group:")
    lbl_1 = tk.Label(root, text="Keyphrase")
    lbl_2 = tk.Label(root, text="Seed:")
    lbl_0.grid(row=0, column=0, sticky="w") 
    lbl_1.grid(row=1, column=0, sticky="w")
    lbl_2.grid(row=2, column=0, sticky="w")
    e0 = tk.Entry(root)
    e1 = tk.Entry(root)
    e2 = tk.Entry(root)
    e0.grid(row=0, column=1, sticky="e")
    e1.grid(row=1, column=1, sticky="e")
    e2.grid(row=2, column=1, sticky="e")
    login_info[fields[0]] = e0
    login_info[fields[1]] = e1
    login_info[fields[2]] = e2
    
    tk.Button(root, text='Edit', command=new_acnt_table).grid(row=3, column=0,sticky="w", pady=4)
    tk.Button(root, text='Use',  command=use_acnt_table).grid(row=3, column=1,sticky="w", pady=4)
    tk.Button(root, text='Quit', command=quit).grid(row=3, column=2,sticky="e", pady=4) 

root = tk.Tk()
main_table(fields,root)
root.mainloop()
