# -*- coding: utf-8 -*-
__author__ = "Roman Chernikov, Konstantin Klementiev"
__date__ = "01 Nov 2017"

#try:
#    from matplotlib.backends import qt_compat
#except ImportError:
#    from matplotlib.backends import qt4_compat
#    qt_compat = qt4_compat

QtImports = 'PyQt5', 'PyQt4', 'PySide6', 'PySide2'

for QtImport in QtImports:
    try:
        __import__(QtImport)
        QtName = QtImport
        break
    except ImportError:
        QtName = None
else:
    raise ImportError("Cannot import any PyQt package!")

starImport = False  # star import doesn't work with mock import needed for rtfd

if QtName == "PyQt4":
    from PyQt4 import QtGui, QtCore
    import PyQt4.QtGui as myQtGUI
    myQtGUI2 = myQtGUI

    if starImport:
        from PyQt4.QtGui import *
        from PyQt4.QtCore import *
        Signal = pyqtSignal
    else:
        from PyQt4.QtCore import (
            SIGNAL, QUrl, QObject, QTimer, QProcess,
            QThread, QT_VERSION_STR, PYQT_VERSION_STR)
        from PyQt4.QtGui import QSortFilterProxyModel
        try:
            from PyQt4.QtCore import Signal
        except ImportError:
            from PyQt4.QtCore import pyqtSignal as Signal
    import PyQt4.QtCore
    locals().update(vars(PyQt4.QtCore.Qt))

    from PyQt4.QtOpenGL import QGLWidget
    from PyQt4.QtSql import (QSqlDatabase, QSqlQuery, QSqlTableModel,
                             QSqlQueryModel)
    import PyQt4.QtWebKit as QtWeb
    QtWebCore = QtWeb
    try:
        import PyQt4.Qwt5 as Qwt
    except:  # analysis:ignore
        pass
    from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as\
        FigCanvas
elif QtName == "PyQt5":
    from PyQt5 import QtGui, QtCore
    import PyQt5.QtWidgets as myQtGUI
    myQtGUI2 = myQtGUI

    if starImport:
        from PyQt5.QtGui import *
        from PyQt5.QtCore import *
        from PyQt5.QtWidgets import *
        Signal = pyqtSignal
    else:
        from PyQt5.QtCore import (
            pyqtSignal, QUrl, QObject, QTimer, QProcess, QThread,
            QT_VERSION_STR, PYQT_VERSION_STR, QSortFilterProxyModel)
        try:
            from PyQt5.QtCore import Signal
        except ImportError:
            from PyQt5.QtCore import pyqtSignal as Signal
    import PyQt5.QtCore
    locals().update(vars(PyQt5.QtCore.Qt))

    from PyQt5.QtOpenGL import QGLWidget
    from PyQt5.QtSql import (QSqlDatabase, QSqlQuery, QSqlTableModel,
                             QSqlQueryModel)
    try:
        import PyQt5.QtWebEngineWidgets as QtWeb
    except ImportError:
        import PyQt5.QtWebKitWidgets as QtWeb
    QtWebCore = QtWeb
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as\
        FigCanvas
elif QtName == "PySide6":
    from PySide6 import QtGui, QtCore
    import PySide6.QtWidgets as myQtGUI
    myQtGUI2 = QtGui

    if starImport:
        from PySide6.QtGui import *
        from PySide6.QtCore import *
        from PySide6.QtWidgets import *
    else:
        from PySide6.QtCore import (
            QUrl, QObject, QTimer, QProcess, QThread, QSortFilterProxyModel)
        try:
            from PySide6.QtCore import Signal
        except ImportError:
            from PySide6.QtCore import pyqtSignal as Signal
    import PySide6.QtCore
    QT_VERSION_STR = PySide6.QtCore.qVersion()
    PYQT_VERSION_STR = PySide6.__version__
    locals().update(vars(PySide6.QtCore.Qt))

    from PySide6.QtOpenGLWidgets import QOpenGLWidget as QGLWidget
    from PySide6.QtSql import (QSqlDatabase, QSqlQuery, QSqlTableModel,
                               QSqlQueryModel)
    import PySide6.QtWebEngineWidgets as QtWeb
    import PySide6.QtWebEngineCore as QtWebCore
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as\
        FigCanvas
