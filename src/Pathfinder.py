import itertools, os, time
import networkx as nx
from src.DistanceAPIClient import DistanceAPIClient
from PyQt5.QtCore import QObject, pyqtSignal

class Pathfinder(QObject):

    graph_progress_signal = pyqtSignal(str, list)

    def create_graph(self, points):
        """
        create_graph ... Function creates a weighted graph from given set of points.
        """
        distance_api = DistanceAPIClient(os.getenv("API_KEY"), 'foot-walking')
        graph = nx.Graph()
        for i, point in enumerate(points):
            graph.add_node(i, pos=point)
        for u in graph.nodes():
            for v in graph.nodes():
                if u < v:
                    weight = distance_api.get_distance(
                        graph.nodes[u]['pos'][0],
                        graph.nodes[u]['pos'][1],
                        graph.nodes[v]['pos'][0],
                        graph.nodes[v]['pos'][1])
                    points = [[float(graph.nodes[u]['pos'][0]), float(graph.nodes[u]['pos'][1])], [float(graph.nodes[v]['pos'][0]), float(graph.nodes[v]['pos'][1])]]
                    txt = "The distance from node {} to node {} is {}."
                    message = txt.format(u, v, weight)
                    self.graph_progress_signal.emit(message, points)
                    # print(message)
                    graph.add_edge(u, v, weight=weight)
        return graph


    def brute_force_tsp(self, graph):
        """
        brute_force_tsp ... Function solves the traveling salesman problem for
            given weighted graph using the brute force method.
        """
        # Generate all possible permutations of node indices
        nodes_count = graph.number_of_nodes()
        node_indices = range(nodes_count)
        all_permutations = itertools.permutations(node_indices)

        # Find permutation with minimum total weight
        min_weight = float('inf')
        min_permutation = None
        for permutation in all_permutations:
            weight = sum(graph[permutation[i]][permutation[(i+1) % nodes_count]]['weight'] for i in range(nodes_count))
            if weight < min_weight:
                min_weight = weight
                min_permutation = permutation
                self.graph_progress_signal.emit("...", list(permutation))
                time.sleep(0.1)
        # Convert permutation to Hamiltonian circuit
        hamiltonian_circuit = list(min_permutation)
        hamiltonian_circuit.append(min_permutation[0])

        return {'points': hamiltonian_circuit, 'distance': min_weight}
