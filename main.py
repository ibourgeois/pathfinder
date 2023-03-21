# from src.Pathfinder import Pathfinder
# from src.DistanceAPIClient import DistanceAPIClient
# from src.App import App
# from dotenv import load_dotenv
# import os
from PyQt5.QtWidgets import QApplication
import sys
from src.Window import Window

# load_dotenv()

app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec_())

# print("Loading gpx...")
# a = App()
# input_points = a.load_xml()
# p = Pathfinder()
# print("Creating weighted graph...")
# graph = p.create_graph(input_points)
# print("Solving the TSP...")
# result = p.brute_force_tsp(graph)
# print("Preparing result...")
# resulting_points = a.prepare_resulting_points(result, input_points)
# d = DistanceAPIClient(os.getenv("API_KEY"), 'foot-walking')
# res_gpx = d.generate_result_path(resulting_points)
# a.write_result(res_gpx, resulting_points)
# print("DONE! You can find the result in output/result.gpx.")
