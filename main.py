from Data import *
from Solver import Solver


def main():
    data = Data()
    #data.le_grafo("entrada5.txt")
    data.le_grafo("entradaCompleto.txt")
    #data.le_grafo("entrada25.txt")

    data.print_grafo()
    Solver(data)


if __name__ == '__main__':
    main()