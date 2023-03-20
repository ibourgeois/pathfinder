import itertools
import networkx as nx
from src.DistanceAPIClient import DistanceAPIClient
import os

class Pathfinder:

    def create_graph(self, points):
        distance_api = DistanceAPIClient(os.getenv("API_KEY"), 'foot-walking')
        graph = nx.Graph()
        for i, point in enumerate(points):
            graph.add_node(i, pos=point)
        for u in graph.nodes():
            for v in graph.nodes():
                if u < v:
                    path = distance_api.get_path(graph.nodes[u]['pos'][0], graph.nodes[u]['pos'][1], graph.nodes[v]['pos'][0], graph.nodes[v]['pos'][1])
                    weight = path['features'][0]['properties']['segments'][0]['distance']
                    # weight = distance_api.random_path()
                    txt = "The distance from node {} to node {} is {}."
                    print(txt.format(u, v, weight))
                    graph.add_edge(u, v, weight=weight)
        return graph


    def brute_force_tsp(self, graph):
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

        # Convert permutation to Hamiltonian circuit
        hamiltonian_circuit = list(min_permutation)
        hamiltonian_circuit.append(min_permutation[0])

        return {'points': hamiltonian_circuit, 'distance': min_weight}
