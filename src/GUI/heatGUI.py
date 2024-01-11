import os
from PyQt5 import QtWidgets, QtCore
import threading
import subprocess

# Get the directory of the currently executing script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Define relative paths
heat_temp_file = os.path.join(current_dir, "..\input\heat.txt")
c_code_executable = os.path.join(current_dir, "\\.temp\heat")

os.system(f"cd {current_dir}\temp && .\heat")

class HeatParametersWindow(QtWidgets.QWidget):
    def __init__(self):
        super(HeatParametersWindow, self).__init__()

        self.layout = QtWidgets.QGridLayout(self)

        self.num_aquecedores_label = QtWidgets.QLabel("Number of heaters:")
        self.num_aquecedores_entry = QtWidgets.QLineEdit()
        self.layout.addWidget(self.num_aquecedores_label, 0, 0)
        self.layout.addWidget(self.num_aquecedores_entry, 0, 1)

        self.headers = ['x (m)', 'y (m)', 'Heat (W)']
        self.labels = []
        self.entries = []
        self.num_boxes = 8

        # Add labels for column titles
        for i, header in enumerate(self.headers):
            title_label = QtWidgets.QLabel(header)
            self.layout.addWidget(title_label, 1, i)

            entry_col = []
            for j in range(self.num_boxes):
                entry = QtWidgets.QLineEdit()
                entry_col.append(entry)
                self.layout.addWidget(entry, j+2, i)
            self.labels.append(title_label)
            self.entries.append(entry_col)

        load_button = QtWidgets.QPushButton("Load Data", self)
        load_button.clicked.connect(self.load_data)
        self.layout.addWidget(load_button, self.num_boxes+3, 1)

        save_button = QtWidgets.QPushButton("Save Data", self)
        save_button.clicked.connect(self.save_data)
        self.layout.addWidget(save_button, self.num_boxes+4, 1)
        
        run_button = QtWidgets.QPushButton("Run Case", self)
        run_button.clicked.connect(self.run_simulation)
        self.layout.addWidget(run_button, self.num_boxes+5, 1)

    def load_data(self):
        # Execute the C code to generate heatTemp.txt
        os.system(f"cd {current_dir}\temp && .\heat")
        with open(os.path.join(current_dir, "..\GUI\temp\heatTemp.txt"), 'r') as f:
            lines = f.readlines()

        num_aquecedores = None
        values = []
        for line in lines:
            line = line.strip()
            if line.startswith('#') or line == '':
                continue
            if num_aquecedores is None:
                num_aquecedores = int(line)
            else:
                values.append(line)

        self.num_aquecedores_entry.setText(str(num_aquecedores))

        num_values = len(values)
        num_boxes = self.num_boxes
        for i in range(num_boxes):
            if i < num_values:
                self.entries[0][i].setText(values[i])
            else:
                self.entries[0][i].setText("")

        for i in range(num_boxes):
            index = i + num_boxes
            if index < num_values:
                self.entries[1][i].setText(values[index])
            else:
                self.entries[1][i].setText("")

        for i in range(num_boxes):
            index = i + 2 * num_boxes
            if index < num_values:
                self.entries[2][i].setText(values[index])
            else:
                self.entries[2][i].setText("")

    def save_data(self):
        num_aquecedores = self.num_aquecedores_entry.text()

        values = []
        for i in range(self.num_boxes):
            value = self.entries[0][i].text()
            if value:
                values.append(value)
        for i in range(self.num_boxes):
            value = self.entries[1][i].text()
            if value:
                values.append(value)
        for i in range(self.num_boxes):
            value = self.entries[2][i].text()
            if value:
                values.append(value)

        with open(heat_temp_file, 'w') as f:
            f.write("\t\tLOCAL_DO_POCO_AQUECEDOR\n")
            f.write("\n")
            f.write("number_of_heaters:\t" + str(num_aquecedores) + "\n")
            f.write("\n")
            f.write("xheat\tyheat\tHeat(W)\n")
            f.write("\n")
            for i in range(self.num_boxes):
                x_index = i
                y_index = i + self.num_boxes
                heat_index = i + 2 * self.num_boxes

                x = values[x_index] if x_index < len(values) else ""
                y = values[y_index] if y_index < len(values) else ""
                heat = values[heat_index] if heat_index < len(values) else ""

                f.write(f"{x:<8}{y:<8}{heat:<12}\n")

    def run_simulation(self):
        threading.Thread(target=self.execute_command).start()

    def execute_command(self):
        command = "gcc -o runtest main.c -march=native -fopenmp -O3 -lm && .\\runtest.exe" #  ".\deploy.sh" #"wsl -d Ubuntu-20.04 -- .\runtest"
        subprocess.call(command, shell=True)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = HeatParametersWindow()
    window.setWindowTitle("Heat")
    window.setGeometry(100, 100, 400, 300)
    window.show()
    sys.exit(app.exec_())
