from ortools.linear_solver import pywraplp
from ortools.init import pywrapinit

from Data import *

def main():
    data = Data()
    data.le_grafo("entrada.txt")
    data.print_grafo()



if __name__ == '__main__':
    main()