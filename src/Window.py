from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from src.Pathfinder import Pathfinder
from src.DistanceAPIClient import DistanceAPIClient
from src.App import App
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import os, random, time
from dotenv import load_dotenv

from threading import *

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        load_dotenv()

        self.setWindowTitle("Pathfinder")
        self.setGeometry(100, 200, 800, 600)
        self.setWindowIcon(QIcon('media/icon.png'))
        self.load_stylesheet()
        self.UiComponents()
        self.input_points = None
        self.resulting_points = None
        self.points = None
        self.root_points = None
        self.a = tuple(random.random() for _ in range(7))
        self.b = tuple(random.random() for _ in range(7))
        self.plot()

        if os.getenv("API_KEY") is None:
            self.gpx_label.setText("API_KEY not found. Please check if the .env file exists and the API_KEY variable is set to valid key to OpenRouteService API.")
            self.button_load_file.setEnabled(False)
        else:
            self.pathfinder = Pathfinder()
            self.app = App()
    
    def load_stylesheet(self):
        with open('styles/styles.qss', 'r') as f:
            self.stylesheet = f.read()
        self.setStyleSheet(self.stylesheet)

    def UiComponents(self):
        title_label = QLabel("This is Pathfinder. Start with importing the gpx file.\n If the window \"freezes\" while creating the graph, don't panic. The API has requests per minute limit, so we are just waiting 60 seconds to renew the limit.", self)
        title_label.setGeometry(10, 10, 600, 40)

        self.gpx_label = QLabel("", self)
        self.gpx_label.setGeometry(10, 30, 600, 40)

        self.button_load_file = QPushButton("load gpx", self)
        self.button_load_file.setGeometry(10, 70, 80, 40)
        self.button_load_file.setStyleSheet(self.stylesheet)
        self.button_load_file.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_load_file.clicked.connect(self.load_file)

        self.button_compute = QPushButton("compute", self)
        self.button_compute.setEnabled(False)
        self.button_compute.setGeometry(10, 150, 80, 40)
        self.button_compute.setStyleSheet(self.stylesheet)
        self.button_compute.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_compute.clicked.connect(self.compute_thread)

        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.canvas.move(0, 0)
        self.ax = self.figure.add_subplot(111)

        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.addWidget(title_label)
        layout.addWidget(self.gpx_label)
        layout_buttons = QHBoxLayout()
        layout_buttons.addWidget(self.button_load_file)
        layout_buttons.addWidget(self.button_compute)
        layout_buttons.addStretch()
        layout.addLayout(layout_buttons)
        layout.addWidget(self.canvas)
        self.setCentralWidget(central_widget)

    def load_file(self):
        """
        load_file ... Function loads gpx file, parses it and stores the GPS points.
        """
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "./input", ".gpx Files (*.gpx);;All Files (*)")
        if file_name and os.path.isfile(file_name):
            self.input_points = self.app.load_gpx(file_name)
            self.button_compute.setEnabled(True)
            text = ",\n".join("(%s,%s)" % tup for tup in self.input_points)
            self.gpx_label.setText(text)
            xpoints, ypoints = zip(*self.input_points)
            self.points = list(zip(map(float, xpoints), map(float, ypoints)))
            self.root_points = self.points[:]
            self.a, self.b = zip(*self.root_points)
            self.plot()

    def compute_thread(self):
        thread1 = Thread(target=self.compute)
        thread1.daemon = True
        thread1.start()

    def update_graph_progress(self, progress, points):
        self.points = points
        self.plot()
        self.gpx_label.setText(progress)
    
    def update_path_progress(self, progress, points):
        x, y = zip(*self.app.prepare_resulting_points({'points': points}, self.input_points))
        self.points = zip(y, x)
        self.plot()

    def compute(self):
        """
        compute ... Function does all the computations (creating weighted graph and finding the shortest path)
        and plots the result.
        """
        self.button_compute.setEnabled(False)
        self.button_load_file.setEnabled(False)
        print("Creating weighted graph...")
        self.pathfinder.graph_progress_signal.connect(self.update_graph_progress)
        self.pathfinder.create_graph(self.input_points)
        self.pathfinder.graph_progress_signal.disconnect(self.update_graph_progress)

        print("Solving the TSP...")
        self.pathfinder.graph_progress_signal.connect(self.update_path_progress)
        result = self.pathfinder.brute_force_tsp()
        self.pathfinder.graph_progress_signal.disconnect(self.update_path_progress)

        print("Preparing result...")
        self.resulting_points = self.app.prepare_resulting_points(result, self.input_points)
        res_gpx = self.pathfinder.create_result_path(self.resulting_points)
        self.app.write_result(res_gpx, self.resulting_points)
        self.points = [(float(sublist[1]), float(sublist[0])) for sublist in self.resulting_points]
        self.plot()

        self.gpx_label.setText("This is the minimal path through the given points. You can find the real path in output/result.gpx.")
        self.button_load_file.setEnabled(True)
        print("DONE! You can find the result in output/result.gpx.")

    def plot(self):
        """
        plot ... Function controlls plotting of the graph.
        """
        if self.points is not None:
            x, y = zip(*self.points)
            self.ax.cla()
            self.ax.plot(self.a, self.b, 'ko')
            self.ax.plot(x, y, 'ro-', ms = 10)
            self.ax.set_xlim([min(self.a)-0.005, max(self.a)+0.005])
            self.ax.set_ylim([min(self.b)-0.005, max(self.b)+0.005])
            self.canvas.draw()
        else:
            self.ax.cla()
            self.ax.set_xlim([min(self.a)-0.05, max(self.a)+0.05])
            self.ax.set_ylim([min(self.b)-0.05, max(self.b)+0.05])
            self.ax.plot(self.a, self.b, 'ro-', ms = 5)
            self.canvas.draw()