#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  ejercicio_FINAL.py

import requests
import datetime
from datetime import timedelta
import sqlite3
from itertools import chain
from collections import defaultdict


ventas, gastos = {}, {}
suma_ventas, suma_gastos = 0, 0
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
 
 
def agregar_a_database(diccionario_ventas, diccionario_gastos):
        ''' esta función guardaria los datos (unificando fechas de ingresos y gastos)'''
        merge_dict = defaultdict(list)
        for k, v in chain(diccionario_ventas.items(), diccionario_gastos.items()):
                merge_dict[k].append(v)
                
        for k, v in merge_dict.items():
            try:
                cursor.execute("insert into informes values (?, ?, ?, ?)", (k, v[0], v[1], v[0]+v[1]))
                conn.commit()
                print('Datos agregados a la base \n\n')
            except IndexError:
                print('Por favor, debe agregar la contrapartida a la base de datos (si ingreso un monto de venta ingrese uno de gastos correspondiente a la misma fecha, y viceversa)')
            except sqlite3.IntegrityError:
                print('Usted esta tratando de agregar un registro correspondiente a una fecha ya disponible en la base de datos, por favor dirijase al apartado 4 \n')
                
                
def alarma():
        ''' esta función administra los mensajes y alertas'''
        balance = suma_ventas + suma_gastos
        if balance < 100000:
                print('ALERTA: balance se encuentra en deficit (<100000$)')
        elif balance > 100000 and balance < 150000:
                print('Balance se encuentra en equilibrio (>100000 & <150000$)')
        elif balance > 150000:
                print('Balance se encuentra en superavit (>150000$)')
        else:
                pass

def modificar_tabla():
    try:
        fecha = str(input('Inserte fecha del registor a modificar en tipo YYYY-MM-DD: ')).strip()
        fecha = datetime.datetime.strptime(fecha, '%Y-%m-%d')
        importe_venta = float(input('Ahora el importe de la venta: '))
        importe_gasto = float(input('Ahora el importe del gasto (en valor negativo): '))
        cursor.execute("UPDATE informes SET ventas = ?, gastos = ? where fecha = ?", (importe_venta, importe_gasto, fecha))
        print('Datos modificados correctamente.')
        
    except ValueError:
        print('Por favor, ingrese los datos corrector (formato fecha, venta en positivo, y gasto en negativo)')

def cotizaciones():
    r = requests.get('https://www.dolarsi.com/api/api.php?type=valoresprincipales')
    if r.status_code == 200:
        contenido = r.json()
    else:
        print('No se pudo establecer conexion')
    for cotizacion in contenido:
        print(cotizacion['casa']['nombre'] + '      Compra: ' + cotizacion['casa']['compra'] + '     Venta: ' + cotizacion['casa']['venta'] + '\n')
        
        
'''PROGRAMA GENERAL'''
 
try:
    conn = sqlite3.connect("negocio.db", isolation_level=None)
    cursor = conn.cursor()
    try:
        cursor.execute("create table informes (fecha DATETIME PRIMARY KEY, ventas NUMERIC, gastos NUMERIC, resultado NUMERIC)")
        conn.commit()
                        
    except sqlite3.OperationalError:
        print('Tabla informes disponible')
            
except Error:
        print('No se pudo establecer la conexión con la base de datos')
         
while True:
    welcome = str(input('Bienvenido al gestor de la base de datos productos, elija una opción: \n \ 1-Agregar venta y gasto \n \ 2-Arquear cuentas \n \ 3-Ver base de datos \n \ 4-Modificar base de datos \n \ 5-Ver cotización del dolar \n \ Exit-Salir del programa \n')).lower().strip()
    if welcome == '1':
        agregar_importe()
    elif welcome == '2':
        alarma()
    elif welcome == '3':
        db = cursor.execute('SELECT * from informes ORDER BY fecha ASC')
        for a in db:
            print(str(a) + '\n')
    elif welcome == '4':
        modificar_tabla()
    elif welcome == '5':
        cotizaciones()
    elif welcome == 'exit':
        break
    else:
        print('Seleccione una opcion valida (1, 2, 3, 4, 5 exit): ')
       
conn.close()
