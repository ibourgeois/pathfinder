from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from src.Pathfinder import Pathfinder
from src.DistanceAPIClient import DistanceAPIClient
from src.App import App
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.qt_compat import QtWidgets
import matplotlib.pyplot as plt
import os, random
import sys
from dotenv import load_dotenv

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        load_dotenv()

        self.main_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.main_widget)
        self.l = QtWidgets.QHBoxLayout(self.main_widget)
        self.resulting_points = None
        self.input_points = None

        self.setWindowTitle("Pathfinder")
        self.setGeometry(100, 200, 700, 500)
        self.UiComponents()
        self.pathfinder = Pathfinder()
        self.distance_api_client = DistanceAPIClient(os.getenv("API_KEY"), 'foot-walking')
        self.app = App()

    def UiComponents(self):
        title_label = QLabel("This is Pathfinder. Start with importing the gpx file.", self)
        title_label.setGeometry(10, 10, 600, 40)

        self.gpx_label = QLabel("", self)
        self.gpx_label.setGeometry(10, 30, 600, 40)

        load_file_button = QPushButton("load gpx", self)
        load_file_button.setGeometry(10, 70, 100, 40)
        load_file_button.clicked.connect(self.load_file)

        self.compute_button = QPushButton("compute", self)
        self.compute_button.setEnabled(False)
        self.compute_button.setGeometry(120, 70, 100, 40)
        self.compute_button.clicked.connect(self.compute)


        self.plot_button = QPushButton("plot", self)
        self.plot_button.setEnabled(False)
        self.plot_button.setGeometry(230, 70, 100, 40)
        self.plot_button.clicked.connect(self.plot)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.l.addWidget(self.canvas)

    def load_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "./input", ".gpx Files (*.gpx);;All Files (*)")
        self.input_points = self.app.load_xml(file_name)
        self.compute_button.setEnabled(True)
        self.plot_button.setEnabled(True)
        text = ",".join("(%s,%s)" % tup for tup in self.input_points)
        self.plot(self.input_points)
        self.gpx_label.setText(text)

    def compute(self):
        print("Creating weighted graph...")
        graph = self.pathfinder.create_graph(self.input_points)
        print("Solving the TSP...")
        result = self.pathfinder.brute_force_tsp(graph)
        print("Preparing result...")
        self.resulting_points = self.app.prepare_resulting_points(result, self.input_points)
        res_gpx = self.distance_api_client.generate_result_path(self.resulting_points)
        self.app.write_result(res_gpx, self.resulting_points)
        self.plot()
        print("DONE! You can find the result in output/result.gpx.")

    def plot(self, points=None):
        if points is None or points is False:
            if self.resulting_points is not None:
                points = self.resulting_points
            else:
                points = self.input_points
        self.figure.clear()
        color = (random.random(), random.random(), random.random())
        xpoints = [float(sublist[0]) for sublist in points]
        ypoints = [float(sublist[1]) for sublist in points]
        ax = self.figure.add_subplot(111)
        ax.plot(xpoints, ypoints, '*-', c=color)
        self.canvas.draw()
