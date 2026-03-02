import networkx as nx
import matplotlib.pyplot as plt

# =============================================================================
# CASO DE USO: Red de Antenas de Telecomunicaciones — Algoritmo de Kruskal
# -----------------------------------------------------------------------------
# Jonathan Rodrigo Sánchez Rangel - 23110179 - 7E
# -----------------------------------------------------------------------------
# Escenario: Una empresa de telecomunicaciones necesita conectar 8 antenas
# distribuidas en una región. Cada conexión posible entre antenas tiene un
# costo en metros de cable de fibra óptica.
#
# Modo MÍNIMO: ¿Cómo conectar todas las antenas con el menor cable posible?
#              → Reduce costos de instalación
#
# Modo MÁXIMO: ¿Cuáles son los enlaces de mayor capacidad disponibles?
#              → Identifica la red troncal de mayor ancho de banda
#
# Nodos  → Antenas / Torres de telecomunicaciones
# Aristas → Conexiones posibles entre antenas
# Pesos  → Metros de cable de fibra óptica necesarios
# =============================================================================


# --- Clase Union-Find para detectar ciclos ---
class UnionFind:
    def __init__(self, nodos):
        # Al inicio cada antena es su propio grupo independiente
        self.padre = {nodo: nodo for nodo in nodos}

    def find(self, nodo):
        # Encuentra la raíz del grupo al que pertenece este nodo
        # "Compresión de ruta": aplana el árbol para futuras búsquedas más rápidas
        if self.padre[nodo] != nodo:
            self.padre[nodo] = self.find(self.padre[nodo])
        return self.padre[nodo]

    def union(self, nodo1, nodo2):
        # Une dos grupos distintos
        raiz1 = self.find(nodo1)
        raiz2 = self.find(nodo2)
        if raiz1 != raiz2:
            self.padre[raiz1] = raiz2
            return True   # Unión exitosa — no forma ciclo
        return False      # Ya estaban en el mismo grupo — formaría ciclo


