from abc import ABC, abstractmethod

class TSPAlgorithm(ABC):
    @abstractmethod
    def create_graph(self, points):
        pass

    @abstractmethod
    def solve_tsp_problem(self, graph):
        pass
