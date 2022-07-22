from platform import win32_edition
from tkinter import Frame, Label, Button, PhotoImage, Entry, LabelFrame
import tkinter as tk
import time
from tkinter import messagebox
from PIL import ImageTk, Image,  ImageWin
import sys
#PHIDGET
from Phidget22.Phidget import *
from Phidget22.Devices.DigitalInput import *
import threading
#ETIQUETA
import win32print
import win32ui
import os
from barcode import Code39
from barcode.writer import ImageWriter
from io import BytesIO
#BD
import mysql.connector

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class Pasword(tk.Frame):
    def __init__(self, parent=None):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        global imagen, numSwitch
        self.parent.title("Checador de switches DMU")
        self.lbl = Label(ROOT, text="Ingresar contraseña", anchor="center" ,fg="IndianRed4",font=("Arial CE", 17))
        self.lbl.place(x=100, y=20, width=210, height=40)

        self.btn = Button(ROOT, text="continuar", command= lambda:self.open(), bg="DodgerBlue3" ,font=("Arial CE", 13 )) 
        self.btn.place(x=240,y=90, width=80, height=30)
    
        self.pas = Entry(ROOT, bg="LightCyan3", show="*")
        self.pas.place(x=80,y=90, width=100, height=30)
        
        ruta= resource_path("industriasDMU.png")
        imagen= PhotoImage(file=ruta).subsample(2) 
        ROOT.fondo = Label(ROOT, image=imagen, bg= "IndianRed4").place(x=125,y=130)
        numSwitch=0
        
                
    def open(self):
        valor= int(self.pas.get())
        if valor == 123456:
            self.pas.delete(0, 'end')
            window2()
        else:
            messagebox.showerror(title="Error", message="La contraseña es incorrecta, Intenta de nuevo")
            
            