elif QtName == "PySide2":
    from PySide2 import QtGui, QtCore
    import PySide2.QtWidgets as myQtGUI
    myQtGUI2 = myQtGUI

    if starImport:
        from PySide2.QtGui import *
        from PySide2.QtCore import *
        from PySide2.QtWidgets import *
    else:
        from PySide2.QtCore import (
            QUrl, QObject, QTimer, QProcess, QThread, QSortFilterProxyModel)
        try:
            from PySide2.QtCore import Signal
        except ImportError:
            from PySide2.QtCore import pyqtSignal as Signal
    import PySide2.QtCore
    QT_VERSION_STR = PySide2.QtCore.qVersion()
    PYQT_VERSION_STR = PySide2.__version__
    locals().update(vars(PySide2.QtCore.Qt))

    from PySide2.QtOpenGL import QGLWidget
    from PySide2.QtSql import (QSqlDatabase, QSqlQuery, QSqlTableModel,
                               QSqlQueryModel)
    try:
        import PySide2.QtWebEngineWidgets as QtWeb
    except ImportError:
        import PySide2.QtWebKitWidgets as QtWeb
    QtWebCore = QtWeb
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as\
        FigCanvas
else:
    raise ImportError("Cannot import any Python Qt package!")

if not starImport:
    (QWidget, QApplication, QTabWidget, QToolBar, QStatusBar,
     QTreeView, QAbstractItemView, QHBoxLayout, QVBoxLayout,
     QSplitter, StdQComboBox, QMenu, QListWidget, QTextEdit, QMessageBox,
     QFileDialog, QListWidgetItem, QGroupBox, QProgressBar, QLabel, QTableView,
     QSizePolicy, QLineEdit, QCheckBox, QSpinBox, QSlider, QToolButton,
     QPushButton, QDialog) = (
        myQtGUI.QWidget, myQtGUI.QApplication,
        myQtGUI.QTabWidget, myQtGUI.QToolBar, myQtGUI.QStatusBar,
        myQtGUI.QTreeView, myQtGUI.QAbstractItemView,
        myQtGUI.QHBoxLayout, myQtGUI.QVBoxLayout, myQtGUI.QSplitter,
        myQtGUI.QComboBox, myQtGUI.QMenu, myQtGUI.QListWidget,
        myQtGUI.QTextEdit, myQtGUI.QMessageBox, myQtGUI.QFileDialog,
        myQtGUI.QListWidgetItem, myQtGUI.QGroupBox, myQtGUI.QProgressBar,
        myQtGUI.QLabel, myQtGUI.QTableView, myQtGUI.QSizePolicy,
        myQtGUI.QLineEdit, myQtGUI.QCheckBox, myQtGUI.QSpinBox,
        myQtGUI.QSlider, myQtGUI.QToolButton, myQtGUI.QPushButton,
        myQtGUI.QDialog)
    QAction, QShortcut = myQtGUI2.QAction, myQtGUI2.QShortcut
    (QIcon, QFont, QKeySequence, QStandardItemModel, QStandardItem, QPixmap,
     QDoubleValidator, QIntValidator, QDrag) = (
        QtGui.QIcon, QtGui.QFont, QtGui.QKeySequence, QtGui.QStandardItemModel,
        QtGui.QStandardItem, QtGui.QPixmap, QtGui.QDoubleValidator,
        QtGui.QIntValidator, QtGui.QDrag)


class mySlider(QSlider):
    def __init__(self, parent, scaleDirection, scalePosition):
        super(mySlider, self).__init__(scaleDirection)
        self.setTickPosition(scalePosition)
        self.scale = 1.

    def setRange(self, start, end, step):
        if step == 0:
            return
        self.scale = 1. / step
        # QSlider.setRange(self, int(start/step), int(end/step))
        super(mySlider, self).setRange(int(start/step), int(end/step))

    def setValue(self, value):
        # QSlider.setValue(self, int(value*self.scale))
        super(mySlider, self).setValue(int(value*self.scale))


try:
    glowSlider = Qwt.QwtSlider
    glowTopScale = Qwt.QwtSlider.TopScale
except:  # analysis:ignore
    glowSlider = mySlider
    glowTopScale = QSlider.TicksAbove


class QComboBox(StdQComboBox):
    """
    Disabling off-focus mouse wheel scroll is based on the following solution:
    https://stackoverflow.com/questions/3241830/qt-how-to-disable-mouse-scrolling-of-qcombobox/3242107#3242107
    """

    def __init__(self, *args, **kwargs):
        super(QComboBox, self).__init__(*args, **kwargs)
        # self.scrollWidget=scrollWidget
        self.setFocusPolicy(QtCore.Qt.StrongFocus)

    def wheelEvent(self, *args, **kwargs):
        if self.hasFocus():
            return StdQComboBox.wheelEvent(self, *args, **kwargs)
        else:
            return self.parent().wheelEvent(*args, **kwargs)
