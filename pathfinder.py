import itertools
import networkx as nx
from DistanceAPIClient import DistanceAPIClient
from dotenv import load_dotenv
import os

load_dotenv()

def create_graph(points):
    distance_api = DistanceAPIClient(os.getenv("API_KEY"))
    # create an empty graph
    G = nx.Graph()
    # add nodes to the graph
    for i, point in enumerate(points):
        G.add_node(i, pos=point)
    # add edges to the graph with weights
    for u in G.nodes():
        for v in G.nodes():
            if u < v:
                # weight = ((G.nodes[u]['pos'][0] - G.nodes[v]['pos'][0])**2
                          # + (G.nodes[u]['pos'][1] - G.nodes[v]['pos'][1])**2)**0.5
                # weight = distance_api.random_path()
                path = distance_api.get_path(G.nodes[u]['pos'][0], G.nodes[u]['pos'][1], G.nodes[v]['pos'][0], G.nodes[v]['pos'][1])
                weight = path['features'][0]['properties']['segments'][0]['distance']
                txt = "The distance from node {} to node {} is {}."
                print(txt.format(u, v, weight))
                G.add_edge(u, v, weight=weight)
    return G


def brute_force_tsp(graph):
    # Generate all possible permutations of node indices
    num_nodes = graph.number_of_nodes()
    node_indices = range(num_nodes)
    all_permutations = itertools.permutations(node_indices)

    # Find permutation with minimum total weight
    min_weight = float('inf')
    min_permutation = None
    for permutation in all_permutations:
        weight = sum(graph[permutation[i]][permutation[(i+1) % num_nodes]]['weight'] for i in range(num_nodes))
        if weight < min_weight:
            min_weight = weight
            min_permutation = permutation

    # Convert permutation to Hamiltonian circuit
    hamiltonian_circuit = list(min_permutation)
    hamiltonian_circuit.append(min_permutation[0])

    return hamiltonian_circuit, min_weight
