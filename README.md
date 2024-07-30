# LAUNCHER CREATOR

A python tool to create and edit launchers in linux easly, with a GUI made in PyQt5 using Qt Designer.

### NOTES FOR DELEVOPERS

this UI was made in PyQt5

the tree action buttons are QPushButton instances.

when a push button is clicked, it call a method

    openButton --> OpenFile()

    exportButton --> ExportFile()

    saveButton --> SaveFile()

.desktop file is read line by line, and if this method finds a value (with =)
