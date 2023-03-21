from PyQt5.QtWidgets import *
from src.Pathfinder import Pathfinder
from src.DistanceAPIClient import DistanceAPIClient
from src.App import App
import os
import sys
from dotenv import load_dotenv

class Window(QWidget):
    def __init__(self):
        super().__init__()
        load_dotenv()

        self.setWindowTitle("Pathfinder")
        self.setGeometry(100, 100, 400, 500)
        self.layout = QVBoxLayout()
        self.label = QLabel("This is Pathfinder. Start with importing the gpx file.")
        self.gpx_label = QLabel(self)
        self.load_file_button = QPushButton("load gpx")
        self.compute_button = QPushButton("compute")

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.load_file_button)
        self.layout.addWidget(self.compute_button)
        self.layout.addWidget(self.gpx_label)

        self.setLayout(self.layout)
        self.pathfinder = Pathfinder()
        self.distance_api_client = DistanceAPIClient(os.getenv("API_KEY"), 'foot-walking')
        self.app = App()

        self.load_file_button.clicked.connect(self.load_file)
        self.compute_button.clicked.connect(self.compute)

    def load_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", ".gpx Files (*.gpx);;All Files (*)")
        self.input_points = self.app.load_xml(file_name)
        text = ",".join("(%s,%s)" % tup for tup in self.input_points)
        self.gpx_label.setText(text)

    def compute(self):
        print("Creating weighted graph...")
        graph = self.pathfinder.create_graph(self.input_points)
        print("Solving the TSP...")
        result = self.pathfinder.brute_force_tsp(graph)
        print("Preparing result...")
        resulting_points = self.app.prepare_resulting_points(result, self.input_points)
        res_gpx = self.distance_api_client.generate_result_path(resulting_points)
        self.app.write_result(res_gpx, resulting_points)
        print("DONE! You can find the result in output/result.gpx.")
