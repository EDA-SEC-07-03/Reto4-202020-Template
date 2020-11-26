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
<<<<<<< HEAD
servicefile = '201801-4-citibike-tripdata.csv'
=======
servicefile = '201801-1-citibike-tripdata.csv'
>>>>>>> j.quirogar
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
    print("2- Cargar información de buses de singapur")
    print("3- funcion 4")
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
            print("\nCargando información de transporte de singapur ....")
            controller.loadServices(cont, servicefile)
        elif int(inputs[0]) == 3:
            tiempo = int(input("coloque el tiempo de resistencia: "))
            id_station = int(input("coloque el id de la estacion de su interes: "))
            y = controller.minimumCostPaths(cont, id_station)
            print(y)
        else:
            sys.exit(0)
menu_principal()
        


