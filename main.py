
from PyQt5 import QtWidgets
import sys
from PyQt5.QtCore import Qt, QEvent

from model import Model
from PyQt5.QtWidgets import QFileDialog, QMenuBar, QWidget, QMainWindow
from update import  Ui_MainWindow
from serialPort import PortDialog
import serial
import  time
from command import Command

filePath = 'FilePath'

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.setupUi(self)
        # 设置背景黑色，文字白色
        self.UpdateLogText.setStyleSheet("QTextBrowser{background-color:black}"
                                         "QTextBrowser{color:white}"
                                        )
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)  # 只留下关闭按钮
        self.model = Model()  #实例化model
        self.command = Command()
        self.model.fileName = self.filePathEdit.text()
        self.isClickable()
        self.comPort = serial.Serial()  #创建串口
        # self.filePathEdit.setText(self.model.getFileName(filePath))
        self.actionSetting.triggered.connect(self.showPortSetting)
        self.BrowseButton.clicked.connect(self.selectFile)
        self.UpdateButton.clicked.connect(self.updateFile)
        # 设置css样式
        self.BrowseButton.setStyleSheet("QPushButton{color:white}"
                                  "QPushButton:hover{color:red}"
                                  "QPushButton{background-color:green}"
                                  "QPushButton{border:1px}"
                                  "QPushButton{border-radius:2.5px}"
                                  "QPushButton{padding:2px 4px}")
        self.UpdateButton.setStyleSheet("QPushButton{color:white}"
                                        "QPushButton:hover{color:red}"
                                        "QPushButton{background-color:green}"
                                        "QPushButton{border:1px}"
                                        "QPushButton{border-radius:2.5px}"
                                        "QPushButton{padding:2px 4px}")

        self.myMenuBar.setStyleSheet("QMenuBar{color:white}"
                                     "QMenuBar{background-color:black}"
                                     "QMenuBar:hover{color:red}"

                                     ) #"QMenuBar{background:transparent}"

        self.processLabel.setStyleSheet("QLabel{color:green}")
        self.tipsLabel.setStyleSheet("QLabel{color:red}")

        # self.titleLabel.setStyleSheet("QLabel{color:blue}")

        # self.filePathEdit.setStyleSheet( "QLineEdit{border-radius:2px}"
        #                                  "QLineEdit{border:4px}")
        self.actionSetting.setShortcut('Ctrl+Q') # 设置快捷键
        # self.myMenuBar.installEventFilter(self)


    def selectFile(self):
        fileName, _ = QFileDialog.getOpenFileName(None,"Select a file ","","Bin Files (*.bin)",
                                                 options = QFileDialog.DontUseNativeDialog)
        if fileName:
            self.filePathEdit.setText(fileName)
            self.model.fileName = fileName
            self.isClickable()

            self.debugPrint(fileName)
            self.model.getDataBytes()
            self.debugPrint("{} bytes file size and {} bytes array".format(self.model.fileSize,len(self.model.chunks)))
            # self.sendPackets()
            # self.model.getPackages()
            # CRCs = self.model.generateCRCs()
            # for CRC in CRCs:
            #     self.debugPrint('The CRC for the data package {0} is {1}'.format(CRCs.index(CRC) +1,str(CRC)))
            #     self.debugPrint('The CRC for the data package {0} is {1}'.format(CRCs.index(CRC) + 1, str(CRC)))

    def updateFile(self):
        self.sendPackets()


    def sendPackets(self):
        for block in self.model.getPackages():
            for index,dataByte in enumerate(block):
                dataBytes = self.command.sendDataPacket(index,dataByte)
                self.debugPrint('Sending Packet {0}:\n{1}'.format(index,dataBytes))



    def debugPrint(self, msg):

        self.UpdateLogText.append('[{0}] {1}'.format(self.getTimeStamp(), msg))


    def isClickable(self):
        if self.model.isFileAviable():
            self.UpdateButton.setEnabled(True)
            self.filePathEdit.setEnabled(True)
        else:
            self.UpdateButton.setEnabled(False)
            self.filePathEdit.setEnabled(False)

    # def eventFilter(self, object, event):
    #     if event.type() == QEvent.MouseMove:
    #         if object == self.myMenuBar:
    #             print("over the menu bar")
    #     elif event.type() == QEvent.Leave:
    #         if object == self.myMenuBar:
    #             print("leave the menu bar………")
    #
    #     return QMainWindow.eventFilter(self, object, event)



    def showPortSetting(self):
        dialog = PortDialog()
        dialog.serialPort = self.comPort
        dialog.exec()

    def getTimeStamp(self):
        currentTime = time.time()
        localTime = time.localtime(currentTime)
        timeHead = time.strftime("%H:%M:%S", localTime)
        timeSecs = (currentTime - int(currentTime)) * 1000
        timeStamp = "%s.%03d" % (timeHead, timeSecs)
        return timeStamp




if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())

