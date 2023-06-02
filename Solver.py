from ortools.linear_solver import pywraplp
from ortools.init import pywrapinit


class Solver:
    def __init__(self, Data):
        self.solver = pywraplp.Solver.CreateSolver('SCIP')
        self.variaveis = []

        for i in Data.grafo:
            self.variaveis.append([])

        for maxColor in range(Data.numVertices):
            for vertice in range(Data.numVertices):
                label = "Cor: "+str(maxColor)+" - Vertice: "+str(vertice)
                self.variaveis[maxColor-1].append(self.solver.BoolVar(label))

        print('Number of variables =', self.solver.NumVariables())


