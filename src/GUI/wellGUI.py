import os
from PyQt5 import QtWidgets, QtCore
import threading
import subprocess
import stat

# Get the directory of the currently executing script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Define relative paths
well_temp_file = os.path.join(current_dir, "../input/well.txt")
c_code_executable = os.path.join(current_dir, "temp/well")

os.system(f"cd {current_dir}/temp && ./well")

class WellParametersWindow(QtWidgets.QWidget):
    def __init__(self):
        super(WellParametersWindow, self).__init__()

        self.layout = QtWidgets.QGridLayout(self)

        self.num_wells_label = QtWidgets.QLabel("Wells:")
        self.num_wells_entry = QtWidgets.QLineEdit()
        self.layout.addWidget(self.num_wells_label, 0, 0)
        self.layout.addWidget(self.num_wells_entry, 0, 1)

        self.headers = ['x (m)', 'y (m)', 'q_sc (std m3/d)', 'rw (m)', 'pwf_ini (kPa)', 'pwf_f (kPa)', 'F_pwf', 'Skin']
        self.labels = []
        self.entries = []
        self.num_boxes = 9

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
        self.layout.addWidget(load_button, self.num_boxes+3, 2)

        save_button = QtWidgets.QPushButton("Save Data", self)
        save_button.clicked.connect(self.save_data)
        self.layout.addWidget(save_button, self.num_boxes+4, 2)
        
        run_button = QtWidgets.QPushButton("Run Case", self)
        run_button.clicked.connect(self.run_simulation)
        self.layout.addWidget(run_button, self.num_boxes+5, 2)

    def load_data(self):
        # Execute the C code to generate wellTemp.txt
        os.system(f"cd {current_dir}/temp && ./well")
        with open(os.path.join(current_dir, "temp/wellTemp.txt"), 'r') as f:
            lines = f.readlines()

        num_wells = None
        values = []
        for line in lines:
            line = line.strip()
            if line.startswith('#') or line == '':
                continue
            if num_wells is None:
                num_wells = int(line)
            else:
                values.append(line)

        self.num_wells_entry.setText(str(num_wells))

        num_values = len(values)
        num_boxes = self.num_boxes
        
        for i in range(num_boxes):
            index = i + 0 * num_boxes
            if index < num_values:
                self.entries[0][i].setText(values[index])
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

        for i in range(num_boxes):
            index = i + 3 * num_boxes
            if index < num_values:
                self.entries[3][i].setText(values[index])
            else:
                self.entries[3][i].setText("")

        for i in range(num_boxes):
            index = i + 4 * num_boxes
            if index < num_values:
                self.entries[4][i].setText(values[index])
            else:
                self.entries[4][i].setText("")

        for i in range(num_boxes):
            index = i + 5 * num_boxes
            if index < num_values:
                self.entries[5][i].setText(values[index])
            else:
                self.entries[5][i].setText("")

        for i in range(num_boxes):
            index = i + 6 * num_boxes
            if index < num_values:
                self.entries[6][i].setText(values[index])
            else:
                self.entries[6][i].setText("")

        for i in range(num_boxes):
            index = i + 7 * num_boxes
            if index < num_values:
                self.entries[7][i].setText(values[index])
            else:
                self.entries[7][i].setText("")

        # for i in range(num_boxes):
        #     index = i + 8 * num_boxes
        #     if index < num_values:
        #         self.entries[8][i].setText(values[index])
        #     else:
        #         self.entries[8][i].setText("")

    def save_data(self):
        num_wells = self.num_wells_entry.text()

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
        for i in range(self.num_boxes):
            value = self.entries[3][i].text()
            if value:
                values.append(value)
        for i in range(self.num_boxes):
            value = self.entries[4][i].text()
            if value:
                values.append(value)
        for i in range(self.num_boxes):
            value = self.entries[5][i].text()
            if value:
                values.append(value)
        for i in range(self.num_boxes):
            value = self.entries[6][i].text()
            if value:
                values.append(value)
        for i in range(self.num_boxes):
            value = self.entries[7][i].text()
            if value:
                values.append(value)
        # for i in range(self.num_boxes):
        #     value = self.entries[8][i].text()
        #     if value:
        #         values.append(value)

        with open(well_temp_file, 'w') as f:
            f.write("\t\tLOCAL_DO_POCO_PRODUTOR_OU_INJETOR\n")
            f.write("\n")
            f.write("number_of_wells:\t" + str(num_wells) + "\n")
            f.write("\n")
            f.write("xwell\tywell\tRate(m3/d)\tRw(m)\tpwf_ini(kPa)\tpwf_f(kPa)\tF_pwf\tSkin_factor\n")
            f.write("\n")
            for i in range(self.num_boxes):
                x_index = i
                y_index = i + self.num_boxes            
                rate_index = i + 2 * self.num_boxes
                rw_index = i + 3 * self.num_boxes
                pwf_ini_index = i + 4 * self.num_boxes
                pwf_f_index = i + 5 * self.num_boxes
                f_pwf_index = i + 6 * self.num_boxes
                skin_factor_index = i + 7 * self.num_boxes

                x = values[x_index] if x_index < len(values) else ""
                y = values[y_index] if y_index < len(values) else ""
                rate = values[rate_index] if rate_index < len(values) else ""
                rw = values[rw_index] if rw_index < len(values) else ""
                pwf_ini = values[pwf_ini_index] if pwf_ini_index < len(values) else ""
                pwf_f = values[pwf_f_index] if pwf_f_index < len(values) else ""
                f_pwf = values[f_pwf_index] if f_pwf_index < len(values) else ""
                skin_factor = values[skin_factor_index] if skin_factor_index < len(values) else ""

                f.write(f"{x}\t{y}\t{rate}\t{rw}\t{pwf_ini}\t{pwf_f}\t{f_pwf}\t{skin_factor}\n")

    def run_simulation(self):
        threading.Thread(target=self.execute_command).start()

    def execute_command(self):
        command = "./deploy.sh" #"wsl -d Ubuntu-20.04 -- ./runtest"
        subprocess.call(command, shell=True)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = WellParametersWindow()
    window.setWindowTitle("Well")
    window.setGeometry(100, 100, 400, 300)
    window.show()
    sys.exit(app.exec_())
