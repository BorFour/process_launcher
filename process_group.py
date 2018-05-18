

from PyQt5.QtWidgets import (QWidget, QGridLayout, QLabel,
                             QHBoxLayout, QVBoxLayout, QPushButton)

from process_widget import ProcessWidget
import PyQt5.QtCore


class ProcessGroup(QWidget):
    """docstring for ProcessGroup"""

    def __init__(self, window=None, name=None):
        super(ProcessGroup, self).__init__(window)
        self.container = _ProcessContainer(self)
        self.header = _ProcessGroupHeader(self, name)
        # self.header = QLabel(name or 'This is the header of the process group')
        # self.container = ProcessWidget(self)
        self.init_style()
        self.init_layout()
        self.n_columns = 2

    def add_element(self, element):
        # return
        return self.container.add_element(element)

    def init_style(self):
        pass
        # self.setStyleSheet("margin:5px; border:1px solid rgb(0, 255, 0); ")

    def init_layout(self):
        self.hbox1 = QHBoxLayout()
        # self.hbox1.setSpacing(1)
        self.hbox1.addWidget(self.header)

        self.hbox2 = QHBoxLayout()
        # self.hbox2.setSpacing(1)
        self.hbox2.addWidget(self.container)

        self.vbox = QVBoxLayout()
        # self.vbox.setStretch(2, 2)
        self.vbox.addLayout(self.hbox1)
        self.vbox.addLayout(self.hbox2)
        self.setLayout(self.vbox)

    def toJSON(self):
        ret = {}
        ret["name"] = self.header.name
        ret["processes"] = []
        for process in self.container.elements:
            ret["processes"].append(process.toJSON())

        return ret


class _ProcessGroupHeader(QWidget):

    def __init__(self, window, name=None):
        super(_ProcessGroupHeader, self).__init__(window)
        self.name = name
        self.parent = window
        self.title = QLabel(self.name or 'Group of processes')
        self.title.setAlignment(PyQt5.QtCore.Qt.AlignHCenter)

        self.launch_button = QPushButton(self)
        self.launch_button.setText("Launch all")
        self.launch_button.clicked.connect(self.parent.container.run_all)

        self.stop_button = QPushButton(self)
        self.stop_button.setText("Stop this group's processes")
        self.stop_button.clicked.connect(self.parent.container.kill_them_all)

        self.init_layout()

    def init_layout(self):
        self.widget_layout = QVBoxLayout()
        self.widget_layout.addWidget(self.title)
        self.widget_layout.addWidget(self.launch_button)
        self.widget_layout.addWidget(self.stop_button)
        self.setLayout(self.widget_layout)


class _ProcessContainer(QWidget):

    def __init__(self, parent):
        super(_ProcessContainer, self).__init__(parent)
        self.parent = parent
        self.init_layout()
        self.elements = set()

    def init_layout(self):
        self.widget_layout = QGridLayout()
        self.setLayout(self.widget_layout)

    def add_element(self, element):
        self.widget_layout.addWidget(element, len(self.elements) / self.parent.n_columns,
                                     len(self.elements) % self.parent.n_columns)
        self.elements.add(element)

    def run_all(self):
        for process_widget in self.elements:
            process_widget.process.restart()  # REVIEW: or run?

    def kill_them_all(self):
        for process_widget in self.elements:
            process_widget.process.kill()  # REVIEW: or terminate?

    def restore_processes(self, data: list):
        """Data is normally a list in the JSON format."""
        for d in data:
            p = ProcessWidget(self, d["args"], directory=d["dir"])
            self.add_element(p)
