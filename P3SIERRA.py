from tkinter import *
from tkinter import messagebox
from tkinter import font
import serial
import serial.tools.list_ports
import keyboard

def LabelTitulo():
    titulo = Label(win,bd=0,text="CONTROL DE CORTE",relief="solid",font=myFont,fg="blue",width=7)
    titulo.grid(row=0,column=0,columnspan=7,stick=S+N+W+E)

def OnClickSystemCheck():
    
    valorsystemcheck = "8:0.0:0:"
    ser.write(valorsystemcheck.encode())

def CrearBotonSystemCheck():
    system_check = Button(win, text = "SYC (C)", font = myFont,command = OnClickSystemCheck, height =1 , width = 7,bg="green",fg="white")
    system_check.grid(row = 6, column=0)
    
def CrearBotonesMovimientoPrensaYSierra():
    
    global subir_prensa, bajar_prensa
    
    subir_prensa = Button(win, text = "⬆", font = myFont,command = OnClickBorrar, height =1 , width = 5,bg="orange",fg="white")
    subir_prensa.grid(row = 3, column=0)
    bajar_prensa = Button(win, text = "⬇", font = myFont,command = OnClickBorrarTodo, height =1 , width = 5)
    bajar_prensa.grid(row = 4, column=0)
    mover_prensa = Button(win, text = "MP (SP)", font = myFont,command = OnClickBorrarTodo, height =1 , width = 7,bg="green",fg="white")
    mover_prensa.grid(row = 2, column=0)
    mover_sierra = Button(win, text = "MS (P)", font = myFont,command = OnClickBorrarTodo, height =1 , width = 7,bg="sea green",fg="white")
    mover_sierra.grid(row = 5, column=0)
    mover_prensa.configure(command = lambda parte="PRENSA": OnClickMovimiento(parte))
    subir_prensa.configure(command = lambda dir="1", btn=subir_prensa, btn_2=bajar_prensa: OnClickDireccion(btn,btn_2,dir,"PRENSA"))
    bajar_prensa.configure(command = lambda dir="0", btn=bajar_prensa, btn_2=subir_prensa: OnClickDireccion(btn,btn_2,dir,"PRENSA"))
    mover_sierra.configure(command = lambda parte="SIERRA": OnClickMovimiento(parte))

def CrearCampoNumerico():
    campo = Label(win,bd=0,relief="solid",font=myFont,bg="white",fg="blue",width=5,textvariable=strcampo)
    campo.grid(row=1,column=1,columnspan=3,stick=S+N+W+E)
    
def SalirPrograma():
    win.quit()
    
def CrearDisplayNumerico():
    
    global botones
    
    contador = 0
    botones = []
    for i in range(3):
        for j in range(3):
            numero_boton = contador + j + 1
            nombre_boton = "boton_" + str(numero_boton)
            boton = Button(win, text = str(numero_boton), font = myFont, height =1 , width = 2)
            boton.configure(command = lambda btn=boton: OnClick(btn))
            boton.grid(row = i+3, column=j+1)
            botones.append(boton)
        contador += 3
        
def PonerPuntoyCero():
    
    global zero, punto
    
    zero = Button(win, text = "0", font = myFont,height =1 , width = 2)
    zero.grid(row = 6, column=2)
    zero.configure(command = lambda btn=zero: OnClick(btn))
    punto = Button(win, text = ".", font = myFont,height =1, width = 2)
    punto.grid(row = 6, column=3)
    punto.configure(command = lambda btn=punto: OnClick(btn))

def OnClick(btn):
    global valordecampo
    numero = btn.cget("text")
    if valordecampo == "" and numero == ".":
        valordecampo = "0."
        
    if numero == "." and "." in valordecampo:
        valordecampo = valordecampo
    else:
        valordecampo += numero
    strcampo.set(valordecampo)
    
def OnClickBorrar():
    global valordecampo
    valordecampo = valordecampo[:-1]
    strcampo.set(valordecampo)
    
def OnClickBorrarTodo():
    global valordecampo
    valordecampo = ""
    strcampo.set(valordecampo)
    
def OnClickDireccion(boton,boton_2,dir,parte_en_movimiento):
    global valordireccionprensa, valordirecciondisipadores
    
    orig_color = boton.cget("bg")
    orig_color_letra = boton.cget("fg")
    if orig_color != "orange":
        boton.config(relief=SUNKEN,bg="orange",fg="white")
        boton_2.config(relief=RAISED,bg=orig_color,fg=orig_color_letra)
    
    if parte_en_movimiento == "PRENSA":
        if dir == "1":
            valordireccionprensa = "1"
        else:
            valordireccionprensa = "0"
    elif parte_en_movimiento == "DISIPADORES":
        if dir == "1":
            valordirecciondisipadores = "0"
        else:
            valordirecciondisipadores = "1"
    
