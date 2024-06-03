
import os
import time

import numpy as np
import pandas as pd
import re
import json
from datetime import datetime
import time
import random

#Creacion del archivo de log
tlog = open("log.txt",'w')
fecha_actual = datetime.now().strftime("%d%m%Y")
tlog.write("--------------  INICIO DE LOGS " +fecha_actual+"  -------------- \n")
def union_csv():
    raiz = r'C:\Users\jackson.calderon\Documents\Python Proyects\Scraping\limpieza'
    archivos_csv = [archivo for archivo in os.listdir(raiz) if archivo.endswith('.csv')]
    try:
        os.remove('Archivo_temp1.csv')
        os.remove('Archivo_temp2.csv')
    except:
        print('No se encontro alguno de los archivos a borrar')

    #Leer y guardar cada archivo csv y almacenarlo en una lista de Dataframes
    dataframes=[]
    for archivo in archivos_csv:
        ruta_completa = os.path.join(raiz, archivo)
        df = pd.read_csv(ruta_completa)
        tlog.write("\nlineas por cada archivo: "+archivo+str(df.shape))
        #Print para depurar la cantidad de filas
        #print(archivo, df.shape)
        dataframes.append(df)

    #Unir los DataFrames en uno solo
    merged_df = pd.concat(dataframes, ignore_index=True)
    #Guardar el Dataframe unido en un nuevo archivo CSV
    merged_df.to_csv('Archivo_temp1.csv',index =False)

    print("Archivos CSV unidos correctamente.")


