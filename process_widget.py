
import subprocess

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QWidget, QPushButton, QLabel, QHBoxLayout, QVBoxLayout,
    QTableWidget, QTableWidgetItem)


DEFAULT_DIRECTORY = "~/Playground/python/pyqt5/first_example"
SLEEP_AFTER_COMMAND = 20


class Process(object):
    """docstring for Process"""

    def __init__(self, table_widget: QTableWidget, name=None, directory=None):
        super(Process, self).__init__()
        self.table_widget = table_widget
        self.name = name
        self.directory = directory
        self.popen = None

    @property
    def args(self):
        return [
            self.table_widget.item(i, 0).text()
            for i in range(self.table_widget.rowCount())
            if self.table_widget.item(i, 0)
        ]

    def create_command(self):
        command = "{}".format(self.args[0])
        for argument in self.args[1:]:
            command += " {}".format(argument)
        return command

    def restart(self):
        if self.popen:
            self.kill()
        self.run()

    def run(self):
        self.popen = subprocess.Popen(args=[
            'konsole',
            '--workdir', self.directory,
            # Run the new instance of Konsole in a separate process.
            '--noclose',
            '--separate',
            '-e', '{}'.format(self.create_command())
        ], shell=False)

    def kill(self):
        if self.popen: self.popen.kill()

    def terminate(self):
        if self.popen: self.popen.terminate()
        self.popen = None


class ProcessWidget(QWidget):
    """docstring for ProcessWidget"""
    n_processes = 0

    def __init__(self, window, *args, directory=None):
        super(ProcessWidget, self).__init__(window)
        self.args = list(*args)

        self._init_args_table(self.args)
        self.process = Process(self.args_table_widget,
                               name="process {}".format(
                                   ProcessWidget.n_processes), directory=directory or DEFAULT_DIRECTORY)

        self.directory_text = QLabel(self.process.directory)
        self.button = QPushButton(self)
        self.button.setText("Edit {}".format(
            self.process.name))

        self.restart_button = QPushButton(self)
        self.restart_button.setIcon(QIcon('./img/arrow_restart.png'))
        self.restart_button.setIconSize(QSize(24, 24))
        self.restart_button.clicked.connect(self.process.restart)

        ProcessWidget.n_processes += 1
        self.init_layout()

    def _init_args_table(self, *args):
        # TODO: add something to add more arguments
        self.args_table_widget = QTableWidget()
        self.args_table_widget.setRowCount(0)
        self.args_table_widget.setColumnCount(1)
        for i, arg in enumerate(*args):
            self.args_table_widget.insertRow(i)
            self.args_table_widget.setItem(0, i, QTableWidgetItem(arg))

    def init_layout(self):
        self.hbox1 = QHBoxLayout()
        self.hbox1.addWidget(self.directory_text)

        self.hbox2 = QHBoxLayout()
        self.hbox2.addWidget(self.args_table_widget)

        self.hbox3 = QHBoxLayout()
        self.hbox3.addWidget(self.button)
        self.hbox3.addWidget(self.restart_button)

        self.vbox = QVBoxLayout()
        self.vbox.addLayout(self.hbox1)
        self.vbox.addLayout(self.hbox2)
        self.vbox.addLayout(self.hbox3)
        self.setLayout(self.vbox)

    def toJSON(self):
        ret = {}
        ret["dir"] = self.process.directory
        ret["args"] = []

        for arg in self.process.args:
            ret["args"].append(arg)

        return ret