def OnClickMovimiento(parte_a_mover):
    global valordireccionprensa, valordirecciondisipadores, valordecampo
    
    if valordecampo == "" or valordecampo == "0.":
        valordecampo = "0.0"
    if "." not in valordecampo:
        valordecampo += ".0"
    if valordecampo[-1] == ".":
        valordecampo += "0"
        
    strcampo.set(valordecampo)
    if parte_a_mover == "PRENSA":
        valormovimiento = "2:" + valordecampo + ":" + valordireccionprensa + ":"
    elif parte_a_mover == "DISIPADORES":
        valormovimiento = "1:" + valordecampo + ":" + valordirecciondisipadores + ":"
    elif parte_a_mover == "SIERRA":
        valormovimiento = "3:" + valordecampo + ":" + valordireccionprensa + ":"
    
    #print (valormovimiento)
    cantidad = ser.write(valormovimiento.encode())
    
    #print (cantidad) 
    
def BotonBorrar():
    borrar = Button(win, text = "C", font = myFont,command = OnClickBorrar, height =1 , width = 2)
    borrar.grid(row = 2, column=1)
    borrar_todo = Button(win, text = "CE", font = myFont,command = OnClickBorrarTodo, height =1 , width = 2)
    borrar_todo.grid(row = 2, column=3)
    
def BotonesDireccion():
    
    global forward, reverse
    
    forward = Button(win, text = "⬅", font = myFont, height =1 , width = 5,bg="orange",fg="white")
    forward.grid(row = 3, column=5)
    reverse = Button(win, text = "➡", font = myFont, height =1 , width = 5)
    reverse.grid(row = 4, column=5)
    forward.configure(command = lambda dir="1", btn=forward, btn_2=reverse: OnClickDireccion(btn,btn_2,dir,"DISIPADORES"))
    reverse.configure(command = lambda dir="0", btn=reverse, btn_2=forward: OnClickDireccion(btn,btn_2,dir,"DISIPADORES"))
    
def BotonMovimiento():
    movimiento_disip = Button(win, text = "MD (D)", font = myFont, height =1 , width = 7, bg="green",fg="white")
    movimiento_disip.grid(row = 2, column=5)
    movimiento_disip.configure(command = lambda parte="DISIPADORES": OnClickMovimiento(parte))
    
def OnClickSierra():
    
    valorsierra = "6:0.0:0:"
    ser.write(valorsierra.encode())
    #print (valorsierra)
    
def OnClickComenzar():
    
    if valor_manual_o_auto == "4":
        valor_comenzar = valor_manual_o_auto + ":0.0:1:"
        ser.write(valor_comenzar.encode())
        #print (valor_comenzar)
    elif valor_manual_o_auto == "5":
        if valorlongitud != "" and valorpiezas != "":
            valor_comenzar = valor_manual_o_auto + ":" + valorlongitud + ":" + valorpiezas + ":"
            cantidad = ser.write(valor_comenzar.encode())
            #print (valor_comenzar)
            #print (cantidad)
        else:
            messagebox.showerror("Error","Los campos P y L no deben estar vacios")
    
def BotonSierra():
    bot_sierra = Button(win, text = "SAW (S)", font = myFont,command = OnClickSierra, height =1, width = 7)
    bot_sierra.grid(row = 6, column=6)
   
def OnClickPiezasYLongitud(campo_a_cambiar):
    
    global valorpiezas, valorlongitud, valorvelocidadz, valordecampo
    
    if campo_a_cambiar == "PIEZAS":
        if valordecampo != "":
            valor_entero = int(float(valordecampo))
            strpiezas.set(valor_entero)
            strcampo.set(valor_entero)
            valorpiezas = str(valor_entero)
    elif campo_a_cambiar == "LONGITUD":
        
        if valordecampo != "":
            if valordecampo == "0.":
                valordecampo = "0.0"
            if "." not in valordecampo:
                valordecampo += ".0"
            if valordecampo[-1] == ".":
                valordecampo += "0"
        
            strlongitud.set(valordecampo)
            valorlongitud = valordecampo
            
    elif campo_a_cambiar == "VELOCIDAD":
        if valordecampo != "":
            valor_entero = int(float(valordecampo))
            if valor_entero > 2000 or valor_entero < 250:
                messagebox.showerror("Error","El valor debe estar entre 250 y 2000")
            else:
                strvelocidadz.set(valor_entero)
                strcampo.set(valor_entero)
                valorvelocidadz = str(valor_entero)
                campo_a_enviar = "7:" + valorvelocidadz + ":1:"
                ser.write(campo_a_enviar.encode())
                #print(campo_a_enviar)
   
