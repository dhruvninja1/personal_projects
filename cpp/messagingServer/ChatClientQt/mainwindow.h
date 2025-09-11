#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QTcpSocket>
#include <QTextCursor>
#include <QColor>
#include <QListWidget>
#include <QFileDialog>
#include <QImageReader>
#include <QBuffer>
#include <QMimeData>
#include <QDragEnterEvent>
#include <QDropEvent>
#include <QLabel>
#include <QScrollArea>
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QPushButton>
#include <QProgressBar>
#include <QTimer>

QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

struct PendingImage {
    QString filename;
    QByteArray data;
    QString mimeType;
    qint64 totalSize;
    qint64 receivedSize;
    QString sender;
    QString messageId;
    QProgressBar* progressBar;
};

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

protected:
    void dragEnterEvent(QDragEnterEvent *event) override;
    void dropEvent(QDropEvent *event) override;

private slots:
    void on_connectButton_clicked();
    void on_sendButton_clicked();
    void onSocketReadyRead();
    void onSocketConnected();
    void onSocketDisconnected();
    void on_inputEdit_returnPressed();
    void on_roomsList_itemClicked(QListWidgetItem* item);
    void on_refreshButton_clicked();
    void on_imageButton_clicked();
    void onImageTransferProgress();

private:
    Ui::MainWindow *ui;
    QTcpSocket *socket;
    QString currentRoom;
    QString messageBuffer;
    bool isAdmin = false;
    bool joiningRoom = false;
    
    // Image handling
    QPushButton *imageButton;
    QMap<QString, PendingImage> pendingImages;
    QTimer *progressTimer;
    
    // Methods
    void appendMessage(const QString &html);
    void displayFormattedMessage(const QString& message, bool isHistory);
    QString processMentionsForDisplay(const QString& message);
    void processMessage(const QString& msg);
    QString ansiToHtml(const QString &input);
    
    // Image methods
    void sendImage(const QString &filePath);
    void handleImageData(const QString &message);
    void displayImage(const QString &sender, const QByteArray &imageData, const QString &filename);
    QString generateMessageId();
    bool isImageFile(const QString &filePath);
    QByteArray compressImage(const QByteArray &imageData, const QString &format = "JPEG", int quality = 85);
};

#endif // MAINWINDOW_H