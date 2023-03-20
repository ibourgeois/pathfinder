from src.Pathfinder import Pathfinder
from src.DistanceAPIClient import DistanceAPIClient
from dotenv import load_dotenv
import xml.etree.ElementTree as ET
import networkx as nx
import matplotlib.pyplot as plt
import os
load_dotenv()

def load_xml():
    locations = list()
    tree = ET.parse('input/export.gpx')
    root = tree.getroot()
    for child in root:
        locations.append((child.attrib["lat"], child.attrib["lon"]))
    return locations

def res_points(res, points):
    result_points = list()
    for i in res['points']:
        point = [float(points[i][1]), float(points[i][0])]
        result_points.append(point)
    print(result_points)
    return result_points


points = load_xml()
p = Pathfinder()
graph = p.create_graph(points)
res = p.brute_force_tsp(graph)
resulting_points = res_points(res, points)
d = DistanceAPIClient(os.getenv("API_KEY"), 'foot-walking')
res_gpx = d.generate_result_path(resulting_points)
with open('output/result.gpx', 'w') as file:
    file.write(res_gpx)
