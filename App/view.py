"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 * Contribución de:
 *
 * Dario Correal
 *
 """


import sys
import config
from App import controller
from DISClib.ADT import stack
import timeit
from time import process_time
assert config

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Variables
# ___________________________________________________
servicefile = '201801-1-citibike-tripdata.csv'
initialStation = None
recursionLimit = 20000
# ___________________________________________________
#  Menu principal
# ___________________________________________________
def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información de biciletas")
    print("3- funcion 4")
    print("4- funcion 3")
    print("0-salir")
"""
Menu principal
"""
def menu_principal():
    while True:
        printMenu()
        inputs = input('Seleccione una opción para continuar\n>')
        
        if int(inputs[0]) == 1:
            print("\nInicializando....")
            cont = controller.init()
        elif int(inputs[0]) == 2:
            print("\nCargando información de bicicletas ....")
            controller.loadServices(cont, servicefile)
            
        elif int(inputs[0]) == 3:
            id_station = input("coloque el id de la estacion de su interes: ")
            tiempo = int(input("Ponga el tiempo de resistencia: "))
            id_station = input("coloque el id de la estacion de su interes: ")
            y = controller.ruta_resistencia(cont, id_station, tiempo)
            print(y)
        elif int(inputs[0]) == 4:
            estaciones_de_llegada= controller.top3_estaciones_de_llegada(cont)
            estaciones_de_salida = controller.top3_estaciones_de_salida(cont)
            estaciones_menos_usadas = controller.las3_menos_usadas(cont)
            print("El top 3 de estaciones de llegada",str(estaciones_de_llegada))
            print("El top 3 de estaciones de salida",str(estaciones_de_salida))
            print("El top 3 de las menos usadas",str(estaciones_menos_usadas))

            tiempo = int(input("Ponga el tiempo de resistencia: "))
            id_station = input("coloque el id de la estacion de su interes: ")
            y = controller.ruta_resistencia(cont, id_station, tiempo)
            print(y)
        else:
            sys.exit(0)
menu_principal()
        
