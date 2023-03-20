from src.Pathfinder import Pathfinder
from src.DistanceAPIClient import DistanceAPIClient
from dotenv import load_dotenv
import xml.etree.ElementTree as ET
import networkx as nx
import matplotlib.pyplot as plt
import os, re

load_dotenv()

def load_xml():
    """
    load_xml ... Function loads the input file and parses the xml. It returns
        a list of points (a list of tuples).
    """
    locations = list()
    tree = ET.parse('input/export.gpx')
    root = tree.getroot()
    for child in root:
        locations.append((child.attrib["lat"], child.attrib["lon"]))
    return locations

def prepare_resulting_points(res, points):
    """
    prepare_resulting_points ... Function prepares a list of the resulting points.
    """
    result_points = list()
    for i in res['points']:
        point = [float(points[i][1]), float(points[i][0])]
        result_points.append(point)
    return result_points

def write_result(res_gpx, resulting_points):
    """
    write_result ... Function writes the result in the output gpx file.
        It appends the initial waypoints to the resulting gpx file.
    """
    res_gpx = re.sub(r'</gpx>$', '', res_gpx)
    for point in resulting_points[:-1]:
        wpt_prep = '<wpt lat="{lat}" lon="{lon}"></wpt>'
        wpt = wpt_prep.format(lat=point[1], lon=point[0])
        res_gpx += wpt
    res_gpx += "</gpx>"
    with open('output/result.gpx', 'w') as file:
        file.write(res_gpx)

print("Loading gpx...")
input_points = load_xml()
p = Pathfinder()
print("Creating weighted graph...")
graph = p.create_graph(input_points)
print("Solving the TSP...")
result = p.brute_force_tsp(graph)
print("Preparing result...")
resulting_points = prepare_resulting_points(result, input_points)
d = DistanceAPIClient(os.getenv("API_KEY"), 'foot-walking')
res_gpx = d.generate_result_path(resulting_points)
write_result(res_gpx, resulting_points)
print("DONE! You can find the result in output/result.gpx.")