def window2():
    global images,imagen, noMotor, noSwitch, date, current_time, img0, img1, img2, img3, img4, img5, win2, time_label, frame1, frame2, operario
    win2=tk.Toplevel(ROOT)   
    win2.title("Industrias DMU S.A DE C.V")
    win2.geometry("1450x1350")
    frame1 = Frame(win2) 
    frame1.grid(row=0 , column=0)
    frame1.config( width=1360, height=90)
    imagen= PhotoImage(file="industriasDMU.png")
    frame1.fondo = Label(frame1, image=imagen).place(x=0, y=0)
    label1 = tk.Label(frame1, text='Operador: ', font=("Times", 15 ))
    label1.place(x=350, y=10)
    operario = Entry(frame1, bg="LightCyan3",font=("Arial CE", 19 ))
    operario.place(x=350, y=40, width=100, height=40)
    lblTitle = tk.Label(frame1, text='Sistema de Verificacion de Switches ', fg=("IndianRed4"), font=("Times", 30 ))
    lblTitle.place(x=500, y=10)
    date=time.strftime("%y/%m/%d") #fecha
    lbldate = tk.Label(frame1, text=date ,background='#3a3a3a', fg='#ffffff', font=("calibri", 14))
    lbldate.place(x=1250, y=5)
    
    time_label = tk.Label( frame1,background='#3a3a3a', fg='#ffffff', font=("calibri", 14))
    time_label.place(x=1250, y=30)
    exitbutton = Button(frame1, text="SALIR DEL SISTEMA", bg="red2" ,  command= lambda:[exit()],font=("Arial CE", 11 ))
    exitbutton.place(x=1200, y=60, width=150, height=40)
    frame2 = Frame(win2) 
    frame2.grid(row=1 , column=0)
    frame2.config( width=1360, height=120)
    lblSw = tk.Label(frame2, text='No. Parte Motor ',  fg="IndianRed4",font=("Times", 16 ))
    lblSw.place(x=100, y=10)
    noMotor = Entry(frame2, bg="LightCyan3",font=("Arial CE", 20 ))
    noMotor.place(x=100, y=40, width=500, height=50)
    lblSw = tk.Label(frame2, text='No. Parte Switch ', fg="IndianRed4" ,font=("Times", 16 ))
    lblSw.place(x=750, y=10)
    noSwitch = Entry(frame2, bg="LightCyan3", font=("Arial CE", 20 ))
    noSwitch.place(x=750, y=40, width=500, height=50)  
    
      
    def timer():
        global current_time, time_label, frame1
        current_time = time.strftime("%I:%M:%S")
        time_label.configure(text=current_time)
        time_label.after(1000, timer)
    
    while True:
        timer()
        break
    
    
    def exit():
        global digitalInput0, digitalInput1, digitalInput2, digitalInput3, digitalInput4, digitalInput5, digitalInput6, digitalInput7, digitalInput8, digitalInput9
        ROOT.destroy()
        digitalInput0.close()
        digitalInput1.close()
        digitalInput2.close()
        digitalInput3.close()
        digitalInput4.close()
        digitalInput5.close()
        digitalInput6.close()
        digitalInput7.close()
        digitalInput8.close()
        digitalInput9.close()
        sys.exit()
        
        
    def imgparte():
        global frame3
        frame3 = Frame(win2) 
        frame3.grid(row=2 , column=0)
        frame3.config( width=1360, height=500)
        lblStatus = tk.Label(frame3, text='-Status del Switch-', fg="IndianRed4",font=("Times", 18 ))
        lblStatus.place(x=90, y=0)
        swInf = tk.Label(frame3, text='Inf del Switch ', bg="LightCyan3" ,font=("Times", 18 ))
        swInf.place(x=0, y=30, width=400, height=500)

       
    def frame6input ():
        global frame4, img0, img1, img2, img3, img4, img5, img6, img7, img8, img9
        frame4 = LabelFrame(win2)
        frame4.config( bg="LightCyan3", text="6 funciones")
        frame4.place(x=0, y=240, width=400, height=500)
        lblcheck = tk.Label(frame4, text='!', image=img0, bg='green3')
        lblcheck.place(x=80, y=50, width=70, height=70)
        lbls1 = tk.Label(frame4, text='SW1',font=("Arial CE", 15 ),bg="LightCyan3")
        lbls1.place(x=165, y=50, width=70, height=70)
        lblcheck2 = tk.Label(frame4, text='!', image=img1, bg='green3')
        lblcheck2.place(x=250, y=50, width=70, height=70)
        lblcheck3 = tk.Label(frame4, text='!', image=img2, bg='green3')
        lblcheck3.place(x=80, y=200, width=70, height=70)
        lbls2 = tk.Label(frame4, text='SW2',font=("Arial CE", 15 ),bg="LightCyan3")
        lbls2.place(x=165, y=200, width=70, height=70)
        lblcheck4 = tk.Label(frame4, text='!', image=img3, bg='green3')
        lblcheck4.place(x=250, y=200, width=70, height=70)
        lblcheck5 = tk.Label(frame4, text='!', image=img4, bg='green3')
        lblcheck5.place(x=80, y=350, width=70, height=70)
        lbls3 = tk.Label(frame4, text='SW3',font=("Arial CE", 15 ),bg="LightCyan3")
        lbls3.place(x=165, y=350, width=70, height=70)
        lblcheck6 = tk.Label(frame4, text='!', image=img5, bg='green3')
        lblcheck6.place(x=250, y=350, width=70, height=70)
        
        
    def frame8input():
        global frame5, img0, img1, img2, img3, img4, img5, img6, img7, img8, img9
        frame5 = LabelFrame(win2) 
        frame5.config( bg="LightCyan3", text="8 funciones")
        frame5.place(x=0, y=240, width=400, height=500)
        lblcheck = tk.Label(frame5, text='!', image=img0, bg='green3')
        lblcheck.place(x=80, y=20, width=65, height=65)
        lbls1 = tk.Label(frame5, text='SW1',font=("Arial CE", 15 ),bg="LightCyan3")
        lbls1.place(x=165, y=20, width=70, height=70)
        lblcheck2 = tk.Label(frame5, text='!', image=img1, bg='green3')
        lblcheck2.place(x=250, y=20, width=65, height=65)
        lblcheck3 = tk.Label(frame5, text='!', image=img2, bg='green3')
        lblcheck3.place(x=80, y=120, width=65, height=65)
        lbls2 = tk.Label(frame5, text='SW2',font=("Arial CE", 15 ),bg="LightCyan3")
        lbls2.place(x=165, y=120, width=70, height=70)
        lblcheck4 = tk.Label(frame5, text='!', image=img3, bg='green3')
        lblcheck4.place(x=250, y=120, width=65, height=65)
        lblcheck5 = tk.Label(frame5, text='!', image=img4, bg='green3')
        lblcheck5.place(x=80, y=220, width=65, height=65)
        lbls3 = tk.Label(frame5, text='SW3',font=("Arial CE", 15 ),bg="LightCyan3")
        lbls3.place(x=165, y=220, width=70, height=70)
        lblcheck6 = tk.Label(frame5, text='!', image=img5, bg='green3')
        lblcheck6.place(x=250, y=220, width=65, height=65)
        lblcheck7 = tk.Label(frame5, text='!', image=img6, bg='green3')
        lblcheck7.place(x=80, y=320, width=65, height=65)
        lbls1 = tk.Label(frame5, text='SW4',font=("Arial CE", 15 ),bg="LightCyan3")
        lbls1.place(x=165, y=320, width=70, height=70)
        lblcheck8 = tk.Label(frame5, text='!', image=img7, bg='green3')
        lblcheck8.place(x=250, y=320, width=65, height=65)
    
    
    def frame10input():
        global frame6, img0, img1, img2, img3, img4, img5, img6, img7, img8, img9
        frame6 = LabelFrame(win2) 
        frame6.config( bg="LightCyan3", text="10 funciones")
        frame6.place(x=0, y=240, width=400, height=500)
        lblcheck = tk.Label(frame6, text='!', image=img0, bg='green3')
        lblcheck.place(x=80, y=20, width=65, height=65)
        lbls1 = tk.Label(frame6, text='SW1',font=("Arial CE", 15 ),bg="LightCyan3")
        lbls1.place(x=165, y=20, width=70, height=70)
        lblcheck2 = tk.Label(frame6, text='!', image=img1, bg='green3')
        lblcheck2.place(x=250, y=20, width=65, height=65)
        lblcheck3 = tk.Label(frame6, text='!', image=img2, bg='green3')
        lblcheck3.place(x=80, y=100, width=65, height=65)
        lbls2 = tk.Label(frame6, text='SW2',font=("Arial CE", 15 ),bg="LightCyan3")
        lbls2.place(x=165, y=100, width=70, height=70)
        lblcheck4 = tk.Label(frame6, text='!', image=img3, bg='green3')
        lblcheck4.place(x=250, y=100, width=65, height=65)
        lblcheck5 = tk.Label(frame6, text='!', image=img4, bg='green3')
        lblcheck5.place(x=80, y=180, width=65, height=65)
        lbls3 = tk.Label(frame6, text='SW3',font=("Arial CE", 15 ),bg="LightCyan3")
        lbls3.place(x=165, y=180, width=70, height=70)
        lblcheck6 = tk.Label(frame6, text='!', image=img5, bg='green3')
        lblcheck6.place(x=250, y=180, width=65, height=65)
        lblcheck7 = tk.Label(frame6, text='!', image=img6, bg='green3')
        lblcheck7.place(x=80, y=260, width=65, height=65)
        lbls4 = tk.Label(frame6, text='SW4',font=("Arial CE", 15 ),bg="LightCyan3")
        lbls4.place(x=165, y=260, width=70, height=70)
        lblcheck8 = tk.Label(frame6, text='!', image=img7, bg='green3')
        lblcheck8.place(x=250, y=260, width=65, height=65)
        lblcheck9 = tk.Label(frame6, text='!', image=img8, bg='green3')
        lblcheck9.place(x=80, y=340, width=65, height=65)
        lbls5 = tk.Label(frame6, text='SW5',font=("Arial CE", 15 ),bg="LightCyan3")
        lbls5.place(x=165, y=340, width=70, height=70)
        lblcheck10 = tk.Label(frame6, text='!', image=img9, bg='green3')
        lblcheck10.place(x=250, y=340, width=65, height=65)
        
    def der6func ():
        global frame3, img0, img1, img2, img3, img4, img5, lbl, lbl1, lbl2, lbl3, lbl4, lbl5
        lbl = tk.Label(frame3, text=' ! ',image=img0 , bg='green3')
        lbl.place(x=980, y=198, width=30, height=30)
        lbl1 = tk.Label(frame3, text=' ! ',image=img1 , bg='green3')
        lbl1.place(x=985, y=340, width=30, height=30)
        lbl2 = tk.Label(frame3, text=' ! ',image=img2 , bg='green3')
        lbl2.place(x=1055, y=230, width=30, height=30)
        lbl3 = tk.Label(frame3, text=' ! ',image=img4 , bg='green3')
        lbl3.place(x=1120, y=235, width=30, height=30)
        lbl4 = tk.Label(frame3, text=' ! ',image=img3 , bg='green3')
        lbl4.place(x=1055, y=340, width=30, height=30)
        lbl5 = tk.Label(frame3, text=' ! ',image=img5 , bg='green3')
        lbl5.place(x=1120, y=340, width=30, height=30)
        
    def izne8fun():
        global frame3, img0, img1, img2, img3, img4, img5, img6, img7, lbl, lbl1, lbl2, lbl3, lbl4, lbl5, lbl6, lbl7
        lbl = tk.Label(frame3, text=' ! ',image=img0 , bg='green3')
        lbl.place(x=650, y=250, width=30, height=30)
        lbl1 = tk.Label(frame3, text=' ! ',image=img1 , bg='green3')
        lbl1.place(x=650, y=345, width=30, height=30)
        lbl2 = tk.Label(frame3, text=' ! ',image=img2 , bg='green3')
        lbl2.place(x=745, y=250, width=30, height=30)
        lbl3 = tk.Label(frame3, text=' ! ',image=img3 , bg='green3')
        lbl3.place(x=740, y=338, width=30, height=30)
        lbl4 = tk.Label(frame3, text=' ! ',image=img4 , bg='green3')
        lbl4.place(x=800, y=210, width=30, height=30)
        lbl5 = tk.Label(frame3, text=' ! ',image=img7 , bg='green3')
        lbl5.place(x=970, y=255, width=30, height=30)
        lbl6 = tk.Label(frame3, text=' ! ',image=img5 , bg='green3')
        lbl6.place(x=800, y=340, width=30, height=30)
        lbl7 = tk.Label(frame3, text=' ! ',image=img6 , bg='green3')
        lbl7.place(x=845, y=258, width=30, height=30)
        
    def derne8func ():
        global frame3, img0, img1, img2, img3, img4, img5, img6, img7, lbl, lbl1, lbl2, lbl3, lbl4, lbl5, lbl6, lbl7
        lbl = tk.Label(frame3, text=' ! ',image=img0 , bg='green3')
        lbl.place(x=860, y=228, width=30, height=30)
        lbl1 = tk.Label(frame3, text=' ! ',image=img1 , bg='green3')
        lbl1.place(x=980, y=228, width=30, height=30)
        lbl2 = tk.Label(frame3, text=' ! ',image=img2 , bg='green3')
        lbl2.place(x=1010, y=170, width=30, height=30)
        lbl3 = tk.Label(frame3, text=' ! ',image=img3 , bg='green3')
        lbl3.place(x=1015, y=310, width=30, height=30)
        lbl4 = tk.Label(frame3, text=' ! ',image=img4 , bg='green3')
        lbl4.place(x=1110, y=200, width=30, height=30)
        lbl5 = tk.Label(frame3, text=' ! ',image=img5 , bg='green3')
        lbl5.place(x=1110, y=310, width=30, height=30)
        lbl6 = tk.Label(frame3, text=' ! ',image=img6 , bg='green3')
        lbl6.place(x=1165, y=215, width=30, height=30)
        lbl7 = tk.Label(frame3, text=' ! ',image=img7 , bg='green3')
        lbl7.place(x=1165, y=310, width=30, height=30)
    
    def izH60 ():
        global frame3, img0, img1, img2, img3, img4, img5, img6, img7, lbl, lbl1, lbl2, lbl3, lbl4, lbl5, lbl6, lbl7
        lbl = tk.Label(frame3, text=' ! ',image=img0 , bg='green3')
        lbl.place(x=720, y=320, width=30, height=30)
        lbl1 = tk.Label(frame3, text=' ! ',image=img1 , bg='green3')
        lbl1.place(x=820, y=320, width=30, height=30)
        lbl2 = tk.Label(frame3, text=' ! ',image=img2 , bg='green3')
        lbl2.place(x=750, y=240, width=30, height=30)
        lbl3 = tk.Label(frame3, text=' ! ',image=img3 , bg='green3')
        lbl3.place(x=750, y=310, width=30, height=30)
        lbl4 = tk.Label(frame3, text=' ! ',image=img4 , bg='green3')
        lbl4.place(x=820, y=230, width=30, height=30)
        lbl5 = tk.Label(frame3, text=' ! ',image=img5 , bg='green3')
        lbl5.place(x=880, y=230, width=30, height=30)
        lbl6 = tk.Label(frame3, text=' ! ',image=img6 , bg='green3')
        lbl6.place(x=880, y=270, width=30, height=30)
        lbl7 = tk.Label(frame3, text=' ! ',image=img7 , bg='green3')
        lbl7.place(x=960, y=270, width=30, height=30)
        
        
    def izneg10func():
        global frame3, img0, img1, img2, img3, img4, img5, img6, img7, lbl, lbl1, lbl2, lbl3, lbl4, lbl5, lbl6, lbl7, lbl8, lbl9
        lbl = tk.Label(frame3, text=' ! ',image=img0 , bg='green3')
        lbl.place(x=600, y=230, width=30, height=30)
        lbl1 = tk.Label(frame3, text=' ! ',image=img1 , bg='green3')
        lbl1.place(x=600, y=310, width=30, height=30)
        lbl2 = tk.Label(frame3, text=' ! ',image=img2 , bg='green3')
        lbl2.place(x=710, y=260, width=30, height=30)
        lbl3 = tk.Label(frame3, text=' ! ',image=img3 , bg='green3')
        lbl3.place(x=550, y=270, width=30, height=30)
        lbl4 = tk.Label(frame3, text=' ! ',image=img4 , bg='green3')
        lbl4.place(x=750, y=180, width=30, height=30)
        lbl5 = tk.Label(frame3, text=' ! ',image=img7 , bg='green3')
        lbl5.place(x=910, y=240, width=30, height=30)
        lbl6 = tk.Label(frame3, text=' ! ',image=img5 , bg='green3')
        lbl6.place(x=745, y=310, width=30, height=30)
        lbl7 = tk.Label(frame3, text=' ! ',image=img6 , bg='green3')
        lbl7.place(x=800, y=240, width=30, height=30)
        lbl8 = tk.Label(frame3, text=' ! ',image=img8 , bg='green3')
        lbl8.place(x=850, y=190, width=30, height=30)
        lbl9 = tk.Label(frame3, text=' ! ',image=img9 , bg='green3')
        lbl9.place(x=850, y=300, width=30, height=30)
    
    
    def derneg10func():
        global frame3, img0, img1, img2, img3, img4, img5, img6, img7, lbl, lbl1, lbl2, lbl3, lbl4, lbl5, lbl6, lbl7, lbl8, lbl9
        lbl = tk.Label(frame3, text=' ! ',image=img0 , bg='green3')
        lbl.place(x=870, y=300, width=30, height=30)
        lbl1 = tk.Label(frame3, text=' ! ',image=img1 , bg='green3')
        lbl1.place(x=980, y=300, width=30, height=30)
        lbl2 = tk.Label(frame3, text=' ! ',image=img2 , bg='green3')
        lbl2.place(x=930, y=245, width=30, height=30)
        lbl3 = tk.Label(frame3, text=' ! ',image=img3 , bg='green3')
        lbl3.place(x=930, y=350, width=30, height=30)
        lbl4 = tk.Label(frame3, text=' ! ',image=img4 , bg='green3')
        lbl4.place(x=1040, y=230, width=30, height=30)
        lbl5 = tk.Label(frame3, text=' ! ',image=img5 , bg='green3')
        lbl5.place(x=1040, y=390, width=30, height=30)
        lbl6 = tk.Label(frame3, text=' ! ',image=img6 , bg='green3')
        lbl6.place(x=1120, y=280, width=30, height=30)
        lbl7 = tk.Label(frame3, text=' ! ',image=img7 , bg='green3')
        lbl7.place(x=1120, y=370, width=30, height=30)
        lbl8 = tk.Label(frame3, text=' ! ',image=img8 , bg='green3')
        lbl8.place(x=1090, y=330, width=30, height=30)
        lbl9 = tk.Label(frame3, text=' ! ',image=img9 , bg='green3')
        lbl9.place(x=1210, y=340, width=30, height=30)
        
        
    def codigos():
        global lbl, lbl1, lbl2, lbl3, lbl4, lbl5, lbl6, lbl7, lbl8, lbl9, fondo, frame3, foto,parte, img0, img1, img2, img3, img4, img5, img6, img7, img8, img9, noMotor, noSwitch, numSwitch, s0, s1, s2, s3, s4, s5, s6, s7, s8, s9
        parte =''
        m=noMotor.get()
        sw=noSwitch.get()
        if m == '175H0A4600' and sw == '185F1A4600': # derecho 6 funciones
            numSwitch=6
            imgparte()
            frame6input()
            ruta= resource_path("176A1-A4602.png")
            foto= PhotoImage(file=ruta) 
            der6func()
            fondo = tk.Label(frame3,image=foto, bg= "LightCyan3").place(x=400, y=0, width=1000, height=500)
            lbl.lift(fondo)
            lbl1.lift(fondo)
            lbl2.lift(fondo)
            lbl3.lift(fondo)
            lbl4.lift(fondo)
            lbl5.lift(fondo)
            parte='176A1-A4602'
        elif m =='185H0A4600' and sw == '185F1A4600':# IZQUIERDO negro 8 funciones
            numSwitch=8
            ruta= resource_path("186A1-A4600.png")
            foto= PhotoImage(file=ruta) 
            imgparte()
            fondo = Label(frame3, image=foto, bg= "LightCyan3").place(x=400, y=0, width=1000, height=500)
            frame8input()
            izne8fun()
            lbl.lift(fondo)
            lbl1.lift(fondo)
            lbl2.lift(fondo)
            lbl3.lift(fondo)
            lbl4.lift(fondo)
            lbl5.lift(fondo)
            lbl6.lift(fondo)
            lbl7.lift(fondo)
            parte='186A1-A4600'
        elif m =='175H0A4600' and sw == '175F1A4600':# derecho negro 8 funciones
            numSwitch=8
            ruta= resource_path("176A1-A4600.png")
            foto= PhotoImage(file=ruta) 
            imgparte()
            fondo = Label(frame3, image=foto, bg= "LightCyan3").place(x=400, y=0, width=1000, height=500)
            frame8input()
            derne8func()
            lbl.lift(fondo)
            lbl1.lift(fondo)
            lbl2.lift(fondo)
            lbl3.lift(fondo)
            lbl4.lift(fondo)
            lbl5.lift(fondo)
            lbl6.lift(fondo)
            lbl7.lift(fondo)
            parte='176A1-A4600'
        elif m =='185H0A0000' and sw == '185F1A0001':# Izquierdo negro 8 funciones H60
            numSwitch=8
            ruta= resource_path("H60.png")
            foto= PhotoImage(file=ruta) 
            imgparte()
            fondo = Label(frame3, image=foto, bg= "LightCyan3").place(x=400, y=0, width=1000, height=500)
            frame8input()
            izH60()
            lbl.lift(fondo)
            lbl1.lift(fondo)
            lbl2.lift(fondo)
            lbl3.lift(fondo)
            lbl4.lift(fondo)
            lbl5.lift(fondo)
            lbl6.lift(fondo)
            lbl7.lift(fondo)
            parte='187A1-D4180'
        elif m == '185H0A4902' and sw == '185F1A4902':#Izquierdo negro 10 funciones
            numSwitch=10
            ruta= resource_path("186A1-A4902.png")
            foto= PhotoImage(file=ruta) 
            imgparte()
            fondo = Label(frame3, image=foto, bg= "LightCyan3").place(x=400, y=0, width=1000, height=500)
            frame10input()
            izneg10func()
            lbl.lift(fondo)
            lbl1.lift(fondo)
            lbl2.lift(fondo)
            lbl3.lift(fondo)
            lbl4.lift(fondo)
            lbl5.lift(fondo)
            lbl6.lift(fondo)
            lbl7.lift(fondo)
            lbl8.lift(fondo)
            lbl9.lift(fondo)
            parte='186A1-A4902'
        elif m == '175H0A4902' and sw == '175F1A4902':#Derecho negro 10 funciones
            numSwitch=10
            ruta= resource_path("176A1-A4902.png")
            foto= PhotoImage(file=ruta) 
            imgparte()
            fondo = Label(frame3, image=foto, bg= "LightCyan3").place(x=400, y=0, width=1000, height=500)
            frame10input()
            derneg10func()
            lbl.lift(fondo)
            lbl1.lift(fondo)
            lbl2.lift(fondo)
            lbl3.lift(fondo)
            lbl4.lift(fondo)
            lbl5.lift(fondo)
            lbl6.lift(fondo)
            lbl7.lift(fondo)
            lbl8.lift(fondo)
            lbl9.lift(fondo)
            parte='176A1-A4902'
        else:
            messagebox.showerror(title="Error", message="Asegurate de escanear los codigos en el orden correcto")               
            
 
    okbutton = Button(frame2, text="OK", bg="green3" ,  command= lambda:[codigos()],font=("Arial CE", 12 ))
    okbutton.place(x=1270, y=40, width=50, height=50)
    #BOTON PARA LIMPIAR LOS INPUTS
    cleanbutton = Button(frame2, text="LIMPIAR", bg="cyan3" , fg="IndianRed4", command= lambda:[cleanEntry()],font=("Arial CE", 12 ))
    cleanbutton.place(x=640, y=40, width=70, height=50)
    
    
