import os
from PyQt5 import QtWidgets, QtCore
import threading
import subprocess

# Get the directory of the currently executing script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Define a relative path to the "input" directory from the script's directory
relative_path = "../input/geometry.txt"

# Combine the current directory with the relative path to create the full file path
geometry_file = os.path.join(current_dir, relative_path)

# Define an array of parameter names
parameters = [
    "Comprimento_direcao_x(m)",
    "Comprimento_direcao_y(m)",
    "Comprimento_direcao_z(m)"
]


class GeometryParametersWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(GeometryParametersWindow, self).__init__()
        self.setWindowTitle("Geometry")

        self.central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QtWidgets.QGridLayout(self.central_widget)
        self.form_layout = QtWidgets.QFormLayout()
        self.layout.addLayout(self.form_layout, 0, 0)

        self.entries = []
        for parameter in parameters:
            label = QtWidgets.QLabel(parameter)
            entry = QtWidgets.QLineEdit()
            self.form_layout.addRow(label, entry)
            self.entries.append(entry)

        load_button = QtWidgets.QPushButton("Load Data", self)
        load_button.clicked.connect(self.load_data)
        self.layout.addWidget(load_button, 1, 0)

        save_button = QtWidgets.QPushButton("Save Data", self)
        save_button.clicked.connect(self.save_data)
        self.layout.addWidget(save_button, 2, 0)

        run_button = QtWidgets.QPushButton("Run Case", self)
        run_button.clicked.connect(self.run_simulation)
        self.layout.addWidget(run_button, 3, 0)
        
    def load_data(self):
        with open(geometry_file, 'r') as f:
            lines = f.readlines()

        values = []
        for parameter in parameters:
            for line in lines:
                if parameter in line:
                    value = line.split(':')[1].strip()
                    values.append(value)
                    break
            else:
                values.append('')

        for entry, value in zip(self.entries, values):
            entry.setText(value)

    def save_data(self):
        values = [entry.text() for entry in self.entries]

        with open(geometry_file, 'r') as f:
            lines = f.readlines()

        for i, line in enumerate(lines):
            for j, parameter in enumerate(parameters):
                if parameter in line:
                    lines[i] = parameter + ': ' + values[j] + '\n'
                    break

        with open(geometry_file, 'w') as f:
            f.writelines(lines)

    def run_simulation(self):
        threading.Thread(target=self.execute_command).start()

    def execute_command(self):
        command = "./deploy.sh"
        subprocess.call(command, shell=True)

# You can add additional code to handle other functionalities specific to the Geometry GUI if needed
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = GeometryParametersWindow()
    window.show()
    app.exec_()
