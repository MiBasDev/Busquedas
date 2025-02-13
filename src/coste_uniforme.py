import heapq

def ucs(graph, start, goal):
    frontera = []  # Cola de prioridad (Heap)
    heapq.heappush(frontera, (0, start))  # (coste_acumulado, ciudad)
    visitados = set()
    ruta = {}
    costes = {start: 0}  # Coste acumulado desde el inicio

    output = []  # Lista para guardar el output en un archivo

    output.append(f"Inicio de la búsqueda UCS desde {start} hasta {goal}\n")
    output.append(f"C={{}}\nFrontera={{start}}\n")

    while frontera:
        coste_actual, ciudad_actual = heapq.heappop(frontera)

        # Si el nodo ya fue visitado, se omite
        if ciudad_actual in visitados:
            output.append(f"Se omite {ciudad_actual} porque ya fue explorado.\n")
            continue
        
        visitados.add(ciudad_actual)

        output.append(f"Explorando nodo: {ciudad_actual} con coste acumulado: {coste_actual}\n")
        output.append('C={' + ', '.join([f"{ciudad}({ruta.get(ciudad, 'inicio')})[{costes[ciudad]}]" for ciudad in visitados]) + '}')

        # Si hemos alcanzado el destino, terminamos la búsqueda
        if ciudad_actual == goal:
            output.append("\n --- Se ha alcanzado el destino. Terminando búsqueda. --- \n")
            break  

        nueva_frontera = []
        for vecino, coste in graph.get(ciudad_actual, []):
            nuevo_coste = coste_actual + coste
            if vecino not in costes or nuevo_coste < costes[vecino]:
                costes[vecino] = nuevo_coste
                heapq.heappush(frontera, (nuevo_coste, vecino))
                ruta[vecino] = ciudad_actual
                nueva_frontera.append(f"{vecino}({ciudad_actual})[{nuevo_coste}]")

        output.append(f"Frontera actualizada: {', '.join(nueva_frontera)}\n")

    camino, distancia = reconstruir_camino(ruta, start, goal), costes.get(goal, float('inf'))

    output.append(f"Ruta óptima encontrada: {' → '.join(camino)}\n")
    output.append(f"Distancia total: {distancia} km\n")

    # Descomentar para guardar la salida en un archivo de texto
    #with open("resultado_ucs.txt", "w", encoding="utf-8") as file:
    #    file.writelines("\n".join(output))

    for line in output:
        print(line) 
    
    return camino, distancia

def reconstruir_camino(ruta, start, goal):
    camino = []
    actual = goal
    while actual != start:
        camino.append(actual)
        actual = ruta.get(actual, start)  # Retrocede en la ruta
    camino.append(start)
    return list(reversed(camino))

# Grafo representando el problema
graph = {
    "Ourense": [("Ponferrada", 175), ("Benavente", 236)],
    "Ponferrada": [("Ourense", 175), ("León", 113), ("Benavente", 125)],
    "Benavente": [("Ponferrada", 125), ("León", 75), ("Valladolid", 112), ("Palencia", 112), ("Ourense", 236)],
    "León": [("Ponferrada", 113), ("Benavente", 75), ("Palencia", 131), ("Osorno", 121)],
    "Palencia": [("León", 131), ("Benavente", 112), ("Valladolid", 48), ("Osorno", 49), ("Burgos", 92)],
    "Valladolid": [("Benavente", 112), ("Palencia", 48), ("Aranda", 95)],
    "Osorno": [("Palencia", 49), ("León", 121), ("Burgos", 59)],
    "Burgos": [("Osorno", 59), ("Palencia", 92), ("Aranda", 84), ("Soria", 143), ("Logroño", 150)],
    "Logroño": [("Burgos", 150), ("Soria", 106)],
    "Aranda": [("Valladolid", 95), ("Burgos", 84), ("Osma", 58)],
    "Osma": [("Aranda", 58), ("Soria", 58), ("Calatayud", 140)],
    "Soria": [("Burgos", 143), ("Logroño", 106), ("Osma", 58), ("Calatayud", 91)],
    "Calatayud": [("Osma", 140), ("Soria", 91)]
}

# Ejecutamos el algoritmo
camino_optimo, distancia_total = ucs(graph, "Ourense", "Calatayud")
print("Ruta óptima:", " → ".join(camino_optimo))
print("Distancia total:", distancia_total, "km")
#print("El resultado ha sido guardado en 'resultado_ucs.txt'")
