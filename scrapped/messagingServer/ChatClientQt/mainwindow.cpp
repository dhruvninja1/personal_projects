#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QMessageBox>
#include <QTextCursor>
#include <QFont>
#include <QBrush>
#include <QRegularExpression>
#include <QMap>
#include <QListWidgetItem>
#include <QByteArray>
#include <QFileDialog>
#include <QImageReader>
#include <QBuffer>
#include <QMimeData>
#include <QUrl>
#include <QPixmap>
#include <QLabel>
#include <QScrollArea>
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QProgressBar>
#include <QTimer>
#include <QCryptographicHash>
#include <QStandardPaths>
#include <QDir>
#include <QDateTime>

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
    , socket(new QTcpSocket(this))
    , progressTimer(new QTimer(this))
{
    ui->setupUi(this);
    
    connect(socket, &QTcpSocket::readyRead, this, &MainWindow::onSocketReadyRead);
    connect(socket, &QTcpSocket::connected, this, &MainWindow::onSocketConnected);
    connect(socket, &QTcpSocket::disconnected, this, &MainWindow::onSocketDisconnected);

    connect(ui->inputEdit, &QLineEdit::returnPressed, this, &MainWindow::on_sendButton_clicked);
    connect(ui->roomsList, &QListWidget::itemClicked, this, &MainWindow::on_roomsList_itemClicked);
    connect(ui->refreshButton, &QPushButton::clicked, this, &MainWindow::on_refreshButton_clicked);
    connect(ui->imageButton, &QPushButton::clicked, this, &MainWindow::on_imageButton_clicked);
    
    connect(progressTimer, &QTimer::timeout, this, &MainWindow::onImageTransferProgress);

    ui->chatText->setReadOnly(true);
    ui->statusLabel->setText("Not connected. Drag & drop images supported!");
    
    // Enable drag and drop
    setAcceptDrops(true);
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::on_imageButton_clicked()
{
    if (!socket->isValid() || currentRoom.isEmpty()) {
        appendMessage("<span style='color:red;'>You must be connected and in a room to send images.</span>");
        return;
    }

    QString fileName = QFileDialog::getOpenFileName(this,
        tr("Select Image"), "",
        tr("Image Files (*.png *.jpg *.jpeg *.gif *.bmp *.svg)"));
    
    if (!fileName.isEmpty()) {
        sendImage(fileName);
    }
}

void MainWindow::dragEnterEvent(QDragEnterEvent *event)
{
    if (event->mimeData()->hasUrls()) {
        bool hasImages = false;
        foreach (const QUrl &url, event->mimeData()->urls()) {
            if (url.isLocalFile() && isImageFile(url.toLocalFile())) {
                hasImages = true;
                break;
            }
        }
        if (hasImages) {
            event->acceptProposedAction();
        }
    }
}

void MainWindow::dropEvent(QDropEvent *event)
{
    if (!socket->isValid() || currentRoom.isEmpty()) {
        appendMessage("<span style='color:red;'>You must be connected and in a room to send images.</span>");
        return;
    }

    foreach (const QUrl &url, event->mimeData()->urls()) {
        if (url.isLocalFile()) {
            QString filePath = url.toLocalFile();
            if (isImageFile(filePath)) {
                sendImage(filePath);
            }
        }
    }
    event->acceptProposedAction();
}

bool MainWindow::isImageFile(const QString &filePath)
{
    QStringList supportedFormats;
    supportedFormats << "png" << "jpg" << "jpeg" << "gif" << "bmp" << "svg";
    
    QFileInfo fileInfo(filePath);
    QString suffix = fileInfo.suffix().toLower();
    return supportedFormats.contains(suffix);
}

QString MainWindow::generateMessageId()
{
    // Use QDateTime and qrand for Qt 5.15 compatibility
    static bool seeded = false;
    if (!seeded) {
        qsrand(QDateTime::currentMSecsSinceEpoch());
        seeded = true;
    }
    return QString::number(QDateTime::currentMSecsSinceEpoch()) + "_" + 
           QString::number(qrand() % 10000);
}

QByteArray MainWindow::compressImage(const QByteArray &imageData, const QString &format, int quality)
{
    QPixmap pixmap;
    pixmap.loadFromData(imageData);
    
    // Resize if too large (max 800x600)
    if (pixmap.width() > 800 || pixmap.height() > 600) {
        pixmap = pixmap.scaled(800, 600, Qt::KeepAspectRatio, Qt::SmoothTransformation);
    }
    
    QByteArray compressedData;
    QBuffer buffer(&compressedData);
    buffer.open(QIODevice::WriteOnly);
    pixmap.save(&buffer, format.toUtf8().constData(), quality);
    
    return compressedData;
}

void MainWindow::sendImage(const QString &filePath)
{
    QFile file(filePath);
    if (!file.open(QIODevice::ReadOnly)) {
        appendMessage("<span style='color:red;'>Failed to open image file.</span>");
        return;
    }

    QByteArray imageData = file.readAll();
    file.close();
    
    // Compress image if it's too large (>500KB)
    if (imageData.size() > 500000) {
        QFileInfo fileInfo(filePath);
        QString format = fileInfo.suffix().toUpper();
        if (format == "JPG") format = "JPEG";
        
        imageData = compressImage(imageData, format, 75);
        appendMessage("<span style='color:orange;'>Image compressed for transmission.</span>");
    }

    QFileInfo fileInfo(filePath);
    QString filename = fileInfo.fileName();
    QString messageId = generateMessageId();
    
    // Create image message protocol:
    // IMAGE_START|messageId|filename|dataSize|base64Data|IMAGE_END
    QString base64Data = imageData.toBase64();
    QString imageMessage = QString("IMAGE_START|%1|%2|%3|%4|IMAGE_END")
                          .arg(messageId)
                          .arg(filename)
                          .arg(imageData.size())
                          .arg(base64Data);

    socket->write((ui->usernameEdit->text() + " - " + imageMessage).toUtf8());
    
    // Show preview locally
    appendMessage(QString("<span style='color:green;'>Sending image: %1 (%2 KB)</span>")
                 .arg(filename)
                 .arg(imageData.size() / 1024));
}

void MainWindow::handleImageData(const QString &message)
{
    // Parse image message: IMAGE_START|messageId|filename|dataSize|base64Data|IMAGE_END
    QStringList parts = message.split("|");
    if (parts.size() < 6 || parts[0] != "IMAGE_START" || parts[5] != "IMAGE_END") {
        return; // Invalid image message
    }
    
    QString messageId = parts[1];
    QString filename = parts[2];
    qint64 dataSize = parts[3].toLongLong();
    QString base64Data = parts[4];
    
    // Decode base64 data
    QByteArray imageData = QByteArray::fromBase64(base64Data.toUtf8());
    
    if (imageData.size() != dataSize) {
        appendMessage("<span style='color:red;'>Image data corruption detected.</span>");
        return;
    }
    
    // Extract sender from the full message (before the " - IMAGE_START")
    int dashPos = message.indexOf(" - IMAGE_START");
    QString sender = (dashPos != -1) ? message.left(dashPos) : "Unknown";
    
    displayImage(sender, imageData, filename);
}

void MainWindow::displayImage(const QString &sender, const QByteArray &imageData, const QString &filename)
{
    // Create pixmap from image data
    QPixmap pixmap;
    pixmap.loadFromData(imageData);
    
    if (pixmap.isNull()) {
        appendMessage("<span style='color:red;'>Failed to display image: " + filename + "</span>");
        return;
    }
    
    // Scale image for display (max 300x200)
    if (pixmap.width() > 300 || pixmap.height() > 200) {
        pixmap = pixmap.scaled(300, 200, Qt::KeepAspectRatio, Qt::SmoothTransformation);
    }
    
    // Convert pixmap to HTML img tag using base64
    QByteArray ba;
    QBuffer buffer(&ba);
    buffer.open(QIODevice::WriteOnly);
    pixmap.save(&buffer, "PNG");
    QString base64 = ba.toBase64();
    
    QString senderColor = sender.contains("[ADMIN]") ? "rgb(218,165,32)" : "rgb(0,255,255)";
    bool bold = sender.contains("[ADMIN]");
    
    QString imageHtml = QString(
        "<div style='margin: 5px 0;'>"
        "<span style='color:%1;%2'>%3</span> shared an image:<br/>"
        "<img src='data:image/png;base64,%4' style='max-width:300px; max-height:200px; border:1px solid #ccc; border-radius:5px; margin:5px 0;'/><br/>"
        "<span style='color:gray; font-size:small;'>%5 (%6 KB)</span>"
        "</div>")
        .arg(senderColor)
        .arg(bold ? "font-weight:bold;" : "")
        .arg(sender.toHtmlEscaped())
        .arg(base64)
        .arg(filename)
        .arg(imageData.size() / 1024);
    
    appendMessage(imageHtml);
}

void MainWindow::onImageTransferProgress()
{
    // Update progress bars for pending images
    for (auto it = pendingImages.begin(); it != pendingImages.end(); ++it) {
        PendingImage& pending = it.value();
        if (pending.progressBar) {
            int progress = (pending.receivedSize * 100) / pending.totalSize;
            pending.progressBar->setValue(progress);
        }
    }
}

// Rest of the original MainWindow methods...
void MainWindow::on_connectButton_clicked()
{
    socket->abort();
    QString host = ui->hostEdit->text();
    quint16 port = ui->portEdit->text().toUShort();
    socket->connectToHost(host, port);
    ui->statusLabel->setText("Connecting...");
}

void MainWindow::onSocketConnected()
{
    ui->statusLabel->setText("Connected. Sending credentials...");
    socket->write(ui->passwordEdit->text().toUtf8());
}

void MainWindow::onSocketDisconnected()
{
    ui->statusLabel->setText("Disconnected.");
    appendMessage("<span style='color:red;'>Disconnected from server.</span>");
}

void MainWindow::on_sendButton_clicked()
{
    QString msg = ui->inputEdit->text().trimmed();
    if (msg.isEmpty()) return;
    QString username = ui->usernameEdit->text();

    QString sendMsg;
    if (msg.startsWith("/join")) {
        appendMessage("<span style='color:orange;'>Please use the room list to join rooms instead of typing /join commands.</span>");
        ui->inputEdit->clear();
        return;
    } else if (msg == "/rooms" || msg == "/who") {
        sendMsg = msg;
    } else if (isAdmin && msg.startsWith("admin.")) {
        sendMsg = msg;
    } else {
        if (currentRoom.isEmpty()) {
            appendMessage("<span style='color:red;'>You must join a room first! Use the room list on the right.</span>");
            return;
        }
        sendMsg = username + " - " + msg;
    }

    socket->write(sendMsg.toUtf8());
    ui->inputEdit->clear();

    if (!(sendMsg.startsWith("/") || sendMsg.startsWith("admin."))) {
        displayFormattedMessage(sendMsg, false);
    }
}

void MainWindow::onSocketReadyRead()
{
    while (socket->bytesAvailable()) {
        QByteArray data = socket->readAll();
        messageBuffer += QString::fromUtf8(data);

        QStringList prefixes = {"ADMIN_AUTH_SUCCESS", "AUTH_SUCCESS", "FAIL", "OK",
                                "ROOM_JOINED:", "ROOMS_LIST:", "USERS_LIST:", "ROOM_ERROR:",
                                "ROOM_ANNOUNCEMENT:", "ROOM_DELETED:", "HISTORY:",
                                "ADMIN_SUCCESS:", "ADMIN_MUTE:", "ADMIN_KICK:",
                                "ADMIN_UNMUTE:", "ADMIN_ERROR:", "MUTED:"};

        QString remaining = messageBuffer;
        messageBuffer.clear();

        while (!remaining.isEmpty()) {
            bool foundPrefix = false;
            QString currentMessage;
            int earliestPos = remaining.length();
            QString earliestPrefix;

            for (const QString& prefix : prefixes) {
                int pos = remaining.indexOf(prefix);
                if (pos != -1 && pos < earliestPos) {
                    earliestPos = pos;
                    earliestPrefix = prefix;
                    foundPrefix = true;
                }
            }

            if (foundPrefix && earliestPos == 0) {
                int nextPrefixPos = remaining.length();
                for (const QString& nextPrefix : prefixes) {
                    int pos = remaining.indexOf(nextPrefix, earliestPrefix.length());
                    if (pos != -1 && pos < nextPrefixPos) {
                        nextPrefixPos = pos;
                    }
                }
                currentMessage = remaining.left(nextPrefixPos);
                remaining = remaining.mid(nextPrefixPos);
            } else if (foundPrefix) {
                currentMessage = remaining.left(earliestPos);
                remaining = remaining.mid(earliestPos);
            } else {
                currentMessage = remaining;
                remaining.clear();
            }

            if (!currentMessage.isEmpty()) {
                processMessage(currentMessage.trimmed());
            }
        }
    }
}

void MainWindow::processMessage(const QString& msg)
{
    if (msg == "ADMIN_AUTH_SUCCESS") {
        isAdmin = true;
        socket->write(ui->usernameEdit->text().toUtf8());
    } else if (msg == "AUTH_SUCCESS") {
        socket->write(ui->usernameEdit->text().toUtf8());
    } else if (msg == "FAIL") {
        appendMessage("<span style='color:red;'>Authentication failed.</span>");
        socket->disconnectFromHost();
    } else if (msg == "OK") {
        appendMessage("<span style='color:rgb(0,150,0);'>Authentication successful!</span>");
        if (isAdmin) {
            appendMessage("<span style='color:rgb(218,165,32);'>You are logged in as an ADMIN!</span>");
        }
        socket->write("/rooms");
        socket->flush();
    }
    else if (msg.startsWith("ROOM_JOINED:")) {
        currentRoom = msg.mid(12);
        joiningRoom = false;
        ui->chatText->clear();
        appendMessage(QString("<span style='color:rgb(0,150,0);'>Joined room: %1</span>").arg(currentRoom));
        appendMessage(QString("<span style='color:rgb(0,255,255);'>=== %1 Channel ===</span>").arg(currentRoom));
        appendMessage("Type a message and press Enter or drag & drop images.");
        appendMessage("Room commands: /join &lt;roomname&gt;, /rooms, /who");
        if (isAdmin) {
            appendMessage("Admin commands: admin.mute &lt;user&gt;, admin.kick &lt;user&gt;, admin.unmute &lt;user&gt;");
            appendMessage("Room management: admin.makeroom &lt;room&gt;, admin.removeroom &lt;room&gt;");
        }
    }
    else if (msg.startsWith("ROOMS_LIST:")) {
        QString payload = msg.mid(11).trimmed();
        if (payload.startsWith("Available rooms: ")) {
            payload = payload.mid(17);
        }
        ui->roomsList->clear();
        if (!payload.isEmpty()) {
            QStringList parts = payload.split(", ", Qt::SkipEmptyParts);
            for (const QString& part : parts) {
                QString trimmed = part.trimmed();
                int parenPos = trimmed.indexOf('(');
                QString roomName = (parenPos > 0) ? trimmed.left(parenPos).trimmed() : trimmed;
                if (!roomName.isEmpty()) {
                    auto *item = new QListWidgetItem(trimmed, ui->roomsList);
                    item->setData(Qt::UserRole, roomName);
                    item->setFlags(Qt::ItemIsSelectable | Qt::ItemIsEnabled);
                }
            }
        }
        ui->roomsList->setEnabled(true);
    }
    else if (msg.startsWith("USERS_LIST:")) {
        appendMessage(QString("<span style='color:blue;'>%1</span>").arg(msg.mid(11).toHtmlEscaped()));
    }
    else if (msg.startsWith("ROOM_ERROR:")) {
        appendMessage(QString("<span style='color:red;'>%1</span>").arg(msg.mid(11).toHtmlEscaped()));
    }
    else if (msg.startsWith("ROOM_ANNOUNCEMENT:")) {
        appendMessage(QString("<span style='color:blue;'>📢 %1</span>").arg(msg.mid(18).toHtmlEscaped()));
    }
    else if (msg.startsWith("ROOM_DELETED:")) {
        QString deletedMsg = msg.mid(13);
        appendMessage(QString("<span style='color:red;'>🚫 %1</span>").arg(deletedMsg.toHtmlEscaped()));
        int firstQuote = deletedMsg.indexOf("'");
        int secondQuote = deletedMsg.indexOf("'", firstQuote + 1);
        if (firstQuote != -1 && secondQuote != -1) {
            QString deletedRoomName = deletedMsg.mid(firstQuote + 1, secondQuote - firstQuote - 1);
            if (currentRoom == deletedRoomName) {
                currentRoom.clear();
                appendMessage("<span style='color:yellow;'>You have been removed from the deleted room.</span>");
            }
        }
    }
    else if (msg.startsWith("HISTORY:")) {
        QString historyMsg = msg.mid(8);
        // Check if this is an image message
        if (historyMsg.contains("IMAGE_START|")) {
            handleImageData(historyMsg);
        } else {
            displayFormattedMessage(historyMsg, true);
        }
    }
    else if (msg.startsWith("ADMIN_SUCCESS:")) {
        appendMessage(QString("<span style='color:rgb(0,150,0);'>%1</span>").arg(msg.mid(14).toHtmlEscaped()));
    }
    else if (msg.startsWith("ADMIN_MUTE:")) {
        appendMessage(QString("<span style='color:red;'>%1</span>").arg(msg.mid(11).toHtmlEscaped()));
    }
    else if (msg.startsWith("ADMIN_KICK:")) {
        appendMessage(QString("<span style='color:red;'>%1</span>").arg(msg.mid(11).toHtmlEscaped()));
        socket->disconnectFromHost();
    }
    else if (msg.startsWith("ADMIN_UNMUTE:")) {
        appendMessage(QString("<span style='color:rgb(144,238,144);'>%1</span>").arg(msg.mid(13).toHtmlEscaped()));
    }
    else if (msg.startsWith("ADMIN_ERROR:")) {
        appendMessage(QString("<span style='color:red;'>Admin Error: %1</span>").arg(msg.mid(12).toHtmlEscaped()));
    }
    else if (msg.startsWith("MUTED:")) {
        appendMessage(QString("<span style='color:red;'>%1</span>").arg(msg.mid(6).toHtmlEscaped()));
    }
    else if (msg.contains(" has joined") || msg.contains(" has left") || msg.contains(" has been ")) {
        appendMessage(QString("<span style='color:lightgray;'>%1</span>").arg(msg.toHtmlEscaped()));
    }
    else {
        // Check if this is an image message
        if (msg.contains("IMAGE_START|")) {
            handleImageData(msg);
        } else {
            displayFormattedMessage(msg, false);
        }
    }
}

void MainWindow::displayFormattedMessage(const QString& message, bool isHistory)
{
    QString processedMsg = processMentionsForDisplay(message);
    int dashPos = processedMsg.indexOf(" - ");
    if (dashPos != -1) {
        QString senderName = processedMsg.left(dashPos);
        QString actualMessage = processedMsg.mid(dashPos + 3);
        QString senderColor = senderName.contains("[ADMIN]") ? "rgb(218,165,32)" : "rgb(0,255,255)";
        bool bold = senderName.contains("[ADMIN]");

        QString formattedMsg = QString("<span style='color:%1;%2'>%3</span> - %4")
                                   .arg(senderColor)
                                   .arg(bold ? "font-weight:bold;" : "")
                                   .arg(senderName.toHtmlEscaped())
                                   .arg(actualMessage);

        if (isHistory) {
            formattedMsg = QString("<span style='color:gray; font-style:italic;'>%1</span>").arg(formattedMsg);
        }
        appendMessage(formattedMsg);
    } else {
        appendMessage(isHistory
                          ? QString("<span style='color:gray; font-style:italic;'>%1</span>").arg(processedMsg.toHtmlEscaped())
                          : processedMsg.toHtmlEscaped());
    }
}

QString MainWindow::processMentionsForDisplay(const QString& message)
{
    QString processed = message;
    QString cleanCurrentUsername = ui->usernameEdit->text();
    if (cleanCurrentUsername.startsWith("[ADMIN] ")) {
        cleanCurrentUsername = cleanCurrentUsername.mid(8);
    }
    int pos = 0;
    while ((pos = processed.indexOf("MENTION_START@", pos)) != -1) {
        int endPos = processed.indexOf("MENTION_END", pos);
        if (endPos != -1) {
            QString mentionedUser = processed.mid(pos + 14, endPos - pos - 14);
            QString replacement = (mentionedUser == cleanCurrentUsername)
                                      ? QString("<span style='background-color:yellow; font-weight:bold; color:black;'>@%1</span>").arg(mentionedUser)
                                      : QString("<span style='font-weight:bold; color:white;'>@%1</span>").arg(mentionedUser);
            processed.replace(pos, endPos - pos + 11, replacement);
            pos += replacement.length();
        } else break;
    }
    return processed;
}

void MainWindow::on_roomsList_itemClicked(QListWidgetItem* item)
{
    if (!socket->isValid()) {
        appendMessage("<span style='color:red;'>You must be connected to join a room.</span>");
        return;
    }

    QString roomName = item->data(Qt::UserRole).toString().trimmed();
    if (roomName.isEmpty() || roomName == currentRoom || joiningRoom) return;

    joiningRoom = true;
    ui->inputEdit->clear();

    QString joinCommand = "/join " + roomName;
    socket->write(joinCommand.toUtf8());
    socket->flush();

    appendMessage("<span style='color:green;'>Joining room: " + roomName + "...</span>");
}

void MainWindow::on_refreshButton_clicked()
{
    if (!socket->isValid()) {
        appendMessage("<span style='color:red;'>You must be connected to refresh.</span>");
        return;
    }

    if (!joiningRoom) {
        QString refreshCommand = "/rooms";
        socket->write(refreshCommand.toUtf8());
        socket->flush();
        appendMessage("<span style='color:blue;'>Refreshing rooms list...</span>");
    }
}

QString MainWindow::ansiToHtml(const QString &input)
{
    static QMap<int, QString> colorMap = {
        {30,"black"},{31,"red"},{32,"green"},{33,"yellow"},
        {34,"blue"},{35,"magenta"},{36,"cyan"},{37,"white"},
        {90,"gray"},{91,"lightcoral"},{92,"lightgreen"},{93,"khaki"},
        {94,"lightblue"},{95,"violet"},{96,"lightcyan"},{97,"white"}
    };
    QString output;
    QRegularExpression re("\x1b\\[([0-9;]*)m");
    int lastPos = 0; QString currentColor="black"; bool bold=false;
    auto it = re.globalMatch(input);
    while (it.hasNext()) {
        auto match = it.next();
        int start = match.capturedStart();
        QString chunk = input.mid(lastPos, start-lastPos);
        if (!chunk.isEmpty()) {
            output += QString("<span style='color:%1;%2'>%3</span>")
            .arg(currentColor).arg(bold?"font-weight:bold;":"").arg(chunk.toHtmlEscaped());
        }
        for (const QString &c : match.captured(1).split(';')) {
            int code = c.toInt(); if (!code) continue;
            if (code == 0) { currentColor="black"; bold=false; }
            else if (code == 1) bold=true;
            else if (colorMap.contains(code)) currentColor=colorMap[code];
        }
        lastPos = match.capturedEnd();
    }
    QString rest = input.mid(lastPos);
    if (!rest.isEmpty()) {
        output += QString("<span style='color:%1;%2'>%3</span>")
        .arg(currentColor).arg(bold?"font-weight:bold;":"").arg(rest.toHtmlEscaped());
    }
    return output;
}

void MainWindow::appendMessage(const QString &html)
{
    QTextCursor cursor = ui->chatText->textCursor();
    cursor.movePosition(QTextCursor::End);
    ui->chatText->setTextCursor(cursor);
    ui->chatText->insertHtml(html + "<br>");
    ui->chatText->moveCursor(QTextCursor::End);
}

void MainWindow::on_inputEdit_returnPressed() { on_sendButton_clicked(); }