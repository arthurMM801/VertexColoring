from ortools.linear_solver import pywraplp
import matplotlib.pyplot as plt
import networkx as nx
import random

def random_color():
    hex = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, "a", "b", "c", "d", "e", "f"]
    hexadecimal = "#"
    random_num = lambda max: random.randint(0, max-1)

    for i in range(6):
        hexadecimal += str(hex[random_num(len(hex))])

    return ''.join(str(hexadecimal))


def arr_color(n):
    return [random_color() for i in range(n)]


class Solver:
    def __init__(self, Data):
        self.solver = pywraplp.Solver.CreateSolver('SCIP')
        self.variaveis = []
        self.cores = []

        # Inicialização
        for i in Data.grafo:
            self.variaveis.append([])

        # Criação de variaveis

        # Variavel[i][j] Binaria:
        # Sera 1 se o vertice i tiver a cor j
        # 0 caso contrario
        for vertice in range(Data.numVertices):
            for color in range(Data.numVertices):
                label = "Vertice:"+str(vertice+1)+" Cor:"+str(color+1)
                self.variaveis[vertice].append(self.solver.BoolVar(name=label))

        # Cores[i] Binario
        # Sera 1 se a cor i estiver na solução
        # 0 caso contrario
        for cor in range(Data.numVertices):
            label = "Cor "+str(cor+1)
            self.cores.append(self.solver.BoolVar(name=label))

        print('Number of variables =', self.solver.NumVariables())



        # Restrições

        # Vizinhos não podem ter a mesma cor
        for arco in Data.edges:
            for cor in range(Data.numVertices):
                self.solver.Add(self.variaveis[arco.u-1][cor] + self.variaveis[arco.v-1][cor] <= 1)


        # O vertice i so pode ter uma cor
        for vertice in range(Data.numVertices):
            cores_do_vertice = sum(self.variaveis[vertice][cor] for cor in range(Data.numVertices))
            self.solver.Add(cores_do_vertice == 1)


        # Se a cor j está na solução
        for vertice in range(Data.numVertices):
            for cor in range(len(self.cores)):
                self.solver.Add(self.variaveis[vertice][cor] <= self.cores[cor])


        print('Number of constraints =', self.solver.NumConstraints())

        # Objective

        total_cores = sum(self.cores[cor] for cor in range(len(self.cores)))
        self.solver.Minimize(total_cores)


        # Solução

        print(f'\nResolvendo com {self.solver.SolverVersion()}')
        status = self.solver.Solve()

        vertice_colors = []

        if status == pywraplp.Solver.OPTIMAL:
            print('\nSolução:')
            print('Valor objetivo =', self.solver.Objective().Value())
            print("\nVertice_Cores")
            for i in range(Data.numVertices):
                for j in range(Data.numVertices):
                    if self.variaveis[i][j].solution_value() == 1:
                        vertice_colors.append(j)
                        print('Vértice', i+1, ' | Cor', j+1)
            print("\nCores")
            for i in range(len(self.cores)):
                print(i+1,' = ', self.cores[i].solution_value())

            arr_colors = arr_color(Data.numVertices)
            coloring_vertices = []
            for color in vertice_colors:
                coloring_vertices.append(arr_colors[color])

            # Transformar vertice_colors para hexadecimal
            self.printColoringGraph(Data.G, coloring_vertices)
        else:
            print('O problema não tem solução otima.')

        print('\nInformações Avançadas:')
        print('Problema resolvido em %f millisegundos' % self.solver.wall_time())
        print('Problema resolvido em %d iterações' % self.solver.iterations())
        print('Problema resolvido em %d nós de ramificação e limite' % self.solver.nodes())
        self.exportModel(self.solver, "Minimum_Vertex_Coloring_Model.txt")


    def exportModel(self, solver, output):
        with open(output, 'w') as file:
                file.write(solver.ExportModelAsLpFormat(False))


    def printColoringGraph(self, G, colors):
        nx.draw(G, with_labels=True, node_color=colors, node_size=1000)
        plt.show()