def insertdb():
    global noSwitch, noMotor, parte, date, mydb, current_time, count, o, operario
    m=noMotor.get()
    sw=noSwitch.get()
    o= int(operario.get())
    try:
        mydb  = mysql.connector.connect(user="root", password="Navaroot123",
                                    host="localhost", database="switches", port="3306")
        mycursor = mydb.cursor()
        sql = "INSERT INTO valores (CodigoSw, CodigoMot, CodigoFin, FechaProduc, HoraProduc, Operario) VALUES (%s,%s,%s,%s,%s,%s)"
        val = (sw, m, parte+'-'+str(count), date , current_time,o)
        mycursor.execute(sql, val)
        mydb.commit()

        #print(mycursor.rowcount, "Values inserted succesfull.")
    except mysql.connector.Error as error:
        #print("Failed to insert values into Valores table {}".format(error))
        messagebox.showerror(title="Error", message="Algo salio mal, no se guardaron los datos correctamente en la Base de Datos")

    finally:
        if mydb.is_connected():
            mydb.close()
            print("MySQL connection is closed")
            
            
def cleanEntry():
        noMotor.delete(0, 'end')
        noSwitch.delete(0, 'end')    
        
         
def clean():
    global s0, s1, s2, s3, s4, s5, s6, s7, s8, s9, numSwitch,foto, frame4, frame5, frame6, frame3, lbl, lbl1
    desaparecer(lbl)
    desaparecer(lbl1)
    desaparecer(lbl2)
    desaparecer(lbl3)
    desaparecer(lbl4)
    desaparecer(lbl5)
    th2 = threading.Thread(target=imgValidation, daemon= True)
    th2.start()
    foto=None
    s0 = s1 =s2 = s3 = s4 = s5 = s6 = s7 = s8 = s9 = False
    noMotor.delete(0, 'end')
    noSwitch.delete(0, 'end')
    if numSwitch == 6:
        desaparecer(frame4)
    elif numSwitch ==8:
        desaparecer(frame5)
        desaparecer(lbl6)
        desaparecer(lbl7)
    else:
        desaparecer(frame6)
        desaparecer(lbl6)
        desaparecer(lbl7)
        desaparecer(lbl8)
        desaparecer(lbl9)
    numSwitch = 0
    
    