# --- Clase principal del Simulador ---
class SimuladorKruskal:
    def __init__(self):
        self.aristas = []
        self.nodos = set()

    def agregar_arista(self, u, v, peso):
        self.aristas.append((u, v, peso))
        self.nodos.add(u)
        self.nodos.add(v)

    def ejecutar_kruskal(self, buscar_maximo=False):
        tipo = "MÁXIMO (Red Troncal)" if buscar_maximo else "MÍNIMO (Menor Costo)"
        objetivo = (
            "Mayor capacidad de transmisión" if buscar_maximo
            else "Menor metraje de cable instalado"
        )

        print("\n" + "="*62)
        print(f"   RED DE ANTENAS — Kruskal {tipo}")
        print(f"   Objetivo: {objetivo}")
        print("="*62)

        # Ordenar aristas: menor a mayor (mínimo) o mayor a menor (máximo)
        self.aristas.sort(key=lambda x: x[2], reverse=buscar_maximo)

        uf = UnionFind(self.nodos)
        arbol_resultado = []
        coste_total = 0
        step = 1

        print(f"\n{'Paso':<6} | {'Enlace':<22} | {'Cable (m)':<10} | {'Decisión'}")
        print("-"*62)

        for u, v, peso in self.aristas:
            raiz_u = uf.find(u)
            raiz_v = uf.find(v)

            if raiz_u != raiz_v:
                # Las antenas pertenecen a grupos distintos → aceptar enlace
                uf.union(u, v)
                arbol_resultado.append((u, v, peso))
                coste_total += peso
                print(f"  {step:<5}| {u} ↔ {v:<18} | {peso:<10} | ✅ ACEPTADO (une grupos)")
            else:
                # Ya están en el mismo grupo → rechazar para evitar ciclo
                print(f"  {step:<5}| {u} ↔ {v:<18} | {peso:<10} | ❌ RECHAZADO (ciclo)")

            step += 1

        print("-"*62)
        print(f"\n  Cable total utilizado : {coste_total} metros")
        print(f"  Antenas conectadas    : {len(self.nodos)}")
        print(f"  Enlaces instalados    : {len(arbol_resultado)}")
        print("="*62)
        return arbol_resultado, coste_total

    def visualizar(self, arbol_resultado, coste_total, buscar_maximo=False):
        tipo = "Máximo — Red Troncal" if buscar_maximo else "Mínimo — Menor Costo"
        color_arbol = '#FF4500' if buscar_maximo else '#1E90FF'

        G = nx.Graph()
        for u, v, w in self.aristas:
            G.add_edge(u, v, weight=w)

        # Layout manual para simular distribución geográfica de antenas
        pos = {
            "Antena-Central": ( 0,    0),
            "Antena-Norte":   ( 0,    2.5),
            "Antena-Sur":     ( 0,   -2.5),
            "Antena-Este":    ( 2.5,  0),
            "Antena-Oeste":   (-2.5,  0),
            "Antena-NE":      ( 2,    2),
            "Antena-NO":      (-2,    2),
            "Antena-SE":      ( 2,   -2),
        }

        plt.figure(figsize=(13, 9))
        plt.title(
            f"Red de Antenas de Telecomunicaciones — Kruskal {tipo}\n"
            f"Cable total instalado: {coste_total} metros",
            fontsize=12, fontweight='bold'
        )

        # Nodos
        nx.draw_networkx_nodes(G, pos, node_size=1800, node_color='#D3D3D3')
        nx.draw_networkx_labels(G, pos, font_size=7, font_weight='bold')

        # Todas las conexiones posibles (gris punteado)
        nx.draw_networkx_edges(G, pos, width=1, alpha=0.35,
                               edge_color='gray', style='dashed')

        # Pesos en todas las aristas
        labels = {(u, v): f"{w}m" for u, v, w in self.aristas}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=7)

        # Árbol de Kruskal resaltado
        aristas_sol = [(u, v) for u, v, w in arbol_resultado]
        nx.draw_networkx_edges(G, pos, edgelist=aristas_sol,
                               width=4, edge_color=color_arbol)

        # Leyenda
        color_nombre = "Naranja/Rojo" if buscar_maximo else "Azul"
        leyenda = (
            f"--- Gris punteado  = enlace posible\n"
            f"━━━ {color_nombre} grueso = enlace seleccionado por Kruskal"
        )
        plt.gcf().text(0.01, 0.05, leyenda, fontsize=8,
                       bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

        plt.axis('off')
        plt.tight_layout()
        plt.show()


# =============================================================================
# RED DE ANTENAS — CONEXIONES POSIBLES
# agregar_arista(antena_origen, antena_destino, metros_de_cable)
# =============================================================================
if __name__ == "__main__":

    sim = SimuladorKruskal()

    datos = [
        ("Antena-Central", "Antena-Norte",   300),
        ("Antena-Central", "Antena-Sur",     250),
        ("Antena-Central", "Antena-Este",    180),
        ("Antena-Central", "Antena-Oeste",   220),
        ("Antena-Norte",   "Antena-NE",      150),
        ("Antena-Norte",   "Antena-NO",      170),
        ("Antena-Este",    "Antena-NE",      130),
        ("Antena-Este",    "Antena-SE",      160),
        ("Antena-Sur",     "Antena-SE",      140),
        ("Antena-Oeste",   "Antena-NO",      190),
        ("Antena-NE",      "Antena-SE",      210),
        ("Antena-NO",      "Antena-Oeste",   200),
        ("Antena-Norte",   "Antena-Este",    280),
        ("Antena-Sur",     "Antena-Oeste",   310),
    ]

    for u, v, w in datos:
        sim.agregar_arista(u, v, w)

    print("╔══════════════════════════════════════╗")
    print("║   RED DE ANTENAS — Kruskal           ║")
    print("╠══════════════════════════════════════╣")
    print("║  1. Árbol de Mínimo Costo            ║")
    print("║     (menor cable a instalar)         ║")
    print("║  2. Árbol de Máximo Costo            ║")
    print("║     (red troncal mayor capacidad)    ║")
    print("╚══════════════════════════════════════╝")

    opcion = input("\nElige una opción (1 o 2): ").strip()

    if opcion == '1':
        resultado, total = sim.ejecutar_kruskal(buscar_maximo=False)
        sim.visualizar(resultado, total, buscar_maximo=False)
    elif opcion == '2':
        resultado, total = sim.ejecutar_kruskal(buscar_maximo=True)
        sim.visualizar(resultado, total, buscar_maximo=True)
    else:
        print("Opción no válida.")