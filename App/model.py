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
import config
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dfs
from DISClib.Algorithms.Graphs import dfo
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
assert config

"""
En este archivo definimos los TADs que vamos a usar y las operaciones
de creacion y consulta sobre las estructuras de datos.
"""

# -----------------------------------------------------
#                       API
# -----------------------------------------------------
def newAnalyzer():
    """ Inicializa el analizador

   stops: Tabla de hash para guardar los vertices del grafo
   connections: Grafo para representar las rutas entre estaciones
   components: Almacena la informacion de los componentes conectados
   paths: Estructura que almancena los caminos de costo minimo desde un
           vertice determinado a todos los otros vértices del grafo
    """
    try:
        analyzer = {
                    'stations': None,
                    'connections': None,
                    'components': None,
                    'paths': None
                    }

        analyzer['stations'] = m.newMap(numelements=14000,
                                     maptype='PROBING',
                                     comparefunction=compareStopIds)

        analyzer['connections'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=14000,
                                              comparefunction=compareStopIds)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')


# Funciones para agregar informacion al grafo

def addStopConnection(analyzer, lastservice, servicess, service):
    """
    Adiciona las estaciones al grafo como vertices y arcos entre las
    estaciones adyacentes.

    Los vertices tienen por nombre el identificador de la estacion
    seguido de la ruta que sirve.  Por ejemplo:

    75009-10

    Si la estacion sirve otra ruta, se tiene: 75009-101
    """
    try:
        origin = servicess
        destination = lastservice
        addStation(analyzer, origin)
        time = str(service['tripduration'])
        addStation(analyzer, destination)
        addConnection(analyzer, origin, destination, time)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:addStopConnection')

def agregar_camino(analyser, initial_id, dest_id, server):
    time = int(server['tripduration'])
    addStation(analyser, initial_id)
    addStation(analyser, dest_id)
    addConnection(analyser, initial_id, dest_id, time)
    return analyser


def addStation(analyzer, stationid):
    """
    Adiciona una estación como un vertice del grafo
    """
    try:
        if not gr.containsVertex(analyzer['connections'], stationid):
            gr.insertVertex(analyzer['connections'], stationid)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:addstop')

def addConnection(analyzer, origin, destination, time):
    """
    Adiciona un arco entre dos estaciones
    """
    edge = gr.getEdge(analyzer['connections'], origin, destination)
    if edge is None:
        gr.addEdge(analyzer['connections'], origin, destination, time)
    return analyzer

# ==============================
# Funciones de consulta
# ==============================


def connectedComponents(analyzer):
    """
    Calcula los componentes conectados del grafo
    Se utiliza el algoritmo de Kosaraju
    """
    analyzer['components'] = scc.KosarajuSCC(analyzer['connections'])
    return scc.connectedComponents(analyzer['components'])


def minimumCostPaths(analyzer, initialStation):
    """
    Calcula los caminos de costo mínimo desde la estacion initialStation
    a todos los demas vertices del grafo
    """
    analyzer['paths'] = djk.Dijkstra(analyzer['connections'], initialStation)
    return analyzer


def hasPath(analyzer, destStation):
    """
    Indica si existe un camino desde la estacion inicial a la estación destino
    Se debe ejecutar primero la funcion minimumCostPaths
    """
    return djk.hasPathTo(analyzer['paths'], destStation)


def minimumCostPath(analyzer, destStation):
    """
    Retorna el camino de costo minimo entre la estacion de inicio
    y la estacion destino
    Se debe ejecutar primero la funcion minimumCostPaths
    """
    path = djk.pathTo(analyzer['paths'], destStation)
    return path


def totalStops(analyzer):
    """
    Retorna el total de estaciones (vertices) del grafo
    """
    return gr.numVertices(analyzer['connections'])


def totalConnections(analyzer):
    """
    Retorna el total arcos del grafo
    """
    return gr.numEdges(analyzer['connections'])


def servedRoutes(analyzer):
    """
    Retorna la estación que sirve a mas rutas.
    Si existen varias rutas con el mismo numero se
    retorna una de ellas
    """
    lstvert = m.keySet(analyzer['stations'])
    itlstvert = it.newIterator(lstvert)
    maxvert = None
    maxdeg = 0
    while(it.hasNext(itlstvert)):
        vert = it.next(itlstvert)
        lstroutes = m.get(analyzer['stations'], vert)['value']
        degree = lt.size(lstroutes)
        if(degree > maxdeg):
            maxvert = vert
            maxdeg = degree
    return maxvert, maxdeg

#///////////////////////////////////////////////////////#    
"///////////////////////////////////////////////////////"
#///////////////////////////////////////////////////////#