def window3():
    global win2
    win3=tk.Toplevel(ROOT)#se creo nueva ventana de ROOT 
    win3.title("Industrias DMU S.A DE C.V") 
    win3.configure(bg="lawn green") 
    ancho_ventana = 400
    alto_ventana = 200
    x_ventana = win3.winfo_screenwidth() // 2 - ancho_ventana // 2
    y_ventana = win3.winfo_screenheight() // 2 - alto_ventana // 2
    posicion = str(ancho_ventana) + "x" + str(alto_ventana) + "+" + str(x_ventana) + "+" + str(y_ventana)
    win3.geometry(posicion)
    win3.resizable(0,0)
    lbl = Label(win3, text="¡VALIDACION EXITOSA!", anchor="center",font=("Arial CE", 20), bg="lawn green")
    lbl.place(x=50, y=20, width=300, height=60)
    btnetiqueta = Button(win3, text="Imprimir codigo de barras", command= lambda:[insertdb(),clean(),impresionbarcode(),win3.destroy()], bg="green3" ,font=("Arial CE", 15 )) 
    btnetiqueta.place(x=50,y=100, width=300, height=60)
    
    
def imgValidation():
    global resize_check,st1, st0, st2, st3, st4, st5 ,img0, img1, img2, img3, img4, img5, img6, img7, img8, img9, numSwitch, s0, s1, s2, s3, s4, s5, s6, s7, s8, s9
    ruta= resource_path("SinCorriente.png")
    img = Image.open(ruta)
    resizeimg = img.resize((80, 80))
    s0 = s1 =s2 = s3 = s4 = s5 = s6 = s7 = s8 = s9 = False
    img0 = ImageTk.PhotoImage(resizeimg)
    img1 = ImageTk.PhotoImage(resizeimg)
    img2 = ImageTk.PhotoImage(resizeimg)
    img3 = ImageTk.PhotoImage(resizeimg)
    img4 = ImageTk.PhotoImage(resizeimg)
    img5 = ImageTk.PhotoImage(resizeimg)
    img6 = ImageTk.PhotoImage(resizeimg)
    img7 = ImageTk.PhotoImage(resizeimg)
    img8 = ImageTk.PhotoImage(resizeimg)
    img9 = ImageTk.PhotoImage(resizeimg)
    ruta= resource_path("check.png")
    i = Image.open(ruta)
    resize_check = i.resize((80, 80))
    while(s0 == False or s1==  False or  s2==  False or s3==  False or s4==  False or s5== False or s6== False or s7== False or s8== False or s9== False):
        if st0 == True:
            img0 = ImageTk.PhotoImage(resize_check)
            s0=True
        elif st1 == True:
            img1 = ImageTk.PhotoImage(resize_check)
            s1=True
        elif st2 == True:
            img2 = ImageTk.PhotoImage(resize_check)
            s2=True
        elif st3 == True:
            img3 = ImageTk.PhotoImage(resize_check)
            s3=True
        elif st4 == True:
            img4 = ImageTk.PhotoImage(resize_check)
            s4=True
        elif st5 == True:
            img5 = ImageTk.PhotoImage(resize_check)
            s5=True
        elif numSwitch==6 and s0 == True and s1== True and  s2== True and s3== True and s4== True and s5== True:
            window3()
            break 
        elif st6 == True:
            img6 = ImageTk.PhotoImage(resize_check)
            s6=True
        elif st7 == True:
            img7 = ImageTk.PhotoImage(resize_check)
            s7=True  
        elif numSwitch==8 and s0 == True and s1== True and  s2== True and s3== True and s4== True and s5== True and s6== True and s7== True:
            window3()
            break 
        elif st8 == True:
            img8 = ImageTk.PhotoImage(resize_check)
            s8=True
        elif st9 == True:
            img9 = ImageTk.PhotoImage(resize_check)
            s9=True
            window3()
            break
        
    return img0, img1, img2, img3, img4, img5, img6, img7, img8, img9


