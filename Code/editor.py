 # -*- coding: utf-8 -*-
import os
import tkinter as tk
from tkinter.filedialog import askdirectory, asksaveasfilename
import NB_with_functions as nb
import sys
import time 
from threading import *

root_directory = ""
nb_results=[]


class WriteToWindow():
    def write(self, text):
        txt_edit.insert(tk.END,text)# write text to your window

    def flush(self):
        pass  # this method should exist, but doesn't need to do anything

sys.stdout = WriteToWindow()

def save_file(event=None):
    """Save the current file as a new file."""
    savefilepath = asksaveasfilename(
        defaultextension="txt",
        filetypes=[("Αρχεία txt", "*.txt"), ("Όλα τα αρχεία", "*.*")],
    )
    if not savefilepath:
        return
    with open(savefilepath, "w", encoding='utf-8') as output_file:
        text = txt_edit.get(1.0, tk.END)
        output_file.write(text)

def give_path(event=None):
    '''
    Give the path that includes datasets.
    '''
    global root_directory
    root_directory = r'{}'.format(askdirectory().replace('/', '\\'))

    if not root_directory:
        return
    btnCalculate['state'] = tk.NORMAL 
    txt_edit.delete(1.0, tk.END)
    
    txt_edit.insert(tk.END, '\n--------------- Root Directory ---------------\n')
    txt_edit.insert(tk.END, root_directory)
    txt_edit.insert(tk.END, '\n\n')

def btnCalculateOnClick():  
    nb.main(root_directory)

def threading(): 
    # Call work function 
    t1=Thread(target=btnCalculateOnClick) 
    t1.start() 

def popupmsg():
    popup = tk.Toplevel()
    popup.geometry("200x100+%d+%d" % (window.winfo_rootx() + 200,
                  window.winfo_rooty() + 150))
    text1="""Decision Trees - ID3 Algorithm 
    \nτου μεταπτυχιακού φοιτητή Λυμπέρη Δημήτρη
    \nυπό την εποπτεία του καθηγητή 
    \nKου Σταματάτου Ευστάθιου
    \n\nΣάμος 2020"""
    popup.wm_title("Πληροφορίες για την εφαρμογή")
    popup.rowconfigure(0, weight=0)
    popup.rowconfigure(1, weight=0)
    popup.columnconfigure(0, weight=1)
    
def info_dialogue():
    text1="""Naive Bayes Spam Filtering 
    \nτου μεταπτυχιακού φοιτητή Λυμπέρη Δημήτρη
    \nυπό την εποπτεία του καθηγητή 
    \nKου Σταματάτου Ευστάθιου
    \n\nΣάμος 2020"""
    top = tk.Toplevel()
    top.geometry("400x200+%d+%d" % (window.winfo_rootx() + 200,window.winfo_rooty() + 150))
    top.iconbitmap(r'{}'.format(os.path.join(os.path.join(os.getcwd(),os.path.dirname(__file__)),'aegean.ico')))
    top.title("Πληροφορίες")
    
    top.resizable(height = False, width = False)
    msg = tk.Label(top, text=text1)
    msg.pack()

window = tk.Tk()
window.iconbitmap(r'{}'.format(os.path.join(os.path.join(os.getcwd(),os.path.dirname(__file__)),'aegean.ico')))

window.title("Δ.Λυμπέρης 2020 - Naive Bayes Spam Filtering")
window.rowconfigure(0, weight=0)
window.rowconfigure(1, weight=1)
window.rowconfigure(2, weight=1)
window.columnconfigure(0, weight=1)

# Menu creation
menu = tk.Menu(window)
window.config(menu=menu)
fileMenu =tk.Menu(menu, tearoff=0)
fileMenu.add_command(label="Άνοιγμα", underline=0, command=give_path, accelerator="Ctrl+O")
fileMenu.add_command(label="Αποθήκευση", underline=0, command=save_file, accelerator="Ctrl+S")
fileMenu.add('separator')
fileMenu.add_command(label="Έξοδος" ,command=window.quit, underline=0)
menu.add_cascade(label="Αρχείο", menu=fileMenu, underline=0)
menu.add_cascade(label="Σχετικά", command=info_dialogue)
window.bind("<Control-o>", give_path)
window.bind("<Control-s>", save_file)
txt_edit = tk.Text(window)
scrollbar = tk.Scrollbar(window, orient='vertical',)
txt_edit['yscrollcommand']=scrollbar.set
scrollbar.config(command=txt_edit.yview)

function_options = tk.Frame(window, relief=tk.RAISED, bd=1)
program_options = tk.Frame(window, relief=tk.RAISED, bd=1)
bottomBar = tk.Frame(window, relief=tk.RAISED, bd=1)
               
# Calculate button   
btnCalculate= tk.Button(function_options, text="Υπολογισμός", command=threading) 
if not root_directory:
    btnCalculate['state'] = tk.DISABLED     
btnCalculate.grid(row=0, column=4, columnspan=2, rowspan=2,sticky="s", padx=5, pady=5)

function_options.grid(row=0, column=0, sticky="nsew")
program_options.grid(row=1, column=0, sticky="nsew")
txt_edit.grid(row=2, column=0, sticky="nsew")

# scrollbar.grid(row=2, column=1, sticky='nsew')
# bottomBar.grid(row=3, column=0, sticky="nsew")

window.geometry("850x500")
window.mainloop()