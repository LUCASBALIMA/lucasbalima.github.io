import os
from PyQt5 import QtWidgets, QtCore
import threading
import subprocess

# Get the directory of the currently executing script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Define a relative path to the "input" directory from the script's directory
relative_path = "../input/heterogeneity.txt"

# Combine the current directory with the relative path to create the full file path
heterogeneity_file = os.path.join(current_dir, relative_path)

# Define an array of parameter names
parameters = [
    "Presente",
    "x_init",
    "x_final",
    "y_init",
    "y_final",
    "Permeabilidade_em_x(microm2)",
    "Permeabilidade_em_y(microm2)",
    "Porosidade_inicial"
]


class HeterogeneityParametersWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(HeterogeneityParametersWindow, self).__init__()
        self.setWindowTitle("Heterogeneity")

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
        with open(heterogeneity_file, 'r') as f:
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

        with open(heterogeneity_file, 'r') as f:
            lines = f.readlines()

        for i, line in enumerate(lines):
            for j, parameter in enumerate(parameters):
                if parameter in line:
                    lines[i] = parameter + ': ' + values[j] + '\n'
                    break

        with open(heterogeneity_file, 'w') as f:
            f.writelines(lines)

    def run_simulation(self):
        threading.Thread(target=self.execute_command).start()

    def execute_command(self):
        command = "./deploy.sh"
        subprocess.call(command, shell=True)

# You can add additional code to handle other functionalities specific to the Heterogenity GUI if needed

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = HeterogeneityParametersWindow()
    window.show()
    app.exec_()
