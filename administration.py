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
        self.button_stats.clicked.connect(self.show_stats)
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
        self.stats()

        self.show_users()

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

        self.users_text = QLineEdit()
        self.users_text.setPlaceholderText("Начните вводить ФИО пользователя")
        self.users_text.setFixedSize(300, 30)
        self.users_text.setStyleSheet("""
            border-radius: 5px;
            border: 2px solid #3498db;
            padding: 5px;
            font-family: roboto;
            font-size: 12;
        """)
        self.users_text.textChanged.connect(self.filter_users)
        users_layout.addWidget(self.users_text, alignment=Qt.AlignCenter)

        # таблица для вывода пользователей
        self.users_table = QTableWidget()
        self.users_table.setFixedSize(600, 370)
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
        users_layout.addStretch(1)

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

    def filter_users(self):
        try:
            cursor = self.conn.cursor()
            user_fio = self.users_text.text()
            query = (f"""
                select 
                    u.id_user,
                    u.surname,
                    u.name,
                    u.patronymic,
                    r.title as role_name
                from users u
                inner join role r on u.id_role = r.id_role
                where u.is_active = 1 and u.id_role < 3
                and (u.surname like '%{user_fio}%' or u.name like '%{user_fio}%'
                or u.patronymic like '%{user_fio}%')
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

    def show_stats(self): # успеваемость
        self.clear_content_layout()

        self.content_layout_v.addWidget(self.stats_widget)

        self.load_groups_for_stats()

    def stats(self): # элементы для успеваемости
        self.stats_widget = QWidget()
        stats_layout = QVBoxLayout()
        self.stats_widget.setLayout(stats_layout)
        self.type_date = False

        stats_label = QLabel("Успеваемость:")
        stats_label.setAlignment(Qt.AlignLeft)
        stats_label.setStyleSheet("""
            font-size: 22px;
            font-weight: bold;
            font-family: Roboto;
            color: #333;
            margin-top: 20px;
            margin-bottom: 10px;
        """)
        stats_layout.addWidget(stats_label)
        
        top_layout = QHBoxLayout() # для строки поиска

        self.stats_text = QLineEdit()
        self.stats_text.setPlaceholderText("Начните вводить ФИО пользователя")
        self.stats_text.setFixedSize(300, 30)
        self.stats_text.setStyleSheet("""
            border-radius: 5px;
            border: 2px solid #3498db;
            padding: 5px;
            font-family: roboto;
            font-size: 12;
        """)
        if self.load_stats:
            self.stats_text.textChanged.connect(self.filter_stats)
        if self.load_stats_without_date:
            self.stats_text.textChanged.connect(self.filter_stats_without_date)
        top_layout.addWidget(self.stats_text, alignment=Qt.AlignCenter)
        
        stats_layout.addLayout(top_layout)
        
        # для таблицы
        self.stats_table = QTableWidget()
        self.stats_table.setFixedSize(600, 360)
        self.stats_table.setColumnCount(5)
        self.stats_table.setHorizontalHeaderLabels(["Предмет", "ФИО", "Статус посещаемости", "Оценка", "Тип оценки"])
        self.stats_table.horizontalHeader().setStretchLastSection(True)
        self.stats_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.stats_table.setSelectionMode(QTableWidget.SingleSelection)
        self.stats_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.stats_table.itemSelectionChanged.connect(self.on_stats_selected)
        self.stats_table.setStyleSheet("""
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
        header = self.stats_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Fixed)  # предмет
        header.resizeSection(0, 100)
        header.setSectionResizeMode(1, QHeaderView.Fixed)  # фио
        header.resizeSection(1, 150)
        header.setSectionResizeMode(2, QHeaderView.Fixed) # статус посещения
        header.resizeSection(2, 140)
        header.setSectionResizeMode(3, QHeaderView.Fixed) # оценка
        header.resizeSection(3, 70)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # тип оценки
        stats_layout.addWidget(self.stats_table)
        stats_layout.addStretch(1)

        # для выбора даты, типа статуса посещения и кнопки добавления 
        bottom_layout = QHBoxLayout()
        stats_layout.addLayout(bottom_layout)
        group_layout = QVBoxLayout() # область для группы
        bottom_layout.addLayout(group_layout)
        date_layout = QVBoxLayout() # область для даты
        bottom_layout.addLayout(date_layout)

        group_label = QLabel("Группа:")
        group_label.setStyleSheet("font-family: Roboto; color: #333;")
        group_layout.addWidget(group_label, alignment=Qt.AlignLeft)
        
        self.stats_group_combo = QComboBox()
        self.stats_group_combo.addItems(["Выберите группу"])
        self.stats_group_combo.setFixedSize(150, 30)
        self.stats_group_combo.setStyleSheet("""
            border-radius: 5px;
            border: 1px solid #ccc;
            color: #333;
            padding: 5px;
            font-family: Roboto;
        """)
        self.stats_group_combo.currentIndexChanged.connect(self.load_stats)
        group_layout.addWidget(self.stats_group_combo, alignment=Qt.AlignLeft)
        group_layout.addSpacing(8)

        date_label = QLabel("Дата занятия:")
        date_label.setStyleSheet("font-family: Roboto; color: #333;")
        date_layout.addWidget(date_label, alignment=Qt.AlignLeft)
        
        self.stats_date = QDateEdit()
        self.stats_date.setFixedSize(120, 30)
        self.stats_date.setCalendarPopup(True)
        self.stats_date.setDate(QDate.currentDate())
        self.stats_date.setStyleSheet("""
            border-radius: 5px;
            border: 1px solid #ccc;
            color: #333;
            padding: 5px;
            font-family: Roboto;
        """)
        self.stats_date.dateChanged.connect(self.load_stats)
        date_layout.addWidget(self.stats_date, alignment=Qt.AlignLeft)
        date_layout.addSpacing(8)

        button_layout = QVBoxLayout() # для кнопки даты
        bottom_layout.addLayout(button_layout)
        button_layout.addSpacing(10)

        self.type_date_button = QPushButton("С учетом даты")
        self.type_date_button.setFixedSize(150, 35)
        self.type_date_button.setStyleSheet("""
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
        self.type_date_button.clicked.connect(self.stats_without_date)
        button_layout.addWidget(self.type_date_button, alignment=Qt.AlignLeft)

        bottom_layout.addStretch(1)

        self.check_stats = QPushButton()
        self.check_stats.setText("Просмотреть\nсредний балл")
        self.check_stats.setFixedSize(130, 55)
        self.check_stats.setStyleSheet("""
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
            QPushButton:disabled {
                background-color: #95a5a6;
            }
        """)
        self.check_stats.setEnabled(False)
        self.check_stats.clicked.connect(self.check_user_stats)
        bottom_layout.addWidget(self.check_stats)

        self.selected_student_id = None
        self.selected_student_fio = None

    def load_stats(self): # загрузка успеваемости
        try:
            selected_group_id = self.stats_group_combo.currentData()
            stats_date = self.stats_date.date()
            stats_date_str = stats_date.toString("yyyy-MM-dd")
                
            cursor = self.conn.cursor()
            query = """
                select 
                    u.id_user,
                    s.subject_name,
                    u.surname + ' ' + u.name + ' ' + u.patronymic as fio,
                    isnull(t_a.title, '') as attendance_status,
                    isnull(g.grade, '') as grade,
                    isnull(t_g.title, '') as type_grade
                from [subject] s
                inner join lesson l on l.id_subject = s.id_subject
                inner join class c on c.id_class = l.id_class
                inner join name_class n_c on n_c.id_name_class = c.id_name_class
                inner join users u on u.id_user = c.id_user
                inner join attendance a on a.id_lesson = l.id_lesson
                inner join type_attendance t_a on t_a.id_type_att = a.id_type_att
                inner join grade g on g.id_lesson = l.id_lesson
                inner join type_grade t_g on t_g.id_type_gr = g.id_type_gr
                where c.id_class = ? and l.date = ?
                group by u.id_user, s.subject_name, u.surname, u.[name], u.patronymic, 
                    t_a.title, g.grade, t_g.title
                order by s.subject_name, u.surname, u.[name], u.patronymic
            """
            cursor.execute(query, (selected_group_id, stats_date_str))
            stats_data = cursor.fetchall()
            
            # вывод в таблице
            self.stats_table.setRowCount(len(stats_data))
            
            for row, record in enumerate(stats_data):
                id_user = record[0]
                subject_name = record[1]
                fio = record[2]
                attendance_status = record[3]
                grade = str(record[4])
                type_grade = record[5]
                
                # предмет
                subject_item = QTableWidgetItem(subject_name)
                subject_item.setData(Qt.UserRole, {'id_user': id_user, 'fio': fio})
                subject_item.setFlags(subject_item.flags() & ~Qt.ItemIsEditable)
                subject_item.setTextAlignment(Qt.AlignCenter)
                self.stats_table.setItem(row, 0, subject_item)
                
                # фио
                fio_item = QTableWidgetItem(fio)
                fio_item.setData(Qt.UserRole, {'id_user': id_user, 'fio': fio})
                fio_item.setFlags(fio_item.flags() & ~Qt.ItemIsEditable)
                fio_item.setTextAlignment(Qt.AlignCenter)
                self.stats_table.setItem(row, 1, fio_item)
                
                # статус посещаемости
                status_item = QTableWidgetItem(attendance_status)
                status_item.setData(Qt.UserRole, {'id_user': id_user, 'fio': fio})
                status_item.setFlags(status_item.flags() & ~Qt.ItemIsEditable)
                status_item.setTextAlignment(Qt.AlignCenter)
                
                # цвет статуса
                if attendance_status == 'Присутствовал':
                    status_item.setForeground(QColor("#27ae60"))
                elif attendance_status == 'Отсутствовал':
                    status_item.setForeground(QColor("#e74c3c"))
                elif attendance_status == 'Уважительная причина':
                    status_item.setForeground(QColor("#f39c12"))
                    
                self.stats_table.setItem(row, 2, status_item)

                # оценка
                grade_item = QTableWidgetItem(grade)
                grade_item.setData(Qt.UserRole, {'id_user': id_user, 'fio': fio})
                grade_item.setFlags(grade_item.flags() & ~Qt.ItemIsEditable)
                grade_item.setTextAlignment(Qt.AlignCenter)

                # цвет оценки
                grade_int = int(grade)
                if grade_int >= 4:
                    grade_item.setForeground(QColor("#27ae60"))  # зеленый
                elif grade_int == 3:
                    grade_item.setForeground(QColor("#f39c12"))  # оранжевый
                elif grade_int <= 2:
                    grade_item.setForeground(QColor("#e74c3c"))  # красный
                
                self.stats_table.setItem(row, 3, grade_item)

                # тип оценки
                type_gr_item = QTableWidgetItem(type_grade)
                type_gr_item.setData(Qt.UserRole, {'id_user': id_user, 'fio': fio})
                type_gr_item.setFlags(type_gr_item.flags() & ~Qt.ItemIsEditable)
                type_gr_item.setTextAlignment(Qt.AlignCenter)
                self.stats_table.setItem(row, 4, type_gr_item)
            
            cursor.close()
            
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить данные о посещаемости: {str(e)}")
            self.stats_table.setRowCount(0)

    def filter_stats(self): # фильтр успеваемости
        try:
            selected_group_id = self.stats_group_combo.currentData()
            stats_date = self.stats_date.date()
            stats_date_str = stats_date.toString("yyyy-MM-dd")
            user_fio = self.stats_text.text()
                
            cursor = self.conn.cursor()
            query = f"""
                select 
                    u.id_user,
                    s.subject_name,
                    u.surname + ' ' + u.name + ' ' + u.patronymic as fio,
                    isnull(t_a.title, '') as attendance_status,
                    isnull(g.grade, '') as grade,
                    isnull(t_g.title, '') as type_grade
                from [subject] s
                inner join lesson l on l.id_subject = s.id_subject
                inner join class c on c.id_class = l.id_class
                inner join name_class n_c on n_c.id_name_class = c.id_name_class
                inner join users u on u.id_user = c.id_user
                inner join attendance a on a.id_lesson = l.id_lesson
                inner join type_attendance t_a on t_a.id_type_att = a.id_type_att
                inner join grade g on g.id_lesson = l.id_lesson
                inner join type_grade t_g on t_g.id_type_gr = g.id_type_gr
                where c.id_class = ? and l.date = ?
                and (u.surname like '%{user_fio}%' or u.name like '%{user_fio}%'
                or u.patronymic like '%{user_fio}%')
                group by u.id_user, s.subject_name, u.surname, u.[name], u.patronymic, 
                    t_a.title, g.grade, t_g.title
                order by s.subject_name, u.surname, u.[name], u.patronymic
            """
            cursor.execute(query, (selected_group_id, stats_date_str))
            stats_data = cursor.fetchall()
            
            # вывод в таблице
            self.stats_table.setRowCount(len(stats_data))
            
            for row, record in enumerate(stats_data):
                id_user = record[0]
                subject_name = record[1]
                fio = record[2]
                attendance_status = record[3]
                grade = str(record[4])
                type_grade = record[5]
                
                # предмет
                subject_item = QTableWidgetItem(subject_name)
                subject_item.setData(Qt.UserRole, {'id_user': id_user, 'fio': fio})
                subject_item.setFlags(subject_item.flags() & ~Qt.ItemIsEditable)
                subject_item.setTextAlignment(Qt.AlignCenter)
                self.stats_table.setItem(row, 0, subject_item)
                
                # фио
                fio_item = QTableWidgetItem(fio)
                fio_item.setData(Qt.UserRole, {'id_user': id_user, 'fio': fio})
                fio_item.setFlags(fio_item.flags() & ~Qt.ItemIsEditable)
                fio_item.setTextAlignment(Qt.AlignCenter)
                self.stats_table.setItem(row, 1, fio_item)
                
                # статус посещаемости
                status_item = QTableWidgetItem(attendance_status)
                status_item.setData(Qt.UserRole, {'id_user': id_user, 'fio': fio})
                status_item.setFlags(status_item.flags() & ~Qt.ItemIsEditable)
                status_item.setTextAlignment(Qt.AlignCenter)
                
                # цвет статуса
                if attendance_status == 'Присутствовал':
                    status_item.setForeground(QColor("#27ae60"))
                elif attendance_status == 'Отсутствовал':
                    status_item.setForeground(QColor("#e74c3c"))
                elif attendance_status == 'Уважительная причина':
                    status_item.setForeground(QColor("#f39c12"))
                    
                self.stats_table.setItem(row, 2, status_item)

                # оценка
                grade_item = QTableWidgetItem(grade)
                grade_item.setData(Qt.UserRole, {'id_user': id_user, 'fio': fio})
                grade_item.setFlags(grade_item.flags() & ~Qt.ItemIsEditable)
                grade_item.setTextAlignment(Qt.AlignCenter)

                # цвет оценки
                grade_int = int(grade)
                if grade_int >= 4:
                    grade_item.setForeground(QColor("#27ae60"))  # зеленый
                elif grade_int == 3:
                    grade_item.setForeground(QColor("#f39c12"))  # оранжевый
                elif grade_int <= 2:
                    grade_item.setForeground(QColor("#e74c3c"))  # красный
                
                self.stats_table.setItem(row, 3, grade_item)

                # тип оценки
                type_gr_item = QTableWidgetItem(type_grade)
                type_gr_item.setData(Qt.UserRole, {'id_user': id_user, 'fio': fio})
                type_gr_item.setFlags(type_gr_item.flags() & ~Qt.ItemIsEditable)
                type_gr_item.setTextAlignment(Qt.AlignCenter)
                self.stats_table.setItem(row, 4, type_gr_item)
            
            cursor.close()
            
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить данные о посещаемости: {str(e)}")
            self.stats_table.setRowCount(0)

    def load_stats_without_date(self):
        try:
            selected_group_id = self.stats_group_combo.currentData()
                
            cursor = self.conn.cursor()
            query = """
                select 
                    u.id_user,
                    s.subject_name,
                    u.surname + ' ' + u.name + ' ' + u.patronymic as fio,
                    l.date,
                    isnull(t_a.title, '') as attendance_status,
                    isnull(g.grade, '') as grade,
                    isnull(t_g.title, '') as type_grade
                from [subject] s
                inner join lesson l on l.id_subject = s.id_subject
                inner join class c on c.id_class = l.id_class
                inner join name_class n_c on n_c.id_name_class = c.id_name_class
                inner join users u on u.id_user = c.id_user
                inner join attendance a on a.id_lesson = l.id_lesson
                inner join type_attendance t_a on t_a.id_type_att = a.id_type_att
                inner join grade g on g.id_lesson = l.id_lesson
                inner join type_grade t_g on t_g.id_type_gr = g.id_type_gr
                where c.id_class = ?
                group by u.id_user, s.subject_name, u.surname, u.[name], u.patronymic, 
                    l.date, t_a.title, g.grade, t_g.title
                order by s.subject_name, u.surname, u.[name], u.patronymic
            """
            cursor.execute(query, (selected_group_id))
            stats_data = cursor.fetchall()
            
            # вывод в таблице
            self.stats_table.setRowCount(len(stats_data))
            
            for row, record in enumerate(stats_data):
                id_user = record[0]
                subject_name = record[1]
                fio = record[2]
                date = record[3]
                formatted_date = date.strftime("%d.%m.%Y")
                attendance_status = record[4]
                grade = str(record[5])
                type_grade = record[6]
                
                # предмет
                subject_item = QTableWidgetItem(subject_name)
                subject_item.setData(Qt.UserRole, {'id_user': id_user, 'fio': fio})
                subject_item.setFlags(subject_item.flags() & ~Qt.ItemIsEditable)
                subject_item.setTextAlignment(Qt.AlignCenter)
                self.stats_table.setItem(row, 0, subject_item)
                
                # фио
                fio_item = QTableWidgetItem(fio)
                fio_item.setData(Qt.UserRole, {'id_user': id_user, 'fio': fio})
                fio_item.setFlags(fio_item.flags() & ~Qt.ItemIsEditable)
                fio_item.setTextAlignment(Qt.AlignCenter)
                self.stats_table.setItem(row, 1, fio_item)

                # дата урока
                date_item = QTableWidgetItem(formatted_date)
                date_item.setData(Qt.UserRole, {'id_user': id_user, 'fio': fio})
                date_item.setFlags(date_item.flags() & ~Qt.ItemIsEditable)
                date_item.setTextAlignment(Qt.AlignCenter)
                self.stats_table.setItem(row, 2, date_item)
                
                # статус посещаемости
                status_item = QTableWidgetItem(attendance_status)
                status_item.setData(Qt.UserRole, {'id_user': id_user, 'fio': fio})
                status_item.setFlags(status_item.flags() & ~Qt.ItemIsEditable)
                status_item.setTextAlignment(Qt.AlignCenter)
                
                # цвет статуса
                if attendance_status == 'Присутствовал':
                    status_item.setForeground(QColor("#27ae60"))
                elif attendance_status == 'Отсутствовал':
                    status_item.setForeground(QColor("#e74c3c"))
                elif attendance_status == 'Уважительная причина':
                    status_item.setForeground(QColor("#f39c12"))
                    
                self.stats_table.setItem(row, 3, status_item)

                # оценка
                grade_item = QTableWidgetItem(grade)
                grade_item.setData(Qt.UserRole, {'id_user': id_user, 'fio': fio})
                grade_item.setFlags(grade_item.flags() & ~Qt.ItemIsEditable)
                grade_item.setTextAlignment(Qt.AlignCenter)

                # цвет оценки
                grade_int = int(grade)
                if grade_int >= 4:
                    grade_item.setForeground(QColor("#27ae60"))  # зеленый
                elif grade_int == 3:
                    grade_item.setForeground(QColor("#f39c12"))  # оранжевый
                elif grade_int <= 2:
                    grade_item.setForeground(QColor("#e74c3c"))  # красный
                
                self.stats_table.setItem(row, 4, grade_item)

                # тип оценки
                type_gr_item = QTableWidgetItem(type_grade)
                type_gr_item.setData(Qt.UserRole, {'id_user': id_user, 'fio': fio})
                type_gr_item.setFlags(type_gr_item.flags() & ~Qt.ItemIsEditable)
                type_gr_item.setTextAlignment(Qt.AlignCenter)
                self.stats_table.setItem(row, 5, type_gr_item)
            
            cursor.close()
            
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить данные о посещаемости: {str(e)}")
            self.stats_table.setRowCount(0)

    def filter_stats_without_date(self):
        try:
            selected_group_id = self.stats_group_combo.currentData()
            user_fio = self.stats_text.text()
                
            cursor = self.conn.cursor()
            query = f"""
                select 
                    u.id_user,
                    s.subject_name,
                    u.surname + ' ' + u.name + ' ' + u.patronymic as fio,
                    l.date,
                    isnull(t_a.title, '') as attendance_status,
                    isnull(g.grade, '') as grade,
                    isnull(t_g.title, '') as type_grade
                from [subject] s
                inner join lesson l on l.id_subject = s.id_subject
                inner join class c on c.id_class = l.id_class
                inner join name_class n_c on n_c.id_name_class = c.id_name_class
                inner join users u on u.id_user = c.id_user
                inner join attendance a on a.id_lesson = l.id_lesson
                inner join type_attendance t_a on t_a.id_type_att = a.id_type_att
                inner join grade g on g.id_lesson = l.id_lesson
                inner join type_grade t_g on t_g.id_type_gr = g.id_type_gr
                where c.id_class = ?
                and (u.surname like '%{user_fio}%' or u.name like '%{user_fio}%'
                or u.patronymic like '%{user_fio}%')
                group by u.id_user, s.subject_name, u.surname, u.[name], u.patronymic, 
                    l.date, t_a.title, g.grade, t_g.title
                order by s.subject_name, u.surname, u.[name], u.patronymic
            """
            cursor.execute(query, (selected_group_id))
            stats_data = cursor.fetchall()
            
            # вывод в таблице
            self.stats_table.setRowCount(len(stats_data))
            
            for row, record in enumerate(stats_data):
                id_user = record[0]
                subject_name = record[1]
                fio = record[2]
                date = record[3]
                formatted_date = date.strftime("%d.%m.%Y")
                attendance_status = record[4]
                grade = str(record[5])
                type_grade = record[6]
                
                # предмет
                subject_item = QTableWidgetItem(subject_name)
                subject_item.setData(Qt.UserRole, {'id_user': id_user, 'fio': fio})
                subject_item.setFlags(subject_item.flags() & ~Qt.ItemIsEditable)
                subject_item.setTextAlignment(Qt.AlignCenter)
                self.stats_table.setItem(row, 0, subject_item)
                
                # фио
                fio_item = QTableWidgetItem(fio)
                fio_item.setData(Qt.UserRole, {'id_user': id_user, 'fio': fio})
                fio_item.setFlags(fio_item.flags() & ~Qt.ItemIsEditable)
                fio_item.setTextAlignment(Qt.AlignCenter)
                self.stats_table.setItem(row, 1, fio_item)

                # дата урока
                date_item = QTableWidgetItem(formatted_date)
                date_item.setData(Qt.UserRole, {'id_user': id_user, 'fio': fio})
                date_item.setFlags(date_item.flags() & ~Qt.ItemIsEditable)
                date_item.setTextAlignment(Qt.AlignCenter)
                self.stats_table.setItem(row, 2, date_item)
                
                # статус посещаемости
                status_item = QTableWidgetItem(attendance_status)
                status_item.setData(Qt.UserRole, {'id_user': id_user, 'fio': fio})
                status_item.setFlags(status_item.flags() & ~Qt.ItemIsEditable)
                status_item.setTextAlignment(Qt.AlignCenter)
                
                # цвет статуса
                if attendance_status == 'Присутствовал':
                    status_item.setForeground(QColor("#27ae60"))
                elif attendance_status == 'Отсутствовал':
                    status_item.setForeground(QColor("#e74c3c"))
                elif attendance_status == 'Уважительная причина':
                    status_item.setForeground(QColor("#f39c12"))
                    
                self.stats_table.setItem(row, 3, status_item)

                # оценка
                grade_item = QTableWidgetItem(grade)
                grade_item.setData(Qt.UserRole, {'id_user': id_user, 'fio': fio})
                grade_item.setFlags(grade_item.flags() & ~Qt.ItemIsEditable)
                grade_item.setTextAlignment(Qt.AlignCenter)

                # цвет оценки
                grade_int = int(grade)
                if grade_int >= 4:
                    grade_item.setForeground(QColor("#27ae60"))  # зеленый
                elif grade_int == 3:
                    grade_item.setForeground(QColor("#f39c12"))  # оранжевый
                elif grade_int <= 2:
                    grade_item.setForeground(QColor("#e74c3c"))  # красный
                
                self.stats_table.setItem(row, 4, grade_item)

                # тип оценки
                type_gr_item = QTableWidgetItem(type_grade)
                type_gr_item.setData(Qt.UserRole, {'id_user': id_user, 'fio': fio})
                type_gr_item.setFlags(type_gr_item.flags() & ~Qt.ItemIsEditable)
                type_gr_item.setTextAlignment(Qt.AlignCenter)
                self.stats_table.setItem(row, 5, type_gr_item)
            
            cursor.close()
            
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить данные о посещаемости: {str(e)}")
            self.stats_table.setRowCount(0)

    def stats_without_date(self):
        if self.type_date == False:
            self.type_date_button.setText("Без учета даты")
            self.type_date = True
            self.stats_date.setEnabled(False)

            self.stats_table.setColumnCount(6)
            self.stats_table.setHorizontalHeaderLabels(["Предмет", "ФИО", "Дата урока", "Статус посещаемости", "Оценка", "Тип оценки"])
            header = self.stats_table.horizontalHeader()
            header.setSectionResizeMode(0, QHeaderView.Fixed)  # предмет
            header.resizeSection(0, 100)
            header.setSectionResizeMode(1, QHeaderView.Fixed)  # фио
            header.resizeSection(1, 150)
            header.setSectionResizeMode(2, QHeaderView.Fixed)  # дата
            header.resizeSection(2, 100)
            header.setSectionResizeMode(3, QHeaderView.Fixed) # статус посещения
            header.resizeSection(3, 140)
            header.setSectionResizeMode(4, QHeaderView.Fixed) # оценка
            header.resizeSection(4, 70)
            header.setSectionResizeMode(5, QHeaderView.Fixed)  # тип оценки
            header.resizeSection(5, 150)

            self.load_stats_without_date()

        elif self.type_date == True:
            self.type_date_button.setText("С учетом даты")
            self.type_date = False
            self.stats_date.setEnabled(True)

            self.stats_table.setColumnCount(5)
            self.stats_table.setHorizontalHeaderLabels(["Предмет", "ФИО", "Статус посещаемости", "Оценка", "Тип оценки"])
            header = self.stats_table.horizontalHeader()
            header.setSectionResizeMode(0, QHeaderView.Fixed)  # предмет
            header.resizeSection(0, 100)
            header.setSectionResizeMode(1, QHeaderView.Fixed)  # фио
            header.resizeSection(1, 150)
            header.setSectionResizeMode(2, QHeaderView.Fixed) # статус посещения
            header.resizeSection(2, 140)
            header.setSectionResizeMode(3, QHeaderView.Fixed) # оценка
            header.resizeSection(3, 70)
            header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # тип оценки
            
            self.load_stats()

    def on_stats_selected(self): # выбор строки в таблице
        selected_items = self.stats_table.selectedItems()
        
        if selected_items:
            item = selected_items[0]
            item_data = item.data(Qt.UserRole)
            
            if item_data and 'id_user' in item_data and 'fio' in item_data:
                self.selected_student_id = item_data['id_user']
                self.selected_student_fio = item_data['fio']
                self.check_stats.setEnabled(True)
            else:
                self.selected_student_id = None
                self.selected_student_fio = None
                self.check_stats.setEnabled(False)
        else:
            self.selected_student_id = None
            self.selected_student_fio = None
            self.check_stats.setEnabled(False)

    def check_user_stats(self):
        try:
            dialog = QDialog(self)
            dialog.setWindowTitle(f"{self.selected_student_fio}")
            dialog.setFixedSize(300, 300)
            dialog.setWindowFlags(Qt.Dialog | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
            
            layout = QVBoxLayout()
            dialog.setLayout(layout)
            
            avg_grade_table = QTableWidget()
            avg_grade_table.setColumnCount(3)
            avg_grade_table.setHorizontalHeaderLabels(["Группа", "Предмет", "Средний балл"])
            avg_grade_table.horizontalHeader().setStretchLastSection(True)
            avg_grade_table.setSelectionBehavior(QTableWidget.SelectRows)
            avg_grade_table.setSelectionMode(QTableWidget.SingleSelection)
            avg_grade_table.setEditTriggers(QTableWidget.NoEditTriggers)
            avg_grade_table.setStyleSheet("""
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

            cursor = self.conn.cursor()
            
            grades_query = """
                select
                    convert(varchar, n_c.num) + n_c.letter as [group],
                    s.subject_name,
                    isnull(s_s.avg_grade, 'н/а') as avg_grade
                from subj_students s_s
                inner join users u on u.id_user = s_s.id_user
                inner join class c on c.id_user = u.id_user
                inner join name_class n_c on n_c.id_name_class = c.id_name_class
                inner join [subject] s on s.id_subject = s_s.id_subject
                where s_s.id_user = ?
                order by s.subject_name
            """
            cursor.execute(grades_query, (self.selected_student_id))
            grades_data = cursor.fetchall()
            
            cursor.close()
            
            avg_grade_table.setRowCount(len(grades_data))
            
            for row, record in enumerate(grades_data):
                group = record[0]
                subject = record[1]
                avg_grade = record[2]
                
                # группа
                group_name = QTableWidgetItem(group)
                group_name.setFlags(group_name.flags() & ~Qt.ItemIsEditable)
                group_name.setTextAlignment(Qt.AlignCenter)
                avg_grade_table.setItem(row, 0, group_name)
                
                # предмет
                subject_name = QTableWidgetItem(subject)
                subject_name.setFlags(subject_name.flags() & ~Qt.ItemIsEditable)
                subject_name.setTextAlignment(Qt.AlignCenter)
                avg_grade_table.setItem(row, 1, subject_name)
                
                # средний балл
                avg = QTableWidgetItem(f"{str(avg_grade)}")
                avg.setFlags(avg.flags() & ~Qt.ItemIsEditable)
                avg.setTextAlignment(Qt.AlignCenter)
                
                # цвет оценки
                if str(avg_grade) == "н/а" or float(avg_grade) <= 2:
                    avg.setForeground(QColor("#e74c3c"))  # красный
                elif float(avg_grade) == 3:
                    avg.setForeground(QColor("#f39c12"))  # оранжевый
                elif float(avg_grade) >= 4:
                    avg.setForeground(QColor("#27ae60"))  # зеленый
                
                avg_grade_table.setItem(row, 2, avg)
            
            avg_grade_table.resizeColumnsToContents()
            layout.addWidget(avg_grade_table)
            
            dialog.exec_()
            
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить оценки за тест: {str(e)}")

    def load_groups_for_stats(self): # выбор элемента для загрузки групп
        self.load_groups_into_combo(self.stats_group_combo) # в скобках указан элемент для подстановки

    def load_groups_into_combo(self, combo_box): # загрузка групп
        try:
            cursor = self.conn.cursor()
            
            query = """
                select distinct 
                    c.id_class,
                    nc.num,
                    nc.letter
                from schedule s
                inner join class c on s.id_class = c.id_class
                inner join name_class nc on c.id_name_class = nc.id_name_class
                order by nc.num, nc.letter
            """
            cursor.execute(query)
            groups_data = cursor.fetchall()
            
            combo_box.clear()
            
            if groups_data:
                combo_box.addItem("Выберите группу", None)
                for group in groups_data:
                    class_id = group[0]
                    class_num = group[1]
                    class_letter = group[2]
                    group_name = f"{class_num}{class_letter}"
                    combo_box.addItem(group_name, class_id)
            else:
                combo_box.addItem("Нет групп")
                combo_box.setEnabled(False)
                
            cursor.close()
            
        except Exception as e:
            combo_box.clear()
            combo_box.addItem(f"Ошибка загрузки: {str(e)}")
            combo_box.setEnabled(False)


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
