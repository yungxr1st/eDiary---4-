import hashlib
import sys
import pyodbc
import pandas as pd
import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QStyleFactory, QVBoxLayout,
                             QHBoxLayout, QPushButton, QSpinBox, QLabel, QGridLayout, QComboBox, 
                             QLineEdit, QTabWidget, QGroupBox, QListWidget, QDialogButtonBox, 
                             QDialog, QFormLayout, QMessageBox, QListWidgetItem, QTextEdit,
                             QDateEdit, QCheckBox, QTableWidget, QTableWidgetItem, QHeaderView, 
                             QRadioButton, QScrollArea)
from PyQt5.QtGui import (QPixmap, QIcon, QPainter, QColor, QPen, QFont, QPalette)
from PyQt5.QtCore import (Qt, QSize, QTimer, pyqtSignal, QDate)


class MainMenuAdministration(QMainWindow): # главное меню для администрации
    def __init__(self, id_user = None, fio = None, conn = None):
        super().__init__()
        self.id_user = id_user
        self.fio = fio
        self.conn = conn

        central_widget = QWidget()

        self.setWindowTitle("Главное меню")
        self.setFixedSize(900, 600)
        self.setCentralWidget(central_widget)
        self.setStyleSheet("background-color: #f0f0f0;")

        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        main_layout_top = QHBoxLayout()
        main_layout.addLayout(main_layout_top)

        # верхняя часть
        label = QLabel(f"Добро пожаловать, {fio}")
        label.setAlignment(Qt.AlignLeft)
        label.setStyleSheet("""
            font-size: 20px;
            font-family: Roboto;
            color: #333;
            padding-top: 5px;
        """)
        main_layout_top.addWidget(label)

        # кнопка выйти
        self.button_exit = QPushButton("Выйти")
        self.button_exit.setFixedSize(120, 35)
        self.button_exit.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border-radius: 5px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
        """)
        self.button_exit.clicked.connect(self.logout)
        main_layout_top.addWidget(self.button_exit)

        # расположение областей
        main_layout_h = QHBoxLayout() # основная область
        group_button_layout = QVBoxLayout() # область для кнопок
        self.content_layout_v = QVBoxLayout() # область для пользователей/составления расписания/успеваемости/группы и предметы
        main_layout_h.addLayout(group_button_layout)
        main_layout_h.addStretch(3)
        main_layout_h.addLayout(self.content_layout_v)
        main_layout_h.addStretch(1)
        main_layout.addLayout(main_layout_h)

        group_button_layout.addStretch(1)

        # кнопка пользователи
        self.button_users = QPushButton("Пользователи")
        self.button_users.setFixedSize(200, 40)
        self.button_users.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border-radius: 5px;
                font-size: 14px;
                text-align: left;
                padding-left: 15px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
        """)
        self.button_users.clicked.connect(self.show_users)
        group_button_layout.addWidget(self.button_users, alignment=Qt.AlignLeft)
        group_button_layout.addSpacing(5)

        # кнопка расписание
        self.button_schedule = QPushButton("Расписание")
        self.button_schedule.setFixedSize(200, 40)
        self.button_schedule.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border-radius: 5px;
                font-size: 14px;
                text-align: left;
                padding-left: 15px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
        """)
        # self.button_homework.clicked.connect(self.show_homework)
        group_button_layout.addWidget(self.button_schedule, alignment=Qt.AlignLeft)
        group_button_layout.addSpacing(5)

        # кнопка успеваемость
        self.button_stats = QPushButton("Успеваемость")
        self.button_stats.setFixedSize(200, 40)
        self.button_stats.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border-radius: 5px;
                font-size: 14px;
                text-align: left;
                padding-left: 15px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
        """)
        # self.button_stats.clicked.connect(self.show_grades)
        group_button_layout.addWidget(self.button_stats, alignment=Qt.AlignLeft)
        group_button_layout.addSpacing(5)

        # кнопка группы и предметы
        self.button_groups_subjects = QPushButton("Группы и предметы")
        self.button_groups_subjects.setFixedSize(200, 40)
        self.button_groups_subjects.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border-radius: 5px;
                font-size: 14px;
                text-align: left;
                padding-left: 15px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
        """)
        # self.button_schedule.clicked.connect(self.show_schedule)
        group_button_layout.addWidget(self.button_groups_subjects, alignment=Qt.AlignLeft)

        group_button_layout.addStretch(2)

        self.users()

    def logout(self): # выход из учетки
        from main import LoginWindow
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()

    def clear_content_layout(self): # удаление элементов из content_layout_v для вставки другого контента
        for i in reversed(range(self.content_layout_v.count())):
            widget = self.content_layout_v.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

    def show_users(self):
        self.clear_content_layout()

        self.content_layout_v.addWidget(self.users_widget)

        self.load_users()

    def users(self):
        self.users_widget = QWidget()
        users_layout = QVBoxLayout()
        self.users_widget.setLayout(users_layout)

        users_label = QLabel("Пользователи:")
        users_label.setAlignment(Qt.AlignLeft)
        users_label.setStyleSheet("""
            font-size: 22px;
            font-weight: bold;
            font-family: Roboto;
            color: #333;
            margin-top: 20px;
            margin-bottom: 10px;
        """)
        users_layout.addWidget(users_label)

        # таблица для вывода пользователей
        self.users_table = QTableWidget()
        self.users_table.setFixedSize(600, 400)
        self.users_table.setColumnCount(4)
        self.users_table.setHorizontalHeaderLabels([
            "Фамилия", "Имя", "Отчество", "Роль"
        ])
        self.users_table.horizontalHeader().setStretchLastSection(True)
        self.users_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.users_table.setSelectionMode(QTableWidget.SingleSelection)
        self.users_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 5px;
                font-family: Roboto;
                gridline-color: #eee;
                outline: 0;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #f0f0f0;
            }
            QHeaderView::section {
                background-color: #3498db;
                color: white;
                padding: 8px;
                font-weight: bold;
                border: none;
            }
            QTableWidget::item:selected {
                background-color: #e8f4fc;
                color: #2c3e50;
            }
            QHeaderView::section:vertical {
                background-color: #3498db;
                color: white;
                border: none;
                width: 0px;
            }
            QTableWidget::item:focus {
                outline: none;
                border: none;
            }
        """)
        header = self.users_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Fixed)  # фамилия
        header.resizeSection(0, 150)
        header.setSectionResizeMode(1, QHeaderView.Fixed)  # имя
        header.resizeSection(1, 150)
        header.setSectionResizeMode(2, QHeaderView.Fixed)  # отчество
        header.resizeSection(2, 150)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # роль
        users_layout.addWidget(self.users_table)

        self.edit_user_button = QPushButton("Редактировать пользователя")
        self.edit_user_button.setFixedSize(250, 40)
        self.edit_user_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border-radius: 5px;
                font-size: 14px;
                text-align: center;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
        """)
        self.edit_user_button.clicked.connect(self.open_edit_user_dialog)
        users_layout.addWidget(self.edit_user_button, alignment=Qt.AlignRight)

    def load_users(self): # загрузка пользователей 
        try:
            cursor = self.conn.cursor()
            
            query = ("""
                select 
                    u.id_user,
                    u.surname,
                    u.name,
                    u.patronymic,
                    r.title as role_name
                from users u
                inner join role r on u.id_role = r.id_role
                where u.is_active = 1 and u.id_role < 3
                order by u.surname, u.name
            """)
            cursor.execute(query)
            users_data = cursor.fetchall()
            
            self.users_table.setRowCount(len(users_data))
            
            for row, user in enumerate(users_data):
                user_id = user[0]
                surname = user[1]
                name = user[2]
                patronymic = user[3]
                role_name = user[4]
                
                # фамилия
                surname_item = QTableWidgetItem(surname)
                surname_item.setData(Qt.UserRole, {'user_id': user_id})
                surname_item.setFlags(surname_item.flags() & ~Qt.ItemIsEditable)
                surname_item.setTextAlignment(Qt.AlignCenter)
                self.users_table.setItem(row, 0, surname_item)

                # имя
                name_item = QTableWidgetItem(name)
                name_item.setData(Qt.UserRole, {'user_id': user_id})
                name_item.setFlags(name_item.flags() & ~Qt.ItemIsEditable)
                name_item.setTextAlignment(Qt.AlignCenter)
                self.users_table.setItem(row, 1, name_item)

                # отчество
                patronymic_item = QTableWidgetItem(patronymic)
                patronymic_item.setData(Qt.UserRole, {'user_id': user_id})
                patronymic_item.setFlags(patronymic_item.flags() & ~Qt.ItemIsEditable)
                patronymic_item.setTextAlignment(Qt.AlignCenter)
                self.users_table.setItem(row, 2, patronymic_item)

                # роль
                role_name_item = QTableWidgetItem(role_name)
                role_name_item.setData(Qt.UserRole, {'user_id': user_id})
                role_name_item.setFlags(role_name_item.flags() & ~Qt.ItemIsEditable)
                role_name_item.setTextAlignment(Qt.AlignCenter)
                self.users_table.setItem(row, 3, role_name_item)
            
            cursor.close()
            
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить пользователей: {str(e)}")

    def open_edit_user_dialog(self): # редактирование пользователя
        selected_row = self.users_table.currentRow()
        if selected_row >= 0:
            selected_items = self.users_table.selectedItems()
            dialog = EditUserDialog(self, selected_items=selected_items, conn=self.conn)
            if dialog.exec_() == QDialog.Accepted:
                self.load_users()


class EditUserDialog(QDialog): # окно редактирования пользователя
    def __init__(self, parent=None, selected_items=None, conn=None):
        super().__init__(parent)
        self.selected_items = selected_items
        item = selected_items[0]
        item_data = item.data(Qt.UserRole)
        self.id_user = item_data['user_id']
        self.conn = conn

        self.setWindowTitle("Редактирование пользователя")
        self.setFixedSize(350, 300)
        self.setModal(True)
        self.setWindowFlags(Qt.Dialog | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        
        layout = QVBoxLayout()
        self.setLayout(layout)

        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        
        # фамилия
        surname_label = QLabel("Фамилия:")
        surname_label.setFont(QFont("Roboto", 10))
        
        self.surname_edit = QLineEdit()
        self.surname_edit.setFixedSize(250, 35)
        self.surname_edit.setFont(QFont("Roboto", 10))
        self.surname_edit.setStyleSheet("""
            border-radius: 5px;
            border: 2px solid #3498db;
            padding: 5px;
        """)
        form_layout.addRow(surname_label, self.surname_edit)
        
        # имя
        name_label = QLabel("Имя:")
        name_label.setFont(QFont("Roboto", 10))

        self.name_edit = QLineEdit()
        self.name_edit.setFixedSize(250, 35)
        self.name_edit.setFont(QFont("Roboto", 10))
        self.name_edit.setStyleSheet("""
            border-radius: 5px;
            border: 2px solid #3498db;
            padding: 5px;
        """)
        form_layout.addRow(name_label, self.name_edit)
        
        # отчество
        patronymic_label = QLabel("Отчество:")
        patronymic_label.setFont(QFont("Roboto", 10))

        self.patronymic_edit = QLineEdit()
        self.patronymic_edit.setFixedSize(250, 35)
        self.patronymic_edit.setFont(QFont("Roboto", 10))
        self.patronymic_edit.setStyleSheet("""
            border-radius: 5px;
            border: 2px solid #3498db;
            padding: 5px;
        """)
        form_layout.addRow(patronymic_label, self.patronymic_edit)
        
        # роль
        role_label = QLabel("Роль:")
        role_label.setFont(QFont("Roboto", 10))

        self.role_text = QLabel()
        self.role_text.setFixedSize(250, 35)
        self.role_text.setStyleSheet("""
            font-size: 14px;
            font-family: Roboto;
            color: #333;
        """)
        form_layout.addRow(role_label, self.role_text)
        
        layout.addLayout(form_layout)
        
        buttons_layout = QHBoxLayout()
        
        self.save_button = QPushButton("Сохранить")
        self.save_button.setFixedSize(120, 40)
        self.save_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
        """)
        self.save_button.clicked.connect(self.save_user)
        
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.save_button)
        buttons_layout.addStretch()
        
        layout.addLayout(buttons_layout)
        
        self.load_user_data_by_login()

    def load_user_data_by_login(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                select u.id_user, u.surname, u.name, u.patronymic, r.title
                from users u
                inner join role r on u.id_role = r.id_role
                where u.id_user = ?
            """, (self.id_user,))
            user_data = cursor.fetchone()
            
            if user_data:
                self.id_user = user_data[0]
                self.surname_edit.setText(user_data[1] or "")
                self.name_edit.setText(user_data[2] or "")
                self.patronymic_edit.setText(user_data[3] or "")
                self.role_text.setText(user_data[4] or "")
            else:
                QMessageBox.warning(self, "Ошибка", "Пользователь не найден")
                self.reject()
                
            cursor.close()

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить данные пользователя: {str(e)}")

    def save_user(self):  # сохранение
        if not self.validate_data():
            return
        
        try:
            cursor = self.conn.cursor()
            surname = self.surname_edit.text().strip()
            name = self.name_edit.text().strip()
            patronymic = self.patronymic_edit.text().strip()
            
            cursor.execute("""
                update users
                set surname = ?, name = ?, patronymic = ?
                where id_user = ?
            """, (surname, name, patronymic, self.id_user))
            
            QMessageBox.information(
                    self,
                    "Успех",
                    f"Пользователь был изменен"
            )

            self.conn.commit()
            cursor.close()
            self.accept()
            
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось изменить пользователя: {str(e)}")

    def validate_data(self):
        errors = []
        
        if not self.name_edit.text().strip():
            errors.append("Введите имя")
        if not self.surname_edit.text().strip():
            errors.append("Введите фамилию")
        if not self.patronymic_edit.text().strip():
            errors.append("Введите отчество")
        
        if errors:
            QMessageBox.warning(self, "Ошибка валидации", "\n".join(errors))
            return False
        
        return True
