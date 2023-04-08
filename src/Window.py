from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from src.TSPSolver import TSPSolver
from src.App import App
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import os, random
from dotenv import load_dotenv

from threading import *

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        load_dotenv()

        self.setWindowTitle("Pathfinder")
        self.setGeometry(100, 200, 1000, 600)
        self.setWindowIcon(QIcon('media/icon.png'))
        self.load_stylesheet()
        self.method = 'brute_force'
        self.selected_starting_point = 0
        self.UiComponents()
        self.tsp_solver = TSPSolver()
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
            self.app = App()
    
    def load_stylesheet(self):
        with open('styles/styles.qss', 'r') as f:
            self.stylesheet = f.read()
        self.setStyleSheet(self.stylesheet)

    def UiComponents(self):
        title_label = QLabel("Begin with importing the gpx file.\nIf the program stops while creating the graph, don't panic.\nThe API has requests per minute limit, so we are just waiting 60 seconds to renew the limit.", self)
        title_label.setGeometry(10, 10, 600, 40)

        self.gpx_label = QLabel("", self)
        self.gpx_label.setGeometry(10, 30, 600, 40)

        self.method_label = QLabel("Choose the computing method. In case of the nearest neighbour method, you can choose also the starting point.", self)
        self.method_label.setGeometry(10, 50, 600, 40)

        toolbar = QButtonGroup(self)
        self.method_brute_force = QRadioButton('brute force', self)
        self.method_brute_force.setChecked(True)
        self.method_brute_force.clicked.connect(self.set_method_to_brute_force)

        self.method_nearest_neighbour = QRadioButton('nearest neighbour', self)
        self.method_nearest_neighbour.setCheckable(True)
        self.method_nearest_neighbour.clicked.connect(self.set_method_to_nearest_neighbour)

        toolbar.addButton(self.method_brute_force)
        toolbar.addButton(self.method_nearest_neighbour)

        self.dropdown_menu = QComboBox(self)
        self.dropdown_menu.setFixedWidth(80)
        self.dropdown_menu.addItem('random')
        self.dropdown_menu.setEnabled(False)
        self.dropdown_menu.currentIndexChanged.connect(self.selection_changed)

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
        layout.addWidget(self.method_label)
        layout.addWidget(self.method_brute_force)
        layout.addWidget(self.method_nearest_neighbour)
        layout.addWidget(self.dropdown_menu)
        layout_buttons = QHBoxLayout()
        layout_buttons.addWidget(self.button_load_file)
        layout_buttons.addWidget(self.button_compute)
        layout_buttons.addStretch()
        layout.addLayout(layout_buttons)
        layout.addWidget(self.canvas)
        self.setCentralWidget(central_widget)

    def set_method_to_brute_force(self):
        self.method_nearest_neighbour.setChecked(False)
        self.dropdown_menu.setEnabled(False)
        self.method = 'brute_force'

    def set_method_to_nearest_neighbour(self):
        self.method_brute_force.setChecked(False)
        self.dropdown_menu.setEnabled(True)
        self.method = 'nearest_neighbour'

    def populate_dropdown_menu(self):
        if len(self.input_points) > 0:
            for i in range(0, len(self.input_points)):
                self.dropdown_menu.addItem('bod ' + str(i+1))

    def selection_changed(self):
        self.selected_starting_point = self.dropdown_menu.currentIndex()

    def load_file(self):
        """
        load_file ... Function loads gpx file, parses it and stores the GPS points.
        """
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "./input", ".gpx Files (*.gpx);;All Files (*)")
        if file_name and os.path.isfile(file_name):
            self.tsp_solver.graph.clear()
            self.input_points = self.app.load_gpx(file_name)
            self.populate_dropdown_menu()
            # text = ",\n".join("(%s,%s)" % tup for tup in self.input_points)
            self.gpx_label.setText(f"You have loaded {len(self.input_points)} points.")
            xpoints, ypoints = zip(*self.input_points)
            self.points = list(zip(map(float, xpoints), map(float, ypoints)))
            self.root_points = self.points[:]
            self.a, self.b = zip(*self.root_points)
            self.plot()
            self.button_compute.setEnabled(True)

    def compute_thread(self):
        thread1 = Thread(target=self.compute)
        thread1.daemon = True
        thread1.start()

    def update_graph_progress(self, progress, points):
        self.points = points
        self.plot()
        self.gpx_label.setText(progress)
    
    def update_path_progress(self, progress, points):
        x, y = zip(*self.app.prepare_resulting_points(points, self.input_points))
        self.points = zip(y, x)
        self.plot()

    def compute(self):
        """
        compute ... Function does all the computations (creating weighted graph and finding the shortest path)
        and plots the result.
        """
        self.button_compute.setEnabled(False)
        self.button_load_file.setEnabled(False)
        self.tsp_solver.set_method(self.method)
        self.tsp_solver.set_starting_point(self.selected_starting_point)
        print("Creating weighted graph...")
        if self.tsp_solver.graph.number_of_nodes() == 0:
            self.tsp_solver.graph_progress_signal.connect(self.update_graph_progress)
            self.tsp_solver.create_graph(self.input_points)
            self.tsp_solver.graph_progress_signal.disconnect(self.update_graph_progress)

        print("Solving the TSP...")
        self.tsp_solver.graph_progress_signal.connect(self.update_path_progress)
        result = self.tsp_solver.solve_tsp()
        self.tsp_solver.graph_progress_signal.disconnect(self.update_path_progress)
        distance = result["distance"]
        print("Preparing result...")
        self.resulting_points = self.app.prepare_resulting_points(result["points"], self.input_points)
        res_gpx = self.tsp_solver.create_result_path(self.resulting_points)
        self.app.write_result(res_gpx, self.resulting_points)
        self.points = [(float(sublist[1]), float(sublist[0])) for sublist in self.resulting_points]
        self.plot()
        res_distance = round(distance/1000, 2)
        self.gpx_label.setText(f"This is the optimal path through the given points.\nDistance traveled is {res_distance} km. You can find the real path in output/result.gpx.")
        self.button_load_file.setEnabled(True)
        self.button_compute.setEnabled(True)
        print("DONE! You can find the result in output/result.gpx.")

    def plot(self):
        """
        plot ... Function controlls plotting of the graph.
        """
        if self.points is not None:
            x, y = zip(*self.points)
            self.ax.cla()
            self.ax.set_xlim([min(self.a)-0.008, max(self.a)+0.008])
            self.ax.set_ylim([min(self.b)-0.008, max(self.b)+0.008])
            self.ax.plot(self.a, self.b, 'ko', ms = 10)
            self.ax.plot(x, y, 'go-', ms = 15)
            for i in range(0, len(self.a)):
                label = str(i+1)
                x, y = self.a[i], self.b[i]
                self.ax.annotate(label, xy=(x, y), xytext=(self.a[i]-0.00025, self.b[i]-0.0015), color='white')
        else:
            self.ax.cla()
            self.ax.set_xlim([min(self.a)-0.05, max(self.a)+0.05])
            self.ax.set_ylim([min(self.b)-0.05, max(self.b)+0.05])
            self.ax.plot(self.a, self.b, 'ro-', ms = 5)
        self.canvas.draw()