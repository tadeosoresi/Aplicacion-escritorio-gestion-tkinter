#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  tkinter.py
#TCL/TK
import tkinter as tk
from tkinter import ttk #ttk agrega funcionalidades extras y cambia otras de tk
from tkinter import messagebox #Primer tipo retorna una cadena OK #Segundo tipo retorna bool

def agregar_importe():
    '''en esta funcion agregamos dia e importe a los diccionarios de ventas y gastos'''
    try:
        date_entry = str(input('Inserte fecha en tipo YYYY-MM-DD: ')).strip()
        date = datetime.datetime.strptime(date_entry, '%Y-%m-%d')
        importe_venta = float(input('Importe de la venta (0 si todavia no conoce el monto): '))
        importe_gasto = float(input('Ahora el importe del gasto en valor negativo (0 si todavia no conoce el monto): '))
        date_string = str(date)
       
        #aca tomamos datos
        if importe_venta >= 0 and importe_gasto <= 0:
            ventas[date_string] = importe_venta
            gastos[date_string] = importe_gasto
            global suma_ventas, suma_gastos
            suma_ventas, suma_gastos = sum(ventas.values()), sum(gastos.values())
            
            print(f'\n La tabla de ventas contiene\n {ventas} y el total de ventas del periodo es: {suma_ventas}$ \n \n La tabla de gastos contiene\n {gastos} y el total de gastos de periodo es: {suma_gastos}$ \n')
       
            agregar_a_database(ventas, gastos)
        else:
            print('Por favor, valor en positivo o cero para ventas y negstivo o cero para gastos.')
       
    except ValueError:
        print('Por favor, escriba fecha y montos en el formato pedido')
        
def seleccion():
    if lista.get(lista.curselection()) == '1-Agregar venta y gasto':
        agregar_importe()
    elif lista.get(lista.curselection()) == '2-Arquear cuentas':
        pass
    elif lista.get(lista.curselection()) == '3-Ver base de datos':
        pass
    elif lista.get(lista.curselection()) == '4-Modificar base de datos':
        pass
    elif lista.get(lista.curselection()) == '4-Modificar base de datos':
        pass
    else:
        root.destroy()
    

root = tk.Tk()
root.title('Gestor de ingresos y gastos')

etiqueta = ttk.Label(text='Bienvenido al gestor de la base de datos productos, elija una opción:')
etiqueta.place(x=20, y=20)

lista = tk.Listbox(width=30, height= 15, selectborderwidth=5, 
                  activestyle = 'dotbox',  
                  font = "Helvetica")
                  
lista.insert(0, '1-Agregar venta y gasto', "2-Arquear cuentas", "3-Ver base de datos", "4-Modificar base de datos",
                "5-Ver cotización del dolar", "Exit-Salir del programa")
lista.place(x=20, y=50)

boton_menu = tk.Button(text='Seleccionar', width=20, height=2, highlightcolor='blue', command=seleccion)
boton_menu.place(x=70, y=500)

root.config(width=1200, height=600)
root.mainloop()


'''import tkinter as tk
win=tk.Tk()
win.title("Aplicación TK")
win.mainloop()
cd raiz---> pyinstaller tkinter.py (ahi empieza a crear el distribuible)
guardar .pyw para que no abra con consola'''
