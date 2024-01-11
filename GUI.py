import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QPushButton
sys.path.append('.\src\GUI')

os.system(".\src\GUI\mklogo.exe")

from generalGUI import GeneralParametersWindow
from fluidGUI import FluidParametersWindow
from geometryGUI import GeometryParametersWindow
from rockGUI import RockParametersWindow
from wellGUI import WellParametersWindow
from heatGUI import HeatParametersWindow
from heterogeneityGUI import HeterogeneityParametersWindow
from cc_slabGUI import CCSlabParametersWindow

class TabbedMainWindow(QMainWindow):
    def __init__(self):
        super(TabbedMainWindow, self).__init__()
        self.setWindowTitle("2D Shale Gas Flow Simulator")

        # Create a tab widget
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Create tabs for different parameter windows
        self.create_tab(GeneralParametersWindow, "General")
        self.create_tab(FluidParametersWindow, "Fluid")
        self.create_tab(GeometryParametersWindow, "Geometry")
        self.create_tab(RockParametersWindow, "Rock")
        self.create_tab(WellParametersWindow, "Well")
        self.create_tab(HeatParametersWindow, "Heat")
        self.create_tab(HeterogeneityParametersWindow, "Heterogeneity")
        self.create_tab(CCSlabParametersWindow, "CC Slab")

    def create_tab(self, window_class, tab_name):
        tab = QWidget()
        layout = QVBoxLayout()
        window = window_class()
        layout.addWidget(window)
        tab.setLayout(layout)
        self.tabs.addTab(tab, tab_name)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TabbedMainWindow()
    window.setGeometry(100, 100, 600, 600)
    window.show()
    sys.exit(app.exec_())
