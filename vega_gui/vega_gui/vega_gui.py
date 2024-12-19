import sys
from python_qt_binding.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QScrollArea, QLineEdit, QLabel, QSlider, QPushButton, QHBoxLayout
from python_qt_binding.QtCore import Qt

class VegaGui(QMainWindow):
    def __init__(self, title):
        super(VegaGui, self).__init__()

        self.setWindowTitle(title)

        # Main layout
        self.main_layout = QVBoxLayout()

        # Scroll area widget contents
        self.scroll_widget = QWidget()
        self.scroll_widget.setLayout(self.main_layout)

        # Set the central widget
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)

        # Add input fields for XYZ coordinates
        self.create_input_fields()

        # Add sliders
        self.create_sliders()

        # Add buttons
        self.create_buttons()

        # Create labels to show current values of sliders
        self.slider_labels = []
        for i in range(4):
            label = QLabel(f"Slider {i+1} value: 0")
            self.slider_labels.append(label)
            self.main_layout.addWidget(label)

        # Initialize planning state
        self.trajectory_planned = False

    def create_input_fields(self):
        # Create input fields for XYZ coordinates and rotation angle
        self.coord_labels = ['X:', 'Y:', 'Z:', 'Rotation Angle:']
        self.coord_inputs = []

        for label in self.coord_labels:
            h_layout = QHBoxLayout()
            label_widget = QLabel(label)
            input_widget = QLineEdit()
            self.coord_inputs.append(input_widget)
            h_layout.addWidget(label_widget)
            h_layout.addWidget(input_widget)
            self.main_layout.addLayout(h_layout)

    def create_sliders(self):
        # Create sliders with labels for displaying values
        self.sliders = []
        for i in range(4):
            slider = QSlider(Qt.Horizontal)
            slider.setMinimum(0)
            slider.setMaximum(100)
            slider.setValue(0)
            slider.valueChanged.connect(self.update_slider_label)
            self.sliders.append(slider)
            self.main_layout.addWidget(slider)

    def update_slider_label(self):
        # Update the label when the slider value changes
        for i, slider in enumerate(self.sliders):
            self.slider_labels[i].setText(f"Slider {i+1} value: {slider.value()}")

    def create_buttons(self):
        # Plan trajectory button
        self.plan_button = QPushButton("Plan trajectory")
        self.plan_button.clicked.connect(self.plan_trajectory)
        self.main_layout.addWidget(self.plan_button)

        # Execute trajectory button (locked by default)
        self.execute_button = QPushButton("Execute trajectory")
        self.execute_button.setEnabled(False)  # Locked initially
        self.execute_button.clicked.connect(self.execute_trajectory)
        self.main_layout.addWidget(self.execute_button)

        # Success status label
        self.status_label = QLabel("Status: Not planned yet")
        self.main_layout.addWidget(self.status_label)

    def plan_trajectory(self):
        # Placeholder for the actual trajectory planning logic
        # Get inputs from the user
        x = float(self.coord_inputs[0].text())
        y = float(self.coord_inputs[1].text())
        z = float(self.coord_inputs[2].text())
        rotation_angle = float(self.coord_inputs[3].text())

        # Get the values from the sliders (for additional parameters like speed, force, etc.)
        slider_values = [slider.value() for slider in self.sliders]

        # Insert your logic to plan the trajectory here
        # Example: You could calculate the trajectory, or set up a system command to plan it
        print(f"Planning trajectory with coordinates: X={x}, Y={y}, Z={z}, Rotation={rotation_angle}")
        print(f"Slider values: {slider_values}")

        # Example trajectory planning logic (this would be replaced with actual logic)
        # If planning is successful:
        self.trajectory_planned = True
        self.status_label.setText("Status: Trajectory planned successfully")

        # Enable the Execute button now that the trajectory is planned
        self.execute_button.setEnabled(True)

    def execute_trajectory(self):
        # Check if trajectory is planned before executing
        if not self.trajectory_planned:
            self.status_label.setText("Status: Plan the trajectory first")
            return

        # Placeholder for the actual trajectory execution logic
        # You would now execute the trajectory with the planned data
        print("Executing trajectory...")

        # Insert your logic to execute the trajectory here
        # Example: Sending commands to the system or moving a robot
        # If execution is successful:
        self.status_label.setText("Status: Trajectory executed successfully")

def main():
    app = QApplication(sys.argv)

    # Create the main window with the title
    vega_gui = VegaGui('Vega control GUI')

    vega_gui.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
