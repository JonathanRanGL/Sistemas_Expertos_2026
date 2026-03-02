import networkx as nx
import matplotlib.pyplot as plt
import sys

# =============================================================================
# CASO DE USO: Red de Tuberías de Agua Potable — Algoritmo de Prim
# -----------------------------------------------------------------------------
# Jonathan Rodrigo Sánchez Rangel - 23110179 - 7E
# -----------------------------------------------------------------------------
# Escenario: Una empresa de agua potable necesita conectar 7 zonas de una
# ciudad a la red principal. Cada conexión posible entre zonas tiene un costo
# en metros de tubería a instalar. El objetivo es conectar TODAS las zonas
# gastando el menor metraje total posible.
#
# Nodos  → Zonas de la ciudad (Planta, Zona Norte, Zona Sur, etc.)
# Aristas → Conexiones posibles entre zonas
# Pesos  → Metros de tubería necesarios para esa conexión
# =============================================================================

# Nombres de las zonas (índice → nombre)
ZONAS = {
    0: "Planta",
    1: "Z.Norte",
    2: "Z.Sur",
    3: "Z.Este",
    4: "Z.Oeste",
    5: "Z.Centro",
    6: "Z.Industrial"
}

class SimuladorPrim:
    def __init__(self, vertices):
        self.V = vertices
        self.grafo = []  # Lista de aristas: [origen, destino, peso]

    def agregar_arista(self, u, v, w):
        self.grafo.append([u, v, w])

    def ejecutar_prim(self):
        visitados = [False] * self.V
        mst_aristas = []

        # Empezamos desde la Planta (nodo 0)
        visitados[0] = True
        num_aristas = 0
        peso_total = 0

        print("\n" + "="*60)
        print("   RED DE TUBERÍAS DE AGUA POTABLE — Algoritmo de Prim")
        print("="*60)
        print(f"  Inicio: {ZONAS[0]} (nodo raíz del árbol)")
        print(f"  Objetivo: conectar las {self.V} zonas con mínimo metraje")
        print("="*60)
        print(f"\n{'Paso':<6} | {'Conexión':<30} | {'Tubería (m)':<12}")
        print("-"*55)

        while num_aristas < self.V - 1:
            minimo = sys.maxsize
            x = 0
            y = 0
            encontrado = False

            for i in range(len(self.grafo)):
                u, v, w = self.grafo[i]

                # Una zona ya conectada hacia una zona nueva
                if visitados[u] and not visitados[v]:
                    if w < minimo:
                        minimo = w
                        x = u
                        y = v
                        encontrado = True

                elif visitados[v] and not visitados[u]:
                    if w < minimo:
                        minimo = w
                        x = v
                        y = u
                        encontrado = True

            if encontrado:
                visitados[y] = True
                mst_aristas.append((x, y, minimo))
                peso_total += minimo
                num_aristas += 1
                print(f"  {num_aristas:<5} | {ZONAS[x]} → {ZONAS[y]:<22} | {minimo} m")

        print("-"*55)
        print(f"\n  ✅ Tubería total instalada: {peso_total} metros")
        print(f"  ✅ Zonas conectadas: {', '.join(ZONAS.values())}")
        print("="*60)
        return mst_aristas, peso_total

    def graficar(self, mst_aristas, peso_total):
        G = nx.Graph()

        # Agregar todas las aristas con nombres de zonas
        for u, v, w in self.grafo:
            G.add_edge(ZONAS[u], ZONAS[v], weight=w)

        # Layout manual para que las zonas se vean ordenadas
        pos = {
            "Planta":       ( 0,    0),
            "Z.Norte":      ( 0,    2),
            "Z.Sur":        ( 0,   -2),
            "Z.Este":       ( 2,    1),
            "Z.Oeste":      (-2,    1),
            "Z.Centro":     ( 2,   -1),
            "Z.Industrial": (-2,   -1),
        }

        plt.figure(figsize=(12, 8))
        plt.title(
            f"Red de Tuberías de Agua Potable — Prim\n"
            f"Tubería total instalada: {peso_total} metros",
            fontsize=13, fontweight='bold'
        )

        # Nodos
        nx.draw_networkx_nodes(G, pos, node_size=1600, node_color='#87CEEB')
        nx.draw_networkx_labels(G, pos, font_size=8, font_weight='bold')

        # Todas las conexiones posibles (gris punteado)
        nx.draw_networkx_edges(G, pos, width=1, alpha=0.4,
                               edge_color='gray', style='dashed')

        # Pesos en todas las aristas
        labels = {(ZONAS[u], ZONAS[v]): f"{w} m" for u, v, w in self.grafo}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=7)

        # Árbol de Prim resaltado en azul
        aristas_mst = [(ZONAS[u], ZONAS[v]) for u, v, w in mst_aristas]
        nx.draw_networkx_edges(G, pos, edgelist=aristas_mst,
                               width=4, edge_color='#1E90FF')

        # Leyenda
        leyenda = (
            "--- Gris punteado = conexión posible\n"
            "━━━ Azul grueso   = tubería instalada (Prim)"
        )
        plt.gcf().text(0.01, 0.05, leyenda, fontsize=8,
                       bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

        plt.axis('off')
        plt.tight_layout()
        plt.show()


# =============================================================================
# RED DE CONEXIONES POSIBLES
# agregar_arista(zona_origen, zona_destino, metros_de_tubería)
# =============================================================================
if __name__ == "__main__":
    simulador = SimuladorPrim(7)

    simulador.agregar_arista(0, 1, 120)  # Planta      ↔ Z.Norte
    simulador.agregar_arista(0, 2, 95)   # Planta      ↔ Z.Sur
    simulador.agregar_arista(0, 3, 150)  # Planta      ↔ Z.Este
    simulador.agregar_arista(0, 4, 110)  # Planta      ↔ Z.Oeste
    simulador.agregar_arista(1, 3, 80)   # Z.Norte     ↔ Z.Este
    simulador.agregar_arista(1, 4, 60)   # Z.Norte     ↔ Z.Oeste
    simulador.agregar_arista(2, 5, 70)   # Z.Sur       ↔ Z.Centro
    simulador.agregar_arista(2, 6, 130)  # Z.Sur       ↔ Z.Industrial
    simulador.agregar_arista(3, 5, 55)   # Z.Este      ↔ Z.Centro
    simulador.agregar_arista(4, 6, 75)   # Z.Oeste     ↔ Z.Industrial
    simulador.agregar_arista(5, 6, 90)   # Z.Centro    ↔ Z.Industrial

    resultado, total = simulador.ejecutar_prim()
    simulador.graficar(resultado, total)