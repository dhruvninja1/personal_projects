#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QTcpSocket>
#include <QTextCursor>
#include <QColor>
#include <QListWidget>

QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private slots:
    void on_connectButton_clicked();
    void on_sendButton_clicked();
    void onSocketReadyRead();
    void onSocketConnected();
    void onSocketDisconnected();
    void on_inputEdit_returnPressed();
    void on_roomsList_itemClicked(QListWidgetItem* item);
    void on_refreshButton_clicked();

private:
    Ui::MainWindow *ui;
    QTcpSocket *socket;
    QString currentRoom;
    QString messageBuffer;
    bool isAdmin = false;
    bool joiningRoom = false; // Flag to prevent duplicate join commands

    void appendMessage(const QString &html);
    void displayFormattedMessage(const QString& message, bool isHistory);
    QString processMentionsForDisplay(const QString& message);
    void processMessage(const QString& msg);
    QString ansiToHtml(const QString &input);
};

#endif // MAINWINDOW_H
