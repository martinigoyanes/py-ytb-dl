from PyQt5 import QtWidgets, QtGui, QtCore
# from PyQt5.QtWidgets import QApplication, QMainWindow
import myapp
import sys
from PyQt5.QtWidgets import QInputDialog

#TODO: Log messages to the white boxes
#TODO: Render the downloading bar

class Ui_GUI(object):
    def setupUi(self, GUI):
        GUI.setObjectName("GUI")
        GUI.resize(818, 434)
        font = QtGui.QFont()
        font.setPointSize(16)
        GUI.setFont(font)

        self.DLBar = QtWidgets.QProgressBar(GUI)
        self.DLBar.setGeometry(QtCore.QRect(20, 332, 201, 51))
        self.DLBar.setAutoFillBackground(True)
        self.DLBar.setProperty("value", 0)
        self.DLBar.setObjectName("DLBar")

        self.DLButton = QtWidgets.QPushButton(GUI)
        self.DLButton.setGeometry(QtCore.QRect(40, 370, 171, 32))
        self.DLButton.setObjectName("DLButton")
        self.DLButton.clicked.connect(self.start_download)

        self.SpotifyLoginButton = QtWidgets.QPushButton(GUI)
        self.SpotifyLoginButton.setGeometry(QtCore.QRect(671, 290, 141, 32))
        self.SpotifyLoginButton.setObjectName("SpotifyLoginButton")
        self.SpotifyLoginButton.clicked.connect(myapp.connect_spotify)

        self.SpotifyLogo = QtWidgets.QLabel(GUI)
        self.SpotifyLogo.setGeometry(QtCore.QRect(720, 330, 81, 81))
        self.SpotifyLogo.setText("")
        self.SpotifyLogo.setPixmap(QtGui.QPixmap("spotify-logo.jpg"))
        self.SpotifyLogo.setScaledContents(True)
        self.SpotifyLogo.setObjectName("SpotifyLogo")

        self.OutputFolderValueButton = QtWidgets.QPushButton(GUI)
        self.OutputFolderValueButton.setGeometry(QtCore.QRect(410, 390, 200, 30))
        self.OutputFolderValueButton.setObjectName("OutputFolderValueButton")
        self.OutputFolderValueButton.setText(myapp.config.OUT_FOLDER)
        self.OutputFolderValueButton.clicked.connect(self.change_output_folder)

        self.OutputFolderLabel = QtWidgets.QLabel(GUI)
        self.OutputFolderLabel.setGeometry(QtCore.QRect(400, 365, 130, 31))
        self.OutputFolderLabel.setObjectName("OutputFolderLabel")
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.OutputFolderLabel.setFont(font)

        self.OptionsButton = QtWidgets.QPushButton(GUI)
        self.OptionsButton.setGeometry(QtCore.QRect(700, 260, 112, 32))
        self.OptionsButton.setObjectName("OptionsButton")

        self.ProgessLabelTitle = QtWidgets.QLabel(GUI)
        self.ProgessLabelTitle.setGeometry(QtCore.QRect(90, 10, 81, 21))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.ProgessLabelTitle.setFont(font)
        self.ProgessLabelTitle.setStyleSheet("color: rgb(0, 0, 0);")
        self.ProgessLabelTitle.setObjectName("ProgessLabelTitle")

        self.WarningLabelTitle = QtWidgets.QLabel(GUI)
        self.WarningLabelTitle.setGeometry(QtCore.QRect(390, 10, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.WarningLabelTitle.setFont(font)
        self.WarningLabelTitle.setStyleSheet("color: rgb(238, 255, 0);")
        self.WarningLabelTitle.setScaledContents(True)
        self.WarningLabelTitle.setObjectName("WarningLabelTitle")

        self.ErrorsLabelTitle = QtWidgets.QLabel(GUI)
        self.ErrorsLabelTitle.setGeometry(QtCore.QRect(680, 10, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.ErrorsLabelTitle.setFont(font)
        self.ErrorsLabelTitle.setStyleSheet("color: rgb(232, 0, 0);")
        self.ErrorsLabelTitle.setObjectName("ErrorsLabelTitle")

        self.ProgressLabelContent = QtWidgets.QLabel(GUI)
        self.ProgressLabelContent.setGeometry(QtCore.QRect(20, 35, 271, 291))
        self.ProgressLabelContent.setStyleSheet(
            "color: rgb(0, 0, 0);\n" "background-color: rgb(255, 255, 255);")
        self.ProgressLabelContent.setFrameShape(QtWidgets.QFrame.Box)
        self.ProgressLabelContent.setFrameShadow(QtWidgets.QFrame.Plain)
        self.ProgressLabelContent.setLineWidth(4)
        self.ProgressLabelContent.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.ProgressLabelContent.setObjectName("ProgressLabelContent")

        self.WarningsLabelContent = QtWidgets.QLabel(GUI)
        self.WarningsLabelContent.setGeometry(QtCore.QRect(320, 40, 251, 321))
        self.WarningsLabelContent.setStyleSheet(
            "color: rgb(0, 0, 0);\n" "background-color: rgb(255, 255, 255);")
        self.WarningsLabelContent.setFrameShape(QtWidgets.QFrame.Box)
        self.WarningsLabelContent.setLineWidth(4)
        self.WarningsLabelContent.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.WarningsLabelContent.setObjectName("WarningsLabelContent")

        self.ErrorsLabelContent = QtWidgets.QLabel(GUI)
        self.ErrorsLabelContent.setGeometry(QtCore.QRect(600, 45, 211, 211))
        self.ErrorsLabelContent.setStyleSheet(
            "color: rgb(0, 0, 0);\n" "background-color: rgb(255, 255, 255);")
        self.ErrorsLabelContent.setFrameShape(QtWidgets.QFrame.Box)
        self.ErrorsLabelContent.setLineWidth(4)
        self.ErrorsLabelContent.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.ErrorsLabelContent.setObjectName("ErrorsLabelContent")

        self.retranslateUi(GUI)
        QtCore.QMetaObject.connectSlotsByName(GUI)

    def retranslateUi(self, GUI):
        _translate = QtCore.QCoreApplication.translate
        GUI.setWindowTitle(_translate("GUI", "Spotify Downloader"))
        self.DLButton.setText(_translate("GUI", "Start Downloading"))
        self.SpotifyLoginButton.setText(_translate("GUI", "Spotify Login"))
        self.OutputFolderLabel.setText(_translate("GUI", "Output Folder:"))
        self.OptionsButton.setText(_translate("GUI", "Options"))
        self.ProgessLabelTitle.setText(_translate("GUI", "Progress"))
        self.WarningLabelTitle.setText(_translate("GUI", "Warnings"))
        self.ErrorsLabelTitle.setText(_translate("GUI", "Errors"))

    def start_download(self):
        input = QInputDialog.getText(self.DLButton ,"Spotify Downloader", "What is the last song (inclusive) from your library to download?")
        if input[1]:
            import threading
            threading.Thread(target=myapp.start_download, args=(input[0],)).start()

    def change_output_folder(self):
        input = QInputDialog.getText(self.OutputFolderValueButton ,"Spotify Downloader", "New output folder:")
        if input[1]:
            self.OutputFolderValueButton.setText(input[0])
            self.OutputFolderValueButton.adjustSize()
            myapp.config.OUT_FOLDER = input[0]

if __name__ == "__main__":
    import sys
    import myapp
    myapp.setup()
    app = QtWidgets.QApplication(sys.argv)
    GUI = QtWidgets.QDialog()
    ui = Ui_GUI()
    ui.setupUi(GUI)
    GUI.show()
    sys.exit(app.exec_())
