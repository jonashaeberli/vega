from python_qt_binding import QtCore, QtGui, QtWidgets


class ManageScrollWidgets():
    def __init__(self, ui):
        self.ui = ui  # Assign ui to self.ui
        self.widget_sets = []
        self.model = ScrollModel()

    def add_widget_set(self, type='move'):
        widget_set_layout = QtWidgets.QHBoxLayout()

        if type == 'move':
            # Create individual widgets
            type_combo_box = QtWidgets.QComboBox()
            type_combo_box.addItem("Start")
            type_combo_box.addItem("End")
            type_combo_box.addItem("Via")
            
            x_label = QtWidgets.QLabel("X:")
            x_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
            x_spin_box = QtWidgets.QDoubleSpinBox()

            y_label = QtWidgets.QLabel("Y:")
            y_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
            y_spin_box = QtWidgets.QDoubleSpinBox()

            z_label = QtWidgets.QLabel("Z:")
            z_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
            z_spin_box = QtWidgets.QDoubleSpinBox()

            yaw_label = QtWidgets.QLabel("Yaw:")
            yaw_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
            yaw_spin_box = QtWidgets.QDoubleSpinBox()

            delete_btn = QtWidgets.QPushButton("Delete")

            # Add widgets to layout
            widget_set_layout.addWidget(type_combo_box)
            widget_set_layout.addWidget(x_label)
            widget_set_layout.addWidget(x_spin_box)
            widget_set_layout.addWidget(y_label)
            widget_set_layout.addWidget(y_spin_box)
            widget_set_layout.addWidget(z_label)
            widget_set_layout.addWidget(z_spin_box)
            widget_set_layout.addWidget(yaw_label)
            widget_set_layout.addWidget(yaw_spin_box)
            widget_set_layout.addWidget(delete_btn)

        elif type == 'gripper':
            # Create individual widgets
            type_combo_box = QtWidgets.QComboBox()
            type_combo_box.addItem("Gripper")

            x_label = QtWidgets.QLabel("X:")
            x_spin_box = QtWidgets.QDoubleSpinBox()

            y_label = QtWidgets.QLabel("Y:")
            y_spin_box = QtWidgets.QDoubleSpinBox()

            z_label = QtWidgets.QLabel("Z:")
            z_spin_box = QtWidgets.QDoubleSpinBox()

            yaw_label = QtWidgets.QLabel("Yaw:")
            yaw_spin_box = QtWidgets.QDoubleSpinBox()

            delete_btn = QtWidgets.QPushButton("Delete")

            # Add widgets to layout
            widget_set_layout.addWidget(type_combo_box)
            widget_set_layout.addWidget(x_label)
            widget_set_layout.addWidget(x_spin_box)
            widget_set_layout.addWidget(y_label)
            widget_set_layout.addWidget(y_spin_box)
            widget_set_layout.addWidget(z_label)
            widget_set_layout.addWidget(z_spin_box)
            widget_set_layout.addWidget(yaw_label)
            widget_set_layout.addWidget(yaw_spin_box)
            widget_set_layout.addWidget(delete_btn)

        # Create a new QWidget for the widget set layout
        widget_set = QtWidgets.QWidget()
        widget_set.setLayout(widget_set_layout)
        
        # Optionally, connect delete button to remove the widget set
        delete_btn.clicked.connect(lambda: self.remove_widget_set(widget_set))

        self.ui.scroll_area_program.layout().addWidget(widget_set)

        # Track the widget set
        self.widget_sets.append(widget_set)

        return widget_set

    def remove_widget_set(self, widget_set):
        # Remove the widget set from the layout and list
        self.ui.scroll_area_program.layout().removeWidget(widget_set)
        widget_set.deleteLater()
        self.widget_sets.remove(widget_set)


class ScrollModel():
    def __init__(self):
        pass