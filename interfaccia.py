#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 13 11:35:33 2021

@author: antoniocurci
"""
from tkinter import *
from tkinter import scrolledtext

window = Tk()

window.title("SpotPredict")
window.geometry('500x400')


lbl = Label(window, text="Inserisci il nome di una canzone (ES: your song elton john)")
lbl.grid(column=0, row=0)

txt = Entry(window,width=20)
txt.focus_set()
txt.grid(column=0, row=1)


def clicked():
    out = txt.get()
    return out

def inserisciTesto(stringInput):
    textSection.insert(INSERT, stringInput)
    
def getTextFromUI():
    testo = txt.get()
    return testo
    
textSection = scrolledtext.ScrolledText(window,width=50,height=15)
textSection.grid(column=0,row=2)

btn = Button(window, text="Invio", command=clicked)
btn.grid(column=1, row=1)


window.mainloop()