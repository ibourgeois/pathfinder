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
            self.load_file_button.setEnabled(False)
        else:
            self.pathfinder = Pathfinder()
            self.distance_api_client = DistanceAPIClient(os.getenv("API_KEY"), 'foot-walking')
            self.app = App()

    def UiComponents(self):
        title_label = QLabel("This is Pathfinder. Start with importing the gpx file.\n If the window \"freezes\" while creating the graph, don't panic. The API has requests per minute limit, so we are just waiting 60 seconds to renew the limit.", self)
        title_label.setGeometry(10, 10, 600, 40)

        self.gpx_label = QLabel("", self)
        self.gpx_label.setGeometry(10, 30, 600, 40)

        self.load_file_button = QPushButton("load gpx", self)
        self.load_file_button.setGeometry(10, 70, 80, 40)
        self.load_file_button.setStyleSheet("""
            QPushButton::disabled {
                background-color: #F44336;
                color: #E7E7E7;
                border: 2px solid #F44336;
                opacity: 0.2;
            }
            QPushButton::hover {
                background-color: #4CAF50;
            }
            transition-duration: 0.8s;
            background-color: white;
            color: black;
            border: 2px solid #4CAF50;
            border-radius: 10px;
            padding: 10px;
            """)
        self.load_file_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.load_file_button.clicked.connect(self.load_file)

        self.compute_button = QPushButton("compute", self)
        self.compute_button.setEnabled(False)
        self.compute_button.setGeometry(10, 150, 80, 40)
        self.compute_button.setStyleSheet("""
            QPushButton::disabled {
                background-color: #F44336;
                color: #E7E7E7;
                border: 2px solid #F44336;
                opacity: 0.6;
            }
            QPushButton::hover {
                background-color: #4CAF50;
            }
            transition-duration: 0.8s;
            background-color: white;
            color: black;
            border: 2px solid #4CAF50;
            border-radius: 10px;
            padding: 10px;
            """)
        self.compute_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.compute_button.clicked.connect(self.compute_thread)

        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.canvas.move(0, 0)
        self.ax = self.figure.add_subplot(111)

        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.addWidget(title_label)
        layout.addWidget(self.gpx_label)
        layout_buttons = QHBoxLayout()
        layout_buttons.addWidget(self.load_file_button)
        layout_buttons.addWidget(self.compute_button)
        layout_buttons.addStretch()
        layout.addLayout(layout_buttons)
        layout.addWidget(self.canvas)
        self.setCentralWidget(central_widget)

    def load_file(self):
        """
        load_file ... Function loads gpx file, parses it and stores the GPS points.
        """
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "./input", ".gpx Files (*.gpx);;All Files (*)")
        if file_name != '':
            self.input_points = self.app.load_gpx(file_name)
            self.compute_button.setEnabled(True)
            text = ",\n".join("(%s,%s)" % tup for tup in self.input_points)
            self.gpx_label.setText(text)
            xpoints = [float(sublist[0]) for sublist in self.input_points]
            ypoints = [float(sublist[1]) for sublist in self.input_points]
            self.points = zip(xpoints, ypoints)
            self.root_points = zip(xpoints, ypoints)
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
        self.compute_button.setEnabled(False)
        self.load_file_button.setEnabled(False)
        print("Creating weighted graph...")
        self.pathfinder.graph_progress_signal.connect(self.update_graph_progress)
        graph = self.pathfinder.create_graph(self.input_points)
        self.pathfinder.graph_progress_signal.disconnect(self.update_graph_progress)

        print("Solving the TSP...")
        self.pathfinder.graph_progress_signal.connect(self.update_path_progress)
        result = self.pathfinder.brute_force_tsp(graph)
        self.pathfinder.graph_progress_signal.disconnect(self.update_path_progress)

        print("Preparing result...")
        self.resulting_points = self.app.prepare_resulting_points(result, self.input_points)
        res_gpx = self.distance_api_client.generate_result_path(self.resulting_points)
        self.app.write_result(res_gpx, self.resulting_points)
        ypoints = [float(sublist[0]) for sublist in self.resulting_points]
        xpoints = [float(sublist[1]) for sublist in self.resulting_points]
        self.points = zip(xpoints, ypoints)
        self.plot()

        self.gpx_label.setText("This is the minimal path through the given points. You can find the real path in output/result.gpx.")
        self.load_file_button.setEnabled(True)
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