def onStateChange(self, state):
    global st1, st0, st2, st3, st4, st5, st6, st7, st8, st9, digitalInput0, digitalInput1, digitalInput2, digitalInput3, digitalInput4, digitalInput5, digitalInput6, digitalInput7, digitalInput8, digitalInput9
    in0= digitalInput0.getChannel()
    in1= digitalInput1.getChannel()
    in2= digitalInput2.getChannel()
    in3= digitalInput3.getChannel()
    in4= digitalInput4.getChannel()
    in5= digitalInput5.getChannel()
    in6= digitalInput6.getChannel()
    in7= digitalInput7.getChannel()
    in8= digitalInput8.getChannel()
    in9= digitalInput9.getChannel()
    st0 = st1 =st2 = st3 = st4 = st5 = st6 = st7 = st8 = st9 = False
    if state != 0 :
        if self.getChannel() == in0:
            st0=True
        elif self.getChannel() == in1:
            st1=True
        elif self.getChannel() == in2:
            st2=True
        elif self.getChannel() == in3:
            st3=True
        elif self.getChannel() == in4:
            st4=True
        elif self.getChannel() == in5:
            st5=True
        elif self.getChannel() == in6:
            st6=True
        elif self.getChannel() == in7:
            st7=True
        elif self.getChannel() == in8:
            st8=True
        elif self.getChannel() == in9:
            st9=True
    else:
        pass
    
    
