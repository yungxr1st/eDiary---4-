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
        self.button_schedule.clicked.connect(self.show_schedule)
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
        self.button_groups_subjects.clicked.connect(self.show_groups_subjects)
        group_button_layout.addWidget(self.button_groups_subjects, alignment=Qt.AlignLeft)

        group_button_layout.addStretch(2)

        self.users()
        self.stats()
        self.groups_subjects()
        self.schedule()

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
        self.users_text.setMaxLength(92)
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
        self.stats_text.setMaxLength(92)
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
                    isnull(t_a.title, ' ') as attendance_status,
                    isnull(g.grade, ' ') as grade,
                    isnull(t_g.title, ' ') as type_grade
                from lesson l
                inner join grade g on g.id_lesson = l.id_lesson
                inner join type_grade t_g on t_g.id_type_gr = g.id_type_gr
                inner join attendance a on a.id_lesson = l.id_lesson
                inner join type_attendance t_a on t_a.id_type_att = a.id_type_att
                inner join name_class n_c on n_c.id_name_class = l.id_name_class
                inner join class c on c.id_name_class = n_c.id_name_class
                inner join users u on u.id_user = c.id_user
                inner join subject s on s.id_subject = l.id_subject
                where n_c.id_name_class = ? and l.date = ?
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
                if grade == '0':
                    grade = ''
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
                if grade != '':
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
                    isnull(t_a.title, ' ') as attendance_status,
                    isnull(g.grade, ' ') as grade,
                    isnull(t_g.title, ' ') as type_grade
                from lesson l
                inner join grade g on g.id_lesson = l.id_lesson
                inner join type_grade t_g on t_g.id_type_gr = g.id_type_gr
                inner join attendance a on a.id_lesson = l.id_lesson
                inner join type_attendance t_a on t_a.id_type_att = a.id_type_att
                inner join name_class n_c on n_c.id_name_class = l.id_name_class
                inner join class c on c.id_name_class = n_c.id_name_class
                inner join users u on u.id_user = c.id_user
                inner join subject s on s.id_subject = l.id_subject
                where n_c.id_name_class = ? and l.date = ?
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
                if grade == '0':
                    grade = ''
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
                if grade != '':
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
                    isnull(t_a.title, ' ') as attendance_status,
                    isnull(g.grade, ' ') as grade,
                    isnull(t_g.title, ' ') as type_grade
                from lesson l
                inner join grade g on g.id_lesson = l.id_lesson
                inner join type_grade t_g on t_g.id_type_gr = g.id_type_gr
                inner join attendance a on a.id_lesson = l.id_lesson
                inner join type_attendance t_a on t_a.id_type_att = a.id_type_att
                inner join name_class n_c on n_c.id_name_class = l.id_name_class
                inner join class c on c.id_name_class = n_c.id_name_class
                inner join users u on u.id_user = c.id_user
                inner join subject s on s.id_subject = l.id_subject
                where n_c.id_name_class = ?
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
                if grade == '0':
                    grade = ''
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
                if grade != '':
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
                    isnull(t_a.title, ' ') as attendance_status,
                    isnull(g.grade, ' ') as grade,
                    isnull(t_g.title, ' ') as type_grade
                from lesson l
                inner join grade g on g.id_lesson = l.id_lesson
                inner join type_grade t_g on t_g.id_type_gr = g.id_type_gr
                inner join attendance a on a.id_lesson = l.id_lesson
                inner join type_attendance t_a on t_a.id_type_att = a.id_type_att
                inner join name_class n_c on n_c.id_name_class = l.id_name_class
                inner join class c on c.id_name_class = n_c.id_name_class
                inner join users u on u.id_user = c.id_user
                inner join subject s on s.id_subject = l.id_subject
                where n_c.id_name_class = ?
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
                if grade == '0':
                    grade = ''
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
                if grade != '':
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
                from subj_teachers s_t
                inner join subject s on s.id_subject = s_t.id_subject
                inner join name_class n_c on n_c.id_name_class = s_t.id_name_class
                inner join class c on c.id_name_class = n_c.id_name_class
                inner join users u on u.id_user = c.id_user
                inner join subj_students s_s on s_s.id_subject = s.id_subject
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
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить средний балл ученика: {str(e)}")

    def load_groups_for_stats(self): # выбор элемента для загрузки групп
        self.load_groups_into_combo(self.stats_group_combo) # в скобках указан элемент для подстановки

    def load_groups_into_combo(self, combo_box): # загрузка групп
        try:
            cursor = self.conn.cursor()
            
            query = """
                select 
                    n_c.id_name_class,
                    convert(varchar, n_c.num) + n_c.letter,
                    s.subject_name
                from name_class n_c
                inner join subj_teachers s_t on s_t.id_name_class = n_c.id_name_class
                inner join subject s on s.id_subject = s_t.id_subject
                order by n_c.num, n_c.letter
            """
            cursor.execute(query)
            groups_data = cursor.fetchall()
            
            combo_box.clear()
            
            if groups_data:
                combo_box.addItem("Выберите группу", None)
                for group in groups_data:
                    class_id = group[0]
                    num_letter = group[1]
                    group_name = f"{num_letter}"
                    combo_box.addItem(group_name, class_id)
            else:
                combo_box.addItem("Нет групп")
                combo_box.setEnabled(False)
                
            cursor.close()
            
        except Exception as e:
            combo_box.clear()
            combo_box.addItem(f"Ошибка загрузки: {str(e)}")
            combo_box.setEnabled(False)

    def show_groups_subjects(self):
        self.clear_content_layout()

        self.content_layout_v.addWidget(self.groups_subjects_widget)

        self.load_groups()
        self.load_subjects()
        self.load_teachers_for_groups()
        self.load_groups_for_groups()
        self.load_groups_for_subjects()
        self.load_subjects_into_combo()

    def groups_subjects(self):
        self.groups_subjects_widget = QWidget()
        groups_subjects_layout = QVBoxLayout()
        self.groups_subjects_widget.setLayout(groups_subjects_layout)
        self.groups_subjects_tab = QTabWidget() # вкладки
        self.tab_groups = QWidget() # вкладка групп
        self.groups_subjects_tab.addTab(self.tab_groups, "Группы")
        self.tab_subjects = QWidget() # вкладка предметов
        self.groups_subjects_tab.addTab(self.tab_subjects, "Предметы")

        gr_sub_label = QLabel("Группы и предметы:")
        gr_sub_label.setAlignment(Qt.AlignLeft)
        gr_sub_label.setStyleSheet("""
            font-size: 22px;
            font-weight: bold;
            font-family: Roboto;
            color: #333;
            margin-top: 20px;
            margin-bottom: 10px;
        """)
        groups_subjects_layout.addWidget(gr_sub_label)
        groups_subjects_layout.addWidget(self.groups_subjects_tab)

        # --------------------------------------------------- tab-вкладка группы ---------------------------------------------------
        groups_layout = QHBoxLayout()
        self.tab_groups.setLayout(groups_layout)

        self.groups_table = QTableWidget()
        self.groups_table.setFixedSize(350, 400)
        self.groups_table.setColumnCount(2)
        self.groups_table.setHorizontalHeaderLabels(["ФИО ученика", "Группа"])
        self.groups_table.horizontalHeader().setStretchLastSection(True)
        self.groups_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.groups_table.setSelectionMode(QTableWidget.SingleSelection)
        self.groups_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.groups_table.itemSelectionChanged.connect(self.on_groups_selected)
        self.groups_table.setStyleSheet("""
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
        header = self.groups_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Fixed)  # фио
        header.resizeSection(0, 180)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # группа
        groups_layout.addWidget(self.groups_table, alignment=Qt.AlignCenter)
        groups_layout.addStretch(1)

        groups_right_layout = QVBoxLayout()
        groups_layout.addSpacing(21)
        groups_layout.addLayout(groups_right_layout)
        groups_layout.addSpacing(20)

        group_label = QLabel("Группа:")
        group_label.setStyleSheet("font-family: Roboto; color: #333;")
        groups_right_layout.addStretch(2)
        groups_right_layout.addWidget(group_label, alignment=Qt.AlignLeft)

        self.groups_group_combo = QComboBox()
        self.groups_group_combo.addItems(["Выберите группу"])
        self.groups_group_combo.setFixedSize(150, 30)
        self.groups_group_combo.setStyleSheet("""
            border-radius: 5px;
            border: 1px solid #ccc;
            color: #333;
            padding: 5px;
            font-family: Roboto;
        """)
        # self.group_combo.currentIndexChanged.connect(self.load_stats)
        groups_right_layout.addWidget(self.groups_group_combo, alignment=Qt.AlignLeft)
        groups_right_layout.addSpacing(15)

        fio_label = QLabel("ФИО ученика:")
        fio_label.setStyleSheet("font-family: Roboto; color: #333;")
        groups_right_layout.addWidget(fio_label, alignment=Qt.AlignLeft)
        
        self.groups_fio = QLineEdit()
        self.groups_fio.setMaxLength(92)
        self.groups_fio.setFixedSize(230, 35)
        self.groups_fio.setStyleSheet("""
            border-radius: 5px;
            border: 2px solid #3498db;
            padding: 5px;
            font-family: roboto;
            font-size: 14px;
        """)
        groups_right_layout.addWidget(self.groups_fio, alignment=Qt.AlignLeft)
        groups_right_layout.addStretch(1)

        groups_button_layout = QHBoxLayout()
        groups_right_layout.addLayout(groups_button_layout)

        self.add_to_group = QPushButton()
        self.add_to_group.setText("Добавить в\nгруппу")
        self.add_to_group.setFixedSize(110, 50)
        self.add_to_group.setStyleSheet("""
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
        self.add_to_group.clicked.connect(self.add_user_to_group)
        self.add_to_group.setEnabled(False)
        groups_button_layout.addWidget(self.add_to_group)
        groups_button_layout.addSpacing(10)

        self.del_from_group = QPushButton()
        self.del_from_group.setText("Удалить из\nгруппы")
        self.del_from_group.setFixedSize(110, 50)
        self.del_from_group.setStyleSheet("""
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
        self.del_from_group.clicked.connect(self.del_user_from_group)
        self.del_from_group.setEnabled(False)
        groups_button_layout.addWidget(self.del_from_group)
        groups_right_layout.addStretch(1)

        self.selected_groups_user = None
        self.selected_subjects_user = None
        
        # --------------------------------------------------- tab-вкладка предметы ---------------------------------------------------
        subjects_layout = QHBoxLayout()
        self.tab_subjects.setLayout(subjects_layout)

        self.subjects_table = QTableWidget()
        self.subjects_table.setFixedSize(350, 400)
        self.subjects_table.setColumnCount(3)
        self.subjects_table.setHorizontalHeaderLabels(["Группа", "Предмет", "ФИО преподавателя"])
        self.subjects_table.horizontalHeader().setStretchLastSection(True)
        self.subjects_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.subjects_table.setSelectionMode(QTableWidget.SingleSelection)
        self.subjects_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.subjects_table.itemSelectionChanged.connect(self.on_subjects_selected)
        self.subjects_table.setStyleSheet("""
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
        header = self.subjects_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Fixed)  # группа
        header.resizeSection(0, 70)
        header.setSectionResizeMode(1, QHeaderView.Fixed)  # предмет
        header.resizeSection(1, 90)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # преподаватель
        subjects_layout.addWidget(self.subjects_table, alignment=Qt.AlignCenter)
        subjects_layout.addStretch(1)

        subjects_right_layout = QVBoxLayout()
        subjects_layout.addSpacing(10)
        subjects_layout.addLayout(subjects_right_layout)
        subjects_layout.addSpacing(10)

        subjects_group_label = QLabel("Группа:")
        subjects_group_label.setStyleSheet("font-family: Roboto; color: #333;")
        subjects_right_layout.addStretch(1)
        subjects_right_layout.addWidget(subjects_group_label, alignment=Qt.AlignLeft)

        self.subjects_group_combo = QComboBox()
        self.subjects_group_combo.addItems(["Выберите группу"])
        self.subjects_group_combo.setFixedSize(150, 30)
        self.subjects_group_combo.setStyleSheet("""
            border-radius: 5px;
            border: 1px solid #ccc;
            color: #333;
            padding: 5px;
            font-family: Roboto;
        """)
        # self.subjects_group_combo.currentIndexChanged.connect(self.load_stats)
        subjects_right_layout.addWidget(self.subjects_group_combo, alignment=Qt.AlignLeft)
        subjects_right_layout.addSpacing(10)

        subject_label = QLabel("Предмет:")
        subject_label.setStyleSheet("font-family: Roboto; color: #333;")
        subjects_right_layout.addWidget(subject_label, alignment=Qt.AlignLeft)

        self.subject_combo = QComboBox()
        self.subject_combo.addItems(["Выберите предмет"])
        self.subject_combo.setFixedSize(150, 30)
        self.subject_combo.setStyleSheet("""
            border-radius: 5px;
            border: 1px solid #ccc;
            color: #333;
            padding: 5px;
            font-family: Roboto;
        """)
        # self.subject_combo.currentIndexChanged.connect(self.load_stats)
        subjects_right_layout.addWidget(self.subject_combo, alignment=Qt.AlignLeft)
        subjects_right_layout.addSpacing(10)

        teacher_fio_label = QLabel("ФИО преподавателя:")
        teacher_fio_label.setStyleSheet("font-family: Roboto; color: #333;")
        subjects_right_layout.addWidget(teacher_fio_label, alignment=Qt.AlignLeft)

        self.subject_teacher_fio = QComboBox()
        self.subject_teacher_fio.addItems(["Выберите преподавателя"])
        self.subject_teacher_fio.setFixedSize(200, 30)
        self.subject_teacher_fio.setStyleSheet("""
            border-radius: 5px;
            border: 1px solid #ccc;
            color: #333;
            padding: 5px;
            font-family: Roboto;
        """)
        # self.subject_teacher_fio.currentIndexChanged.connect(self.print)
        subjects_right_layout.addWidget(self.subject_teacher_fio, alignment=Qt.AlignLeft)
        subjects_right_layout.addStretch(1)
        
        # self.subject_teacher_fio = QLineEdit()
        # self.subject_teacher_fio.setMaxLength(92)
        # self.subject_teacher_fio.setFixedSize(230, 35)
        # self.subject_teacher_fio.setStyleSheet("""
        #     border-radius: 5px;
        #     border: 2px solid #3498db;
        #     padding: 5px;
        #     font-family: roboto;
        #     font-size: 14px;
        # """)
        # subjects_right_layout.addWidget(self.subject_teacher_fio, alignment=Qt.AlignLeft)
        # subjects_right_layout.addStretch(1)

        subjects_button_layout = QHBoxLayout()
        subjects_right_layout.addLayout(subjects_button_layout)

        self.add_to_subject = QPushButton()
        self.add_to_subject.setText("Прикрепить\nпреподавателя")
        self.add_to_subject.setFixedSize(120, 50)
        self.add_to_subject.setStyleSheet("""
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
        self.add_to_subject.clicked.connect(self.add_teacher_to_group)
        self.add_to_subject.setEnabled(False)
        subjects_button_layout.addWidget(self.add_to_subject)
        subjects_button_layout.addSpacing(10)

        self.del_from_subject = QPushButton()
        self.del_from_subject.setText("Открепить\nпреподавателя")
        self.del_from_subject.setFixedSize(120, 50)
        self.del_from_subject.setStyleSheet("""
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
        self.del_from_subject.clicked.connect(self.del_teacher_from_group)
        self.del_from_subject.setEnabled(False)
        subjects_button_layout.addWidget(self.del_from_subject)
        subjects_right_layout.addStretch(1)

    def load_teachers_for_groups(self):
        self.subject_teacher_fio.clear()
        self.subject_teacher_fio.addItems(["Выберите преподавателя"])
        try:
            cursor = self.conn.cursor()
            
            query = """
                select
                    u.id_user,
                    u.surname + ' ' + u.[name] + ' ' + u.patronymic as fio
                from users u
                where u.id_role = 2
            """
            cursor.execute(query)
            teachers_data = cursor.fetchall()
            
            if teachers_data:
                for group in teachers_data:
                    id_user = group[0]
                    fio = group[1]
                    self.subject_teacher_fio.addItem(fio, id_user)
            else:
                self.subject_teacher_fio.setText("Нет преподавателей")
                
            cursor.close()
            
        except Exception as e:
            self.subject_teacher_fio.clear()
            self.subject_teacher_fio.setText(f"Ошибка загрузки: {str(e)}")

    def load_groups(self):
        try:
            cursor = self.conn.cursor()
            
            query = ("""
                select
                    u.id_user,
                    u.surname + ' ' + u.[name] + ' ' + u.patronymic as fio,
                    isnull(convert(varchar, n_c.num) + n_c.letter, 'Не назначена') as [group],
                    c.id_class
                from users u
                left join class c on c.id_user = u.id_user
                left join name_class n_c on n_c.id_name_class = c.id_name_class
                where u.id_role = 1
            """)
            cursor.execute(query)
            groups_data = cursor.fetchall()
            
            self.groups_table.setRowCount(len(groups_data))
            
            for row, record in enumerate(groups_data):
                user_id = record[0]
                fio = record[1]
                group = record[2]
                id_group = record[3]
                
                # фамилия
                fio_item = QTableWidgetItem(fio)
                fio_item.setData(Qt.UserRole, {'user_id': user_id, 'fio': fio, 'id_group': id_group})
                fio_item.setFlags(fio_item.flags() & ~Qt.ItemIsEditable)
                fio_item.setTextAlignment(Qt.AlignCenter)
                self.groups_table.setItem(row, 0, fio_item)

                # имя
                group_item = QTableWidgetItem(group)
                group_item.setData(Qt.UserRole, {'user_id': user_id, 'fio': fio, 'id_group': id_group})
                group_item.setFlags(group_item.flags() & ~Qt.ItemIsEditable)
                group_item.setTextAlignment(Qt.AlignCenter)
                self.groups_table.setItem(row, 1, group_item)
            
            cursor.close()
            
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить список учеников и групп: {str(e)}")

    def load_groups_for_groups(self): # выбор элемента для загрузки групп
        self.load_groups_into_combo(self.groups_group_combo) # в скобках указан элемент для подстановки

    def on_groups_selected(self): # выбор строки в таблице
        selected_items = self.groups_table.selectedItems()
        
        if selected_items:
            item = selected_items[0]
            item_data = item.data(Qt.UserRole)
            if item_data['id_group'] == None:
                item_data['id_group'] = 0
            
            if (item_data and 'user_id' in item_data 
                    and 'fio' in item_data and 'id_group' in item_data):
                self.selected_groups_user = item_data['user_id']
                self.groups_fio.setText(item_data['fio'])
                # self.groups_group_combo.setCurrentIndex(item_data['id_group'])
                self.add_to_group.setEnabled(True)
                self.del_from_group.setEnabled(True)
            else:
                self.selected_groups_user = None
                self.groups_fio.setText = None
                self.add_to_group.setEnabled(False)
                self.del_from_group.setEnabled(False)
        else:
            self.selected_groups_user = None
            self.groups_fio.setText = None
            self.add_to_group.setEnabled(False)
            self.del_from_group.setEnabled(False)

    def add_user_to_group(self): # добавление ученика в группу
        if self.groups_group_combo.currentIndex() == 0:
            QMessageBox.warning(self, "Ошибка", "Выберите группу")
            return
            
        if not self.groups_fio:
            QMessageBox.warning(self, "Ошибка", "Укажите ФИО ученика")
            return
        
        fio_cursor = self.conn.cursor()
        fio_query = """
            select id_user
            from users u
            where u.surname + ' ' + u.[name] + ' ' + u.patronymic = ?
            and id_role = 1
        """
        fio_cursor.execute(fio_query, self.groups_fio.text())
        fio = fio_cursor.fetchone()
        fio_cursor.close()

        if not fio:
            QMessageBox.warning(self, "Ошибка", "Укажите ФИО существующего ученика")
            return
        
        group_cursor = self.conn.cursor()
        group_query = """
            select
                c.id_class
            from class c
            inner join name_class n_c on n_c.id_name_class = c.id_name_class
            inner join users u on u.id_user = c.id_user
            where c.id_user = ?
            and c.id_name_class = ?
        """
        group_cursor.execute(group_query, (self.selected_groups_user, self.groups_group_combo.currentData()))
        group = group_cursor.fetchone()
        group_cursor.close()

        if group:
            QMessageBox.warning(self, "Ошибка", "Ученик уже состоит в этой группе")
            return

        subject_cursor = self.conn.cursor()
        subject_query = """
            select
                s_t.id
            from subj_teachers s_t
            where s_t.id_name_class = ?
        """
        subject_cursor.execute(subject_query, (self.groups_group_combo.currentData()))
        subject = subject_cursor.fetchone()
        subject_cursor.close()

        if not subject:
            QMessageBox.warning(self, "Ошибка", "Данной группе не назначен преподаватель")
            return
        
        # сделать предупреждение о невозможности добавить ученика в группу, если в ней отсутствует преподаватель
        # если преподаватель есть - добавить строку добавления записи в таблицу subj_students
            
        try:
            cursor = self.conn.cursor()
            
            query = """
                declare @id_subject int;
                select
                    @id_subject = s_t.id_subject
                from subj_teachers s_t
                where s_t.id_name_class = ?;
                insert into class(id_name_class, id_user)
                values(?, ?);
                insert into subj_students(id_subject, id_user)
                values (@id_subject, ?)
            """
            cursor.execute(query, (
                self.groups_group_combo.currentData(),
                self.groups_group_combo.currentData(),
                self.selected_groups_user,
                self.selected_groups_user
            ))

            self.conn.commit()
            cursor.close()
            
            QMessageBox.information(self, "Успех", "Ученик добавлен в группу")
            
            self.load_groups()
            
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить ученика в группу: {str(e)}")
            if 'cursor' in locals():
                self.conn.rollback()

    def del_user_from_group(self):
        if self.groups_group_combo.currentIndex() == 0:
            QMessageBox.warning(self, "Ошибка", "Выберите группу")
            return
            
        if not self.groups_fio:
            QMessageBox.warning(self, "Ошибка", "Укажите ФИО ученика")
            return
        
        fio_cursor = self.conn.cursor()
        fio_query = """
            select id_user
            from users u
            where u.surname + ' ' + u.[name] + ' ' + u.patronymic = ?
        """
        fio_cursor.execute(fio_query, self.groups_fio.text())
        fio = fio_cursor.fetchone()
        fio_cursor.close()

        if not fio:
            QMessageBox.warning(self, "Ошибка", "Укажите ФИО существующего ученика")
            return
        
        group_cursor = self.conn.cursor()
        group_query = """
            select
                c.id_class
            from class c
            inner join name_class n_c on n_c.id_name_class = c.id_name_class
            inner join users u on u.id_user = c.id_user
            where c.id_user = ?
            and c.id_name_class = ?
        """
        group_cursor.execute(group_query, (self.selected_groups_user, self.groups_group_combo.currentData()))
        group = group_cursor.fetchone()
        group_cursor.close()

        if not group:
            QMessageBox.warning(self, "Ошибка", "Ученик не состоит в данной группе")
            return
        
        reply = QMessageBox.question(
            self,
            "Подтверждение",
            f"Вы уверены, что хотите удалить {self.groups_fio.text()} "
            f"из группы ({self.groups_group_combo.currentText()})?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.No:
            return
        
        try:
            cursor = self.conn.cursor()
            
            delete_query = """
                declare @id_subject int;
                select
                    @id_subject = s_t.id_subject
                from subj_teachers s_t
                where s_t.id_name_class = ?;
                delete from class
                where id_user = ? and id_name_class = ?;
                delete from subj_students
                where id_user = ? and id_subject = @id_subject
            """
            cursor.execute(delete_query, (
                self.groups_group_combo.currentData(),
                self.selected_groups_user,
                self.groups_group_combo.currentData(),
                self.selected_groups_user
            ))
            self.conn.commit()
            
            QMessageBox.information(
                self, 
                "Успех", 
                f"Ученик успешно удален"
            )
            
            # очистка полей
            # self.question_text_edit.clear()
            # self.validate_homework_text()
            # self.load_homework()

            cursor.close()
            self.load_groups()
            
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось удалить ученика: {str(e)}")
            if 'cursor' in locals():
                self.conn.rollback()

    def load_subjects(self):
        try:
            cursor = self.conn.cursor()
            
            query = ("""
                select
                    s_t.id,
                    s_t.id_name_class,
                    s_t.id_subject,
                    s_t.id_user,
                    isnull(convert(varchar, n_c.num) + n_c.letter, 'Не назначена') as [group],
                    isnull(s.subject_name, 'Не назначен') as subject_name,
                    isnull(u.surname + ' ' + u.[name] + ' ' + u.patronymic, 'Не назначен') as fio
                from subj_teachers s_t
                left join users u on u.id_user = s_t.id_user
                left join subject s on s.id_subject = s_t.id_subject
                right join name_class n_c on n_c.id_name_class = s_t.id_name_class
            """) # переписать запрос
            cursor.execute(query)
            subject_data = cursor.fetchall()
            
            self.subjects_table.setRowCount(len(subject_data))
            
            for row, record in enumerate(subject_data):
                id_s_t = record[0]
                id_group = record[1]
                id_subject = record[2]
                id_user = record[3]
                name_group = record[4]
                subject_name = record[5]
                fio = record[6]
                
                # группа
                group_item = QTableWidgetItem(name_group)
                group_item.setData(Qt.UserRole, {
                    'id_s_t': id_s_t,
                    'id_group': id_group,
                    'id_subject': id_subject,
                    'id_user': id_user,
                    'fio': fio
                })
                group_item.setFlags(group_item.flags() & ~Qt.ItemIsEditable)
                group_item.setTextAlignment(Qt.AlignCenter)
                self.subjects_table.setItem(row, 0, group_item)

                # предмет
                subject_item = QTableWidgetItem(subject_name)
                subject_item.setData(Qt.UserRole, {
                    'id_s_t': id_s_t,
                    'id_group': id_group,
                    'id_subject': id_subject,
                    'id_user': id_user,
                    'fio': fio
                })
                subject_item.setFlags(subject_item.flags() & ~Qt.ItemIsEditable)
                subject_item.setTextAlignment(Qt.AlignCenter)
                self.subjects_table.setItem(row, 1, subject_item)

                # фио преподавателя
                fio_item = QTableWidgetItem(fio)
                fio_item.setData(Qt.UserRole, {
                    'id_s_t': id_s_t,
                    'id_group': id_group,
                    'id_subject': id_subject,
                    'id_user': id_user,
                    'fio': fio
                })
                fio_item.setFlags(fio_item.flags() & ~Qt.ItemIsEditable)
                fio_item.setTextAlignment(Qt.AlignCenter)
                self.subjects_table.setItem(row, 2, fio_item)
            
            cursor.close()
            
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить список учеников и групп: {str(e)}")

    def on_subjects_selected(self): # выбор строки в таблице
        selected_items = self.subjects_table.selectedItems()
        
        if selected_items:
            item = selected_items[0]
            item_data = item.data(Qt.UserRole)
            if item_data['id_group'] == None:
                item_data['id_group'] = 0
            
            if (item_data and 'id_s_t' in item_data
                    and 'id_group' in item_data 
                    and 'id_subject' in item_data
                    and 'id_user' in item_data
                    and 'fio' in item_data):
                self.selected_subjects_user = item_data['id_user']
                # if item_data['fio'] == "Не назначен":
                #     self.subject_teacher_fio.clear()
                #     self.subject_teacher_fio.setPlaceholderText(item_data['fio'])
                # else:
                #     self.subject_teacher_fio.clear()
                #     self.subject_teacher_fio.setText(item_data['fio'])
                # self.groups_group_combo.setCurrentIndex(item_data['id_group'])
                self.add_to_subject.setEnabled(True)
                self.del_from_subject.setEnabled(True)
            else:
                self.selected_subjects_user = None
                # self.subject_teacher_fio.setText = None
                self.subject_teacher_fio.clear()
                self.subject_teacher_fio.addItems(["Выберите преподавателя"])
                self.add_to_subject.setEnabled(False)
                self.del_from_subject.setEnabled(False)
        else:
            self.selected_subjects_user = None
            # self.subject_teacher_fio.setText = None
            self.subject_teacher_fio.clear()
            self.subject_teacher_fio.addItems(["Выберите преподавателя"])
            self.add_to_subject.setEnabled(False)
            self.del_from_subject.setEnabled(False)

    def add_teacher_to_group(self): # добавление преподавателя к группе и предмету
        if self.subjects_group_combo.currentIndex() == 0:
            QMessageBox.warning(self, "Ошибка", "Выберите группу")
            return
        
        if self.subject_combo.currentIndex() == 0:
            QMessageBox.warning(self, "Ошибка", "Выберите предмет")
            return
            
        if self.subject_teacher_fio.currentIndex() == 0:
            QMessageBox.warning(self, "Ошибка", "Выберите преподавателя")
            return
        
        fio_cursor = self.conn.cursor()
        fio_query = """
            select id_user
            from users u
            where u.id_user = ?
            and id_role = 2
        """
        fio_cursor.execute(fio_query, self.subject_teacher_fio.currentData())
        fio = fio_cursor.fetchone()
        fio_cursor.close()

        if not fio:
            QMessageBox.warning(self, "Ошибка", "Выберите существующего преподавателя")
            return
        
        subject_group_cursor = self.conn.cursor()
        group_query = """
            select
                s_t.id
            from subj_teachers s_t
            inner join [subject] s on s.id_subject = s_t.id_subject
            inner join name_class n_c on n_c.id_name_class = s_t.id_name_class
            inner join users u on u.id_user = s_t.id_user
            where s_t.id_subject = ? 
            and u.id_user = ?
            and s_t.id_name_class = ?
        """
        subject_group_cursor.execute(group_query, (
            self.subject_combo.currentData(),
            self.subject_teacher_fio.currentData(),
            self.subjects_group_combo.currentData()
        ))
        subject_group = subject_group_cursor.fetchone()
        subject_group_cursor.close()

        if subject_group:
            QMessageBox.warning(self, "Ошибка", "Преподаватель уже прикреплен на предмет в этой группе")
            return
            
        try:
            cursor = self.conn.cursor()
            
            query = """
                declare @id_user int;
                select @id_user = id_user
                from users u
                where u.id_user = ?
                and u.id_role = 2;
                insert into subj_teachers(id_subject, id_user, id_name_class)
                values(?, @id_user, ?)
            """
            cursor.execute(query, (
                self.subject_teacher_fio.currentData(),
                self.subject_combo.currentData(),
                self.subjects_group_combo.currentData()
            ))

            self.conn.commit()
            cursor.close()
            
            QMessageBox.information(self, "Успех", "Преподаватель прикреплен на предмет у группы")
            
            self.load_subjects()
            
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось прикрепить преподавателя на предмет у группы: {str(e)}")
            if 'cursor' in locals():
                self.conn.rollback()

    def del_teacher_from_group(self): # удаление преподавателя у группы и предмета
        if self.subjects_group_combo.currentIndex() == 0:
            QMessageBox.warning(self, "Ошибка", "Выберите группу")
            return
        
        if self.subject_combo.currentIndex() == 0:
            QMessageBox.warning(self, "Ошибка", "Выберите предмет")
            return
            
        if self.subject_teacher_fio.currentIndex() == 0:
            QMessageBox.warning(self, "Ошибка", "Выберите преподавателя")
            return
        
        fio_cursor = self.conn.cursor()
        fio_query = """
            select id_user
            from users u
            where u.id_user = ?
            and id_role = 2
        """
        fio_cursor.execute(fio_query, self.subject_teacher_fio.currentData())
        fio = fio_cursor.fetchone()
        fio_cursor.close()

        if not fio:
            QMessageBox.warning(self, "Ошибка", "Укажите ФИО существующего преподавателя")
            return
        
        subject_group_cursor = self.conn.cursor()
        group_query = """
            select
                s_t.id
            from subj_teachers s_t
            inner join [subject] s on s.id_subject = s_t.id_subject
            inner join name_class n_c on n_c.id_name_class = s_t.id_name_class
            inner join users u on u.id_user = s_t.id_user
            where s_t.id_subject = ? and s_t.id_user = ?
            and s_t.id_name_class = ?
        """
        subject_group_cursor.execute(group_query, (
            self.subject_combo.currentData(),
            self.selected_subjects_user,
            self.subjects_group_combo.currentData()
        ))
        subject_group = subject_group_cursor.fetchone()
        subject_group_cursor.close()

        if not subject_group:
            QMessageBox.warning(self, "Ошибка", "Преподаватель не прикреплен к предмету в этой группе")
            return
        
        reply = QMessageBox.question(
            self,
            "Подтверждение",
            f"Вы уверены, что хотите открепить {self.subject_teacher_fio.currentText()} "
            f"от группы ({self.subjects_group_combo.currentText()}, "
            f"{self.subject_combo.currentText()})?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.No:
            return
        
        try:
            cursor = self.conn.cursor()
            
            delete_query = """
                delete from subj_teachers
                where id_subject = ? and id_user = ?
                and id_name_class = ?
            """
            cursor.execute(delete_query, (
                self.subject_combo.currentData(),
                self.selected_subjects_user,
                self.subjects_group_combo.currentData()
            ))
            self.conn.commit()
            
            QMessageBox.information(
                self, 
                "Успех", 
                f"Преподаватель успешно откреплен от группы и предмета"
            )
            
            # очистка полей
            # self.question_text_edit.clear()
            # self.validate_homework_text()
            # self.load_homework()

            cursor.close()
            self.load_subjects()
            
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось открепить преподавателя от группы и предмета: {str(e)}")
            if 'cursor' in locals():
                self.conn.rollback()

    def load_groups_for_subjects(self): # выбор элемента для загрузки групп
        try:
            cursor = self.conn.cursor()
            
            query = """
                select 
                    n_c.id_name_class,
                    convert(varchar, n_c.num) + n_c.letter
                from name_class n_c
                order by n_c.num, n_c.letter
            """
            cursor.execute(query)
            groups_data = cursor.fetchall()
            
            self.subjects_group_combo.clear()
            
            if groups_data:
                self.subjects_group_combo.addItem("Выберите группу", None)
                for group in groups_data:
                    class_id = group[0]
                    num_letter = group[1]
                    group_name = f"{num_letter}"
                    self.subjects_group_combo.addItem(group_name, class_id)
            else:
                self.subjects_group_combo.addItem("Нет групп")
                self.subjects_group_combo.setEnabled(False)
                
            cursor.close()
            
        except Exception as e:
            self.subjects_group_combo.clear()
            self.subjects_group_combo.addItem(f"Ошибка загрузки: {str(e)}")
            self.subjects_group_combo.setEnabled(False)

    def load_subjects_into_combo(self): # загрузка предметов
        try:
            cursor = self.conn.cursor()
            
            query = """
                select
                    id_subject,
                    subject_name
                from [subject]
                order by subject_name
            """
            cursor.execute(query)
            groups_data = cursor.fetchall()
            
            self.subject_combo.clear()
            
            if groups_data:
                self.subject_combo.addItem("Выберите предмет", None)
                for group in groups_data:
                    id_subject = group[0]
                    subject_name = group[1]
                    group_name = f"{subject_name}"
                    self.subject_combo.addItem(group_name, id_subject)
            else:
                self.subject_combo.addItem("Нет предметов")
                self.subject_combo.setEnabled(False)
                
            cursor.close()
            
        except Exception as e:
            self.subject_combo.clear()
            self.subject_combo.addItem(f"Ошибка загрузки: {str(e)}")
            self.subject_combo.setEnabled(False)

    def show_schedule(self):
        self.clear_content_layout()

        self.content_layout_v.addWidget(self.schedule_widget)

        self.create_empty_schedule_table()
        self.load_groups_for_schedule()
        self.load_cabinets_for_schedule()

    def schedule(self):
        self.schedule_widget = QWidget()
        schedule_layout = QVBoxLayout()
        self.schedule_widget.setLayout(schedule_layout)

        schedule_label = QLabel("Составление расписания:")
        schedule_label.setAlignment(Qt.AlignLeft)
        schedule_label.setStyleSheet("""
            font-size: 22px;
            font-weight: bold;
            font-family: Roboto;
            color: #333;
            margin-top: 20px;
            margin-bottom: 10px;
        """)
        schedule_layout.addWidget(schedule_label)

        top_layout = QHBoxLayout() # верхняя область
        schedule_layout.addLayout(top_layout)
        group_layout = QVBoxLayout() # область для группы и названия предмета
        top_layout.addLayout(group_layout)
        day_layout = QVBoxLayout() # область для дня недели

        group_label = QLabel("Группа:")
        group_label.setStyleSheet("font-family: Roboto; color: #333;")
        group_layout.addWidget(group_label, alignment=Qt.AlignLeft)
        
        self.schedule_group_combo = QComboBox()
        self.schedule_group_combo.addItems(["Выберите группу"])
        self.schedule_group_combo.setCurrentIndex(0)
        self.schedule_group_combo.setFixedSize(120, 30)
        self.schedule_group_combo.setStyleSheet("""
            border-radius: 5px;
            border: 1px solid #ccc;
            color: #333;
            padding: 5px;
            font-family: Roboto;
        """)
        self.schedule_group_combo.setCurrentIndex(0)
        self.schedule_group_combo.currentIndexChanged.connect(self.load_schedule)
        self.schedule_group_combo.currentIndexChanged.connect(self.load_subject_name_for_schedule)
        self.schedule_group_combo.currentIndexChanged.connect(self.load_teachers_for_schedule)
        group_layout.addWidget(self.schedule_group_combo, alignment=Qt.AlignLeft)

        self.schedule_subject = QLabel()
        self.schedule_subject.setText("Предмет у группы")
        self.schedule_subject.setStyleSheet("""
            font-family: Roboto;
            font-size: 12px;
            color: #333;
        """)
        top_layout.addWidget(self.schedule_subject, alignment=Qt.AlignLeft)

        day_label = QLabel("День недели:")
        day_label.setStyleSheet("font-family: Roboto; color: #333;")
        top_layout.addLayout(day_layout)
        day_layout.addWidget(day_label, alignment=Qt.AlignLeft)
        
        self.schedule_day_combo = QComboBox()
        self.schedule_day_combo.addItems([
            "Выберите день",
            "Понедельник",
            "Вторник",
            "Среда",
            "Четверг",
            "Пятница"
        ])
        self.schedule_day_combo.setCurrentIndex(0)
        self.schedule_day_combo.setFixedSize(120, 30)
        self.schedule_day_combo.setStyleSheet("""
            border-radius: 5px;
            border: 1px solid #ccc;
            color: #333;
            padding: 5px;
            font-family: Roboto;
        """)
        self.schedule_day_combo.currentIndexChanged.connect(self.load_schedule)
        day_layout.addWidget(self.schedule_day_combo, alignment=Qt.AlignLeft)

        self.num_label = QLabel()
        self.num_label.setText("Номер занятия:  ")
        self.num_label.setStyleSheet("""
            font-family: Roboto;
            font-size: 12px;
            color: #333;
        """)
        top_layout.addWidget(self.num_label, alignment=Qt.AlignLeft)
        
        # для таблицы
        self.schedule_table = QTableWidget()
        self.schedule_table.setFixedSize(600, 337)
        self.schedule_table.setColumnCount(5)
        self.schedule_table.setHorizontalHeaderLabels(["Номер занятия", "Группа", "Предмет", "Преподаватель", "Кабинет"])
        self.schedule_table.horizontalHeader().setStretchLastSection(True)
        self.schedule_table.verticalHeader().setDefaultSectionSize(60)
        self.schedule_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.schedule_table.setSelectionMode(QTableWidget.SingleSelection)
        self.schedule_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.schedule_table.itemSelectionChanged.connect(self.on_schedule_selected)
        self.schedule_table.setStyleSheet("""
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
        header = self.schedule_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Fixed)  # номер занятия
        header.resizeSection(0, 110)
        header.setSectionResizeMode(1, QHeaderView.Fixed)  # группа
        header.resizeSection(1, 70)
        header.setSectionResizeMode(2, QHeaderView.Fixed) # предмет
        header.resizeSection(2, 120)
        header.setSectionResizeMode(3, QHeaderView.Fixed) # фио преподавателя
        header.resizeSection(3, 180)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # кабинет
        schedule_layout.addWidget(self.schedule_table)
        schedule_layout.addStretch(1)

        # для выбора фио преподавателя, номера занятия, кабинета, и кнопок
        bottom_layout = QHBoxLayout()
        schedule_layout.addLayout(bottom_layout)
        teacher_layout = QVBoxLayout() # область для фио преподавателя
        bottom_layout.addLayout(teacher_layout)
        num_layout = QVBoxLayout() # область для номера занятия и номера кабинета
        bottom_layout.addLayout(num_layout)
        bottom_layout.addStretch(1)
        buttons_layout = QHBoxLayout() # область для кнопок взаимодействия
        bottom_layout.addLayout(buttons_layout)

        fio_text = QLabel("ФИО преподавателя")
        fio_text.setStyleSheet("font-family: Roboto; color: #333;")
        teacher_layout.addWidget(fio_text, alignment=Qt.AlignLeft)

        self.teacher_combo = QComboBox()
        self.teacher_combo.addItems(["Выберите преподавателя"])
        self.teacher_combo.setFixedSize(200, 30)
        self.teacher_combo.setStyleSheet("""
            border-radius: 5px;
            border: 1px solid #ccc;
            color: #333;
            padding: 5px;
            font-family: Roboto;
        """)
        # self.schedule_group_combo.currentIndexChanged.connect(self.load_stats)
        teacher_layout.addWidget(self.teacher_combo, alignment=Qt.AlignLeft)
        teacher_layout.addStretch(1)

        cabinet_text = QLabel("Номер кабинета")
        cabinet_text.setStyleSheet("font-family: Roboto; color: #333;")
        num_layout.addWidget(cabinet_text, alignment=Qt.AlignLeft)

        self.cabinet_combo = QComboBox()
        self.cabinet_combo.addItems(["Выберите кабинет"])
        self.cabinet_combo.setFixedSize(125, 30)
        self.cabinet_combo.setStyleSheet("""
            border-radius: 5px;
            border: 1px solid #ccc;
            color: #333;
            padding: 5px;
            font-family: Roboto;
        """)
        # self.schedule_group_combo.currentIndexChanged.connect(self.load_stats)
        num_layout.addWidget(self.cabinet_combo, alignment=Qt.AlignLeft)
        num_layout.addStretch(1)

        self.add_schedule_button = QPushButton("Добавить")
        self.add_schedule_button.setFixedSize(90, 35)
        self.add_schedule_button.setStyleSheet("""
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
        self.add_schedule_button.clicked.connect(self.add_schedule)
        self.add_schedule_button.setEnabled(False)
        buttons_layout.addWidget(self.add_schedule_button)

        self.del_schedule_button = QPushButton("Очистить")
        self.del_schedule_button.setFixedSize(90, 35)
        self.del_schedule_button.setStyleSheet("""
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
        self.del_schedule_button.clicked.connect(self.del_schedule)
        self.del_schedule_button.setEnabled(False)
        buttons_layout.addWidget(self.del_schedule_button)

        self.selected_schedule_id = None
        self.selected_lesson_num = None

    def load_schedule(self):
        self.num_label.setText("Номер занятия:  ")
        if (self.schedule_group_combo.currentIndex() > 0 and 
            self.schedule_day_combo.currentIndex() > 0):
            try:
                cursor = self.conn.cursor()

                # второй вариант запроса
                # select
                #     sch.id_schedule,
                #     sch.lesson_num,
                #     convert(varchar, n_c.num) + n_c.letter as [group],
                #     s.subject_name,
                #     u.surname + ' ' + u.[name] + ' ' + u.patronymic as fio,
                #     convert(varchar, cab.num)
                # from schedule sch
                # inner join name_class n_c on n_c.id_name_class = sch.id_name_class
                # inner join subject s on s.id_subject = sch.id_subject
                # inner join users u on u.id_user = sch.id_user
                # inner join cabinet cab on cab.id_cabinet = sch.id_cabinet
                
                query = ("""
                    select
                        sch.id_schedule,
                        sch.lesson_num,
                        convert(varchar, n_c.num) + n_c.letter as [group],
                        s.subject_name,
                        u.surname + ' ' + u.[name] + ' ' + u.patronymic as fio,
                        convert(varchar, cab.num)
                    from schedule sch
                    inner join subject s on s.id_subject = sch.id_subject
                    inner join name_class n_c on n_c.id_name_class = sch.id_name_class
                    inner join cabinet cab on cab.id_cabinet = sch.id_cabinet
                    inner join users u on u.id_user = sch.id_user
                    inner join subj_teachers s_t on s_t.id_subject = s.id_subject
                    where sch.id_name_class = ?
                    and sch.day_of_week = ?
                """) # переписать запрос
                cursor.execute(query, (
                    self.schedule_group_combo.currentData(), 
                    self.schedule_day_combo.currentText()
                ))
                schedule_data = cursor.fetchall()
                
                schedule_dict = {}
                for record in schedule_data:
                    lesson_num = record[1]
                    schedule_dict[lesson_num] = {
                        'id_schedule': record[0],
                        'lesson_num': record[1],
                        'group_name': record[2],
                        'subject_name': record[3],
                        'fio': record[4],
                        'cabinet': record[5]
                    }
                
                max_lessons = 5
                self.schedule_table.setRowCount(max_lessons)
                
                for lesson_num in range(1, max_lessons + 1):
                    row = lesson_num - 1
                    
                    if lesson_num in schedule_dict:
                        data = schedule_dict[lesson_num]
                        
                        # номер занятия
                        l_num_item = QTableWidgetItem(str(data['lesson_num']))
                        l_num_item.setData(Qt.UserRole, {
                            'id_schedule': data['id_schedule'],
                            'lesson_num': data['lesson_num']
                        })
                        l_num_item.setFlags(l_num_item.flags() & ~Qt.ItemIsEditable)
                        l_num_item.setTextAlignment(Qt.AlignCenter)
                        self.schedule_table.setItem(row, 0, l_num_item)

                        # группа
                        group_item = QTableWidgetItem(data['group_name'])
                        group_item.setData(Qt.UserRole, {
                            'id_schedule': data['id_schedule'],
                            'lesson_num': data['lesson_num']
                        })
                        group_item.setFlags(group_item.flags() & ~Qt.ItemIsEditable)
                        group_item.setTextAlignment(Qt.AlignCenter)
                        self.schedule_table.setItem(row, 1, group_item)

                        # предмет
                        subject_item = QTableWidgetItem(data['subject_name'])
                        subject_item.setData(Qt.UserRole, {
                            'id_schedule': data['id_schedule'],
                            'lesson_num': data['lesson_num']
                        })
                        subject_item.setFlags(subject_item.flags() & ~Qt.ItemIsEditable)
                        subject_item.setTextAlignment(Qt.AlignCenter)
                        self.schedule_table.setItem(row, 2, subject_item)

                        # фио
                        fio_item = QTableWidgetItem(data['fio'])
                        fio_item.setData(Qt.UserRole, {
                            'id_schedule': data['id_schedule'],
                            'lesson_num': data['lesson_num']
                        })
                        fio_item.setFlags(fio_item.flags() & ~Qt.ItemIsEditable)
                        fio_item.setTextAlignment(Qt.AlignCenter)
                        self.schedule_table.setItem(row, 3, fio_item)

                        # кабинет
                        cabinet_item = QTableWidgetItem(data['cabinet'])
                        cabinet_item.setData(Qt.UserRole, {
                            'id_schedule': data['id_schedule'],
                            'lesson_num': data['lesson_num']
                        })
                        cabinet_item.setFlags(cabinet_item.flags() & ~Qt.ItemIsEditable)
                        cabinet_item.setTextAlignment(Qt.AlignCenter)
                        self.schedule_table.setItem(row, 4, cabinet_item)
                        
                    else:
                        l_num_item = QTableWidgetItem(str(lesson_num))
                        l_num_item.setFlags(l_num_item.flags() & ~Qt.ItemIsEditable)
                        l_num_item.setTextAlignment(Qt.AlignCenter)
                        self.schedule_table.setItem(row, 0, l_num_item)
                        
                        for col in range(1, 5):
                            empty_item = QTableWidgetItem("")
                            empty_item.setFlags(empty_item.flags() & ~Qt.ItemIsEditable)
                            empty_item.setTextAlignment(Qt.AlignCenter)
                            self.schedule_table.setItem(row, col, empty_item)
                
                cursor.close()
                
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить расписание для группы: {str(e)}")
                self.create_empty_schedule_table()
        else:
            self.create_empty_schedule_table()
            self.on_schedule_selected()

    def on_schedule_selected(self): # выбор строки в таблице
        selected_items = self.schedule_table.selectedItems()
        
        if selected_items:
            item = selected_items[0]
            row = self.schedule_table.row(item)
            
            lesson_num_item = self.schedule_table.item(row, 0)
            if lesson_num_item:
                self.selected_lesson_num = int(lesson_num_item.text())
                self.num_label.setText(f"Номер занятия: {self.selected_lesson_num}")
            else:
                self.selected_lesson_num = row + 1
                self.num_label.setText(f"Номер занятия: {self.selected_lesson_num}")
                
            item_data = item.data(Qt.UserRole)
            
            if item_data and 'id_schedule' in item_data and 'lesson_num' in item_data:
                self.selected_schedule_id = item_data['id_schedule']
                self.selected_lesson_num = item_data['lesson_num']

                self.num_label.setText(f"Номер занятия: {self.selected_lesson_num}")
                
                row = self.schedule_table.row(item)
                group_name = self.schedule_table.item(row, 1).text() if self.schedule_table.item(row, 1) else ""
                subject_name = self.schedule_table.item(row, 2).text() if self.schedule_table.item(row, 2) else ""
                teacher_fio = self.schedule_table.item(row, 3).text() if self.schedule_table.item(row, 3) else ""
                cabinet_num = self.schedule_table.item(row, 4).text() if self.schedule_table.item(row, 4) else ""
                
                for i in range(self.schedule_group_combo.count()):
                    if self.schedule_group_combo.itemText(i) == group_name:
                        self.schedule_group_combo.setCurrentIndex(i)
                        break

                for i in range(self.schedule_day_combo.count()):
                    if self.schedule_day_combo.itemText(i) == self.schedule_day_combo.currentText():
                        pass
                
                for i in range(self.teacher_combo.count()):
                    if self.teacher_combo.itemText(i) == teacher_fio:
                        self.teacher_combo.setCurrentIndex(i)
                        break
                
                for i in range(self.cabinet_combo.count()):
                    if self.cabinet_combo.itemText(i) == cabinet_num:
                        self.cabinet_combo.setCurrentIndex(i)
                        break
                
                self.add_schedule_button.setEnabled(True)
                self.del_schedule_button.setEnabled(True)
            else:
                self.selected_schedule_id = None
                self.selected_lesson_num = None
                if lesson_num_item:
                    self.selected_lesson_num = int(lesson_num_item.text())
                    self.num_label.setText(f"Номер занятия: {self.selected_lesson_num}")
                self.cabinet_combo.setCurrentIndex(0)
                self.teacher_combo.setCurrentIndex(0)
                self.add_schedule_button.setEnabled(True)
                self.del_schedule_button.setEnabled(False)
        else:
            self.selected_schedule_id = None
            self.selected_lesson_num = None
            self.num_label.setText("Номер занятия:  ")
            self.add_schedule_button.setEnabled(False)
            self.del_schedule_button.setEnabled(False)

    def add_schedule(self): # добавление расписания для группы
        if self.schedule_group_combo.currentIndex() == 0:
            QMessageBox.warning(self, "Ошибка", "Выберите группу")
            return
        
        if self.schedule_day_combo.currentIndex() == 0:
            QMessageBox.warning(self, "Ошибка", "Выберите день недели")
            return
        
        if self.teacher_combo.currentIndex() == 0:
            QMessageBox.warning(self, "Ошибка", "Выберите преподавателя")
            return
        
        if self.cabinet_combo.currentIndex() == 0:
            QMessageBox.warning(self, "Ошибка", "Выберите кабинет")
            return
        
        selected_row = None
        if hasattr(self, 'selected_lesson_num') and self.selected_lesson_num:
            selected_row = self.selected_lesson_num - 1
        
        if selected_row is None:
            QMessageBox.warning(self, "Ошибка", "Выберите номер занятия в таблице")
            return
        
        try:
            cursor = self.conn.cursor()
            
            check_cabinet_query = """
                select count(*)
                from schedule sch
                where sch.id_cabinet = ?
                and sch.day_of_week = ?
                and sch.lesson_num = ?
                and sch.id_schedule != ?  -- исключаем текущую запись при обновлении
            """
            current_schedule_id = self.selected_schedule_id if hasattr(self, 'selected_schedule_id') and self.selected_schedule_id else 0
            cursor.execute(check_cabinet_query, (
                self.cabinet_combo.currentData(),
                self.schedule_day_combo.currentText(),
                self.selected_lesson_num,
                current_schedule_id
            ))
            if cursor.fetchone()[0] > 0:
                QMessageBox.warning(self, "Ошибка", "Кабинет уже занят в это время")
                cursor.close()
                return
            
            check_teacher_query = """
                select count(*)
                from schedule sch
                where sch.id_user = ?
                and sch.day_of_week = ?
                and sch.lesson_num = ?
                and sch.id_schedule != ?
            """
            cursor.execute(check_teacher_query, (
                self.teacher_combo.currentData(),
                self.schedule_day_combo.currentText(),
                self.selected_lesson_num,
                current_schedule_id
            ))
            if cursor.fetchone()[0] > 0:
                QMessageBox.warning(self, "Ошибка", "Преподаватель уже занят в это время")
                cursor.close()
                return
            
            check_group_query = """
                select count(*)
                from schedule sch
                where sch.id_name_class = ?
                and sch.day_of_week = ?
                and sch.lesson_num = ?
                and sch.id_schedule != ?
            """
            cursor.execute(check_group_query, (
                self.schedule_group_combo.currentData(),
                self.schedule_day_combo.currentText(),
                self.selected_lesson_num,
                current_schedule_id
            ))
            if cursor.fetchone()[0] > 0:
                QMessageBox.warning(self, "Ошибка", "У группы уже есть занятие в это время")
                cursor.close()
                return
            
            subject_query = """
                select s_t.id_subject
                from subj_teachers s_t
                inner join users u on u.id_user = s_t.id_user
                where s_t.id_name_class = ?
                and u.id_user = ?
            """
            cursor.execute(subject_query, (
                self.schedule_group_combo.currentData(),
                self.teacher_combo.currentData()
            ))
            subject_data = cursor.fetchone()
            if not subject_data:
                QMessageBox.warning(self, "Ошибка", "Данный преподаватель не ведет предмет у выбранной группы")
                cursor.close()
                return
            
            id_subject = subject_data[0]
            
            if current_schedule_id > 0:
                update_query = """
                    update schedule
                    set id_name_class = ?,
                        id_subject = ?,
                        id_user = ?,
                        day_of_week = ?,
                        lesson_num = ?,
                        id_cabinet = ?
                    where id_schedule = ?
                """
                cursor.execute(update_query, (
                    self.schedule_group_combo.currentData(),
                    id_subject,
                    self.teacher_combo.currentData(),
                    self.schedule_day_combo.currentText(),
                    self.selected_lesson_num,
                    self.cabinet_combo.currentData(),
                    current_schedule_id
                ))
                
                self.conn.commit()
                cursor.close()
                
                QMessageBox.information(self, "Успех", "Расписание успешно обновлено")
                
            else:
                insert_query = """
                    insert into schedule(id_name_class, id_subject, id_user, day_of_week, lesson_num, id_cabinet)
                    values(?, ?, ?, ?, ?, ?)
                """
                cursor.execute(insert_query, (
                    self.schedule_group_combo.currentData(),
                    id_subject,
                    self.teacher_combo.currentData(),
                    self.schedule_day_combo.currentText(),
                    self.selected_lesson_num,
                    self.cabinet_combo.currentData()
                ))
                
                self.conn.commit()
                cursor.close()
                
                QMessageBox.information(self, "Успех", "Занятие успешно добавлено в расписание")
            
            self.load_schedule()
            
            self.schedule_table.clearSelection()
            self.selected_schedule_id = None
            self.selected_lesson_num = None
            self.add_schedule_button.setEnabled(False)
            self.del_schedule_button.setEnabled(False)
            
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить расписание: {str(e)}")
            if 'cursor' in locals():
                self.conn.rollback()

    def del_schedule(self): # удаление расписания у группы
        if not hasattr(self, 'selected_schedule_id') or not self.selected_schedule_id:
            QMessageBox.warning(self, "Ошибка", "Выберите запись расписания для удаления")
            return
        
        row = None
        for i in range(self.schedule_table.rowCount()):
            item = self.schedule_table.item(i, 0)
            if item and item.data(Qt.UserRole):
                data = item.data(Qt.UserRole)
                if data.get('id_schedule') == self.selected_schedule_id:
                    row = i
                    break
        
        if row is None:
            QMessageBox.warning(self, "Ошибка", "Не удалось найти выбранную запись")
            return
        
        reply = QMessageBox.question(
            self,
            "Подтверждение удаления",
            f"Вы уверены, что хотите удалить занятие?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.No:
            return
        
        try:
            cursor = self.conn.cursor()
            
            delete_query = """
                delete from schedule
                where id_schedule = ?
            """
            cursor.execute(delete_query, (self.selected_schedule_id,))
            self.conn.commit()
            
            QMessageBox.information(
                self,
                "Успех",
                "Занятие успешно удалено из расписания"
            )
            
            cursor.close()
            
            self.load_schedule()
            
            self.schedule_table.clearSelection()
            self.selected_schedule_id = None
            self.selected_lesson_num = None
            self.add_schedule_button.setEnabled(False)
            self.del_schedule_button.setEnabled(False)
            
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось удалить занятие: {str(e)}")
            if 'cursor' in locals():
                self.conn.rollback()

    def create_empty_schedule_table(self): # пустая таблица
        self.num_label.setText("Номер занятия:  ")

        max_lessons = 5
        self.schedule_table.setRowCount(max_lessons)
        
        for lesson_num in range(1, max_lessons + 1):
            row = lesson_num - 1
            
            # номер занятия
            l_num_item = QTableWidgetItem(str(lesson_num))
            l_num_item.setFlags(l_num_item.flags() & ~Qt.ItemIsEditable)
            l_num_item.setTextAlignment(Qt.AlignCenter)
            self.schedule_table.setItem(row, 0, l_num_item)
            
            for col in range(1, 5):
                empty_item = QTableWidgetItem("")
                empty_item.setFlags(empty_item.flags() & ~Qt.ItemIsEditable)
                empty_item.setTextAlignment(Qt.AlignCenter)
                self.schedule_table.setItem(row, col, empty_item)

    def load_groups_for_schedule(self): # выбор элемента для загрузки групп
        self.load_groups_into_combo(self.schedule_group_combo) # в скобках указан элемент для подстановки

    def load_subject_name_for_schedule(self):
        try:
            cursor = self.conn.cursor()
            
            query = """
                select
                    s.subject_name
                from name_class n_c
                inner join subj_teachers s_t on s_t.id_name_class = n_c.id_name_class
                inner join subject s on s.id_subject = s_t.id_subject
                where n_c.id_name_class = ?
                order by n_c.num, n_c.letter
            """
            cursor.execute(query, self.schedule_group_combo.currentData())
            groups_data = cursor.fetchall()
            
            if groups_data:
                for group in groups_data:
                    subject_name = group[0]
                    self.schedule_subject.setText(subject_name)
            else:
                self.schedule_subject.setText("Нет предмета")
                
            cursor.close()
            
        except Exception as e:
            self.schedule_subject.clear()
            self.schedule_subject.setText(f"Ошибка загрузки: {str(e)}")

    def load_teachers_for_schedule(self):
        self.teacher_combo.clear()
        self.teacher_combo.addItems(["Выберите преподавателя"])
        if self.schedule_group_combo.currentIndex() > 0:
            try:
                cursor = self.conn.cursor()
                
                query = """
                    select
                        u.id_user,
                        u.surname + ' ' + u.[name] + ' ' + u.patronymic as fio
                    from users u
                    inner join subj_teachers s_t on s_t.id_user = u.id_user
                    inner join subject s on s.id_subject = s_t.id_subject
                    where s.subject_name = ?
                """
                cursor.execute(query, self.schedule_subject.text())
                teachers_data = cursor.fetchall()
                
                if teachers_data:
                    for group in teachers_data:
                        id_user = group[0]
                        fio = group[1]
                        self.teacher_combo.addItem(fio, id_user)
                else:
                    self.teacher_combo.setText("Нет преподавателей")
                    
                cursor.close()
                
            except Exception as e:
                self.teacher_combo.clear()
                self.teacher_combo.setText(f"Ошибка загрузки: {str(e)}")

    def load_cabinets_for_schedule(self):
        try:
            cursor = self.conn.cursor()
            
            query = """
                select
                    id_cabinet,
                    num
                from cabinet
                order by num
            """
            cursor.execute(query)
            cabinets_data = cursor.fetchall()
            
            if cabinets_data:
                for group in cabinets_data:
                    id_cabinet = group[0]
                    cabinet_name = group[1]
                    self.cabinet_combo.addItem(cabinet_name, id_cabinet)
            else:
                self.schedule_subject.setText("Нет кабинетов")
                
            cursor.close()
            
        except Exception as e:
            self.schedule_subject.clear()
            self.schedule_subject.setText(f"Ошибка загрузки: {str(e)}")


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
        self.surname_edit.setMaxLength(30)
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
        self.name_edit.setMaxLength(30)
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
        self.patronymic_edit.setMaxLength(30)
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