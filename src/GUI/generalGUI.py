import os
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QComboBox
import threading
import subprocess

# Get the directory of the currently executing script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Define a relative path to the "input" directory from the script's directory
relative_path = "..\input\general.txt"

# Combine the current directory with the relative path to create the full file path
geral_file = os.path.join(current_dir, relative_path)

# Define an array of parameter names
parameters = [
    "Numero_blocos_direcao_x",
    "Numero_blocos_direcao_y",
    "Constante_alpha_c",
    "Constante_beta_c",
    "Tolerancia_metodo_iterativo",
    "Tolerancia_T",
    "Razao_crescimento_passo_de_tempo",
    "Tempo_maximo_de_simulacao",
    "Passo_de_tempo_inicial",
    "Passo_de_tempo_final",
    "Passo_de_tempo_impressao",
    "Kap_type",
    "Solution_type"
]


class GeneralParametersWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(GeneralParametersWindow, self).__init__()
        self.setWindowTitle("General")

        self.central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QtWidgets.QGridLayout(self.central_widget)
        self.form_layout = QtWidgets.QFormLayout()
        self.layout.addLayout(self.form_layout, 0, 0)

        self.entries = []
        for parameter in parameters:
            label = QtWidgets.QLabel(parameter)
            entry = QtWidgets.QLineEdit()
            # Replace QLineEdit with QComboBox for specific parameters
            if parameter == "Kap_type":
                entry = QComboBox()
                entry.addItems(["1", "2", "3", "4", "5", "6"])  # Add selection options

            if parameter == "Solution_type":
                entry = QComboBox()
                entry.addItems(["1", "2", "3"])  # Add selection options
                
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
        with open(geral_file, 'r') as f:
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
            if isinstance(entry, QComboBox):
                entry.setCurrentText(value)  # Set the selected item in the QComboBox
            else:
                entry.setText(value)  # For other widgets like QLineEdit


    def save_data(self):
        values = []
        for entry in self.entries:
            if isinstance(entry, QtWidgets.QComboBox):
                values.append(entry.currentText())
            elif isinstance(entry, QtWidgets.QLineEdit):
                values.append(entry.text())
            else:
                values.append('')

        with open(geral_file, 'r') as f:
            lines = f.readlines()

        for i, line in enumerate(lines):
            for j, parameter in enumerate(parameters):
                if parameter in line:
                    lines[i] = parameter + ': ' + values[j] + '\n'
                    break

        with open(geral_file, 'w') as f:
            f.writelines(lines)

    def run_simulation(self):
        threading.Thread(target=self.execute_command).start()

    def execute_command(self):
        command = "gcc -o runtest main.c -march=native -fopenmp -O3 -lm && .\\runtest.exe" # ".\deploy.sh"
        subprocess.call(command, shell=True)
