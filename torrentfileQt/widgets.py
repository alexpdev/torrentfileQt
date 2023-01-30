import os
from pathlib import Path
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

class DropGroupBox(QGroupBox):

    pathSelected = Signal(str)

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
        self.setAcceptDrops(True)
        self.layout = QVBoxLayout(self)
        self._label = QLabel("")
        self._label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._path = None
        self.layout.addWidget(self._label)
        self.hlayout = QHBoxLayout()
        self.layout.addLayout(self.hlayout)

    def addButton(self, button: QPushButton):
        """Add a button widget to groupbox."""
        self.hlayout.addWidget(button)

    def setLabelText(self, text: str):
        """Set the label text."""
        self._label.setText(text)

    def getLabelText(self) -> str:
        """Get the label text."""
        return self._label.text()

    def setPath(self, path: str):
        """Set the path."""
        self._path = path
        path_obj = Path(path)
        if len(path_obj.parts) > 2:
            last_sect = path_obj.parts[-2:]
            self.setLabelText("..." + os.path.join(*last_sect))
        else:
            self.setLabelText(path)

    def getPath(self) -> str:
        """Get the path."""
        return self._path

    def dragEnterEvent(self, event: QMouseEvent) -> bool:
        """Drag enter event for widget."""
        if event.mimeData().hasUrls:
            event.accept()
            return True
        return event.ignore()

    def dragMoveEvent(self, event: QMouseEvent) -> bool:
        """Drag Move Event for widgit."""
        if event.mimeData().hasUrls:
            event.accept()
            return True
        return event.ignore()

    def dropEvent(self, event: QMouseEvent) -> bool:
        """Drag drop event for widgit."""
        urls = event.mimeData().urls()
        path = urls[0].toLocalFile()
        if os.path.exists(path):
            path = os.path.normpath(path)
            self.setLabelText(path)
            self.pathSelected.emit(path)
            return True
        return False
