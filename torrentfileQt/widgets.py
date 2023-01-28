import os
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *


class DropGroupBox(QGroupBox):

    pathSelected = Signal(str, str)

    def __init__(self, parent: QWidget = None):
        """
        A groupbox with buttons inside for dragging and dropping.

        Parameters
        ----------
        parent : QWidget, optional
            _description_, by default None
        """
        super().__init__(parent=parent)
        self.setProperty("DropGroupBox", True)
        self.layout = QVBoxLayout(self)
        self._label = QLabel("")
        self._label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self._label)
        self.hlayout = QHBoxLayout()
        self.layout.addLayout(self.hlayout)

    def addButton(self, button: QPushButton):
        self.hlayout.addWidget(button)

    def setLabelText(self, text):
        self._label.setText(text)

    def dragEnterEvent(self, event):
        """Drag enter event for widget."""
        if event.mimeData().hasUrls:
            event.accept()
            return True
        return event.ignore()

    def dragMoveEvent(self, event):
        """Drag Move Event for widgit."""
        if event.mimeData().hasUrls:
            event.accept()
            return True
        return event.ignore()

    def dropEvent(self, event) -> bool:
        """Drag drop event for widgit."""
        urls = event.mimeData().urls()
        path = urls[0].toLocalFile()
        if os.path.exists(path):
            path = os.path.normpath(path)
            self.setLabelText(path)
            self.pathSelected.emit(path)
            return True
        return False
