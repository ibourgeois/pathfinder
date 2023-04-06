import sys, time
from src.TSPSolver import TSPSolver
from src.TSPAlgorithm import TSPAlgorithm

class TSPMeta(type(TSPSolver), type(TSPAlgorithm)):
    pass

class NearestNeighbourTSPSolver(TSPSolver, TSPAlgorithm, metaclass=TSPMeta):

    def create_graph(self, points) -> None:
        return super().create_graph(points)

    def solve_tsp_problem(self, tsp_solver):
        """
        brute_force_tsp ... Function solves the traveling salesman problem for
            given weighted graph using the nearest neighbour method.
        """
        visited = set()
        start = 0
        visited.add(start)
        path = [start]
        sum_distance = 0

        while len(path) < len(tsp_solver.graph.nodes()):
            nearest_neighbor = None
            nearest_distance = sys.maxsize
            for neighbor in tsp_solver.graph.neighbors(start):
                if neighbor not in visited:
                    distance = tsp_solver.graph.get_edge_data(start, neighbor)["weight"]
                    if distance < nearest_distance:
                        nearest_neighbor = neighbor
                        nearest_distance = distance
            start = nearest_neighbor
            sum_distance += nearest_distance
            visited.add(start)
            path.append(start)
            tsp_solver.graph_progress_signal.emit("...", path)
            time.sleep(0.1)

        path.append(path[0])
        # Return best solution
        return {'points': path, 'distance': sum_distance}