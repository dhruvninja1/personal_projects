QT       += widgets
QT       += network

SOURCES  += main.cpp \
            mainwindow.cpp

ICON = app_icons.icns
macx {
    QMAKE_INFO_PLIST = Info.plist
}

DEFINES += QT_DEPRECATED_WARNINGS


#DEFINES += QT_DISABLE_DEPRECATED_BEFORE=0x060000

HEADERS  += mainwindow.h

FORMS    += mainwindow.ui
CONFIG += release

# Uncomment if you add resources later
# RESOURCES += resources.qrc

# Optional: set C++ standard
CONFIG += c++17

# For Windows: enable console output (optional)
# CONFIG += console
