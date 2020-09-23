from PyQt5.QtCore import QAbstractTableModel, Qt, QModelIndex, QVariant
from PyQt5 import QtGui
import numpy as np
from prettytable import PrettyTable

class TableModel(QAbstractTableModel):
    strategys = 1
    states = 2
    def __init__(self, limit=None):
        super().__init__()
        self.table_data = np.zeros((self.strategys, self.states, self.states))
        self.limit=limit

    # устанавлив.аем данные по заданному модельному индексу
    def setData(self, index, data, role=Qt.EditRole):
        # если элемент не редактируем, то изменения не вносятся
        if role != Qt.EditRole:
            return False
        # изменяем данные в массиве по заданному индексу заданным значением
        row = index.row()
        column = index.column()
        if self.limit is None or data <= self.limit:
            self.table_data[row//(self.states + 1), row%(self.states + 1) - 1, column] = data
        return True

    def rowCount(self, parent=QModelIndex()):
        return (self.states + 1)*self.strategys

    def columnCount(self, parent=QModelIndex()):
        return self.states

    # метод для передачи представлениям и делегатам информации о данных модели
    def data(self, index, role=Qt.DisplayRole):
        state2 = index.column()
        strategy = index.row()//(self.states+1)
        state1 = index.row()%(self.states+1)
        # если отображаемые или редактируемые данные
        if role == Qt.EditRole or role == Qt.DisplayRole:
            if state1 == 0:
                # return str(f'Strategy {strategy + 1}')
                return ''
            else:
                dt = self.table_data[strategy, state1 - 1, state2]
                return float(dt)

        # если цвет фона и столбец с изменяющимся в зависимости от знака числа фоном
        if role == Qt.BackgroundColorRole:
            if state1 != 0:
                return QtGui.QBrush(QtGui.QColor('#eaeaf0'))
        return QVariant()

    # метод для передачи представлениям и делегатам информации о заголовках в модели
    def headerData(self, p_int, Qt_Orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return QVariant()
        # если заголовки столбцов
        if Qt_Orientation == Qt.Horizontal:
            return f'Состояние {p_int + 1}'
        # если заголовки строк
        elif Qt_Orientation == Qt.Vertical:
            if p_int%(self.states + 1) == 0:
                return f'Стратегия {p_int//(self.states+1) + 1}'
            else:
                return f'Состояние {p_int%(self.states + 1)}'
        return QVariant()

    #метод, возвращающийкомбинацию флагов, соответствующую каждому элементу
    def flags(self, index):
        if index.row()%(self.states + 1) == 0:
            return Qt.ItemIsEnabled
        return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable

    # метод для добавления новых состояний в модель
    def insertStates(self, state, count, parent):
        # уведомляем о том, что собираемся вставить новые столбцы
        self.beginInsertColumns(parent, state, state + count - 1)
        r = np.zeros((self.strategys, self.states + count, self.states + count))
        # print(self.table_data[1,:, 0])
        for i in reversed(range(self.strategys)):
            self.beginInsertRows(parent, (i+1) * (self.states) + 1, (i +1)* (self.states) + count)
            for j in range(self.states):
                r[i,:, j] = np.hstack((self.table_data[i,:,j], np.zeros(count)))
            self.endInsertRows()
        self.table_data = r
        print(self.table_data)
        # уведомляем о том, что количество столбцов изменилось
            # (self.strategys - count)*state + self.strategys*count - 1)
        self.endInsertColumns()
        # for i in (range(1, self.strategys + 1)):
        #     print('oo', i * (self.states + 1))
        #     self.beginInsertRows(parent, i * (self.states + 1) - 1, count)# (self.strategys - count)*state + self.strategys*count - 1)
        #     # print(self.strategys*sta+te + self.strategys*count - 1)
        #     self.endInsertRows()
        # self.beginInsertRows(parent, self.states + 1,
        #                      count)  # (self.strategys - count)*state + self.strategys*count - 1)
        # #     # print(self.strategys*sta+te + self.strategys*count - 1)
        # self.endInsertRows()
        return True

    # метод для удаления состояний из модели
    def removeStates(self, new_states, count, parent):
        # уведомляем о том, что собираемся удалить столбцы из модели
        self.beginRemoveColumns(parent, new_states, new_states + count - 1)
        self.table_data = self.table_data[:, :new_states + 1]
        # уведомляем о том, что количество столбцов изменилось
        self.endRemoveColumns()
        for i in reversed(range(self.strategys)):
            # уведомляем о том, что собираемся удалить строки из модели
            self.beginRemoveRows(parent, (i+1) * (self.states) + 1 - count, (i +1)* (self.states))
            self.table_data[i] = self.table_data[i, :new_states + 1]
            # уведомляем о том, что количество строк изменилось
            self.endRemoveRows()

    # метод для добавления новых строк в модель
    def insertStrategys(self, row, count, parent):
        # уведомляем о том, что собираемся вставить новые строки
        self.beginInsertRows(parent, row, row + count*self.states + count - 1)
        r = np.zeros((count, self.states, self.states))
        self.table_data = np.vstack((self.table_data, r))
        # уведомляем о том, что количество строк изменилось
        self.endInsertRows()
        return True

    # метод для удаления строк из модели
    def removeStrategys(self, new_strategys, count, parent):
        # уведомляем о том, что собираемся удалить строки из модели
        self.beginRemoveRows(parent, new_strategys*self.states, new_strategys*self.states + count*self.states + count - 1)
        self.table_data = self.table_data[:new_strategys + 1]
        # уведомляем о том, что количество строк изменилось
        self.endRemoveRows()

    def resize(self, new_strategys, new_states):
        if new_strategys > self.strategys:
            self.insertStrategys(self.strategys, new_strategys - self.strategys, QModelIndex())
        elif new_strategys < self.strategys:
            self.removeStrategys(new_strategys, self.strategys - new_strategys, QModelIndex())
        self.strategys = new_strategys
        if new_states > self.states:
            self.insertStates(self.states, new_states - self.states, QModelIndex())
        elif new_states < self.states:
            self.removeStates(new_states, self.states - new_states, QModelIndex())
        self.states = new_states

    def get_data(self):
        return self.table_data

    def get_table_to_save(self):
        head = [self.headerData(x, Qt.Horizontal, role=Qt.DisplayRole) for x in range(self.states)]
        table = '<table border="1">\n<tr>'
        # for s in range(self.strategys):
        #     table += (f'<i>Стратегия {s + 1}</i>' + '<br>')
        for strategy in range(self.strategys):
            table += ('<td>\n' + f'<table><caption>Стратегия №{strategy + 1}</caption>')
            table += ('<tr><th>' + '</th><th>'.join(head) + '</th></tr>')
            for i in range(self.states):
                table += ('<tr><td>' + '</td><td>'.join(map(str, self.table_data[strategy, i])) + '</td></tr>')
            table += ('</table></td>')
        table += '</tr></table>'
        return table

    def get_size(self):
        return self.strategys, self.states