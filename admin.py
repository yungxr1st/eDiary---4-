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


class MainMenuAdmin(QMainWindow):
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

        # кнопки добавить/редактировать/удалить
        buttons_layout = QHBoxLayout()
        main_layout.addLayout(buttons_layout)
        buttons_layout.setSpacing(10)

        self.user_add_button = QPushButton("Добавить пользователя")
        self.user_add_button.setFixedSize(200, 40)
        self.user_add_button.setStyleSheet("""
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
        self.user_add_button.clicked.connect(self.open_add_user_dialog)
        buttons_layout.addWidget(self.user_add_button)

        self.user_edit_button = QPushButton("Редактировать пользователя")
        self.user_edit_button.setFixedSize(200, 40)
        self.user_edit_button.setStyleSheet("""
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
        self.user_edit_button.clicked.connect(self.open_edit_user_dialog)
        buttons_layout.addWidget(self.user_edit_button)

        self.user_delete_button = QPushButton("Удалить пользователя")
        self.user_delete_button.setFixedSize(200, 40)
        self.user_delete_button.setStyleSheet("""
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
        self.user_delete_button.clicked.connect(self.open_delete_user_dialog)
        buttons_layout.addWidget(self.user_delete_button)

        # таблица для вывода пользователей
        self.users_table = QTableWidget()
        self.users_table.setColumnCount(6)
        self.users_table.setHorizontalHeaderLabels([
            "Фамилия", "Имя", "Отчество", "Логин", "Роль", "Активен"
        ])
        self.users_table.horizontalHeader().setStretchLastSection(True)
        self.users_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.users_table.setSelectionMode(QTableWidget.SingleSelection)
        
        table_style = ("""
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
        self.users_table.setStyleSheet(table_style)
        
        # заголовки
        header = self.users_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)  # фамилия
        header.setSectionResizeMode(1, QHeaderView.Stretch)  # имя
        header.setSectionResizeMode(2, QHeaderView.Stretch)  # отчество
        header.setSectionResizeMode(3, QHeaderView.Stretch)  # логин
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # роль
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)  # активность
        
        main_layout.addWidget(self.users_table)

        stats_layout = QHBoxLayout()
        self.total_users_label = QLabel("Всего пользователей: 0")
        self.active_users_label = QLabel("Активных: 0")
        self.inactive_users_label = QLabel("Неактивных: 0")
        
        stats_style = "font-family: Roboto; color: #555; font-weight: bold; padding: 5px;"
        self.total_users_label.setStyleSheet(stats_style)
        self.active_users_label.setStyleSheet(stats_style)
        self.inactive_users_label.setStyleSheet(stats_style)
        
        stats_layout.addWidget(self.total_users_label)
        stats_layout.addWidget(self.active_users_label)
        stats_layout.addWidget(self.inactive_users_label)
        stats_layout.addStretch()
        
        main_layout.addLayout(stats_layout)

        bottom_layout = QHBoxLayout() # нижняя часть
        bottom_layout.addStretch(1)
        main_layout.addLayout(bottom_layout)

        self.group_subject_button = QPushButton("Группы и предметы") # кнопка группы и предметы
        self.group_subject_button.setFixedSize(250, 40)
        self.group_subject_button.setStyleSheet("""
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
        self.group_subject_button.clicked.connect(self.group_subject)
        bottom_layout.addWidget(self.group_subject_button)

        self.load_users()
        
        self.users_table.itemSelectionChanged.connect(self.update_buttons_state)

    def logout(self): # выход из учетки
        from main import (LoginWindow)
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()

    def group_subject(self): # открытие окна группы и предметы
        group_subject = GroupSubjectDialog(self, conn=self.conn)
        group_subject.exec_() == QDialog.Accepted

    def load_users(self): # загрузка пользователей
        try:
            cursor = self.conn.cursor()
            
            query = ("""
                select 
                    u.id_user,
                    u.surname,
                    u.name,
                    u.patronymic,
                    u.login,
                    r.title as role_name,
                    u.is_active
                from users u
                inner join role r on u.id_role = r.id_role
                order by u.surname, u.name
            """)
            
            cursor.execute(query)
            users_data = cursor.fetchall()
            
            self.users_table.setRowCount(len(users_data))
            
            total_users = 0
            active_users = 0
            inactive_users = 0
            
            for row, user in enumerate(users_data):
                user_id = user[0]
                surname = user[1]
                name = user[2]
                patronymic = user[3]
                login = user[4]
                role_name = user[5]
                is_active = bool(user[6])
                
                total_users += 1
                if is_active:
                    active_users += 1
                else:
                    inactive_users += 1
                
                items = [
                    QTableWidgetItem(surname if surname else ""),
                    QTableWidgetItem(name if name else ""),
                    QTableWidgetItem(patronymic if patronymic else ""),
                    QTableWidgetItem(login),
                    QTableWidgetItem(role_name),
                    QTableWidgetItem("Да" if is_active else "Нет")
                ]
                
                for col, item in enumerate(items):
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                    if col == 5:
                        item.setForeground(QColor("#27ae60") if is_active else QColor("#e74c3c"))
                        item.setTextAlignment(Qt.AlignCenter)
                    self.users_table.setItem(row, col, item)
            
            cursor.close()
            
            self.total_users_label.setText(f"Всего пользователей: {total_users}")
            self.active_users_label.setText(f"Активных: {active_users}")
            self.inactive_users_label.setText(f"Неактивных: {inactive_users}")
            
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить пользователей: {str(e)}")

    def update_buttons_state(self):
        selected_rows = self.users_table.selectionModel().selectedRows()
        has_selection = len(selected_rows) > 0
        
        self.user_edit_button.setEnabled(has_selection)
        self.user_delete_button.setEnabled(has_selection)

    def open_add_user_dialog(self): # добавление пользователя
        dialog = AddEditUserDialog(self, conn=self.conn)
        if dialog.exec_() == QDialog.Accepted:
            self.load_users()

    def open_edit_user_dialog(self): # редактирование пользователя
        selected_row = self.users_table.currentRow()
        if selected_row >= 0:
            login = self.users_table.item(selected_row, 3).text()
            dialog = AddEditUserDialog(self, login=login, conn=self.conn)
            if dialog.exec_() == QDialog.Accepted:
                self.load_users()

    def open_delete_user_dialog(self): # удаление пользователя
        selected_row = self.users_table.currentRow()
        if selected_row >= 0:
            login = self.users_table.item(selected_row, 3).text()
            user_name = f"{self.users_table.item(selected_row, 0).text()} {self.users_table.item(selected_row, 1).text()}"
            
            reply = QMessageBox.question(
                self,
                "Подтверждение удаления",
                f"Вы уверены, что хотите отключить пользователя:\n{user_name}?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                try:
                    cursor = self.conn.cursor()
                    cursor.execute("""
                        update users
                        set is_active = 0
                        where login = ?
                    """, (login,))
                    self.conn.commit()
                    cursor.close()
                    QMessageBox.information(self, "Успех", "Пользователь отключен")
                    self.load_users()
                except Exception as e:
                    QMessageBox.critical(self, "Ошибка", f"Не удалось отключить пользователя: {str(e)}")


class AddEditUserDialog(QDialog):
    def __init__(self, parent=None, user_id=None, login=None, conn=None):
        super().__init__(parent)
        self.user_id = user_id
        self.login = login
        self.conn = conn
        self.is_edit_mode = login is not None or user_id is not None

        self.setWindowTitle("Редактирование пользователя" if self.is_edit_mode else "Добавление пользователя")
        self.setFixedSize(350, 400)
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
        
        # логин
        login_label = QLabel("Логин:")
        login_label.setFont(QFont("Roboto", 10))

        self.login_edit = QLineEdit()
        self.login_edit.setFixedSize(250, 35)
        self.login_edit.setFont(QFont("Roboto", 10))
        self.login_edit.setStyleSheet("""
            border-radius: 5px;
            border: 2px solid #3498db;
            padding: 5px;
        """)
        form_layout.addRow(login_label, self.login_edit)
        
        # пароль
        password_label = QLabel("Пароль:")
        password_label.setFont(QFont("Roboto", 10))

        self.password_edit = QLineEdit()
        self.password_edit.setFixedSize(250, 35)
        self.password_edit.setFont(QFont("Roboto", 10))
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.password_edit.setStyleSheet("""
            border-radius: 5px;
            border: 2px solid #3498db;
            padding: 5px;
        """)
        form_layout.addRow(password_label, self.password_edit)
        
        # роль
        role_label = QLabel("Роль:")
        role_label.setFont(QFont("Roboto", 10))

        self.role_combo = QComboBox()
        self.role_combo.setFixedSize(250, 35)
        self.role_combo.setFont(QFont("Roboto", 10))
        self.role_combo.setStyleSheet("""
            border-radius: 5px;
            border: 2px solid #3498db;
            color: #333;
            padding: 5px;
        """)
        self.load_roles()
        form_layout.addRow(role_label, self.role_combo)
        
        self.active_checkbox = QCheckBox("Активный пользователь")
        self.active_checkbox.setFont(QFont("Roboto", 10))
        self.active_checkbox.setChecked(True)
        self.active_checkbox.setStyleSheet("font-family: Roboto;")
        form_layout.addRow("", self.active_checkbox)
        
        layout.addLayout(form_layout)
        
        buttons_layout = QHBoxLayout()
        
        self.save_button = QPushButton("Сохранить")
        self.save_button.setFixedSize(200, 40)
        self.save_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
                font-family: Roboto;
                font-weight: bold;
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
        
        if self.is_edit_mode: # для режима редактирования
            if self.login:
                self.load_user_data_by_login()
            else:
                self.load_user_data()

    def load_roles(self): # список ролей
        try:
            cursor = self.conn.cursor()
            cursor.execute("select id_role, title from role order by id_role")
            roles = cursor.fetchall()
            
            for role_id, role_name in roles:
                self.role_combo.addItem(role_name, role_id)
            
            cursor.close()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить роли: {str(e)}")

    def load_user_data(self): 
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                select surname, name, patronymic, login, id_role, is_active
                from users where id_user = ?
            """, (self.user_id,))
            
            user_data = cursor.fetchone()
            if user_data:
                self.surname_edit.setText(user_data[0] or "")
                self.name_edit.setText(user_data[1] or "")
                self.patronymic_edit.setText(user_data[2] or "")
                self.login_edit.setText(user_data[3] or "")
                
                role_id = user_data[4]
                for i in range(self.role_combo.count()):
                    if self.role_combo.itemData(i) == role_id:
                        self.role_combo.setCurrentIndex(i)
                        break
                
                self.active_checkbox.setChecked(bool(user_data[5]))
            
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
            login = self.login_edit.text().strip()
            role_id = self.role_combo.currentData()
            is_active = 1 if self.active_checkbox.isChecked() else 0
            
            if self.is_edit_mode:
                if self.password_edit.text():
                    password_hash = hashlib.sha256(self.password_edit.text().encode()).hexdigest()
                    cursor.execute("""
                        update users
                        set surname = ?, name = ?, patronymic = ?,
                            login = ?, password = ?, id_role = ?, is_active = ?
                        where id_user = ?
                    """, (surname, name, patronymic, login, password_hash, role_id, is_active, self.user_id))
                else:
                    cursor.execute("""
                        update users
                        set surname = ?, name = ?, patronymic = ?,
                            login = ?, id_role = ?, is_active = ?
                        where id_user = ?
                    """, (surname, name, patronymic, login, role_id, is_active, self.user_id))
            else:
                password = self.password_edit.text()
                if not password:
                    QMessageBox.warning(self, "Ошибка", "Укажите пароль")
                    return
                
                password_hash = hashlib.sha256(password.encode()).hexdigest()
                cursor.execute("""
                    insert into users (surname, name, patronymic, login, password, id_role, is_active)
                    values (?, ?, ?, ?, ?, ?, ?)
                """, (surname, name, patronymic, login, password_hash, role_id, is_active))
            
            self.conn.commit()
            cursor.close()
            self.accept()
            
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить пользователя: {str(e)}")

    def validate_data(self):
        errors = []
        
        if not self.name_edit.text().strip():
            errors.append("Введите имя")
        if not self.surname_edit.text().strip():
            errors.append("Введите фамилию")
        if not self.patronymic_edit.text().strip():
            errors.append("Введите отчество")
        if not self.login_edit.text().strip():
            errors.append("Введите логин")
        
        try:
            cursor = self.conn.cursor()
            query = "select count(*) from users where login = ?"
            params = [self.login_edit.text().strip()]
            
            if self.is_edit_mode:
                query += " AND id_user != ?"
                params.append(self.user_id)
            
            cursor.execute(query, params)
            count = cursor.fetchone()[0]
            if count > 0:
                errors.append("Пользователь с таким логином уже существует")
            cursor.close()
        except:
            pass
        
        if errors:
            QMessageBox.warning(self, "Ошибка валидации", "\n".join(errors))
            return False
        
        return True
    
    def load_user_data_by_login(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                select id_user, surname, name, patronymic, login, id_role, is_active
                from users where login = ?
            """, (self.login,))
            user_data = cursor.fetchone()
            
            if user_data:
                self.user_id = user_data[0]
                self.surname_edit.setText(user_data[1] or "")
                self.name_edit.setText(user_data[2] or "")
                self.patronymic_edit.setText(user_data[3] or "")
                self.login_edit.setText(user_data[4] or "")
                
                role_id = user_data[5]
                for i in range(self.role_combo.count()):
                    if self.role_combo.itemData(i) == role_id:
                        self.role_combo.setCurrentIndex(i)
                        break
                
                self.active_checkbox.setChecked(bool(user_data[6]))
            else:
                QMessageBox.warning(self, "Ошибка", "Пользователь не найден")
                self.reject()
                
            cursor.close()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить данные пользователя: {str(e)}")


class GroupSubjectDialog(QDialog): # окно группы и предметы
    def __init__(self, parent = None, conn = None):
        super().__init__(parent)
        self.conn = conn
        self.current_mode = "groups" # для переключения между группами и предметами
        self.setWindowTitle("Группы и предметы")
        self.setFixedSize(600, 500)
        self.setModal(True)
        self.setWindowFlags(Qt.Dialog | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        main_layout_h = QHBoxLayout() # для горизонтальной расстановки элементов
        main_layout.addLayout(main_layout_h)

        button_layout = QVBoxLayout() # область для кнопок
        main_layout_h.addLayout(button_layout)
        button_layout.addStretch(1)

        self.group_button = QPushButton("Группы")
        self.group_button.setFixedSize(150, 40)
        self.group_button.setStyleSheet("""
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
        self.group_button.setCheckable(True)
        self.group_button.setChecked(True)
        self.group_button.clicked.connect(self.group)
        button_layout.addWidget(self.group_button, alignment=Qt.AlignLeft)

        self.subject_button = QPushButton("Предметы")
        self.subject_button.setFixedSize(150, 40)
        self.subject_button.setStyleSheet("""
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
        self.subject_button.setCheckable(True)
        self.subject_button.clicked.connect(self.subject)
        button_layout.addWidget(self.subject_button, alignment=Qt.AlignLeft)
        button_layout.addStretch(1)

        self.content_layout = QVBoxLayout() # область для таблицы и строк для записи
        main_layout_h.addLayout(self.content_layout)
        self.content_layout.addStretch(1)

        # таблица для вывода групп и предметов
        self.group_subject_table = QTableWidget()
        self.group_subject_table.setFixedSize(300, 250)
        self.group_subject_table.setColumnCount(2)
        self.group_subject_table.setHorizontalHeaderLabels([
            "Цифра группы", "Буква группы"
        ])
        self.group_subject_table.horizontalHeader().setStretchLastSection(True)
        self.group_subject_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.group_subject_table.setSelectionMode(QTableWidget.SingleSelection)
        
        table_style = ("""
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
        self.group_subject_table.setStyleSheet(table_style)
        self.content_layout.addWidget(self.group_subject_table, alignment=Qt.AlignCenter)
        
        # заголовки
        header = self.group_subject_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)  # цифра группы
        header.setSectionResizeMode(1, QHeaderView.Stretch)  # буква группы

        # область для виджетов посередине
        input_layout = QVBoxLayout()
        input_layout.setAlignment(Qt.AlignCenter)

        # виджет для групп, чтобы заменять поля для групп на поля для предметов
        self.group_input_widget = QWidget()
        group_input_layout = QVBoxLayout()
        group_input_layout.setAlignment(Qt.AlignCenter)
        self.group_input_widget.setLayout(group_input_layout)

        # строка для номера группы
        groupNum_label = QLabel("Номер группы")
        groupNum_label.setFont(QFont("Roboto", 10))
        group_input_layout.addWidget(groupNum_label)

        self.groupNum_line = QLineEdit()
        self.groupNum_line.setFixedSize(150, 30)
        self.groupNum_line.setFont(QFont("Roboto", 10))
        self.groupNum_line.setStyleSheet("""
            border-radius: 5px;
            border: 2px solid #3498db;
            color: #333;
            padding: 5px;
        """)
        group_input_layout.addWidget(self.groupNum_line)
        group_input_layout.addSpacing(10)

        # строка для буквы группы
        groupLet_label = QLabel("Буква группы")
        groupLet_label.setFont(QFont("Roboto", 10))
        group_input_layout.addWidget(groupLet_label)

        self.groupLet_line = QLineEdit()
        self.groupLet_line.setFixedSize(150, 30)
        self.groupLet_line.setFont(QFont("Roboto", 10))
        self.groupLet_line.setStyleSheet("""
            border-radius: 5px;
            border: 2px solid #3498db;
            color: #333;
            padding: 5px;
        """)
        group_input_layout.addWidget(self.groupLet_line)

        # виджет для предметов, чтобы заменять поля для предметов на поля для групп
        self.subject_input_widget = QWidget()
        self.subject_input_widget.setVisible(False)
        subject_input_layout = QVBoxLayout()
        subject_input_layout.setAlignment(Qt.AlignCenter)
        self.subject_input_widget.setLayout(subject_input_layout)

        # строка для названия предмета
        subject_label = QLabel("Название предмета")
        subject_label.setFont(QFont("Roboto", 10))
        subject_input_layout.addSpacing(38)
        subject_input_layout.addWidget(subject_label)

        self.subject_line = QLineEdit()
        self.subject_line.setFixedSize(150, 30)
        self.subject_line.setFont(QFont("Roboto", 10))
        self.subject_line.setStyleSheet("""
            border-radius: 5px;
            border: 2px solid #3498db;
            color: #333;
            padding: 5px;
        """)
        subject_input_layout.addWidget(self.subject_line)

        subject_input_layout.addSpacing(30)

        input_layout.addWidget(self.group_input_widget)
        input_layout.addWidget(self.subject_input_widget)
        self.content_layout.addLayout(input_layout)
        self.content_layout.addSpacing(10)

        content_button = QHBoxLayout() # область для добавления кнопок в области контента
        self.content_layout.addLayout(content_button)
        content_button.addStretch(1)

        self.add_button = QPushButton("Добавить группу")
        self.add_button.setFixedSize(150, 40)
        self.add_button.setStyleSheet("""
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
        self.add_button.clicked.connect(self.add_item)
        content_button.addWidget(self.add_button, alignment=Qt.AlignCenter)

        self.delete_button = QPushButton("Удалить группу")
        self.delete_button.setFixedSize(150, 40)
        self.delete_button.setStyleSheet("""
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
        self.delete_button.clicked.connect(self.delete_item)
        content_button.addWidget(self.delete_button, alignment=Qt.AlignCenter)
        content_button.addStretch(1)

        self.group()
        self.group_subject_table.itemSelectionChanged.connect(self.update_buttons_state)
        self.update_buttons_state()

    def group(self): # вывод групп
        self.current_mode = "groups"
        self.group_button.setChecked(True)
        self.subject_button.setChecked(False)
        self.group_input_widget.setVisible(True)
        self.subject_input_widget.setVisible(False)
        self.add_button.setText("Добавить группу")
        self.delete_button.setText("Удалить группу")
        self.group_subject_table.clear()
        self.group_subject_table.setColumnCount(2)
        self.group_subject_table.setHorizontalHeaderLabels(["Цифра группы", "Буква группы"])
        self.load_groups()

    def subject(self): # вывод предметов
        self.current_mode = "subjects"
        self.group_button.setChecked(False)
        self.subject_button.setChecked(True)
        self.group_input_widget.setVisible(False)
        self.subject_input_widget.setVisible(True)
        self.add_button.setText("Добавить предмет")
        self.delete_button.setText("Удалить предмет")
        self.group_subject_table.clear()
        self.group_subject_table.setColumnCount(1)
        self.group_subject_table.setHorizontalHeaderLabels(["Название предмета"])
        self.load_subjects()

    def load_groups(self): # загрузка групп из бд
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                select id_name_class, num, letter 
                from name_class 
                order by num, letter
            """)
            groups_data = cursor.fetchall()
            
            self.group_subject_table.setRowCount(len(groups_data))
            
            for row, group in enumerate(groups_data):
                id_name_class = group[0]
                num = group[1]
                letter = group[2]
                
                # номер группы
                num_item = QTableWidgetItem(str(num))
                num_item.setData(Qt.UserRole, id_name_class)
                num_item.setFlags(num_item.flags() & ~Qt.ItemIsEditable)
                self.group_subject_table.setItem(row, 0, num_item)
                
                # буква группы
                letter_item = QTableWidgetItem(letter)
                letter_item.setFlags(letter_item.flags() & ~Qt.ItemIsEditable)
                self.group_subject_table.setItem(row, 1, letter_item)
            
            cursor.close()
            
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить группы: {str(e)}")

    def load_subjects(self): # загрузка предметов из бд
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                select subject_name 
                from subject 
                order by subject_name
            """)
            subjects_data = cursor.fetchall()
            
            self.group_subject_table.setRowCount(len(subjects_data))
            
            for row, subject in enumerate(subjects_data):
                subject_name = subject[0]
                
                # название предмета
                name_item = QTableWidgetItem(subject_name)
                name_item.setFlags(name_item.flags() & ~Qt.ItemIsEditable)
                self.group_subject_table.setItem(row, 0, name_item)
            
            cursor.close()
            
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить предметы: {str(e)}")

    def add_item(self): # добавление предмета (группа или предмет)
        if self.current_mode == "groups":
            self.add_group()
        else:
            self.add_subject()

    def add_group(self): # добавление группы
        num_text = self.groupNum_line.text().strip()
        letter_text = self.groupLet_line.text().strip().upper()
        
        if not num_text:
            QMessageBox.warning(self, "Предупреждение", "Введите номер группы")
            return
        
        if not num_text.isdigit():
            QMessageBox.warning(self, "Предупреждение", "Номер группы должен быть числом")
            return
        
        if not letter_text or len(letter_text) != 1:
            QMessageBox.warning(self, "Предупреждение", "Введите одну букву для группы")
            return
        
        if not letter_text.isalpha():
            QMessageBox.warning(self, "Предупреждение", "Буква группы должна быть буквой алфавита")
            return
        
        num = int(num_text)
        letter = letter_text
        
        # проверка существующих групп
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                select count(*) from name_class 
                where num = ? and letter = ?
            """, (num, letter))
            
            if cursor.fetchone()[0] > 0:
                QMessageBox.warning(self, "Предупреждение", "Такая группа уже существует")
                cursor.close()
                return
            
            # добавление группы
            cursor.execute("""
                insert into name_class (num, letter) 
                values (?, ?)
            """, (num, letter))
            
            self.conn.commit()
            cursor.close()
            
            QMessageBox.information(self, "Успех", "Группа успешно добавлена")
            
            # очистка таблицы
            self.groupNum_line.clear()
            self.groupLet_line.clear()
            self.load_groups()
            
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить группу: {str(e)}")

    def add_subject(self): # добавление предмета
        subject_name = self.subject_line.text().strip()
        
        if not subject_name:
            QMessageBox.warning(self, "Предупреждение", "Введите название предмета")
            return
        
        # проверка существующих предметов
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                select count(*) from subject 
                where subject_name = ?
            """, (subject_name,))
            
            if cursor.fetchone()[0] > 0:
                QMessageBox.warning(self, "Предупреждение", "Такой предмет уже существует")
                cursor.close()
                return
            
            # добавление предмета
            cursor.execute("""
                insert into subject (subject_name) 
                values (?)
            """, (subject_name,))
            
            self.conn.commit()
            cursor.close()
            
            QMessageBox.information(self, "Успех", "Предмет успешно добавлен")
            
            # очистка таблицы
            self.subject_line.clear()
            self.load_subjects()
            
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить предмет: {str(e)}")

    def delete_item(self): # удаление предмета (группа или предмет)
        selected_row = self.group_subject_table.currentRow()
        
        if selected_row < 0:
            QMessageBox.warning(self, "Предупреждение", "Выберите элемент для удаления")
            return
        
        if self.current_mode == "groups":
            self.delete_group(selected_row)
        else:
            self.delete_subject(selected_row)

    def delete_group(self, row): # удаление группы
        id_name_class_item = self.group_subject_table.item(row, 0)
        if not id_name_class_item:
            return
        
        id_name_class = id_name_class_item.data(Qt.UserRole)
        num = self.group_subject_table.item(row, 0).text()
        letter = self.group_subject_table.item(row, 1).text()
        
        reply = QMessageBox.question(
            self,
            "Подтверждение удаления",
            f"Вы уверены, что хотите удалить группу {num}{letter}?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.No:
            return
        
        try:
            cursor = self.conn.cursor()
            
            # проверка на использование группы в других таблицах
            cursor.execute("""
                select count(*) from class 
                where id_name_class = ?
            """, (id_name_class,))
            
            if cursor.fetchone()[0] > 0:
                QMessageBox.warning(
                    self,
                    "Ошибка",
                    "Невозможно удалить группу, так как она используется в других таблицах."
                )
                cursor.close()
                return
            
            # удаление группы
            cursor.execute("""
                delete from name_class 
                where id_name_class = ?
            """, (id_name_class,))
            
            self.conn.commit()
            cursor.close()
            
            QMessageBox.information(self, "Успех", "Группа успешно удалена")
            self.load_groups()
            
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось удалить группу: {str(e)}")

    def delete_subject(self, row): # удаление предмета
        id_subject_item = self.group_subject_table.item(row, 0)
        if not id_subject_item:
            return
        
        id_subject = id_subject_item.data(Qt.UserRole)
        subject_name = self.group_subject_table.item(row, 1).text()
        
        reply = QMessageBox.question(
            self,
            "Подтверждение удаления",
            f"Вы уверены, что хотите удалить предмет '{subject_name}'?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.No:
            return
        
        try:
            cursor = self.conn.cursor()
            
            # проверка на использование предмета в других таблицах
            cursor.execute("""
                select count(*) from schedule 
                where id_subject = ?
            """, (id_subject,))
            
            if cursor.fetchone()[0] > 0:
                QMessageBox.warning(
                    self,
                    "Ошибка",
                    "Невозможно удалить предмет, так как он используется в других таблицах."
                )
                cursor.close()
                return
            
            # удаление предмета
            cursor.execute("""
                delete from subject 
                where id_subject = ?
            """, (id_subject,))
            
            self.conn.commit()
            cursor.close()
            
            QMessageBox.information(self, "Успех", "Предмет успешно удален")
            self.load_subjects()
            
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось удалить предмет: {str(e)}")

    def update_buttons_state(self): # обновление кнопок
        has_selection = self.group_subject_table.currentRow() >= 0
        self.delete_button.setEnabled(has_selection)