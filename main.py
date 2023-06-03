from Data import *
from Solver import Solver


def main():
    data = Data()
    data.le_grafo("entrada.txt")
    data.print_grafo()

    Solver(data)



if __name__ == '__main__':
    main()