def phidgetChanels():
    global digitalInput0, digitalInput1, digitalInput2, digitalInput3, digitalInput4, digitalInput5, digitalInput6, digitalInput7, digitalInput8, digitalInput9
    
    digitalInput0 = DigitalInput()
    digitalInput1 = DigitalInput()
    digitalInput2 = DigitalInput()
    digitalInput3 = DigitalInput()
    digitalInput4 = DigitalInput()
    digitalInput5 = DigitalInput()
    digitalInput6 = DigitalInput()
    digitalInput7 = DigitalInput()
    digitalInput8 = DigitalInput()
    digitalInput9 = DigitalInput()

    digitalInput0.setDeviceSerialNumber(537128)
    digitalInput0.setChannel(0)
    digitalInput1.setDeviceSerialNumber(537128)
    digitalInput1.setChannel(1)
    digitalInput2.setDeviceSerialNumber(537128)
    digitalInput2.setChannel(2)
    digitalInput3.setDeviceSerialNumber(537128)
    digitalInput3.setChannel(3)
    digitalInput4.setDeviceSerialNumber(537128)
    digitalInput4.setChannel(4)
    digitalInput5.setDeviceSerialNumber(537128)
    digitalInput5.setChannel(5)
    digitalInput6.setDeviceSerialNumber(537128)
    digitalInput6.setChannel(6)
    digitalInput7.setDeviceSerialNumber(537128)
    digitalInput7.setChannel(7)
    digitalInput8.setDeviceSerialNumber(537128)
    digitalInput8.setChannel(8)
    digitalInput9.setDeviceSerialNumber(537128)
    digitalInput9.setChannel(9)

    digitalInput0.setOnStateChangeHandler(onStateChange)
    digitalInput1.setOnStateChangeHandler(onStateChange)
    digitalInput2.setOnStateChangeHandler(onStateChange)
    digitalInput3.setOnStateChangeHandler(onStateChange)
    digitalInput4.setOnStateChangeHandler(onStateChange)
    digitalInput5.setOnStateChangeHandler(onStateChange)
    digitalInput6.setOnStateChangeHandler(onStateChange)
    digitalInput7.setOnStateChangeHandler(onStateChange)
    digitalInput8.setOnStateChangeHandler(onStateChange)
    digitalInput9.setOnStateChangeHandler(onStateChange)

    digitalInput0.openWaitForAttachment(5000)
    digitalInput1.openWaitForAttachment(5000)
    digitalInput2.openWaitForAttachment(5000)
    digitalInput3.openWaitForAttachment(5000)
    digitalInput4.openWaitForAttachment(5000)
    digitalInput5.openWaitForAttachment(5000)
    digitalInput6.openWaitForAttachment(5000)
    digitalInput7.openWaitForAttachment(5000)
    digitalInput8.openWaitForAttachment(5000)
    digitalInput9.openWaitForAttachment(5000)

