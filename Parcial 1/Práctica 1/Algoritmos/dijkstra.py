import heapq
import networkx as nx
import matplotlib.pyplot as plt


# =============================================================================
# CASO DE USO: Red de Internet - Enrutamiento por menor latencia
# -----------------------------------------------------------------------------
# Jonathan Rodrigo Sánchez Rangel - 23110179 - 7E
# -----------------------------------------------------------------------------
# Escenario: Un paquete de datos sale desde tu PC (nodo "PC_Casa") y necesita
# llegar a un Servidor Web (nodo "Servidor"). En el camino existen varios
# routers y switches interconectados. Cada conexión tiene una latencia en
# milisegundos (ms). Dijkstra encuentra la ruta con MENOR latencia total.
#
# Nodos  → Dispositivos de red (PC, Routers, Switches, Servidor)
# Aristas → Conexiones entre dispositivos
# Pesos  → Latencia en milisegundos (ms)
# =============================================================================

def visualizar_dijkstra(grafo_dict, inicio, fin):

    # --- CONFIGURACIÓN DEL GRAFO ---
    G = nx.DiGraph()
    for nodo, vecinos in grafo_dict.items():
        for vecino, peso in vecinos.items():
            G.add_edge(nodo, vecino, weight=peso)

    # Layout manual para que la topología de red se vea ordenada
    pos = {
        'PC_Casa':   (-2,  0),
        'Router_A':  (-1,  1),
        'Router_B':  (-1, -1),
        'Switch_C':  ( 0,  1),
        'Switch_D':  ( 0, -1),
        'Router_E':  ( 1,  0.5),
        'Router_F':  ( 1, -0.5),
        'Servidor':  ( 2,  0),
    }

    plt.figure(figsize=(13, 7))

    # --- VARIABLES DEL ALGORITMO ---
    distancias = {nodo: float('inf') for nodo in G.nodes}
    distancias[inicio] = 0
    previos   = {nodo: None for nodo in G.nodes}
    cola      = [(0, inicio)]
    visitados = set()

    # --- FUNCIÓN DE DIBUJO ---
    def dibujar_estado(nodo_actual=None, vecinos_actuales=[], camino_final=[]):
        plt.cla()
        plt.title(
            f"Dijkstra — Red de Internet\n"
            f"Buscando ruta de menor latencia: {inicio}  →  {fin}",
            fontsize=12, fontweight='bold'
        )

        # Colores de nodos según su estado
        colores_nodos = []
        for n in G.nodes:
            if n in camino_final:
                colores_nodos.append('#32CD32')   # Verde  → en el camino óptimo
            elif n == nodo_actual:
                colores_nodos.append('#FFD700')   # Dorado → procesando ahora
            elif n in visitados:
                colores_nodos.append('#ADD8E6')   # Azul   → ya procesado
            else:
                colores_nodos.append('#D3D3D3')   # Gris   → sin explorar

        # Dibujar nodos
        nx.draw_networkx_nodes(G, pos, node_color=colores_nodos, node_size=1800)
        nx.draw_networkx_labels(G, pos, font_size=7, font_weight='bold')

        # Aristas base en gris
        nx.draw_networkx_edges(G, pos, edge_color='gray', arrows=True,
                               arrowsize=15, width=1.2)

        # Aristas que se están evaluando ahora (rojo)
        if nodo_actual:
            aristas_activas = [(nodo_actual, v) for v in vecinos_actuales
                               if G.has_edge(nodo_actual, v)]
            if aristas_activas:
                nx.draw_networkx_edges(G, pos, edgelist=aristas_activas,
                                       edge_color='red', width=2.5, arrows=True)

        # Camino final (verde)
        if camino_final:
            aristas_camino = list(zip(camino_final, camino_final[1:]))
            nx.draw_networkx_edges(G, pos, edgelist=aristas_camino,
                                   edge_color='#32CD32', width=3.5, arrows=True)

        # Pesos en las aristas (latencia en ms)
        labels_pesos = {(u, v): f"{d['weight']} ms"
                        for u, v, d in G.edges(data=True)}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels_pesos, font_size=7)

        # Latencia acumulada sobre cada nodo (en azul)
        pos_dist = {k: (v[0], v[1] + 0.18) for k, v in pos.items()}
        labels_dist = {
            n: (f"{distancias[n]} ms" if distancias[n] != float('inf') else "∞")
            for n in G.nodes
        }
        nx.draw_networkx_labels(G, pos_dist, labels=labels_dist,
                                font_color='blue', font_size=7)

        # Leyenda
        leyenda = (
            "⬛ Gris   = Sin explorar\n"
            "🟡 Dorado = Procesando\n"
            "🔵 Azul   = Ya procesado\n"
            "🟢 Verde  = Ruta óptima"
        )
        plt.gcf().text(0.01, 0.15, leyenda, fontsize=8,
                       verticalalignment='bottom',
                       bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

        plt.axis('off')
        plt.tight_layout()
        plt.pause(1.5)

    # --- BUCLE PRINCIPAL DE DIJKSTRA ---
    while cola:
        dist_actual, u = heapq.heappop(cola)

        dibujar_estado(
            nodo_actual=u,
            vecinos_actuales=list(grafo_dict[u].keys()) if u in grafo_dict else []
        )

        if u == fin:
            break

        if dist_actual > distancias[u]:
            continue

        visitados.add(u)

        if u in grafo_dict:
            for v, peso in grafo_dict[u].items():
                nueva_dist = dist_actual + peso
                if nueva_dist < distancias[v]:
                    distancias[v] = nueva_dist
                    previos[v] = u
                    heapq.heappush(cola, (nueva_dist, v))

    # --- RECONSTRUCCIÓN DEL CAMINO ÓPTIMO ---
    camino = []
    curr = fin
    if distancias[fin] != float('inf'):
        while curr is not None:
            camino.insert(0, curr)
            curr = previos[curr]

    # Resultado en consola
    print("\n" + "="*55)
    print("  RESULTADO — Red de Internet (Dijkstra)")
    print("="*55)
    print(f"  Origen  : {inicio}")
    print(f"  Destino : {fin}")
    print(f"  Latencia total mínima : {distancias[fin]} ms")
    print(f"  Ruta óptima : {' → '.join(camino)}")
    print("="*55)

    dibujar_estado(camino_final=camino)
    plt.show()


# =============================================================================
# TOPOLOGÍA DE RED
# Cada par representa: 'Dispositivo': {'Vecino': latencia_en_ms}
# =============================================================================
red_internet = {
    'PC_Casa':  {'Router_A': 5,  'Router_B': 10},
    'Router_A': {'PC_Casa': 5,   'Switch_C': 8,  'Switch_D': 20},
    'Router_B': {'PC_Casa': 10,  'Switch_C': 15, 'Switch_D': 6},
    'Switch_C': {'Router_A': 8,  'Router_B': 15, 'Router_E': 7,  'Router_F': 25},
    'Switch_D': {'Router_A': 20, 'Router_B': 6,  'Router_E': 30, 'Router_F': 5},
    'Router_E': {'Switch_C': 7,  'Switch_D': 30, 'Servidor': 4},
    'Router_F': {'Switch_C': 25, 'Switch_D': 5,  'Servidor': 9},
    'Servidor': {}
}

if __name__ == "__main__":
    visualizar_dijkstra(red_internet, 'PC_Casa', 'Servidor')