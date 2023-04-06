import os

currentDirectory = os.getcwd()

logFolderName = 'logs'
logFilePath = os.path.join(currentDirectory, logFolderName)

didbFolderName = 'didb'
didbFilePath = os.path.join(currentDirectory, didbFolderName)

_didbName_ = 'didb'

def set_didbName(didbName):
    global _didbName_
    print("Setting didb name as " + str(didbName))
    _didbName_ = didbName