def BotonesCantidadCortes():
    
    global bot_num_piezas, bot_long_cortes, bot_vel_z
    
    bot_vel_z = Button(win, text = "VELZ (V)", font = myFont, command = OnClickPiezasYLongitud("VELOCIDAD"), height =1, width = 7)
    bot_vel_z.grid(row = 2, column=6)
    bot_num_piezas = Button(win, text = "PZS (N)", font = myFont, state = DISABLED, command = OnClickPiezasYLongitud("PIEZAS"), height =1, width = 7)
    bot_num_piezas.grid(row = 3, column=6)
    bot_long_cortes = Button(win, text = "LONG (L)", font = myFont, state = DISABLED,command = OnClickPiezasYLongitud("LONGITUD"),height = 1, width = 7)
    bot_long_cortes.grid(row = 4, column = 6)
    bot_num_piezas.configure(command = lambda campo = "PIEZAS": OnClickPiezasYLongitud(campo))
    bot_long_cortes.configure(command = lambda campo = "LONGITUD": OnClickPiezasYLongitud(campo))
    bot_vel_z.configure(command = lambda campo = "VELOCIDAD": OnClickPiezasYLongitud(campo))
    
def CrearCamposCortes():
    campo_vel_z = Label(win,bd=0,relief="solid",font=myFont,bg="white",fg="blue",width=7,textvariable=strvelocidadz)
    campo_vel_z.grid(row=2,column=7,stick=S+N+W+E)
    campo_num_piezas = Label(win,bd=0,relief="solid",font=myFont,bg="white",fg="blue",width=7,textvariable=strpiezas)
    campo_num_piezas.grid(row=3,column=7,stick=S+N+W+E)
    campo_long_cortes = Label(win,bd=0,relief="solid",font=myFont,bg="white",fg="blue",width=7,textvariable=strlongitud)
    campo_long_cortes.grid(row=4,column=7,stick=S+N+W+E)
   
def OnClickManAuto(tipo_de_movimiento,boton,boton_2):
    global valor_manual_o_auto,bot_num_piezas, bot_long_cortes
    
    orig_color = boton.cget("bg")
    orig_color_letra = boton.cget("fg")
    if orig_color != "orange":
        boton.config(relief=SUNKEN,bg="orange",fg="white")
        boton_2.config(relief=RAISED,bg=orig_color,fg=orig_color_letra)
    
    if tipo_de_movimiento == "manual":
        valor_manual_o_auto = "4"
        bot_long_cortes.configure(state="disabled")
        bot_num_piezas.configure(state="disabled")
    elif tipo_de_movimiento == "auto":
        valor_manual_o_auto = "5"
        bot_num_piezas.configure(state="normal")
        bot_long_cortes.configure(state="normal")
   
def BotonManualYAutomatico():
    
    global bot_automatico, bot_manual
    
    bot_automatico = Button(win, text = "AUT (A)", font = myFont,command = OnClickManAuto, height =1, width = 7)
    bot_automatico.grid(row = 1, column=6)
    bot_manual = Button(win, text = "MAN (M)", font = myFont, command = OnClickManAuto, height = 1, width = 7, bg = "orange", fg = "white")
    bot_manual.grid(row = 1, column = 7)
    bot_automatico.configure(command = lambda cod="auto",btn=bot_automatico, btn_2=bot_manual: OnClickManAuto(cod,btn,btn_2))
    bot_manual.configure(command = lambda cod="manual",btn=bot_manual, btn_2=bot_automatico: OnClickManAuto(cod,btn,btn_2))
    
def CrearBotonComenzar():
    
    global bot_comenzar
    
    bot_comenzar = Button(win, wraplength=140,text = "GO/STOP\n(ENTER)",font = myFontSmall,command = OnClickComenzar, height =2, width = 7, bg = "red", fg = "white")
    bot_comenzar.grid(row = 5, column=7, rowspan=2, columnspan=2,stick=S+N+W+E)
    
def CrearBotonSalir():
    bot_salir = Button(win, text="QUIT (Q)", font = myFont, command = SalirPrograma, height = 1, width = 7)
    bot_salir.grid(row = 0, column = 7)
    
def ChecarSerial():
    global ser, valorpiezas, valorlongitud, valorvelocidadz
    
    ports = list(serial.tools.list_ports.comports())
    
    for p in ports:
        if ser.port == p[0]:
            if not ser.isOpen():
                ser.open()
            break
        else:
            ser.close()
            strpiezas.set("")
            strlongitud.set("")
            strvelocidadz.set("250")
            valorpiezas = ""
            valorlongitud = ""
    win.after(1000,ChecarSerial)
    
