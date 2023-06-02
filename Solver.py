from ortools.linear_solver import pywraplp
from ortools.init import pywrapinit


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
        # Sera 1 se o vertice j tiver a cor i
        # 0 caso contrario
        for maxColor in range(Data.numVertices):
            for vertice in range(Data.numVertices):
                label = "Cor: "+str(maxColor)+" - Vertice: "+str(vertice)
                self.variaveis[maxColor-1].append(self.solver.BoolVar(label))

        # Cores[i] Binario
        # Sera 1 se a cor i estiver na solução
        # 0 caso contrario
        for cor in range(Data.numVertices):
            self.cores.append(self.solver.BoolVar(str(cor)))

        print('Number of variables =', self.solver.NumVariables())

        
        # Restrições








