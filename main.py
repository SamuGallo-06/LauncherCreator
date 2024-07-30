import os

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QPushButton, QComboBox, QLineEdit, QCheckBox, QStatusBar
)

from PyQt5.uic import loadUi

APP_TITLE = "Launcher Creator"

class LauncherCreator(QMainWindow):

    MAIN_HEADER = "#!/usr/bin/env xdg-open\n"
    DESKTOP_HEADER = "[Desktop Entry]\n"
    VERSION_HEADER = "Version="
    TYPE_HEADER = "Type="
    TERMINAL_HEADER = "Terminal="
    EXEC_HEADER = "Exec="
    NAME_HEADER = "Name="
    ICON_HEADER = "Icon="
    COMMENT_HEADER = "Comment="

    isFileLoaded = False

    def __init__(self):
        self.isFileLoaded = False
        super().__init__()
        # Load the UI file
        loadUi("/usr/share/launcherCreator/launcherCreator.ui", self)
        # Show the window
        self.setWindowTitle(APP_TITLE)
        self.setup()
        self.statusbar.showMessage("Pronto")
        self.show()

    def setup(self):
        self.setFixedSize(self.width(), self.height())
        self.saveButton = self.findChild(QPushButton, "saveButton")
        self.openButton = self.findChild(QPushButton, "openButton")
        self.exportButton = self.findChild(QPushButton, "exportButton")
        self.nameEntry = self.findChild(QLineEdit, "nameEntry")
        self.commandEntry = self.findChild(QLineEdit, "commandEntry")
        self.versionEntry = self.findChild(QLineEdit, "versionEntry")
        self.commentEntry = self.findChild(QLineEdit, "commentEntry")
        self.iconEntry = self.findChild(QLineEdit, "iconEntry")
        self.terminalCheckBox = self.findChild(QCheckBox, "terminalCheckBox")
        self.applicationTypeEntry = self.findChild(QComboBox, "applicationTypeEntry")
        self.statusbar = self.findChild(QStatusBar, "statusbar")
        self.HandleButtons()

    def HandleButtons(self):
        self.saveButton.clicked.connect(self.SaveFile)
        self.openButton.clicked.connect(self.OpenFile)
        self.exportButton.clicked.connect(self.ExportFile)

    def OpenFile(self):
        self.filePath = QFileDialog.getOpenFileName(filter="Desktop Entries (*.desktop)")
        self.file = open(self.filePath[0])
        self.isFileLoaded = True

        # Crea un dizionario per memorizzare i valori
        desktopValues = {}

        # Ignora le righe vuote o quelle che iniziano con "#"
        for line in self.file.readlines():
            line = line.strip()
            if line and not line.startswith("#") and line.find("=") != -1:
                key = line.split("=")[0]
                value = line.split("=")[1]
                desktopValues[key] = value.strip()

        #name
        if("Name" in desktopValues):
            self.nameEntry.setText(desktopValues["Name"])
        else:
            self.nameEntry.clear()
        
        #command
        if("Exec" in desktopValues):
            self.commandEntry.setText(desktopValues["Exec"])
        else:
            self.nameEntry.clear()
        
        #version
        if("Version" in desktopValues):
            self.versionEntry.setText(desktopValues["Version"])
        else:
            self.nameEntry.clear()
        
        #icon
        if("Icon" in desktopValues):
            self.iconEntry.setText(desktopValues["Icon"])
        else:
            self.nameEntry.clear()
        
        #comment
        if("Comment" in desktopValues):
            self.commentEntry.setText(desktopValues["Comment"])
        else:
            self.nameEntry.clear()

        #type
        if("Type" in desktopValues):
            if(desktopValues["Type"] == "Applicazion"):
                self.applicationTypeEntry.setCurrentIndex(0)
            elif(desktopValues["Type"] == "Link"):
                self.applicationTypeEntry.setCurrentIndex(1)
            elif(desktopValues["Type"] == "Directory"):
                self.applicationTypeEntry.setCurrentIndex(2)

        #terminal
        if("Terminal" in desktopValues):
            if(desktopValues["Terminal"] == "True"):
                self.terminalCheckBox.setChecked(True)
            else:
                self.terminalCheckBox.setChecked(False)

        self.statusbar.showMessage("File caricato")

    def SaveFile(self):
        if(not self.isFileLoaded):
            self.ExportFile()
        else:
            self.WriteFile()

    def WriteFile(self):
        self.file.truncate(0)
        self.file.write(self.MAIN_HEADER)
        self.file.write(self.DESKTOP_HEADER)
        self.file.write(self.VERSION_HEADER + self.versionEntry.text() + "\n")
        self.file.write(self.NAME_HEADER + self.nameEntry.text() + "\n")
        self.file.write(self.COMMENT_HEADER + self.commentEntry.text() + "\n")

        if(self.applicationTypeEntry.currentText() == "Applicazione"):
            self.file.write(self.TYPE_HEADER + "Application" + "\n")
        elif(self.applicationTypeEntry.currentText() == "Link"):
            self.file.write(self.TYPE_HEADER + "Link" + "\n")
        elif(self.applicationTypeEntry.currentText() == "Directory"):
            self.file.write(self.TYPE_HEADER + "Directory" + "\n")

        self.file.write(self.EXEC_HEADER + self.commandEntry.text() + "\n")
        self.file.write(self.ICON_HEADER + self.iconEntry.text() + "\n")
        self.file.write(self.TERMINAL_HEADER + str(self.terminalCheckBox.isChecked()))

        self.statusbar.showMessage("File salvato")

    def ExportFile(self):
        self.filePath = QFileDialog.getSaveFileName(filter="Desktop Entries (*.desktop)")
        if(not(os.path.exists(self.filePath[0]))):
            open(self.filePath[0], "x").close()
        self.file = open(self.filePath[0], "a")
        self.isFileLoaded = True
        self.WriteFile()

if __name__ == "__main__":
    app = QApplication([])
    # Create the main window
    window = LauncherCreator()
    # Run the application
    app.exec()