def top3_estaciones_de_llegada(analyzer):
    "retorna el nombre de top3 estaciones de llegada"
    lista_vertices=gr.vertices(analyzer["graph"])
    first_iterator=it.newIterator(lista_vertices)
    dic_estaciones={}
    while it.hasNext(first_iterator):
        estacion=it.next(first_iterator)
        viajes=gr.indegree(analyzer["graph"], estacion)
        dic_estaciones[estacion]=viajes
        estaciones= saber_los_mayores(dic_estaciones)
        rta_1 = buscar_info_estacion(estaciones[0],analyzer)
        rta_2 = buscar_info_estacion(estaciones[1],analyzer)
        rta_3 = buscar_info_estacion(estaciones[2],analyzer)
        rta = [rta_1["name"],rta_2["name"],rta_3["name"]]
        return rta
def top3_estaciones_de_salida(analyzer):
    "retorna el nombre de top3 estaciones de salida"
    lista_vertices=gr.vertices(analyzer["graph"])
    first_iterator=it.newIterator(lista_vertices)
    dic_estaciones={}
    while it.hasNext(first_iterator):
        estacion=it.next(first_iterator)
        viajes=gr.outdegree(analyzer["graph"], estacion)
        dic_estaciones[estacion]=viajes
        estaciones= saber_los_mayores(dic_estaciones)
        rta_1 = buscar_info_estacion(estaciones[0],analyzer)
        rta_2 = buscar_info_estacion(estaciones[1],analyzer)
        rta_3 = buscar_info_estacion(estaciones[2],analyzer)
        rta = [rta_1["name"],rta_2["name"],rta_3["name"]]
        return rta

def las3_menos_usadas(analyzer):
    "retorna el nombre de  top3 estaciones con menos uso"
    lista_vertices=gr.vertices(analyzer["graph"])
    first_iterator=it.newIterator(lista_vertices)
    dic_estaciones={}
    while it.hasNext(first_iterator):
        estacion=it.next(first_iterator)
        viajes=gr.degree(analyzer["graph"], estacion)
        dic_estaciones[estacion]=viajes
        estaciones= saber_los_menores(dic_estaciones)
        rta_1 = buscar_info_estacion(estaciones[0],analyzer)
        rta_2 = buscar_info_estacion(estaciones[1],analyzer)
        rta_3 = buscar_info_estacion(estaciones[2],analyzer)
        rta = [rta_1["name"],rta_2["name"],rta_3["name"]]
        return rta

    


# ==============================
# Funciones Help
# ==============================

def saber_los_mayores(dic):
    lista =list(dic.values())
    lista.sort()
    primer_mayor = lista[-1]
    segundo_mayor= lista[-2]
    tercer_mayor = lista[-3]
    listaa=[]
    for i in dic:
        if dic[i]== primer_mayor or dic[i]==segundo_mayor or dic[i]==tercer_mayor and dic[i]:
            listaa.append(i)
    rta=[listaa[0],listaa[1],listaa[2]]
    return rta


def saber_los_menores(dic):
    lista =list(dic.values())
    lista.sort()
    primer_mayor = lista[1]
    segundo_mayor= lista[2]
    tercer_mayor = lista[3]
    listaa=[]
    for i in dic:
        if dic[i]== primer_mayor or dic[i]==segundo_mayor or dic[i]==tercer_mayor and dic[i]:
            listaa.append(i)
    rta=[listaa[0],listaa[1],listaa[2]]
    return rta

def buscar_info_estacion(id,analyzer )
"busca info de la estacion"
infor= analyzer["info"]
entrada = m.get(infor, id)
valor= me.getValue(entrada) # me.get value no sta
return valor



#///////////////////////////////////////////////////////#    
"///////////////////////////////////////////////////////"
#///////////////////////////////////////////////////////#




def cleanServiceDistance(service):
    """
    En caso de que el archivo tenga un espacio en la
    distancia, se reemplaza con cero.
    """
    if int(service['tripduration']) == '':
        service['tripduration'] = 0


def formatVertex(service):
    """
    Se formatea el nombrer del vertice con el id de la estación
    seguido de la ruta.
    """
    name = service['start station name'] + '-'
    name = name + service['start station id']
    return name


# ==============================
# Funciones de Comparacion
# ==============================


def compareStopIds(stop, keyvaluestop):
    """
    Compara dos estaciones
    """
    stopcode = keyvaluestop['key']
    if (stop == stopcode):
        return 0
    elif (stop > stopcode):
        return 1
    else:
        return -1


def compareroutes(route1, route2):
    """
    Compara dos rutas
    """
    if (route1 == route2):
        return 0
    elif (route1 > route2):
        return 1
    else:
        return -1
# funciones del reto
def ruta_resistencia(grafo, id_station, tiempo):
    rta = dfs.DepthFirstSearch(grafo, id_station)
    return rta  

