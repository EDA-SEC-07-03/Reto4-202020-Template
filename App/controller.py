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
import config as cf
from DISClib.ADT.graph import gr
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from App import model
import csv

"""
El controlador se encarga de mediar entre la vista y el modelo.
Existen algunas operaciones en las que se necesita invocar
el modelo varias veces o integrar varias de las respuestas
del modelo en una sola respuesta.  Esta responsabilidad
recae sobre el controlador.
"""

# ___________________________________________________
#  Inicializacion del catalogo
# ___________________________________________________


def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # analyzer es utilizado para interactuar con el modelo
    analyzer = model.newAnalyzer()
    return analyzer


# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________


def loadServices(analyzer, servicesfile):
    """
    Carga los datos de los archivos CSV en el modelo.
    Se crea un arco entre cada par de estaciones que
    pertenecen al mismo servicio y van en el mismo sentido.

    addRouteConnection crea conexiones entre diferentes rutas
    servidas en una misma estación.
    """
    servicesfile = cf.data_dir + servicesfile
    input_file = csv.DictReader(open(servicesfile, encoding="utf-8"),
                                delimiter=",")
    for service in input_file:
        servicess = service['start station id']
        lastservice = service['end station id']
        tuplencio = (servicess, lastservice)
        mapa = mp.newMap()
        if (lastservice != None) and (servicess != None):
            if mp.contains(mapa, tuplencio) == False:   
                model.agregar_camino(analyzer, servicess, lastservice, service)
                lst = lt.newList()
                lt.addFirst(lst,int(service['tripduration']))
                mp.put(mapa, tuplencio, lst)
            else:
                z = int(service['tripduration'])
                lt.addFirst(mp.get(mapa,tuplencio), z)
                for i in mp.get(mapa,tuplencio):
                    x = lt.getElement(mp.get(mapa,tuplencio),i)
                    suma += x
                promedio = suma/lt.size(mp.get(mapa,tuplencio)) 
                gr.addEdge(analyzer,servicess, lastservice, promedio)
            
    
    return analyzer

# ___________________________________________________
#  Funciones para consultas
# ___________________________________________________


def top3_estaciones_de_llegada(Analyzer):
    "top3 estaciones de llegada"
    graph=Analyzer
    return model.top3_estaciones_de_llegada(graph)

def top3_estaciones_de_salida(Analyzer):
    "top3 estaciones de salida"
    graph=Analyzer
    return model.top3_estaciones_de_salida(graph)

def las3_menos_usadas(Analyzer):
    "3 estaciones menos usadas"
    graph=Analyzer
    return model.las3_menos_usadas(graph)

def totalStops(analyzer):
    """
    Total de paradas de autobus
    """
    return model.totalStops(analyzer)


def totalConnections(analyzer):
    """
    Total de enlaces entre las paradas
    """
    return model.totalConnections(analyzer)


def connectedComponents(analyzer):
    """
    Numero de componentes fuertemente conectados
    """
    return model.connectedComponents(analyzer)


def minimumCostPaths(analyzer, initialStation):
    """
    Calcula todos los caminos de costo minimo de initialStation a todas
    las otras estaciones del sistema
    """
    return model.minimumCostPaths(analyzer, initialStation)


def hasPath(analyzer, destStation):
    """
    Informa si existe un camino entre initialStation y destStation
    """
    return model.hasPath(analyzer, destStation)


def minimumCostPath(analyzer, destStation):
    """
    Retorna el camino de costo minimo desde initialStation a destStation
    """
    return model.minimumCostPath(analyzer, destStation)


def servedRoutes(analyzer):
    """
    Retorna el camino de costo minimo desde initialStation a destStation
    """
    maxvert, maxdeg = model.servedRoutes(analyzer)
    return maxvert, maxdeg

def ruta_resistencia(analyser, id_station, tiempo):
    x = model.ruta_resistencia(analyser, id_station,tiempo)
    return x


