# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'GUI.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QListWidget,
    QListWidgetItem, QPushButton, QSizePolicy, QSpinBox,
    QTextBrowser, QVBoxLayout, QWidget)

class GraphicUI(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(941, 694)
        self.heigh_input = QLineEdit(Form)
        self.heigh_input.setObjectName(u"heigh_input")
        self.heigh_input.setGeometry(QRect(60, 110, 113, 20))
        self.add_button = QPushButton(Form)
        self.add_button.setObjectName(u"add_button")
        self.add_button.setGeometry(QRect(430, 110, 75, 24))
        self.part_display = QListWidget(Form)
        self.part_display.setObjectName(u"part_display")
        self.part_display.setGeometry(QRect(60, 190, 361, 201))
        self.layoutWidget = QWidget(Form)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(0, 0, 2, 2))
        self.verticalLayout_4 = QVBoxLayout(self.layoutWidget)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.height_label = QLabel(Form)
        self.height_label.setObjectName(u"height_label")
        self.height_label.setGeometry(QRect(0, 110, 54, 16))
        self.height_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.width_label = QLabel(Form)
        self.width_label.setObjectName(u"width_label")
        self.width_label.setGeometry(QRect(190, 110, 54, 16))
        self.width_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.width_input = QLineEdit(Form)
        self.width_input.setObjectName(u"width_input")
        self.width_input.setGeometry(QRect(250, 110, 113, 20))
        self.label_3 = QLabel(Form)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(60, 160, 54, 16))
        self.nesting_button = QPushButton(Form)
        self.nesting_button.setObjectName(u"nesting_button")
        self.nesting_button.setGeometry(QRect(770, 390, 75, 24))
        self.delete_button = QPushButton(Form)
        self.delete_button.setObjectName(u"delete_button")
        self.delete_button.setGeometry(QRect(60, 440, 75, 24))
        self.sheet_h_label = QLabel(Form)
        self.sheet_h_label.setObjectName(u"sheet_h_label")
        self.sheet_h_label.setGeometry(QRect(610, 110, 81, 16))
        self.sheet_h_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.heigh_input_sheet = QLineEdit(Form)
        self.heigh_input_sheet.setObjectName(u"heigh_input_sheet")
        self.heigh_input_sheet.setGeometry(QRect(710, 110, 113, 20))
        self.width_input_sheet = QLineEdit(Form)
        self.width_input_sheet.setObjectName(u"width_input_sheet")
        self.width_input_sheet.setGeometry(QRect(710, 180, 113, 20))
        self.sheet_w_label = QLabel(Form)
        self.sheet_w_label.setObjectName(u"sheet_w_label")
        self.sheet_w_label.setGeometry(QRect(620, 180, 71, 16))
        self.sheet_w_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.SET_button = QPushButton(Form)
        self.SET_button.setObjectName(u"SET_button")
        self.SET_button.setGeometry(QRect(830, 140, 75, 24))
        self.sheet_size_label = QLabel(Form)
        self.sheet_size_label.setObjectName(u"sheet_size_label")
        self.sheet_size_label.setGeometry(QRect(680, 220, 61, 16))
        self.Counters = QSpinBox(Form)
        self.Counters.setObjectName(u"Counters")
        self.Counters.setGeometry(QRect(380, 110, 42, 22))
        self.sheetsize_display = QTextBrowser(Form)
        self.sheetsize_display.setObjectName(u"sheetsize_display")
        self.sheetsize_display.setGeometry(QRect(580, 240, 261, 61))
        self.preview_button = QPushButton(Form)
        self.preview_button.setObjectName(u"preview_button")
        self.preview_button.setGeometry(QRect(770, 420, 75, 24))
        self.usedratio_display = QTextBrowser(Form)
        self.usedratio_display.setObjectName(u"usedratio_display")
        self.usedratio_display.setGeometry(QRect(580, 490, 261, 31))
        self.label_7 = QLabel(Form)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(580, 470, 141, 16))
        self.wolf_label = QLabel(Form)
        self.wolf_label.setObjectName(u"wolf_label")
        self.wolf_label.setGeometry(QRect(0, 50, 91, 16))
        self.wolf_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.sheetsize_display_2 = QTextBrowser(Form)
        self.sheetsize_display_2.setObjectName(u"sheetsize_display_2")
        self.sheetsize_display_2.setGeometry(QRect(100, 40, 201, 31))
        self.import_button = QPushButton(Form)
        self.import_button.setObjectName(u"import_button")
        self.import_button.setGeometry(QRect(60, 410, 75, 24))

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.add_button.setText(QCoreApplication.translate("Form", u"ADD", None))
        self.height_label.setText(QCoreApplication.translate("Form", u"<html><head/><body><p align=\"center\">height</p></body></html>", None))
        self.width_label.setText(QCoreApplication.translate("Form", u"<html><head/><body><p align=\"center\">width</p></body></html>", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"Part set", None))
        self.nesting_button.setText(QCoreApplication.translate("Form", u"Nesting", None))
        self.delete_button.setText(QCoreApplication.translate("Form", u"Delete", None))
        self.sheet_h_label.setText(QCoreApplication.translate("Form", u"<html><head/><body><p align=\"center\">sheet height</p></body></html>", None))
        self.sheet_w_label.setText(QCoreApplication.translate("Form", u"<html><head/><body><p align=\"center\">sheet width</p></body></html>", None))
        self.SET_button.setText(QCoreApplication.translate("Form", u"SET", None))
        self.sheet_size_label.setText(QCoreApplication.translate("Form", u"Sheet size", None))
        self.preview_button.setText(QCoreApplication.translate("Form", u"Preview", None))
        self.label_7.setText(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" font-weight:700;\">\u5269\u4f59\u53ef\u7528\u9762\u79ef\u6240\u5360\u6bd4</span></p></body></html>", None))
        self.wolf_label.setText(QCoreApplication.translate("Form", u"<html><head/><body><p align=\"center\">wolf quantity</p></body></html>", None))
        self.import_button.setText(QCoreApplication.translate("Form", u"Import", None))
    # retranslateUi

