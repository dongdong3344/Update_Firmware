import os
import serial
import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPalette, QFont
from PyQt5.QtSerialPort import QSerialPortInfo
from serialSetting import Ui_SerialDialog


Blue  = QColor(128,128,128)
Red   = QColor(255,0,0)
Green = QColor(0,199,140)


class PortDialog(QtWidgets.QDialog, Ui_SerialDialog):
    def __init__(self, parent=None):
        super(PortDialog, self).__init__(parent)
        self.initUI()


    def initUI(self):
        self.setupUi(self)
        self.setWindowFlags(Qt.WindowCloseButtonHint)  # 只显示关闭按钮
        self.setupPortBoxs()
        self.refreshPort()
        self.serialPort = serial.Serial()  # 创建串口
        self.OpenPortButton.clicked.connect(self.openPort)  # 绑定打开串口方法
        self.RefreshPortButton.clicked.connect(self.refreshPort)  # 绑定刷新串口方法
        self.PortBox.activated.connect(self.showPortInfo)  # 展示不同串口信息
        self.setButtonStyle()



    def refreshPort(self):
        # self.PortBox.clear()
        portList = QSerialPortInfo.availablePorts()
        ports = []
        for port in portList:
            port.portName()  # 返回串口号，如COM1
            port.description()  # 返回设备硬件描述 如USB-SERIAL CH340
            ports.append(port.portName() + ' ' + port.description())
        self.PortBox.addItems(ports)
        if len(portList) <= 0:
            self.displayText("NO AVAILABLE PORTS",Red)
            # 无串口时，打开port,一键读取，一键清除按钮不可点击
            self.OpenPortButton.setEnabled(False)
        else:
            self.displayText(self.PortBox.currentText(), Blue)
            self.OpenPortButton.setEnabled(True)



    def openPort(self):
        portName = self.PortBox.currentText().split(' ')[0]
        self.serialPort.port     = portName
        self.serialPort.baudrate = int(self.BaudarteBox.currentText())
        self.serialPort.bytesize = int(self.DataBitsBox.currentText())
        self.serialPort.parity   = str(self.ParityBox.currentText())[0:1]
        self.serialPort.stopbits = int(self.StopBitsBox.currentText())

        if self.OpenPortButton.text() =='Open Port':
            try:
                self.serialPort.open()
                self.displayText("{0} OPENED".format(portName),Green)
                self.OpenPortButton.setText('Close Port')
                self.setComboBoxStatus(False)
            except Exception as error:
                self.displayText("{}".format(str(error)),Red)
        else: #是关闭串口时，直接关闭
            self.serialPort.close()
            self.OpenPortButton.setText('Open Port')
            self.displayText("{} CLOSED".format(portName),Red)
            self.setComboBoxStatus(True)

        self.setButtonStyle()

        self.isRefreshable()


    def displayText(self,str,color:QColor):
        self.TipLabel.setText(str)
        pe = QPalette()
        pe.setColor(QPalette.WindowText,color)
        self.TipLabel.setPalette(pe) # 设置文字颜色
        font = QFont()
        font.setPointSize(10)
        self.TipLabel.setFont(font)

    def setupPortBoxs(self):
        self.BaudarteBox.addItems(['9600','19200','38400','57600','115200'])
        self.DataBitsBox.addItems(['5','6','7','8'])
        self.ParityBox.addItems(['None','Even','Odd','Mark','Space'])
        self.StopBitsBox.addItems(['1','1.5','2'])
        self.FlowTypeBox.addItems(['None','RTS/CTS','XON/XOFF'])
        self.BaudarteBox.setCurrentText('115200') #默认选择 115200
        self.DataBitsBox.setCurrentText('8') #默认选择 8

    def showPortInfo(self):
        self.displayText(self.PortBox.currentText(),Blue)

    def setComboBoxStatus(self, bool):
        self.PortBox.setEnabled(bool)
        self.BaudarteBox.setEnabled(bool)
        self.ParityBox.setEnabled(bool)
        self.FlowTypeBox.setEnabled(bool)
        self.DataBitsBox.setEnabled(bool)
        self.StopBitsBox.setEnabled(bool)

    def isRefreshable(self):
        if self.serialPort.isOpen():
            self.RefreshPortButton.setEnabled(False)
        else:
            self.RefreshPortButton.setEnabled(True)

    def setButtonStyle(self):
        if self.serialPort.isOpen():
            self.OpenPortButton.setStyleSheet("QPushButton{color:white}"
                                              "QPushButton:hover{color:yellow}"
                                              "QPushButton{background-color:red}"
                                              "QPushButton{border:1px}"
                                              "QPushButton{border-radius:2.5px}"
                                              "QPushButton{padding:2px 4px}")
        else:
            self.OpenPortButton.setStyleSheet("QPushButton{color:white}"
                                              "QPushButton:hover{color:red}"
                                              "QPushButton{background-color:green}"
                                              "QPushButton{border:1px}"
                                              "QPushButton{border-radius:2.5px}"
                                              "QPushButton{padding:2px 4px}")

        self.RefreshPortButton.setStyleSheet("QPushButton{color:white}"
                                             "QPushButton:hover{color:red}"
                                             "QPushButton{background-color:green}"
                                             "QPushButton{border:1px}"
                                             "QPushButton{border-radius:2.5px}"
                                             "QPushButton{padding:2px 4px}")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    port = PortDialog()
    port.show()
    sys.exit(app.exec_())