count=0
def impresionbarcode():
    global parte, count, code
    if count == count:
        count += 1
        code='PartNo.'+parte+'-'+str(count)
        if count==1000:
            count=0
    rv = BytesIO()
    Code39(str(), writer=ImageWriter()).write(rv)
    ruta= resource_path("datacode.png")
    with open(ruta, 'wb') as f:
        Code39(code, writer=ImageWriter(),add_checksum=False).write(f)
    
    HORZRES = 8
    VERTRES = 10
    LOGPIXELSX = 100
    LOGPIXELSY = 100
    PHYSICALWIDTH = 110
    PHYSICALHEIGHT = 10 #ancho
    PHYSICALOFFSETX = 10 #margen de izquierda
    PHYSICALOFFSETY = 10 #margen de arriba
    printer_name = win32print.GetDefaultPrinter ()
    file_name = "datacode.png"
    hDC = win32ui.CreateDC ()
    hDC.CreatePrinterDC (printer_name)
    printable_area = hDC.GetDeviceCaps (HORZRES), hDC.GetDeviceCaps (VERTRES)
    printer_size = hDC.GetDeviceCaps (PHYSICALWIDTH), hDC.GetDeviceCaps (PHYSICALHEIGHT)
    printer_margins = hDC.GetDeviceCaps (PHYSICALOFFSETX), hDC.GetDeviceCaps (PHYSICALOFFSETY)
    bmp = Image.open (file_name)
    if bmp.size[0] > bmp.size[1]:
        bmp = bmp.rotate (360)
    ratios = [1.0 * printable_area[0] / bmp.size[0], 1.0 * printable_area[1] / bmp.size[1]]
    scale = min (ratios)
    hDC.StartDoc (file_name)
    hDC.StartPage ()
    dib = ImageWin.Dib (bmp)
    scaled_width, scaled_height = [int (scale * i) for i in bmp.size]
    x1 = int ((printer_size[0] - scaled_width) / 2)
    y1 = int ((printer_size[1] - scaled_height) / 2)
    x2 = x1 + scaled_width
    y2 = y1 + scaled_height
    dib.draw (hDC.GetHandleOutput (), (x1, y1, x2, y2))
    os.remove("datacode.png") 
    hDC.EndPage ()
    hDC.EndDoc ()
    hDC.DeleteDC ()


def desaparecer(widget): 
    widget.place_forget() 
        
       
if __name__ == "__main__":
    
    ROOT = tk.Tk()
    ancho_ventana = 400
    alto_ventana = 200
    ruta= resource_path("dmu.ico")
    ROOT.iconphoto(True, tk.PhotoImage(file=ruta))
    x_ventana = ROOT.winfo_screenwidth() // 2 - ancho_ventana // 2
    y_ventana = ROOT.winfo_screenheight() // 2 - alto_ventana // 2
    posicion = str(ancho_ventana) + "x" + str(alto_ventana) + "+" + str(x_ventana) + "+" + str(y_ventana)
    ROOT.geometry(posicion)
    ROOT.resizable(0,0)
    APP = Pasword(parent=ROOT)
    
    #HILOS PARA EJECUTAR LAS FUNCIONES A LA PAR DEL PRINCIPAL
    th = threading.Thread(target=imgValidation, daemon=True)
    th.start()
    th1 = threading.Thread(target=phidgetChanels, daemon=True)
    th1.start()
    th1.join()
    APP.mainloop()