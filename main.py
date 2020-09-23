from window import Ui_MainWindow
from PyQt5 import QtWidgets, QtGui, QtCore
import sys
from TableModel import TableModel
from algorithm import algorithm
from datetime import datetime
from drawWidget import drawWidget


class Window(QtWidgets.QMainWindow):
    report = ''
    optimum = []
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.yield_model = TableModel()
        self.ui.yield_table.setModel(self.yield_model)
        self.ui.yield_table.resizeColumnsToContents()

        self.probability_model = TableModel(1)
        self.ui.probabilitys_table.setModel(self.probability_model)
        self.ui.probabilitys_table.resizeColumnsToContents()
        # palette = self.ui.probabilitys_table.horizontalHeader().palette()
        # palette.setColor(QtGui.QPalette.Normal, QtGui.QPalette.Window, QtCore.Qt.red)
        # self.ui.probabilitys_table.setStyleSheet('QHeaderView {background-color: yellow;}')

        self.ui.changeNumbers_bt.clicked.connect(self.changeMatricesSize)
        self.ui.calcBt.clicked.connect(self.calculateOptimum)

        #
        saveAction = QtWidgets.QAction('Сохранить', self)
        saveAction.setShortcut('Ctrl+S')
        saveAction.triggered.connect(self.save)
        self.ui.menubar.addAction(saveAction)

    def changeMatricesSize(self):
        states = int(self.ui.states_spinB.text())
        strategys = int(self.ui.strategys_spinB.text())
        stages = int(self.ui.stages_spinB.text())
        self.yield_model.resize(strategys, states)
        self.probability_model.resize(strategys, states)
        self.ui.yield_table.resizeColumnsToContents()
        self.ui.probabilitys_table.resizeColumnsToContents()

    def calculateOptimum(self):
        if self.probability_model.get_size() == (int(self.ui.strategys_spinB.text()), int(self.ui.states_spinB.text())):
            res, self.optimum = algorithm(states=int(self.ui.states_spinB.text()), strategys=int(self.ui.strategys_spinB.text()),
                      n=int(self.ui.stages_spinB.text()), probabilitys=self.probability_model.get_data(),
                      yields=self.yield_model.get_data())
            self.ui.textEdit.setHtml(str(res))
            self.report = res
            # self.ui.widget.draw(QtGui.QPainter(), self.optimum
            self.ui.tabWidget.clear()
            palette = QtGui.QPalette()
            brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
            brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
            brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
            brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
            brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
            brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
            for i in range(int(self.ui.stages_spinB.text())):
                try:
                    tab = QtWidgets.QWidget()
                    tab.setObjectName(f"tab{i}")
                    widget = drawWidget(tab)
                    widget.setGeometry(QtCore.QRect(0, 0, 401, 391))
                    widget.setAutoFillBackground(True)
                    widget.setObjectName(f"widget{i}")
                    widget.setPalette(palette)
                    self.ui.tabWidget.addTab(tab, f"Этап {i + 1}")
                    widget.paint(self.optimum[i], self.probability_model.get_data())
                    widget.repaint()
                except Exception:
                    print(Exception.mro())
        else:
            self.ui.statusbar.showMessage('Проверте правильность введенных данных.')

    def save(self):
        try:
            filename, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Сохранить', '/report.html',
                                                                'Результаты алгоритма (*.html)')
            if _ == 'Результаты алгоритма (*.html)':
                with open(filename, 'w') as file:
                    file.write(f'Время {datetime.now()}<br>')
                    file.write('<h3>Исходные данные:</h3>')
                    file.write('<p style="margin-left: 50px;"><b>Матрицы переходных вероятностей:</b></p>')
                    file.write(self.probability_model.get_table_to_save())
                    file.write('<p style="margin-left: 50px;"><b>Матрицы доходностей:</b></p>')
                    file.write(self.yield_model.get_table_to_save())
                    file.write(self.report)
        except Exception:
            print('Error!')





if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = Window()
    main.show()
    sys.exit(app.exec_())