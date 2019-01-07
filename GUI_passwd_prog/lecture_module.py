# -*- coding: utf-8 -*-
"""
Created on Thu Aug  9 06:58:03 2018

@author: olhartin@asu.edu
"""
import os
import random
import numpy as np
from tkinter import *
fields = ['Group', 'Keyphrase', 'Seed']
accntf = ['Accnt','Userid','Password']
## maps any number to some ascii code number or char
def cmap(charnum):
##    print(charnum)
    if (charnum>57): 
        charnum += 7
    else:
        return(charnum)
        
    if (charnum>90): 
        charnum += 6
    else:
        return(charnum)
        
    if (charnum>122): 
        charnum -= 74
##        print(charnum)
        return( cmap(charnum) )
    else:
        return(charnum)
##      encrypt a phrase
def encryptKeyphrase(Message,Keyphrase='   ',seed_=0):
    cypher = ''
    random.seed(seed_)
    for i in range(0,int(len(Message))):
        cypher += chr( cmap(ord(Message[i]) + 
                            ord(Keyphrase[i%len(Keyphrase)]) + 
                            random.randint(1,100) ) )
    return(cypher)
##  create unique seed for any combination of these
##  input strings
def sumofchar(message,keyphrase,accnt,userid,seed_):
    sum = 0
    for i in range(0,int(len(message))):
        sum += int(ord(message[i]))
    for i in range(0,int(len(keyphrase))):
        sum += int(ord(keyphrase[i]))
    for i in range(0,int(len(accnt))):
        sum += int(ord(accnt[i]))
    for i in range(0,int(len(userid))):
        sum += int(ord(userid[i]))
    sum += int(seed_)
    return(sum)
##      ecrypt using message, keyphrase, accnt, userid, and seed
def encrypt3Message(Message,Keyphrase='   ',Accnt='    ',
                            Userid='    ',seed_=0):
    cypher = ''
    seed = sumofchar(Message, Keyphrase, Accnt, Userid, seed_)
    random.seed(seed)
    for i in range(0,int(len(Message))):
        cypher += chr( cmap(ord(Message[i]) + 
                            ord(Keyphrase[i%len(Keyphrase)]) + 
                            ord(Accnt[i%len(Accnt)]) + 
                            ord(Userid[i%len(Userid)]) + 
                            random.randint(1,100) ) )
    return(cypher)
##  generate a password from login and accnout information   
def generate_password(accntinfo,logininfo):
    cypher = generate_password_(logininfo['Keyphrase'].get(),logininfo['Seed'].get(),accntinfo['Accnt'].get(),accntinfo['Userid'].get())
##    cypher = encrypt3Message('123456789',logininfo['Keyphrase'].get(),accntinfo['Accnt'].get(),accntinfo['Userid'].get(),logininfo['Seed'].get())
    accntinfo['Password'].delete(0,END)
    accntinfo['Password'].insert(0,cypher)
    return(cypher)
##  generate a password from login and accnout information       
def generate_password_(keyphrase,seed,accnt,userid):
    cypher = encrypt3Message('123456789',keyphrase,accnt,userid,seed)
    return(cypher)
##  read file, add new accounts and write out
def save_file(entnew,entries):
    error,accnts = read_file(entries)
    write_file(error,accnts,entnew,entries)
    return(1)
##  write file with login and then each account, not including password
def write_file(error,accnts,accntnew,entries):
    filename = entries['Group'].get()+".txt"
    cryptKeyphrase = encryptKeyphrase(entries['Keyphrase'].get())
    seed = entries['Seed'].get()
    fh = open(filename,"w")
    fh.write(cryptKeyphrase + '\n')
    fh.write(seed + '\n')
    if (len(accnts)>0):
        for accnt in accnts:
            line = ''
            acntname = accnt['Accnt']   ## access as dictionary
            line = line + acntname + ' '
            username = accnt['Userid']
##            line = line + username + ' '
            line = line + username + '\n'
##            password = accnt['Password']
##            line = line + password + '\n'
            fh.write(line)
    line = ''
    acntname = accntnew['Accnt'].get()
    line = line + acntname + ' '
    username = accntnew['Userid'].get()
##    line = line + username + ' '
    line = line + username + '\n'
##    password = accntnew['Password'].get()
##    line = line + password + '\n'
    fh.write(line)
    fh.close()
    return(1)
##  read a file
def read_file(entries):
    filename = entries['Group'].get()+".txt"
    Keyphrase = entries['Keyphrase'].get()
    cryptKeyphrase = encryptKeyphrase(Keyphrase)
##    seed = entries['Seed'].get()
    error = 0
    accnts = []
    if (os.path.isfile(filename)):
        fh = open(filename,"r")
        if (fh):
            lines = fh.readlines()
            lineno = 1
            for line in lines:
                if (error == 0):
                    line=line.strip()
                    if (lineno==1):
                        if (line!=cryptKeyphrase):
                            error = 2
                            print('error,line,cryptKeyphase',error,line,cryptKeyphrase)
                    elif (lineno==2):
                        ## Add a checker for seed here
                        if (line!=entries['Seed'].get()):
                            error = 2
                            print('error,line',error,line)
                        else:
                            seed = int(line)
                    elif (lineno>2):
                        accnt_ = line.split()
                        accnt_.append(generate_password_(Keyphrase,seed,accnt_[0],accnt_[1]))
                        accnt = dict(zip(accntf,accnt_))
##                  this is a list of dictionaries
                        accnts.append(accnt)
                lineno += 1
            fh.close()
        else:
            error=1
            fh.close()
    else:
        error=1
    return(error,accnts)
##  create or edit accounts

##  show all accounts      

##  make a form for fields
       
##  Main dialog
##root = Tk()
