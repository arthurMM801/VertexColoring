import matplotlib.pyplot as plt
import networkx as nx


class Data():
    def __init__(self):
        self.G = nx.Graph()
        self.numVertices = 0
        self.numArestas = 0
        self.grafo = []

    def le_grafo(self, filename):
        with open(filename, "r") as f:
            self.numVertices = int(f.readline())
            self.numArestas = int(f.readline())

            for i in range(self.numVertices):
                self.grafo.append([])

            # Criação do grafo com dict
            for edd in f:
                v1, v2 = map(int, edd.strip().split())

                if v1 not in self.grafo:
                    self.G.add_node(v1+1)
                if v2 not in self.grafo:
                    self.G.add_node(v2+1)

                self.grafo[v1].append(v2)
                self.grafo[v2].append(v1)
                self.G.add_edge(v1+1, v2+1)

        print("Grafo:\n", self.grafo)
        print()

    def print_grafo(self):
        nx.draw(self.G, with_labels=True, node_color='yellow', node_size=1000)
        plt.show()

