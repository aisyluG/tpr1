from PyQt5 import QtWidgets, QtGui, QtCore
import math
import numpy as np

def sign(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0
class drawWidget(QtWidgets.QWidget):
    states = 0
    optimums = None
    probabilitys = None
    def __init__(self, parent):
        super().__init__(parent=parent)

    def paintEvent(self, paintEvent):
        p = QtGui.QPainter()
        p.begin(self)
        self.draw(p)
        p.end()

    def paint(self, optimums, probabilitys):
        self.states = len(optimums)
        self.optimums = optimums
        self.probabilitys = probabilitys

    def draw(self, painter):
        if self.states != 0:
            n = self.states
            radius_state = 20
            angle = math.pi/n
            r = int(self.width()/2) - 2*radius_state
            # a = 2 * r * math.sin(math.pi/n)
            # center = QtCore.QPoint(int(self.height()/2), int(self.width()/2))
            x0, y0 = int((self.width() - radius_state)/2), self.height() - radius_state*2

            pen_line = QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.SolidLine)
            points = []
            for i in range(n):
                c = math.sqrt(2 * r ** 2 * (1 - math.cos(i*angle * 2)))
                x = x0 + c * math.cos(i*angle)
                y = y0 - c * math.sin(i*angle)
                points.append(QtCore.QPoint(int(x), int(y)))

            painter.setPen(pen_line)
            for i in range(n):
                strategy = int(self.optimums[i])
                for j in range(n):
                    print(strategy)
                    if self.probabilitys[strategy, i, j] != 0:
                        x = points[j].x()
                        y = points[j].y()
                        text = f'{strategy + 1}({self.probabilitys[strategy, i, j]})'
                        if i == j:
                            path = QtGui.QPainterPath()
                            path.moveTo(x - radius_state, y)
                            path.quadTo(x + 2*radius_state, y + 4*radius_state, x + radius_state, y)
                            painter.drawPath(path)
                            painter.drawText(x + 1.5*radius_state, y + radius_state, text)
                        else:
                            painter.drawLine(points[i], points[int(j)])
                            # рисуем стрелочку
                            # angle_arrow = math.pi * 2 - (j + 1)* math.pi / n
                            angle_arrow = math.pi/n + (j - i)*math.pi/n
                            x1 = x + int(radius_state*math.cos(angle_arrow))
                            y1 = y + int(radius_state * math.sin(angle_arrow))
                            begin = QtCore.QPoint(x1, y1)
                            x2 = x1 + int(radius_state*math.cos(angle_arrow - math.pi/6))
                            y2 = y1 + int(radius_state*math.sin(angle_arrow - math.pi/6))
                            x3 = x1 + int(radius_state * math.cos(angle_arrow + math.pi / 6))
                            y3 = y1 + int(radius_state * math.sin(angle_arrow + math.pi / 6))
                            painter.drawLine(begin, QtCore.QPoint(x2, y2))
                            painter.drawLine(begin, QtCore.QPoint(x3, y3))
                            painter.drawText(abs(points[i].x() + x)/2 + 10*sign(j -i),
                                             abs(points[i].y() + y)/2 + 30*sign(j -i), text)

            pen_fig = QtGui.QPen(QtGui.QColor('#acf0af'), 2, QtCore.Qt.SolidLine)
            painter.setPen(pen_fig)
            painter.setBrush(QtGui.QColor('#acf0af'))
            for i in range(n):
                painter.drawEllipse(points[i], radius_state, radius_state)
            pen_text = QtGui.QPen(QtCore.Qt.black, 5, QtCore.Qt.SolidLine)
            painter.setPen(pen_text)
            for i in range(n):
                painter.drawText(points[i].x() - radius_state, points[i].y() - radius_state,
                                 2*radius_state, 2*radius_state, QtCore.Qt.AlignCenter, str(i + 1))