def ControlTeclado():
    
    global forward, reverse, subir_prensa, bajar_prensa, botones, zero, punto, bot_automatico, bot_manual
    
    win.bind('<Left>', lambda e, dir="1", btn=forward, btn_2=reverse: OnClickDireccion(btn,btn_2,dir,"DISIPADORES"))
    win.bind('<Right>', lambda e, dir="0", btn=reverse, btn_2=forward: OnClickDireccion(btn,btn_2,dir,"DISIPADORES"))
    win.bind('<Up>',lambda e, dir="1", btn=subir_prensa, btn_2=bajar_prensa: OnClickDireccion(btn,btn_2,dir,"PRENSA"))
    win.bind('<Down>' ,lambda e, dir="0", btn=bajar_prensa, btn_2=subir_prensa: OnClickDireccion(btn,btn_2,dir,"PRENSA"))
    win.bind('<space>', lambda e, parte="PRENSA": OnClickMovimiento(parte))
    win.bind('<d>', lambda e,parte="DISIPADORES": OnClickMovimiento(parte))
    win.bind('<p>', lambda e,parte="SIERRA": OnClickMovimiento(parte))
    win.bind('<Return>', lambda e: OnClickComenzar())
    win.bind('<KP_Enter>', lambda e: OnClickComenzar())
    for boton in botones:
        win.bind('<KP_' + boton['text'] +'>', lambda e, btn = boton: OnClick(btn))
        win.bind('<KeyPress-' + boton['text']+ '>', lambda e, btn = boton: OnClick(btn))
    win.bind('<BackSpace>', lambda e: OnClickBorrar())
    win.bind('<b>', lambda e: OnClickBorrarTodo())
    win.bind('<KeyPress-0>', lambda e, btn = zero: OnClick(btn))
    win.bind('<KP_0>', lambda e, btn = zero: OnClick(btn))
    win.bind('<period>', lambda e, btn = punto: OnClick(btn))
    win.bind('<KP_Decimal>', lambda e, btn = punto: OnClick(btn))
    win.bind('<q>', lambda e: SalirPrograma())
    win.bind('<c>', lambda e: OnClickSystemCheck())
    win.bind('<s>', lambda e: OnClickSierra())
    win.bind('<n>', lambda e, campo = "PIEZAS": OnClickPiezasYLongitud(campo))
    win.bind('<l>', lambda e, campo = "LONGITUD": OnClickPiezasYLongitud(campo))
    win.bind('<v>', lambda e, campo = "VELOCIDAD": OnClickPiezasYLongitud(campo))
    win.bind('<m>', lambda e, cod="manual",btn=bot_manual, btn_2=bot_automatico: OnClickManAuto(cod,btn,btn_2))
    win.bind('<a>', lambda e, cod="auto",btn=bot_automatico, btn_2=bot_manual: OnClickManAuto(cod,btn,btn_2))
            
win = Tk()

myFont = font.Font(family = 'Helvetica', size = 36, weight = 'bold')
myFontSmall = font.Font(family = 'Helvetica', size = 23, weight = 'bold')

#ports = list(serial.tools.list_ports.comports())
#/dev/ttyACM0
ser = serial.Serial("/dev/ttyACM0", 9600,timeout=10)
strcampo = StringVar()
strpiezas = StringVar()
strlongitud = StringVar()
strvelocidadz = StringVar()
valordecampo = ""
valorpiezas = ""
valorlongitud = ""
valorvelocidadz = "250"
valordireccionprensa = "1"
valordirecciondisipadores = "0"
valor_manual_o_auto = "4"
strvelocidadz.set(valorvelocidadz)

bot_num_piezas = ""
bon_long_cortes = ""

win.title("Control Corte Moreno")
#win.geometry('1115x480')
w = 1115 # width for the Tk root
h = 480 # height for the Tk root

# get screen width and height
ws = win.winfo_screenwidth() # width of the screen
hs = win.winfo_screenheight() # height of the screen

# calculate x and y coordinates for the Tk root window
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)

# set the dimensions of the screen 
# and where it is placed
win.geometry('%dx%d+%d+%d' % (w, h, x, y))

#win.attributes("-fullscreen", True)

LabelTitulo()
CrearBotonesMovimientoPrensaYSierra()
CrearCampoNumerico()
CrearDisplayNumerico()
PonerPuntoyCero()
BotonBorrar()
BotonesDireccion()
BotonMovimiento()
BotonSierra()
BotonesCantidadCortes()
BotonManualYAutomatico()
CrearCamposCortes()
CrearBotonComenzar()
CrearBotonSalir()
CrearBotonSystemCheck()
ControlTeclado()

win.after(1000,ChecarSerial)
win.mainloop()

    

    
        