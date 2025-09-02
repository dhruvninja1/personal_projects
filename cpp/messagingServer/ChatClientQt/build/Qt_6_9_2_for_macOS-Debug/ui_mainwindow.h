/********************************************************************************
** Form generated from reading UI file 'mainwindow.ui'
**
** Created by: Qt User Interface Compiler version 6.9.2
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_MAINWINDOW_H
#define UI_MAINWINDOW_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QGroupBox>
#include <QtWidgets/QHBoxLayout>
#include <QtWidgets/QLabel>
#include <QtWidgets/QLineEdit>
#include <QtWidgets/QListWidget>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QTextEdit>
#include <QtWidgets/QVBoxLayout>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_MainWindow
{
public:
    QWidget *centralwidget;
    QListWidget *roomsList;
    QPushButton *refreshButton;
    QWidget *widget;
    QVBoxLayout *verticalLayout;
    QGroupBox *groupBox;
    QHBoxLayout *horizontalLayout;
    QLabel *labelHost;
    QLineEdit *hostEdit;
    QLabel *labelPort;
    QLineEdit *portEdit;
    QLabel *labelUsername;
    QLineEdit *usernameEdit;
    QLabel *labelPassword;
    QLineEdit *passwordEdit;
    QPushButton *connectButton;
    QLabel *statusLabel;
    QTextEdit *chatText;
    QHBoxLayout *horizontalLayout_2;
    QLineEdit *inputEdit;
    QPushButton *sendButton;

    void setupUi(QMainWindow *MainWindow)
    {
        if (MainWindow->objectName().isEmpty())
            MainWindow->setObjectName("MainWindow");
        MainWindow->resize(1062, 346);
        centralwidget = new QWidget(MainWindow);
        centralwidget->setObjectName("centralwidget");
        roomsList = new QListWidget(centralwidget);
        roomsList->setObjectName("roomsList");
        roomsList->setGeometry(QRect(0, 0, 181, 351));
        refreshButton = new QPushButton(centralwidget);
        refreshButton->setObjectName("refreshButton");
        refreshButton->setGeometry(QRect(40, 310, 100, 32));
        widget = new QWidget(centralwidget);
        widget->setObjectName("widget");
        widget->setGeometry(QRect(190, 0, 871, 345));
        verticalLayout = new QVBoxLayout(widget);
        verticalLayout->setObjectName("verticalLayout");
        verticalLayout->setContentsMargins(0, 0, 0, 0);
        groupBox = new QGroupBox(widget);
        groupBox->setObjectName("groupBox");
        horizontalLayout = new QHBoxLayout(groupBox);
        horizontalLayout->setObjectName("horizontalLayout");
        labelHost = new QLabel(groupBox);
        labelHost->setObjectName("labelHost");

        horizontalLayout->addWidget(labelHost);

        hostEdit = new QLineEdit(groupBox);
        hostEdit->setObjectName("hostEdit");

        horizontalLayout->addWidget(hostEdit);

        labelPort = new QLabel(groupBox);
        labelPort->setObjectName("labelPort");

        horizontalLayout->addWidget(labelPort);

        portEdit = new QLineEdit(groupBox);
        portEdit->setObjectName("portEdit");

        horizontalLayout->addWidget(portEdit);

        labelUsername = new QLabel(groupBox);
        labelUsername->setObjectName("labelUsername");

        horizontalLayout->addWidget(labelUsername);

        usernameEdit = new QLineEdit(groupBox);
        usernameEdit->setObjectName("usernameEdit");

        horizontalLayout->addWidget(usernameEdit);

        labelPassword = new QLabel(groupBox);
        labelPassword->setObjectName("labelPassword");

        horizontalLayout->addWidget(labelPassword);

        passwordEdit = new QLineEdit(groupBox);
        passwordEdit->setObjectName("passwordEdit");
        passwordEdit->setEchoMode(QLineEdit::EchoMode::Password);

        horizontalLayout->addWidget(passwordEdit);

        connectButton = new QPushButton(groupBox);
        connectButton->setObjectName("connectButton");

        horizontalLayout->addWidget(connectButton);


        verticalLayout->addWidget(groupBox);

        statusLabel = new QLabel(widget);
        statusLabel->setObjectName("statusLabel");

        verticalLayout->addWidget(statusLabel);

        chatText = new QTextEdit(widget);
        chatText->setObjectName("chatText");
        chatText->setReadOnly(true);

        verticalLayout->addWidget(chatText);

        horizontalLayout_2 = new QHBoxLayout();
        horizontalLayout_2->setObjectName("horizontalLayout_2");
        inputEdit = new QLineEdit(widget);
        inputEdit->setObjectName("inputEdit");

        horizontalLayout_2->addWidget(inputEdit);

        sendButton = new QPushButton(widget);
        sendButton->setObjectName("sendButton");

        horizontalLayout_2->addWidget(sendButton);


        verticalLayout->addLayout(horizontalLayout_2);

        MainWindow->setCentralWidget(centralwidget);

        retranslateUi(MainWindow);

        QMetaObject::connectSlotsByName(MainWindow);
    } // setupUi

    void retranslateUi(QMainWindow *MainWindow)
    {
        MainWindow->setWindowTitle(QCoreApplication::translate("MainWindow", "Chat Client", nullptr));
        refreshButton->setText(QCoreApplication::translate("MainWindow", "Refresh", nullptr));
        groupBox->setTitle(QCoreApplication::translate("MainWindow", "Connect", nullptr));
        labelHost->setText(QCoreApplication::translate("MainWindow", "Host:", nullptr));
        hostEdit->setText(QCoreApplication::translate("MainWindow", "localhost", nullptr));
        labelPort->setText(QCoreApplication::translate("MainWindow", "Port:", nullptr));
        portEdit->setText(QCoreApplication::translate("MainWindow", "8080", nullptr));
        labelUsername->setText(QCoreApplication::translate("MainWindow", "Username:", nullptr));
        labelPassword->setText(QCoreApplication::translate("MainWindow", "Password:", nullptr));
        connectButton->setText(QCoreApplication::translate("MainWindow", "Connect", nullptr));
        statusLabel->setText(QCoreApplication::translate("MainWindow", "Not connected.", nullptr));
        inputEdit->setPlaceholderText(QCoreApplication::translate("MainWindow", "Type your message here...", nullptr));
        sendButton->setText(QCoreApplication::translate("MainWindow", "Send", nullptr));
    } // retranslateUi

};

namespace Ui {
    class MainWindow: public Ui_MainWindow {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_MAINWINDOW_H