def limpieza():
    try:
        os.remove('Archivo_temp2.csv')
    except:
        print('No se encontro el Archivo_temp2.csv')
    df = pd.read_csv('Archivo_temp1.csv')

    #Identificar los nombres de las columnas
    print(df.columns)
    N_lineas_temp1=len(df)
    tlog.write("\n\n"+(" ---- " *3) +" Cabeceras "+ (" ---- " *3) )
    tlog.write("\nColumnas del Archivo_temp1.csv\n " + str(df.columns))


    #Comprobar los cantidad de filas y columnas del archivo temp1
    print("Cantidad de filas en temp1: "+str(df.shape))
    tlog.write("\n\n" + (" ---- " * 3) + " Datos Lineas " + (" ---- " * 3))
    tlog.write("\nCantidad lineas temp1: "+str(df.shape))

    #Valores nulos o NaN en car_model
    cant_nulos_car_model = df['car_model'].isnull().sum()
    tlog.write("\nCantidad de lineas nulas de car_model: " + str(cant_nulos_car_model))
    filas_antes_car_model = len(df)

    #Limpieza campos columna car_model
    df['car_model'] = df['car_model'].str.replace(r'^[^a-zA-Z0-9]+', '', regex=True)
    df['car_model'] = df['car_model'].replace(r'(?i).*swift.*', 'Suzuki Swift', regex=True)
    df['car_model'] = df['car_model'].replace(r'(?i).*onix.*', 'Chevrolet Onix', regex=True)
    df['car_model'] = df['car_model'].replace(r'(?i).*mazda 2.*', 'Mazda 2', regex=True)
    df['car_model'] = df['car_model'].replace(r'^(?i)\s*Onix.*', 'Chevrolet Onix', regex=True)
    df['car_model'] = df['car_model'].replace(r'^(?i)\s*Chevrolet Onix.*', 'Chevrolet Onix', regex=True)
    df['car_model'] = df['car_model'].replace(r'^(?i)\s*Mazda 2.*', 'Mazda 2', regex=True)
    df['car_model'] = df['car_model'].replace(r'^(?i)\s*Duster.*', 'Renault Duster', regex=True)
    df['car_model'] = df['car_model'].replace(r'^(?i)\s*Renault Duster.*', 'Renault Duster', regex=True)
    df['car_model'] = df['car_model'].replace(r'^(?i)\s*Suzuki Swfit Hibrido.*', 'Suzuki Swift', regex=True)

    #df['car_model'] = df['car_model'].replace(r'^(?i)\s*Suzuki Swift.*', 'Suzuki Swift', regex=True)
    df['car_model'] = df['car_model'].replace(r'^(?i)\s*Corolla.*', 'Toyota Corolla', regex=True)
    df['car_model'] = df['car_model'].replace(r'^(?i)\s*Toyota Corolla.*', 'Toyota Corolla', regex=True)

    df['car_model'] = df['car_model'].replace(r'^(?i)Chevrolet\s+Onix\s+Rs', np.nan , regex=True)
    df['car_model'] = df['car_model'].replace(r'^(?i)Chevrolet\s+Ónix\s+Ltz\s+1\.0cc\s+Turbo\s+Tp\s+Aa', np.nan, regex=True)
    df['car_model'] = df['car_model'].replace(r'^(?i)Nissan\s+Qashqai\s+2\.0\s+Exclusive$', np.nan, regex=True)
    df['car_model'] = df['car_model'].replace(r'^(?i)Nissan\s+Qashqai\s+2\.0\s+Exclusive$', np.nan, regex=True)
    df['car_model'] = df['car_model'].replace(r'^(?i)\s*Oroch.*', np.nan, regex=True)
    df['car_model'] = df['car_model'].replace(r'(?i)^Renault\s+Logan\s+\S+.*$', np.nan, regex=True)
    df['car_model'] = df['car_model'].replace(r'(?i)^Renault\s+Oroch\s+\S+.*$', np.nan, regex=True)
    df['car_model'] = df['car_model'].replace(r'(?i)(.*\b)Sandero(\b.*)', np.nan, regex=True)
    df['car_model'] = df['car_model'].replace(r'(?i)(.*\b)stepway(\b.*)', np.nan, regex=True)
    df['car_model'] = df['car_model'].replace(r'(?i)(.*\b)Cruiser(\b.*)', np.nan, regex=True)
    df['car_model'] = df['car_model'].replace(r'^(?i)Toyota$', np.nan, regex=True)
    df['car_model'] = df['car_model'].replace(r'^(?i)Suzuki$', np.nan, regex=True)
    df['car_model'] = df['car_model'].replace(r'^(?i)Renault$', np.nan, regex=True)

    #df['car_model'] = df['car_model'].replace(r'(?i)\bSwift\b','Suzuki Swift', regex=True)
    #df['car_model'] = df['car_model'].replace(r'^(?i)\sRenault\s+Logan(?:\s+\S+)*$', np.nan, regex=True)


    #Elimina en car_model basado en chevrolet Onix Rs
    #df = df[~df['car_model'].str.contains(r'\b(Renault Oroch|Chevrolet Onix Rs)\b', case=False, regex=True)]


    #Elimina valores nulos basado en car_model vacios o NaN
    df = df.dropna(subset=['car_model'])

    #Cantidad de lineas despues de borrar x car_model
    print("\nCantidad de lineas despues de drop en car_model: " + str(df.shape))
    filas_despues_car_model = N_lineas_temp1 - len(df)
    print("Cantidad de lineas eliminadas de car_model: " + str(filas_despues_car_model))
    tlog.write("\nCantidad de lineas eliminadas de car_model: " + str(filas_despues_car_model))

    #Limpieza de datos en la columna price
    df['price'] = df['price'].replace(r'(\d)% OFF','', regex=True)

    #modificacion de los colores que tienen 0 y vacio
    df['colour'] = df['colour'].replace({'0':np.nan,'':np.nan})

    #Eliminacion de valores nulos en colour
    cant_nulos_colour = df['colour'].isnull().sum()
    tlog.write("\nCantidad de lineas nulas de colour: " + str(cant_nulos_colour))
    df = df.dropna(subset=['colour'])
    print("\nCantidad de lineas despues de drop en colour: " + str(df.shape))
    filas_despues_colour = N_lineas_temp1 - filas_despues_car_model - len(df)
    print("Cantidad de lineas eliminadas de colour: " + str(filas_despues_colour))
    tlog.write("\nCantidad de lineas eliminadas de colour: " + str(filas_despues_colour))

    N_lineas_temp2 = len(df)
    N_lineas_eliminadas = N_lineas_temp1 - N_lineas_temp2
    print("\nSe eliminaron un total de: ", N_lineas_eliminadas)
    tlog.write(f"\nSe eliminaron un total de: {N_lineas_eliminadas}")

    # Guardar el DataFrame modificado en un nuevo archivo CSV
    df.to_csv('Archivo_temp2.csv', index=False)
    print("Cantidad de filas en temp2: " + str(df.shape))
    tlog.write(f"\nCantidad de filas exitentes en temp2: {df.shape}")


    #Mostrar todas las columnas
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    tlog.write("\n\n" + (" ---- " * 3) + " head de las 10 primeras lineas " + (" ---- " * 3)+"\n")
    tlog.write(str(df.head(10)))
    tlog.write("\n\n" + (" ---- " * 3) + " tail de las 10 ultimas lineas " + (" ---- " * 3) + "\n")
    tlog.write(str(df.tail(10)))


union_csv()
limpieza()

tlog.close()

