import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QStackedWidget, QGridLayout, QVBoxLayout,
                             QHBoxLayout, QLabel, QPushButton, QMessageBox)

from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QTimer, QFile, QTextStream


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('WineTech')
        self.currentStep = 0
        self.selectedSlot = None
        self.rfidCode = None
        self.timeLeft = 0
        self.loadStylesheet()

        self.initUI()
        self.showStep(0)


    def loadStylesheet(self):
        file = QFile("styles.qss")
        if file.open(QFile.ReadOnly | QFile.Text):
            stream = QTextStream(file)
            stylesheet = stream.readAll()
            self.setStyleSheet(stylesheet)
        else:
            print("qss file not found")

    def initUI(self):
        self.mainWidget = QWidget()
        self.setCentralWidget(self.mainWidget)

        self.timerLabel = QLabel('')
        self.timerLabel.setAlignment(Qt.AlignRight)
        self.timerLabel.setStyleSheet('font-size: 18px; color: red;')
        self.timerLabel.hide()

        self.stack = QStackedWidget()

        # Создаем шаги
        self.step0 = self.createStep0()
        self.step1 = self.createStep1()
        self.step2 = self.createStep2()
        self.step3 = self.createStep3()
        self.step4 = self.createStep4()

        self.stack.addWidget(self.step0)
        self.stack.addWidget(self.step1)
        self.stack.addWidget(self.step2)
        self.stack.addWidget(self.step3)
        self.stack.addWidget(self.step4)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.timerLabel)
        mainLayout.addWidget(self.stack)

        self.mainWidget.setLayout(mainLayout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.updateTimer)

    def createStep0(self):
        # Сетка бутылок
        step0Widget = QWidget()
        gridLayout = QGridLayout()
        self.bottles = self.loadBottleData()
        row = 0
        col = 0
        for i, bottle in enumerate(self.bottles):
            bottleWidget = self.createBottleTile(bottle)
            gridLayout.addWidget(bottleWidget, row, col)
            col += 1
            if col >= 4:
                col = 0
                row += 1
        step0Widget.setLayout(gridLayout)
        return step0Widget

    def createBottleTile(self, bottle):
        bottleTile = QWidget()
        layout = QVBoxLayout()
        imageLabel = QLabel()
        pixmap = QPixmap(f'path/to/bottle_images/{bottle["id"]}.jpg')  # Замените на путь к вашим изображениям
        imageLabel.setPixmap(pixmap.scaled(100, 150, Qt.KeepAspectRatio))
        nameLabel = QLabel(bottle['name'])
        locationLabel = QLabel(bottle['location'].replace('\n', ' · '))

        layout.addWidget(imageLabel)
        layout.addWidget(nameLabel)
        layout.addWidget(locationLabel)

        bottleTile.setLayout(layout)
        if bottle['remaining_volume'] >= 120:
            bottleTile.mousePressEvent = lambda event, slot=bottle['slot_number']: self.selectSlot(slot)
        else:
            bottleTile.setEnabled(False)
        return bottleTile

    def createStep1(self):
        step1Widget = QWidget()
        layout = QHBoxLayout()

        self.bottleImageLabel = QLabel()
        self.bottleImageLabel.setFixedSize(300, 450)
        self.bottleImageLabel.setAlignment(Qt.AlignCenter)
        infoLayout = QVBoxLayout()
        self.bottleNameLabel = QLabel()
        self.bottleNameLabel.setFont(QFont('Arial', 24))
        self.bottleLocationLabel = QLabel()
        self.bottleDescriptionLabel = QLabel()
        self.bottleDescriptionLabel.setWordWrap(True)
        buttonsLayout = QHBoxLayout()
        smallPortionButton = QPushButton('Тестовая порция')
        smallPortionButton.clicked.connect(lambda: self.selectPortion('small'))
        bigPortionButton = QPushButton('Полная порция')
        bigPortionButton.clicked.connect(lambda: self.selectPortion('big'))
        backButton = QPushButton('Назад')
        backButton.clicked.connect(self.resetProgress)
        buttonsLayout.addWidget(smallPortionButton)
        buttonsLayout.addWidget(bigPortionButton)
        buttonsLayout.addWidget(backButton)
        infoLayout.addWidget(self.bottleNameLabel)
        infoLayout.addWidget(self.bottleLocationLabel)
        infoLayout.addWidget(self.bottleDescriptionLabel)
        infoLayout.addLayout(buttonsLayout)
        layout.addWidget(self.bottleImageLabel)
        layout.addLayout(infoLayout)
        step1Widget.setLayout(layout)
        return step1Widget

    def createStep2(self):
        step2Widget = QWidget()
        layout = QVBoxLayout()
        label = QLabel('Приложите RFID метку')
        label.setFont(QFont('Arial', 18))
        loadingLabel = QLabel('Загрузка...')
        layout.addWidget(label)
        layout.addWidget(loadingLabel)
        step2Widget.setLayout(layout)
        return step2Widget

    def createStep3(self):
        step3Widget = QWidget()
        layout = QVBoxLayout()
        label = QLabel('Нажмите подсвеченную кнопку для завершения операции')
        label.setFont(QFont('Arial', 18))
        completeButton = QPushButton('Завершить операцию')
        completeButton.clicked.connect(self.completeOperation)
        layout.addWidget(label)
        layout.addWidget(completeButton)
        step3Widget.setLayout(layout)
        return step3Widget

    def createStep4(self):
        step4Widget = QWidget()
        layout = QVBoxLayout()
        label = QLabel('Операция успешно выполнена!')
        label.setFont(QFont('Arial', 18))
        returnButton = QPushButton('Вернуться в главное меню')
        returnButton.clicked.connect(self.resetProgress)
        layout.addWidget(label)
        layout.addWidget(returnButton)
        step4Widget.setLayout(layout)
        return step4Widget

    def loadBottleData(self):
        bottles = [
            {'id': 1, 'name': 'Wine A', 'location': 'France\nBordeaux', 'remaining_volume': 500, 'slot_number': 1,
             'description': 'A fine wine from Bordeaux.'},
            {'id': 2, 'name': 'Wine B', 'location': 'Italy\nTuscany', 'remaining_volume': 100, 'slot_number': 2,
             'description': 'A robust Tuscan wine.'},
            # Добавьте больше бутылок по необходимости
        ]
        return bottles

    def showStep(self, step):
        self.currentStep = step
        self.stack.setCurrentIndex(step)
        if step == 0:
            self.timerLabel.hide()
            self.stopTimer()
        else:
            self.startTimer()

    def startTimer(self):
        self.timeLeft = 60
        self.timerLabel.setText(str(self.timeLeft))
        self.timerLabel.show()
        self.timer.start(1000)

    def stopTimer(self):
        self.timer.stop()

    def updateTimer(self):
        self.timeLeft -= 1
        self.timerLabel.setText(str(self.timeLeft))
        if self.timeLeft <= 0:
            self.timer.stop()
            self.resetProgress()

    def resetProgress(self):
        self.selectedSlot = None
        self.stopTimer()
        self.showStep(0)

    def selectSlot(self, slot):
        bottle = next((b for b in self.bottles if b['slot_number'] == slot), None)
        if bottle:
            self.selectedSlot = slot
            pixmap = QPixmap(f'path/to/bottle_images/{bottle["id"]}.jpg')  # Замените на путь к вашим изображениям
            self.bottleImageLabel.setPixmap(pixmap.scaled(self.bottleImageLabel.size(), Qt.KeepAspectRatio))
            self.bottleNameLabel.setText(bottle['name'])
            self.bottleLocationLabel.setText(bottle['location'].replace('\n', ' · '))
            self.bottleDescriptionLabel.setText(bottle['description'])
            self.showStep(1)

    def selectPortion(self, portionType):
        self.showStep(2)
        QTimer.singleShot(2000, lambda: self.processRFID(portionType))

    def processRFID(self, portionType):
        is_valid = True  # Здесь вы можете добавить проверку RFID
        if not is_valid:
            QMessageBox.warning(self, 'Ошибка', 'Невалидный RFID')
            self.resetProgress()
        else:
            self.rfidCode = 'RFID123456'
            self.showStep(3)

    def completeOperation(self):
        self.showStep(4)
        self.stopTimer()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
