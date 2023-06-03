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
        # Sera 1 se o vertice i tiver a cor j
        # 0 caso contrario
        for vertice in range(Data.numVertices):
            for maxColor in range(Data.numVertices):
                label = "Vertice: "+str(maxColor)+" - Cor: "+str(vertice)
                self.variaveis[vertice].append(self.solver.BoolVar(label))

        # Cores[i] Binario
        # Sera 1 se a cor i estiver na solução
        # 0 caso contrario
        for cor in range(Data.numVertices):
            self.cores.append(self.solver.BoolVar(str(cor)))

        print('Number of variables =', self.solver.NumVariables())



        # Restrições

        # Vizinhos não podem ter a mesma cor
        for vertice in range(Data.numVertices):
            for vizinho in Data.grafo[vertice]:
                if vizinho > vertice:
                    for cor in range(Data.numVertices):
                        self.solver.Add(self.variaveis[vertice][cor] + self.variaveis[vizinho][cor] <= 1)


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

        if status == pywraplp.Solver.OPTIMAL:
            print('\nSolução:')
            print('Valor objetivo =', self.solver.Objective().Value())

            print("\nVertice_Cores")
            for i in range(Data.numVertices):
                for j in range(Data.numVertices):
                    if self.variaveis[i][j].solution_value() == 1:
                        print('Vértice', i+1, ' | Cor', j+1)

            print("\nCores")
            for i in range(len(self.cores)):
                print(i+1,' = ', self.cores[i].solution_value())
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
