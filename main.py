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

uname = "youruser"
pswd = "password"
driver = "{ODBC Driver 17 for SQL Server}"
server = "DESKTOP-Q4NUJUS"
database = "diary"
database1 = "diary_pd"

# conn = pyodbc.connect(
#     'DRIVER=' + driver + ';SERVER=' + server + "\\MSSQLSERVER02" +
#     ';DATABASE=' + database + ';UID=' + uname + ';PWD=' + pswd)

conn = pyodbc.connect(
    'DRIVER=' + driver + ';SERVER=' + server + "\\MSSQLSERVER02" +
    ';DATABASE=' + database1 + ';Trusted_Connection=yes;' + 'TrustServerCertificate=yes;')


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        central_widget = QWidget()

        self.setWindowTitle("Авторизация")
        self.setFixedSize(600, 400)
        self.setCentralWidget(central_widget)
        self.setStyleSheet("background-color: #f0f0f0;")

        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # главная надпись
        title = QLabel("электронный дневник")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #333;
        """)
        main_layout.addStretch(1)
        main_layout.addWidget(title)
        main_layout.addStretch(2)

        # для вставки элементов логина и пароля
        auth_widget = QWidget()
        auth_layout = QVBoxLayout()
        auth_widget.setLayout(auth_layout)
        main_layout.addWidget(auth_widget, alignment=Qt.AlignCenter)
        main_layout.addStretch(1)

        input_style = """
            border-radius: 5px;
            border: 2px solid #585858;
            padding: 5px;
            font-size: 12px;
        """ # ввод текста в элементы

        # логин
        login_label = QLabel("Логин:")
        login_label.setStyleSheet("""
            font-size: 12px;
            font: bold;
            color: black;
            font-family: Roboto;
        """)
        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("Введите логин")
        self.login_input.setStyleSheet(input_style)
        self.login_input.setFixedSize(300, 35)

        # пароль
        pswd_label = QLabel("Пароль:")
        pswd_label.setStyleSheet("""
            font-size: 12px;
            font: bold;
            color: black;
            font-family: Roboto;            
        """)
        self.pswd_input = QLineEdit()
        self.pswd_input.setPlaceholderText("Введите пароль")
        self.pswd_input.setStyleSheet(input_style)
        self.pswd_input.setEchoMode(QLineEdit.Password)
        self.pswd_input.setFixedSize(300, 35)

        # добавление в аутентификацию
        auth_layout.addWidget(login_label)
        auth_layout.addWidget(self.login_input)
        auth_layout.setSpacing(10)
        auth_layout.addWidget(pswd_label)
        auth_layout.addWidget(self.pswd_input)
        auth_layout.setSpacing(10)

        # ошибка 
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: red;")
        self.error_label.setAlignment(Qt.AlignCenter)
        auth_layout.addWidget(self.error_label)

        # кнопка входа
        self.auth_button = QPushButton("Войти")
        self.auth_button.setFixedSize(200, 50)
        self.auth_button.setStyleSheet("""
            QPushButton {
                background-color: #e2734d;
                color: white;
                border-radius: 5px;
                font-size: 18px;
                font: bold;
            }
            QPushButton:hover {
                background-color: #e38a6b;
            }
            QPushButton:pressed {
                background-color: #cf6642;
            }
        """)
        self.auth_button.clicked.connect(self.check_)
        self.login_input.returnPressed.connect(self.check_)
        self.pswd_input.returnPressed.connect(self.check_)
        main_layout.addWidget(self.auth_button, alignment=Qt.AlignCenter)
        main_layout.addStretch(2)

    def hash_password(self, password):
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    def check_(self):
        login = self.login_input.text()
        pswd = self.pswd_input.text()
        self.error_label.setText("")

        if not login or not pswd:
            self.error_label.setText("Введите логин и пароль")
            return
        
        try:
            cursor = conn.cursor()

            hashed_pswd = self.hash_password(pswd)

            query = ("""select u.id_user, u.surname, left(u.name, 1) + '.', left(u.patronymic, 1) + '.', u.id_role
                from users u 
                inner join role r ON u.id_role = r.id_role 
                where u.login = ? and u.password = ? and u.is_active = 1
            """)

            cursor.execute(query, (login, hashed_pswd))
            user_data = cursor.fetchone()

            if user_data:
                id_user = user_data[0]
                surname = user_data[1]
                name = user_data[2]
                patronymic = user_data[3]
                id_role = user_data[4]
                
                fio = f"{surname} {name} {patronymic}".strip()
                
                if id_role == 1: # ученик
                    self.open_main_menu_for_student(id_user, fio)
                if id_role == 2: # преподаватель
                    self.open_main_menu_for_teacher(id_user, fio)
                if id_role == 3: # администратор
                    self.open_main_menu_for_admin(id_user, fio)
                    
            if login == "123" and pswd == "123":
                id_user = 1
                fio = "ученик"

                self.open_main_menu_for_student(id_user, fio)

            elif login == "1" and pswd == "1":
                id_user = 2
                fio = "преподаватель"

                self.open_main_menu_for_teacher(id_user, fio)

            elif login == "admin" and pswd == "admin":
                id_user = 3
                fio = "администратор"

                self.open_main_menu_for_admin(id_user, fio)

            else:
                self.error_label.setText("Неверный логин или пароль")
            
            cursor.close()
            
        except Exception as e:
            self.error_label.setText(f"Ошибка при аутентификации: {str(e)}")
    
    def open_main_menu_for_student(self, id_user, fio): # главное меню для ученика
        self.close()

        self.main_menu_student = MainMenuStudent(id_user, fio)
        self.main_menu_student.show()

    def open_main_menu_for_teacher(self, id_user, fio): #
        self.close()

        self.main_menu_teacher = MainMenuTeacher(id_user, fio)
        self.main_menu_teacher.show()

    def open_main_menu_for_admin(self, id_user, fio):
        self.close()

        self.main_menu_admin = MainMenuAdmin(id_user, fio)
        self.main_menu_admin.show()

class MainMenuStudent(QMainWindow): # главное меню для ученика
    def __init__(self, id_user = None, fio = None):
        super().__init__()
        self.id_user = id_user
        self.fio = fio

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

        # расположение элементов
        main_layout_h = QHBoxLayout() # основная группа
        group_button_layout = QVBoxLayout() # группа для кнопок
        self.content_layout_v = QVBoxLayout() # группа для расписания/посещаемости/заданий/тестов/успеваемости
        main_layout_h.addLayout(group_button_layout)
        main_layout_h.addStretch(3)
        main_layout_h.addLayout(self.content_layout_v)
        main_layout_h.addStretch(1)
        main_layout.addLayout(main_layout_h)

        group_button_layout.addStretch(1)

        # кнопка посещаемости
        self.button_attendance = QPushButton("Посещаемость")
        self.button_attendance.setFixedSize(250, 40)
        self.button_attendance.setStyleSheet("""
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
        self.button_attendance.clicked.connect(self.show_attendance)
        group_button_layout.addWidget(self.button_attendance, alignment=Qt.AlignLeft)
        group_button_layout.addSpacing(5)

        # кнопка задания
        self.button_homework = QPushButton("Задания")
        self.button_homework.setFixedSize(250, 40)
        self.button_homework.setStyleSheet("""
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
        self.button_homework.clicked.connect(self.show_homework)
        group_button_layout.addWidget(self.button_homework, alignment=Qt.AlignLeft)
        group_button_layout.addSpacing(5)

        # кнопка тесты
        self.button_tests = QPushButton("Тесты")
        self.button_tests.setFixedSize(250, 40)
        self.button_tests.setStyleSheet("""
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
        self.button_tests.clicked.connect(self.show_tests)
        group_button_layout.addWidget(self.button_tests, alignment=Qt.AlignLeft)
        group_button_layout.addSpacing(5)

        # кнопка успеваемость
        self.button_stats = QPushButton("Успеваемость")
        self.button_stats.setFixedSize(250, 40)
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
        self.button_stats.clicked.connect(self.show_grades)
        group_button_layout.addWidget(self.button_stats, alignment=Qt.AlignLeft)
        group_button_layout.addSpacing(5)

        # кнопка расписания
        self.button_schedule = QPushButton("Расписание")
        self.button_schedule.setFixedSize(250, 40)
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

        group_button_layout.addStretch(2)

        self.schedule()
        self.attendance()
        self.homework()
        self.grades()
        self.tests()

        self.show_schedule()

        main_layout.addStretch(1)

    def logout(self): # выход из учетки
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()

    def schedule(self): # расписание
        self.schedule_widget = QWidget()
        schedule_layout = QVBoxLayout()
        self.schedule_widget.setLayout(schedule_layout)

        schedule_label = QLabel("Занятия на текущей неделе:")
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
        # content_layout_v.addStretch(1)

        # окно для занятий
        self.schedule_list = QListWidget()
        self.schedule_list.setStyleSheet("""
            QListWidget {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 10px;
                font-family: Roboto;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #eee;
            }
            QListWidget::item:last {
                border-bottom: none;
            }
        """)
        self.schedule_list.setFixedSize(400, 400)
        schedule_layout.addWidget(self.schedule_list)

        self.load_schedule()

        # print(user_id)

    def attendance(self): # посещаемость
        self.attendance_widget = QWidget()
        attendance_layout = QVBoxLayout()
        self.attendance_widget.setLayout(attendance_layout)

        attendance_label = QLabel("Посещаемость занятий:")
        attendance_label.setAlignment(Qt.AlignLeft)
        attendance_label.setStyleSheet("""
            font-size: 22px;
            font-weight: bold;
            font-family: Roboto;
            color: #333;
            margin-top: 20px;
            margin-bottom: 10px;
        """)
        attendance_layout.addWidget(attendance_label)

        # окно для посещаемости
        self.attendance_table = QListWidget()
        self.attendance_table.setStyleSheet("""
            QListWidget {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 10px;
                font-family: Roboto;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #eee;
            }
            QListWidget::item:last {
                border-bottom: none;
            }
        """)
        self.attendance_table.setFixedSize(400, 400)
        attendance_layout.addWidget(self.attendance_table)

    def homework(self): # домашние задания
        self.homework_widget = QWidget()
        homework_layout = QVBoxLayout()
        self.homework_widget.setLayout(homework_layout)

        homework_label = QLabel("Домашние задания:")
        homework_label.setAlignment(Qt.AlignLeft)
        homework_label.setStyleSheet("""
            font-size: 22px;
            font-weight: bold;
            font-family: Roboto;
            color: #333;
            margin-top: 20px;
            margin-bottom: 10px;
        """)
        homework_layout.addWidget(homework_label)

        # окно для дз
        self.homework_table = QListWidget()
        self.homework_table.setStyleSheet("""
            QListWidget {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 10px;
                font-family: Roboto;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #eee;
            }
            QListWidget::item:last {
                border-bottom: none;
            }
        """)
        self.homework_table.setFixedSize(400, 400)
        homework_layout.addWidget(self.homework_table)

    def grades(self): # успеваемость (оценки)
        self.grades_widget = QWidget()
        grades_layout = QVBoxLayout()
        self.grades_widget.setLayout(grades_layout)

        grades_label = QLabel("Успеваемость:")
        grades_label.setAlignment(Qt.AlignLeft)
        grades_label.setStyleSheet("""
            font-size: 22px;
            font-weight: bold;
            font-family: Roboto;
            color: #333;
            margin-top: 20px;
            margin-bottom: 10px;
        """)
        grades_layout.addWidget(grades_label)

        # окно для оценок
        self.grades_table = QListWidget()
        self.grades_table.setStyleSheet("""
            QListWidget {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 10px;
                font-family: Roboto;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #eee;
            }
            QListWidget::item:last {
                border-bottom: none;
            }
        """)
        self.grades_table.setFixedSize(400, 400)
        grades_layout.addWidget(self.grades_table)

    def tests(self): # тесты
        self.tests_widget = QWidget()
        tests_layout = QVBoxLayout()
        self.tests_widget.setLayout(tests_layout)

        tests_label = QLabel("Тесты:")
        tests_label.setAlignment(Qt.AlignLeft)
        tests_label.setStyleSheet("""
            font-size: 22px;
            font-weight: bold;
            font-family: Roboto;
            color: #333;
            margin-top: 20px;
            margin-bottom: 10px;
        """)
        tests_layout.addWidget(tests_label)

        # окно для тестов
        self.tests_table = QListWidget()
        self.tests_table.setStyleSheet("""
            QListWidget {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 10px;
                font-family: Roboto;
                outline: 0;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #eee;
                background-color: #f8f9fa;
                border-radius: 3px;
                margin: 2px;
            }
            QListWidget::item:selected {
                background-color: #e8f4fc;
                color: #000;
            }                        
            QTableWidget::item:focus {
                outline: none;
                border: none;
            }
        """)
        self.tests_table.setFixedSize(400, 400)
        tests_layout.addWidget(self.tests_table)
        self.tests_table.itemDoubleClicked.connect(self.open_test_window)

    def show_schedule(self): # отображение расписания
        self.clear_content_layout()

        self.content_layout_v.addWidget(self.schedule_widget)

        self.load_schedule()

    def show_attendance(self): # отображение посещаемости
        self.clear_content_layout()

        self.content_layout_v.addWidget(self.attendance_widget)

        self.load_attendance()

    def show_homework(self): # отображение дз
        self.clear_content_layout()

        self.content_layout_v.addWidget(self.homework_widget)

        self.load_homework()

    def show_grades(self): # отображение оценок
        self.clear_content_layout()

        self.content_layout_v.addWidget(self.grades_widget)

        self.load_grades()

    def show_tests(self): # отображение тестов
        self.clear_content_layout()

        self.content_layout_v.addWidget(self.tests_widget)

        self.load_tests()

    def clear_content_layout(self): # удаление информации из content_layout_v для последующей вставки другого контента
        for i in reversed(range(self.content_layout_v.count())):
            widget = self.content_layout_v.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

    def load_schedule(self): # загрузка расписания
        try:
            cursor = conn.cursor()

            query = ("""
                select 
                    s.day_of_week, sub.subject_name, nc.num, nc.letter,
                    u.surname + ' ' + LEFT(u.name, 1) + '.' + LEFT(u.patronymic, 1) + '.' as teacher_name,
                    cab.num
                from schedule s
                inner join class c ON s.id_class = c.id_class
                inner join name_class nc ON c.id_name_class = nc.id_name_class
                inner join subject sub ON s.id_subject = sub.id_subject
                inner join users u ON s.id_user = u.id_user
                inner join cabinet cab on cab.id_cabinet = s.id_cabinet
                where c.id_class in (
                    select c2.id_class 
                    from class c2 
                    inner join subj_students ss on c2.id_class = ss.id_user 
                    where ss.id_user = ?
                )
                order by 
                    case s.day_of_week
                        when 'Понедельник' then 1
                        when 'Вторник' then 2
                        when 'Среда' then 3
                        when 'Четверг' then 4
                        when 'Пятница' then 5
                        when 'Суббота' then 6
                        when 'Воскресенье' then 7
                        else 8
                    end,
                    s.lesson_num
            """)

            cursor.execute(query, (self.id_user))
            schedule_data = cursor.fetchall()

            self.schedule_list.clear()

            if schedule_data:
                current_day = None
                
                for lesson in schedule_data:
                    day_of_week = lesson[0]
                    subject_name = lesson[1]
                    class_num = lesson[2]
                    class_letter = lesson[3]
                    teacher_name = lesson[4]
                    cabinet = lesson[5]

                    class_group = f"{class_num}{class_letter}"
                    
                    lesson_text = f"{subject_name}, {class_group}, {teacher_name}, {cabinet}"
                    
                    if day_of_week != current_day:
                        current_day = day_of_week
                        day_header = QListWidgetItem(f"{day_of_week}:")
                        day_header.setFlags(Qt.NoItemFlags)
                        day_header.setFont(QFont("Roboto", 10, QFont.Bold))
                        day_header.setForeground(QColor("#2c3e50"))
                        self.schedule_list.addItem(day_header)
                    
                    lesson_item = QListWidgetItem(f"  {lesson_text}")
                    lesson_item.setFlags(Qt.NoItemFlags)
                    self.schedule_list.addItem(lesson_item)

            else:
                no_schedule_item = QListWidgetItem("Расписание на текущую неделю отсутствует")
                no_schedule_item.setTextAlignment(Qt.AlignCenter)
                no_schedule_item.setFlags(Qt.NoItemFlags)
                no_schedule_item.setForeground(QColor("#7f8c8d"))
                self.schedule_list.addItem(no_schedule_item)
                
            cursor.close()

        except Exception as e:
            error_item = QListWidgetItem(f"Ошибка при загрузке расписания: {str(e)}")
            error_item.setFlags(Qt.NoItemFlags)
            error_item.setForeground(QColor("#e74c3c"))
            self.schedule_list.addItem(error_item)

    def load_attendance(self): # загрузка посещаемости
        try:
            cursor = conn.cursor()

            query = ("""
                select l.date, sub.subject_name, t_att.title as attendance_status,
                    u.surname + ' ' + left(u.name, 1) + '.' + left(u.patronymic, 1) + '.' as teacher_name
                from lesson l
                inner join subject sub on sub.id_subject = l.id_subject
                inner join attendance a on a.id_lesson = l.id_lesson
                inner join type_attendance t_att on t_att.id_type_att = a.id_type_att
                inner join subj_teachers s_t on s_t.id_subject = sub.id_subject
                inner join users u on u.id_user = s_t.id_user
                where a.id_user = ?
                order by l.date desc
            """)

            cursor.execute(query, (self.id_user))
            attendance_data = cursor.fetchall()

            self.attendance_table.clear()

            if attendance_data:
                current_date = None
                
                for record in attendance_data:
                    date = record[0]
                    subject_name = record[1]
                    attendance_status = record[2]
                    teacher_name = record[3]

                    day_of_week = date.strftime("%A")
                    day_list = {
                        'Monday': 'Понедельник',
                        'Tuesday': 'Вторник', 
                        'Wednesday': 'Среда',
                        'Thursday': 'Четверг',
                        'Friday': 'Пятница',
                        'Saturday': 'Суббота',
                        'Sunday': 'Воскресенье'
                    }
                    day = day_list.get(day_of_week, day_of_week)

                    formatted_date = date.strftime("%d.%m.%Y")
                    
                    # цвет для статуса посещаемости
                    if "присутствовал" in attendance_status.lower():
                        status_color = "#27ae60"  # присутствовал
                    elif "отсутствовал" in attendance_status.lower():
                        status_color = "#e74c3c"  # отсутствовал без причин
                    elif "болезнь" or "уважительная причина" or "пропуск по семейным обстоятельствам" in attendance_status.lower():
                        status_color = "#f39c12"  # отсутствовал по причинам
                    
                    attendance_text = f"{formatted_date} ({day}) - {subject_name}"
                    teacher_text = f"Преподаватель: {teacher_name}"
                    status_text = f"Статус: {attendance_status}"
                    
                    date_item = QListWidgetItem(f" {attendance_text}")
                    date_item.setFlags(Qt.NoItemFlags)
                    date_item.setFont(QFont("Roboto", 9, QFont.Bold))
                    date_item.setForeground(QColor("#2c3e50"))
                    self.attendance_table.addItem(date_item)
                    
                    teacher_item = QListWidgetItem(f"   {teacher_text}")
                    teacher_item.setFlags(Qt.NoItemFlags)
                    teacher_item.setFont(QFont("Roboto", 8))
                    self.attendance_table.addItem(teacher_item)
                    
                    status_item = QListWidgetItem(f"   {status_text}")
                    status_item.setFlags(Qt.NoItemFlags)
                    status_item.setFont(QFont("Roboto", 8))
                    status_item.setForeground(QColor(status_color))
                    self.attendance_table.addItem(status_item)
                    
                    separator_item = QListWidgetItem("")
                    separator_item.setFlags(Qt.NoItemFlags)
                    self.attendance_table.addItem(separator_item)

            else:
                no_attendance_item = QListWidgetItem("Данные о посещаемости отсутствуют")
                no_attendance_item.setTextAlignment(Qt.AlignCenter)
                no_attendance_item.setFlags(Qt.NoItemFlags)
                no_attendance_item.setForeground(QColor("#7f8c8d"))
                self.attendance_table.addItem(no_attendance_item)
                
            cursor.close()

        except Exception as e:
            error_item = QListWidgetItem(f"Ошибка при загрузке посещаемости: {str(e)}")
            error_item.setFlags(Qt.NoItemFlags)
            error_item.setForeground(QColor("#e74c3c"))
            self.attendance_table.addItem(error_item)

    def load_homework(self): # загрузка заданий
        try:
            cursor = conn.cursor()

            query = ("""
                select subject.subject_name, exercise.exercise, exercise.upload, exercise.deadline
                from subject
                inner join exercise on exercise.id_subject = subject.id_subject
                inner join subj_students on subj_students.id_subject = subject.id_subject
                where subj_students.id_user = ?
                order by exercise.deadline desc
            """)

            cursor.execute(query, (self.id_user))
            homework_data = cursor.fetchall()

            self.homework_table.clear()

            if homework_data:
                current_date = None

                for record in homework_data:
                    subject_name = record[0]
                    exercise = record[1]
                    upload = record[2]
                    deadline = record[3]

                    formatted_upload = upload.strftime("%d.%m.%Y")
                    formatted_deadline = deadline.strftime("%d.%m.%Y")

                    date_text = f"Задано: {formatted_upload} \n   Срок сдачи: {formatted_deadline}"

                    name_item = QListWidgetItem(f" {subject_name}")
                    name_item.setFlags(Qt.NoItemFlags)
                    name_item.setFont(QFont("Roboto", 9, QFont.Bold))
                    name_item.setForeground(QColor("#2c3e50"))
                    self.homework_table.addItem(name_item)

                    date_item = QListWidgetItem(f"   {date_text}")
                    date_item.setFlags(Qt.NoItemFlags)
                    date_item.setFont(QFont("Roboto", 8))
                    self.homework_table.addItem(date_item)

                    exercise_item = QListWidgetItem(f"   {exercise}")
                    exercise_item.setFlags(Qt.NoItemFlags)
                    exercise_item.setFont(QFont("Roboto", 8))
                    self.homework_table.addItem(exercise_item)

                    separator_item = QListWidgetItem("")
                    separator_item.setFlags(Qt.NoItemFlags)
                    self.homework_table.addItem(separator_item)

            else:
                no_homework_item = QListWidgetItem("Данные о заданиях отсутствуют")
                no_homework_item.setTextAlignment(Qt.AlignCenter)
                no_homework_item.setFlags(Qt.NoItemFlags)
                no_homework_item.setForeground(QColor("#7f8c8d"))
                self.homework_table.addItem(no_homework_item)
                
            cursor.close()

        except Exception as e:
            error_item = QListWidgetItem(f"Ошибка при загрузке домашних заданий: {str(e)}")
            error_item.setFlags(Qt.NoItemFlags)
            error_item.setForeground(QColor("#e74c3c"))
            self.homework_table.addItem(error_item)

    def load_grades(self): # загрузка оценок
        try:
            cursor = conn.cursor()

            query = ("""
                select subject.subject_name, lesson.date, grade.grade, t_g.title
                from lesson
                inner join subject on subject.id_subject = lesson.id_subject
                inner join grade on grade.id_lesson = lesson.id_lesson
                inner join type_grade t_g on t_g.id_type_gr = grade.id_type_gr
                where grade.id_user = ?
                order by lesson.date
            """)

            cursor.execute(query, (self.id_user))
            grades_data = cursor.fetchall()

            self.grades_table.clear()

            if grades_data:
                current_date = None

                for record in grades_data:
                    subject_name = record[0]
                    date = record[1]
                    grade = record[2]
                    title = record[3]

                    formatted_date = date.strftime("%d.%m.%Y")
                    formatted_grade = str(grade)

                    if grade == None:
                        formatted_grade = "нет оценки"

                    date_text = f"Дата урока: {formatted_date}"

                    name_item = QListWidgetItem(f" {subject_name}: {formatted_grade}")
                    name_item.setFlags(Qt.NoItemFlags)
                    name_item.setFont(QFont("Roboto", 9, QFont.Bold))
                    name_item.setForeground(QColor("#2c3e50"))
                    self.grades_table.addItem(name_item)

                    date_item = QListWidgetItem(f"   {date_text}")
                    date_item.setFlags(Qt.NoItemFlags)
                    date_item.setFont(QFont("Roboto", 8))
                    self.grades_table.addItem(date_item)

                    title_item = QListWidgetItem(f"   {title}")
                    title_item.setFlags(Qt.NoItemFlags)
                    title_item.setFont(QFont("Roboto", 8))
                    self.grades_table.addItem(title_item)

                    separator_item = QListWidgetItem("")
                    separator_item.setFlags(Qt.NoItemFlags)
                    self.grades_table.addItem(separator_item)

            else:
                no_grades_item = QListWidgetItem("Данные об оценках отсутствуют")
                no_grades_item.setTextAlignment(Qt.AlignCenter)
                no_grades_item.setFlags(Qt.NoItemFlags)
                no_grades_item.setForeground(QColor("#7f8c8d"))
                self.grades_table.addItem(no_grades_item)
                
            cursor.close()

        except Exception as e:
            error_item = QListWidgetItem(f"Ошибка при загрузке домашних заданий: {str(e)}")
            error_item.setFlags(Qt.NoItemFlags)
            error_item.setForeground(QColor("#e74c3c"))
            self.grades_table.addItem(error_item)

    def load_tests(self): # загрузка тестов
        try:
            cursor = conn.cursor()

            query = ("""
                declare @id_user int = ?;
                select t_n.name, t.upload, t.deadline, 'Вопросов: ' + 
                cast(count(distinct q_a.id_question) as varchar(2)) as questions, 
                convert(varchar, s_t.grade) as grade, 
                convert(varchar, s_t.grade_percent) as grade_percent, 
                t.id_test
                from test_name t_n
                inner join test t on t.id_name = t_n.id_name
                left join test_content t_c on t_c.id_test = t.id_test
                left join question_answer q_a on q_a.id_que_ans = t_c.id_que_ans
                left join solved_tests s_t on s_t.id_test = t.id_test and s_t.id_user = @id_user
                where id_name_class = (select id_name_class from class where id_user = @id_user)
                group by t_n.name, t.upload, t.deadline, t.id_test, s_t.grade, s_t.grade_percent
                order by deadline desc, upload desc, t_n.name desc
            """)

            cursor.execute(query, (self.id_user))
            tests_data = cursor.fetchall()

            self.tests_table.clear()

            if tests_data:
                current_date = None

                for record in tests_data:
                    test_name = record[0]
                    upload = record[1]
                    deadline = record[2]
                    questions = record[3]
                    grade = record[4]
                    grade_percent = record[5]
                    test_id = record[6]

                    formatted_upload = upload.strftime("%d.%m.%Y")
                    formatted_deadline = deadline.strftime("%d.%m.%Y")

                    if grade == None:
                        grade = "Нет оценки"
                    if grade_percent == None:
                        grade_percent = "0"

                    date_text = (
                        f"Тест открыт с: {formatted_upload}\n"
                        f"Срок сдачи: {formatted_deadline}"
                    )

                    name = (
                        f"{test_name}\n{grade} "
                        f"({grade_percent}%)"
                    )

                    questions_sum = (f"{questions}")

                    date_item = (f"{date_text}")

                    test_item = (
                        f"{name}\n"
                        f"{questions_sum}\n"
                        f"{date_item}"
                    )

                    test_list = QListWidgetItem(test_item)
                    self.tests_table.addItem(test_list)

                    test_list.setData(Qt.UserRole, test_id)

            else:
                no_tests_item = QListWidgetItem("Данные о тестах отсутствуют")
                no_tests_item.setTextAlignment(Qt.AlignCenter)
                no_tests_item.setFlags(Qt.NoItemFlags)
                no_tests_item.setForeground(QColor("#7f8c8d"))
                self.tests_table.addItem(no_tests_item)
                
            cursor.close()

        except Exception as e:
            error_item = QListWidgetItem(f"Ошибка при загрузке тестов: {str(e)}")
            error_item.setFlags(Qt.NoItemFlags)
            error_item.setForeground(QColor("#e74c3c"))
            self.tests_table.addItem(error_item)

    def open_test_window(self, item):
        test_id = item.data(Qt.UserRole)
        
        if not test_id:
            QMessageBox.warning(self, "Ошибка", "Не удалось получить информацию о тесте")
            return
        
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT COUNT(*) FROM solved_tests 
                WHERE id_test = ? AND id_user = ?
            """, (test_id, self.id_user))
            
            result = cursor.fetchone()
            if result[0] > 0:
                reply = QMessageBox(
                    QMessageBox.Question,
                    "Тест",
                    "Пройти тест заново?",
                    QMessageBox.Yes | QMessageBox.No
                )
                yes_button = reply.button(QMessageBox.Yes)
                no_button = reply.button(QMessageBox.No)
                if yes_button:
                    yes_button.setText("Да")
                if no_button:
                    no_button.setText("Нет")
                reply.setDefaultButton(QMessageBox.No)

                if reply.exec_() == QMessageBox.No:
                    return
            
            cursor.execute("""
                SELECT tn.name 
                FROM test t
                INNER JOIN test_name tn ON tn.id_name = t.id_name
                WHERE t.id_test = ?
            """, (test_id,))
            
            test_data = cursor.fetchone()
            test_name = test_data[0] if test_data else "Без названия"
            cursor.close()
            
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при проверке теста: {str(e)}")
            return
        
        self.test_window = TestExecutionWindow(test_id, self.id_user, test_name)
        result = self.test_window.exec_()
        self.load_tests()
        
        if hasattr(self, 'tests_widget') and self.tests_widget.isVisible():
            self.load_tests()


class TestExecutionWindow(QDialog):
    def __init__(self, test_id=None, user_id=None, test_name=None):
        super().__init__()
        self.test_id = test_id
        self.user_id = user_id
        self.test_name = test_name
        self.current_question = 0
        self.answers = {} # для хранения ответов
        
        self.setWindowTitle(f"{test_name}")
        self.setFixedSize(500, 400)
        self.setModal(True)
        self.setWindowFlags(Qt.Dialog | Qt.WindowTitleHint)
        
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        top_layout = QHBoxLayout()
        main_layout.addLayout(top_layout)

        self.question_num = QLabel("Вопрос 1")
        self.question_num.setStyleSheet("""
            font-family: Roboto; 
            color: #333;
            font-size: 14pt;
        """)
        top_layout.addWidget(self.question_num, alignment=Qt.AlignLeft)

        # кнопка выхода из теста
        cancel_button = QPushButton("Выход")
        cancel_button.setFixedSize(80, 35)
        cancel_button.setStyleSheet("""
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
        cancel_button.clicked.connect(self.cancel_test)
        top_layout.addWidget(cancel_button, alignment=Qt.AlignRight)

        # текущий вопрос
        self.question_container = QWidget()
        self.question_layout = QVBoxLayout(self.question_container)
        main_layout.addWidget(self.question_container)
        
        progress_layout = QHBoxLayout()
        self.progress_label = QLabel("Вопрос 1 из 1")
        self.progress_label.setStyleSheet("font-size: 12px; color: #7f8c8d;")
        progress_layout.addWidget(self.progress_label)
        progress_layout.addStretch()
        main_layout.addLayout(progress_layout)

        # группа для кнопок
        buttons_layout = QHBoxLayout()

        # предыдущий вопрос
        self.prev_button = QPushButton("Предыдущий")
        self.prev_button.setFixedSize(120, 35)
        self.prev_button.setStyleSheet("""
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
            QPushButton:disabled {
                background-color: #bdc3c7;
                color: #7f8c8d;
            }
        """)
        self.prev_button.clicked.connect(self.show_previous_question)
        buttons_layout.addWidget(self.prev_button)
        self.prev_button.setEnabled(False)
        
        # cледующий вопрос
        self.next_button = QPushButton("Следующий")
        self.next_button.setFixedSize(120, 35)
        self.next_button.setStyleSheet("""
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
            QPushButton:disabled {
                background-color: #bdc3c7;
                color: #7f8c8d;
            }
        """)
        self.next_button.clicked.connect(self.show_next_question)
        buttons_layout.addWidget(self.next_button)
        
        # кнопка завершения теста
        submit_button = QPushButton("Завершить тест")
        submit_button.setFixedSize(150, 35)
        submit_button.setStyleSheet("""
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
        submit_button.clicked.connect(self.submit_test)
        buttons_layout.addWidget(submit_button)
        
        main_layout.addLayout(buttons_layout)
        
        self.questions_data = []
        self.load_test_questions()
        
    def load_test_questions(self):
        try:
            cursor = conn.cursor()
            
            query = ("""
                SELECT DISTINCT 
                    tq.id_question,
                    tq.text as question_text
                FROM test t
                INNER JOIN test_content tc ON tc.id_test = t.id_test
                INNER JOIN question_answer qa ON qa.id_que_ans = tc.id_que_ans
                INNER JOIN test_question tq ON tq.id_question = qa.id_question
                WHERE t.id_test = ?
                ORDER BY tq.id_question
            """)
            
            cursor.execute(query, (self.test_id,))
            questions = cursor.fetchall()
            
            if not questions:
                QMessageBox.warning(self, "Ошибка", "В тесте нет вопросов")
                self.close()
                return
            
            for question in questions:
                question_id = question[0]
                question_text = question[1]
                
                answers_query = ("""
                    SELECT 
                        ta.id_answer,
                        ta.answer,
                        ta.is_true
                    FROM test_answer ta
                    WHERE ta.id_question = ?
                    ORDER BY ta.id_answer
                """)

                cursor.execute(answers_query, (question_id,))
                answers = cursor.fetchall()
                
                correct_count = sum(1 for ans in answers if ans[2] == 1)
                
                question_data = {
                    'question_id': question_id,
                    'text': question_text,
                    'answers': answers,
                    'is_single_choice': correct_count == 1,
                    'correct_count': correct_count
                }
                
                self.questions_data.append(question_data)
                self.answers[question_id] = []
            
            cursor.close()

            self.show_current_question()
            
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при загрузке вопросов: {str(e)}")
            self.close()

    def show_current_question(self): # текущий вопрос
        for i in reversed(range(self.question_layout.count())): 
            self.question_layout.itemAt(i).widget().setParent(None)
        
        if self.current_question >= len(self.questions_data):
            return
        
        question_data = self.questions_data[self.current_question]
        question_id = question_data['question_id']

        self.question_num.setText(f"Вопрос {self.current_question + 1}")

        question_group = QGroupBox()
        question_group.setStyleSheet("""
            QGroupBox {
                font-size: 14px;
                font-weight: bold;
                color: #2c3e50;
                border-radius: 8px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                background-color: #3498db;
                color: white;
                border-radius: 3px;
            }
        """)
        
        group_layout = QVBoxLayout()

        # текст вопроса 
        question_label = QLabel(question_data['text'])
        question_label.setWordWrap(True)
        question_label.setStyleSheet("""
            font-size: 13px;
            color: #333;
            padding: 10px;
            background-color: #f8f9fa;
            border-radius: 5px;
            margin: 5px;
        """)
        group_layout.addWidget(question_label)

        self.answer_widgets = []
        saved_answers = self.answers.get(question_id, [])
        
        for j, answer in enumerate(question_data['answers']):
            answer_id = answer[0]
            answer_text = answer[1]
            is_correct = answer[2]
            
            if question_data['is_single_choice']:
                radio_button = QRadioButton(answer_text)
                radio_button.setStyleSheet("""
                    QRadioButton {
                        font-size: 12px;
                        color: #333;
                        spacing: 5px;
                        padding: 8px;
                        margin: 2px;
                        background-color: #f8f9fa;
                        border-radius: 3px;
                    }
                    QRadioButton:hover {
                        background-color: #e8f4fc;
                    }
                    QRadioButton::indicator {
                        width: 14px;
                        height: 14px;
                    }
                """)
                radio_button.answer_id = answer_id
                radio_button.is_correct = is_correct
                
                if answer_id in saved_answers:
                    radio_button.setChecked(True)
                
                group_layout.addWidget(radio_button)
                self.answer_widgets.append(radio_button)
            else:
                checkbox = QCheckBox(answer_text)
                checkbox.setStyleSheet("""
                    QCheckBox {
                        font-size: 12px;
                        color: #333;
                        spacing: 10px;
                        padding: 8px;
                        margin: 2px;
                        background-color: #f8f9fa;
                        border-radius: 3px;
                    }
                    QCheckBox:hover {
                        background-color: #e8f4fc;
                    }
                    QCheckBox::indicator {
                        width: 18px;
                        height: 18px;
                    }
                """)
                checkbox.answer_id = answer_id
                checkbox.is_correct = is_correct
                
                if answer_id in saved_answers:
                    checkbox.setChecked(True)
                
                group_layout.addWidget(checkbox)
                self.answer_widgets.append(checkbox)
        
        question_group.setLayout(group_layout)
        self.question_layout.addWidget(question_group)
        
        self.update_progress()
        
        self.update_navigation_buttons()

    def save_current_answers(self): # сохранение ответов
        if self.current_question >= len(self.questions_data):
            return
        
        question_data = self.questions_data[self.current_question]
        question_id = question_data['question_id']
        
        self.answers[question_id] = []
        
        for widget in self.answer_widgets:
            if isinstance(widget, QRadioButton) and widget.isChecked():
                self.answers[question_id].append(widget.answer_id)
                break
            elif isinstance(widget, QCheckBox) and widget.isChecked():
                self.answers[question_id].append(widget.answer_id)

    def show_previous_question(self): # предыдущий вопрос
        if self.current_question > 0:
            self.save_current_answers()
            
            self.current_question -= 1
            self.show_current_question()

    def show_next_question(self): # следующий вопрос
        if self.current_question < len(self.questions_data) - 1:
            self.save_current_answers()
            
            self.current_question += 1
            self.show_current_question()

    def update_progress(self):
        total = len(self.questions_data)
        current = self.current_question + 1
        self.progress_label.setText(f"Вопрос {current} из {total}")

    def update_navigation_buttons(self):
        # включение/выключение кнопки предыдущего вопроса
        self.prev_button.setEnabled(self.current_question > 0) 
        
        # включение/выключение кнопки следующего вопроса
        if self.current_question < len(self.questions_data) - 1:
            self.next_button.setText("Следующий")
            self.next_button.setEnabled(True)
        else:
            self.next_button.setText("Следующий")
            self.next_button.setEnabled(False)

    def cancel_test(self): # выход из теста
        self.save_current_answers()
        
        answered_count = sum(1 for answers in self.answers.values() if answers)
        total_questions = len(self.questions_data)
        
        reply = QMessageBox(
            QMessageBox.Warning,
            "Выход",
            f"Вы хотите выйти из теста?\n\n"
            f"Отвечено вопросов: {answered_count} из {total_questions}\n"
            f"Все неотвеченные вопросы будут засчитаны как 0 баллов.\n\n",
            QMessageBox.Yes | QMessageBox.No
        )
        yes_button = reply.button(QMessageBox.Yes)
        no_button = reply.button(QMessageBox.No)
        if yes_button:
            yes_button.setText("Да")
        if no_button:
            no_button.setText("Нет")
        reply.setDefaultButton(QMessageBox.No)
        
        if reply.exec_() == QMessageBox.Yes:
            self.save_partial_test_results()
            self.close()

    def save_partial_test_results(self):
        try:
            cursor = conn.cursor()
            
            total_questions = len(self.questions_data)
            correct_answers = 0
            
            for question_data in self.questions_data:
                question_id = question_data['question_id']
                selected_answers = self.answers.get(question_id, [])
                
                if not selected_answers:
                    continue
                
                if question_data['is_single_choice']:
                    if len(selected_answers) == 1:
                        selected_id = selected_answers[0]
                        for answer in question_data['answers']:
                            if answer[0] == selected_id and answer[2] == 1:
                                correct_answers += 1
                                break
                else:
                    if selected_answers:
                        correct_selected = 0
                        incorrect_selected = 0
                        
                        for answer in question_data['answers']:
                            answer_id = answer[0]
                            is_correct = answer[2]
                            
                            if is_correct and answer_id in selected_answers:
                                correct_selected += 1
                            elif not is_correct and answer_id in selected_answers:
                                incorrect_selected += 1
                        
                        if correct_selected == question_data['correct_count'] and incorrect_selected == 0:
                            correct_answers += 1
            
            if total_questions > 0:
                percentage = (correct_answers / total_questions) * 100
                percentage = max(0.0, min(100.0, percentage))
                
                if percentage >= 90:
                    grade = 5
                elif percentage >= 80:
                    grade = 4
                elif percentage >= 50:
                    grade = 3
                else:
                    grade = 2
            else:
                percentage = 0
                grade = 0
            
            percentage = round(percentage, 2)
            grade = round(grade, 2)
            
            if percentage > 99.99:
                percentage = 100
            
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id_attempt FROM solved_tests 
                WHERE id_user = ? AND id_test = ?
            """, (self.user_id, self.test_id))
            
            existing_attempt = cursor.fetchone()
            
            if existing_attempt:
                cursor.execute("""
                    UPDATE solved_tests 
                    SET grade = ?, grade_percent = ? 
                    WHERE id_attempt = ?
                """, (grade, percentage, existing_attempt[0]))
                action = "обновлены"
            else:
                cursor.execute("""
                    INSERT INTO solved_tests (id_user, id_test, grade, grade_percent)
                    VALUES (?, ?, ?, ?)
                """, (self.user_id, self.test_id, grade, percentage))
                action = "сохранены"
            
            conn.commit()
            cursor.close()
            
            QMessageBox.information(
                self,
                "Тест завершен",
                f"Результаты теста: {action}\n\n"
                f"Правильных ответов: {correct_answers} из {total_questions}\n"
                f"Процент выполнения: {percentage:.1f}%\n"
                f"Оценка: {grade}"
            )
            
        except Exception as e:
            QMessageBox.critical(
                self,
                "Ошибка сохранения",
                f"Не удалось сохранить результаты теста: {str(e)}"
            )
    
    def submit_test(self): # отправка теста
        self.save_current_answers()
        
        unanswered_questions = []
        for i, question_data in enumerate(self.questions_data):
            question_id = question_data['question_id']
            if not self.answers.get(question_id):
                unanswered_questions.append(i + 1)
        
        if unanswered_questions:
            if len(unanswered_questions) > 5:
                questions_text = f"{len(unanswered_questions)} вопросов"
            else:
                questions_text = ", ".join(map(str, unanswered_questions))
            
            reply = QMessageBox(
                QMessageBox.Question,
                "Предупреждение",
                f"Следующие вопросы не имеют ответа: {questions_text}\n\n"
                f"Вы уверены, что хотите завершить тест?",
                QMessageBox.Yes | QMessageBox.No
            )
            yes_button = reply.button(QMessageBox.Yes)
            no_button = reply.button(QMessageBox.No)
            if yes_button:
                yes_button.setText("Да")
            if no_button:
                no_button.setText("Нет")
            reply.setDefaultButton(QMessageBox.No)
            
            if reply.exec_() == QMessageBox.No:
                self.current_question = unanswered_questions[0] - 1
                self.show_current_question()
                return
        
        total_questions = len(self.questions_data)
        correct_answers = 0
        
        for question_data in self.questions_data:
            question_id = question_data['question_id']
            selected_answers = self.answers.get(question_id, [])
            
            if question_data['is_single_choice']:
                if len(selected_answers) == 1:
                    selected_id = selected_answers[0]
                    for answer in question_data['answers']:
                        if answer[0] == selected_id and answer[2] == 1:
                            correct_answers += 1
                            break
            else:
                if selected_answers:
                    correct_selected = 0
                    incorrect_selected = 0
                    
                    for answer in question_data['answers']:
                        answer_id = answer[0]
                        is_correct = answer[2]
                        
                        if is_correct and answer_id in selected_answers:
                            correct_selected += 1
                        elif not is_correct and answer_id in selected_answers:
                            incorrect_selected += 1
                    
                    if correct_selected == question_data['correct_count'] and incorrect_selected == 0:
                        correct_answers += 1
            
        if total_questions > 0: # оценка
            percentage = (correct_answers / total_questions) * 100
            percentage = max(0.0, min(100.0, percentage))
            
            if percentage >= 90:
                grade = 5
            elif percentage >= 80:
                grade = 4
            elif percentage >= 50:
                grade = 3
            else:
                grade = 2
        else:
            percentage = 0
            grade = 0

        percentage = round(percentage, 2)
        grade = round(grade, 2)
        
        if grade > 9.99:
            grade = 9.99
        
        if percentage > 99.99:
            percentage = 100
        
        # сохранение итогов
        try:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id_attempt FROM solved_tests 
                WHERE id_user = ? AND id_test = ?
            """, (self.user_id, self.test_id))
            
            existing_attempt = cursor.fetchone()
            
            if existing_attempt:
                cursor.execute("""
                    UPDATE solved_tests 
                    SET grade = ?, grade_percent = ? 
                    WHERE id_attempt = ?
                """, (grade, percentage, existing_attempt[0]))
                action = "обновлены"
            else:
                cursor.execute("""
                    INSERT INTO solved_tests (id_user, id_test, grade, grade_percent)
                    VALUES (?, ?, ?, ?)
                """, (self.user_id, self.test_id, grade, percentage))
                action = "сохранены"
            
            conn.commit()
            cursor.close()
            
            QMessageBox.information(
                self,
                "Тест завершен",
                f"Результаты теста: {action}\n\n"
                f"Правильных ответов: {correct_answers} из {total_questions}\n"
                f"Процент выполнения: {percentage:.1f}%\n"
                f"Оценка: {grade}"
            )
            
            self.close()
            
        except Exception as e:
            QMessageBox.critical(
                self,
                "Ошибка",
                f"Не удалось сохранить результаты теста: {str(e)}"
            )


class MainMenuTeacher(QMainWindow):
    def __init__(self, id_user = None, fio = None):
        super().__init__()
        self.id_user = id_user
        self.fio = fio

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

        # основная группа
        main_layout_h = QHBoxLayout()

        group_button_layout = QVBoxLayout() # группа для кнопок
        self.content_layout_v = QVBoxLayout() # группа для расписания/посещаемости/заданий/тестов/успеваемости
        main_layout_h.addLayout(group_button_layout)
        main_layout_h.addStretch(3)
        main_layout_h.addLayout(self.content_layout_v)
        main_layout_h.addStretch(1)
        main_layout.addLayout(main_layout_h)

        group_button_layout.addStretch(1)

        # кнопка тесты
        self.button_tests = QPushButton("Тесты")
        self.button_tests.setFixedSize(200, 40)
        self.button_tests.setStyleSheet("""
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
        self.button_tests.clicked.connect(self.test_const_open)
        group_button_layout.addWidget(self.button_tests, alignment=Qt.AlignLeft)

        group_button_layout.addStretch(1)

    def test_const_open(self):
        self.test_window = TestConstructor(self.id_user, self.fio)
        self.test_window.show()

    def logout(self): # выход из учетки
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()


class TestConstructor(QMainWindow):
    def __init__(self, id_user = None, fio = None):
        super().__init__()
        self.id_user = id_user
        self.fio = fio

        central_widget = QWidget()

        self.setWindowTitle("Конструктор тестов")
        self.setFixedSize(900, 600)
        self.setCentralWidget(central_widget)
        self.setStyleSheet("background-color: #f0f0f0;")

        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        title_label = QLabel("Конструктор тестов")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            font-size: 22px;
            font-weight: bold;
            font-family: Roboto;
            color: #2c3e50;
            margin-bottom: 20px;
        """)
        main_layout.addWidget(title_label)

        # основная группа
        content_layout = QHBoxLayout()
        main_layout.addLayout(content_layout)

        left_widget = QWidget() # левая часть составления теста
        left_widget.setFixedWidth(400)
        content_layout.addWidget(left_widget)

        test_info_layout = QVBoxLayout() # группа для информации о тесте
        left_widget.setLayout(test_info_layout)

        # название теста
        name_layout = QHBoxLayout()
        name_label = QLabel("Название теста:")
        name_label.setStyleSheet("font-family: Roboto; color: #333;")
        self.test_name_input = QLineEdit()
        self.test_name_input.setPlaceholderText("Введите название теста")
        self.test_name_input.setStyleSheet("""
            border-radius: 5px;
            border: 1px solid #ccc;
            padding: 5px;
            font-family: Roboto;
        """)
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.test_name_input)
        test_info_layout.addLayout(name_layout)

        # выбор группы
        group_layout = QHBoxLayout()
        group_label = QLabel("Группа:")
        group_label.setStyleSheet("font-family: Roboto; color: #333;")
        group_layout.addWidget(group_label)

        self.group_combo = QComboBox()
        self.group_combo.addItems(["Выберите группу"])
        self.group_combo.setStyleSheet("""
            border-radius: 5px;
            border: 1px solid #ccc;
            color: #333;
            padding: 5px;
            font-family: Roboto;
            min-width: 100px;
        """)
        group_layout.addWidget(self.group_combo)
        test_info_layout.addLayout(group_layout)

        # выбор срока выполнения
        date_layout = QHBoxLayout()
        date_label = QLabel("Срок выполнения:")
        date_label.setStyleSheet("font-family: Roboto; color: #333;")
        self.deadline_date = QDateEdit()
        self.deadline_date.setCalendarPopup(True)
        self.deadline_date.setDate(QDate.currentDate())
        self.deadline_date.setStyleSheet("""
            border-radius: 5px;
            border: 1px solid #ccc;
            color: #333;
            padding: 5px;
            font-family: Roboto;
        """)
        date_layout.addWidget(date_label)
        date_layout.addWidget(self.deadline_date)
        test_info_layout.addLayout(date_layout)

        test_constructor_layout = QVBoxLayout() # группа для составления вопросов
        question_layout = QVBoxLayout()
        test_constructor_layout.addLayout(question_layout)
        question_layout.addSpacing(10)

        self.question_from_db = QPushButton("Выбрать из банка вопросов")
        self.question_from_db.setFixedSize(300, 35)
        self.question_from_db.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 12px;
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
        self.question_from_db.clicked.connect(self.open_que_ans_db)
        question_layout.addWidget(self.question_from_db, alignment=Qt.AlignCenter)
        question_layout.addSpacing(10)

        # вопрос
        question_text_label = QLabel("Текст вопроса:")
        question_text_label.setStyleSheet("font-family: Roboto; color: #333;")
        question_layout.addWidget(question_text_label)
        self.question_text_edit = QTextEdit()
        self.question_text_edit.setMaximumHeight(80)
        self.question_text_edit.setPlaceholderText("Введите текст вопроса...")
        self.question_text_edit.setStyleSheet("""
            border-radius: 5px;
            border: 1px solid #ccc;
            padding: 5px;
            font-family: Roboto;
        """)
        question_layout.addWidget(self.question_text_edit)

        # ответы
        answers_label = QLabel("Варианты ответов:")
        answers_label.setStyleSheet("font-family: Roboto; color: #333; margin-top: 10px;")
        question_layout.addWidget(answers_label)

        self.answer_widgets = []
        for i in range(4):
            answer_layout = QHBoxLayout()
            answer_checkbox = QCheckBox(f"{i+1}.")
            answer_checkbox.setStyleSheet("font-family: Roboto;")
            self.answer_input = QLineEdit()
            self.answer_input.setPlaceholderText("Введите вариант ответа")
            self.answer_input.setStyleSheet("""
                border-radius: 5px;
                border: 1px solid #ccc;
                padding: 5px;
                font-family: Roboto;
                margin-left: 5px;
            """)
            answer_layout.addWidget(answer_checkbox)
            answer_layout.addWidget(self.answer_input)
            question_layout.addLayout(answer_layout)
            self.answer_widgets.append((answer_checkbox, self.answer_input))

        # кнопка добавления вопроса
        self.add_question_btn = QPushButton("Добавить вопрос в тест")
        self.add_question_btn.setFixedSize(200, 40)
        self.add_question_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 12px;
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
        self.add_question_btn.clicked.connect(self.add_question_to_test)
        question_layout.addSpacing(10)
        question_layout.addWidget(self.add_question_btn, alignment=Qt.AlignCenter)

        test_info_layout.addLayout(test_constructor_layout)
        test_info_layout.addStretch(1)

        right_widget = QWidget() # правая часть для составленного теста
        right_layout = QVBoxLayout()
        right_widget.setLayout(right_layout)
        content_layout.addWidget(right_widget)

        # список добавленных вопросов
        self.questions_list = QListWidget()
        self.questions_list.setStyleSheet("""
            QListWidget {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 5px;
                font-family: Roboto;
                min-height: 300px;
                outline: 0;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #eee;
                background-color: #f8f9fa;
                border-radius: 3px;
                margin: 2px;
            }
            QListWidget::item:selected {
                background-color: #e8f4fc;
                color: #2c3e50;
            }                        
            QTableWidget::item:focus {
                outline: none;
                border: none;
            }
        """)
        right_layout.addWidget(self.questions_list)

        # статистика теста
        stats_layout = QHBoxLayout()
        self.questions_count_label = QLabel("Вопросов: 0")
        self.questions_count_label.setStyleSheet("font-family: Roboto; color: #555; font-weight: bold;")
        stats_layout.addWidget(self.questions_count_label)
        stats_layout.addStretch()
        right_layout.addLayout(stats_layout)

        # кнопки для сохранения/очистки теста
        buttons_layout = QHBoxLayout()
        
        self.save_test_btn = QPushButton("Сохранить тест")
        self.save_test_btn.setStyleSheet("""
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
        self.save_test_btn.clicked.connect(self.save_test)
        
        self.clear_test_btn = QPushButton("Очистить")
        self.clear_test_btn.setStyleSheet("""
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
        self.clear_test_btn.clicked.connect(self.clear_questions_list)
        buttons_layout.addWidget(self.save_test_btn)
        buttons_layout.addWidget(self.clear_test_btn)
        
        right_layout.addLayout(buttons_layout)
        right_layout.addStretch(1)

        self.load_groups_from_db()

    def check_question_exists(self, question_text, answers_data): # проверка на доабвленный вопрос
        try:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id_question 
                FROM test_question 
                WHERE text = ?
            """, (question_text,))
            
            existing_question = cursor.fetchone()
            
            if not existing_question:
                cursor.close()
                return None
            
            question_id = existing_question[0]
            
            cursor.execute("""
                SELECT answer, is_true 
                FROM test_answer 
                WHERE id_question = ?
                ORDER BY id_answer
            """, (question_id,))
            
            db_answers = cursor.fetchall()
            
            if len(db_answers) != len(answers_data):
                cursor.close()
                return None
            
            all_match = True
            for i, answer in enumerate(answers_data):
                db_answer_text = db_answers[i][0]
                db_is_correct = bool(db_answers[i][1])
                
                if (answer['text'] != db_answer_text or 
                    answer['is_correct'] != db_is_correct):
                    all_match = False
                    break
            
            cursor.close()
            
            return question_id if all_match else None
            
        except Exception as e:
            print(f"Ошибка при проверке существования вопроса: {str(e)}")
            return None
        
    def is_question_in_test_list(self, question_text, answers_data): # проверка наличия вопроса в списке
        for i in range(self.questions_list.count()):
            item = self.questions_list.item(i)
            item_data = item.data(Qt.UserRole)
            
            if not item_data:
                continue
            
            if item_data['question_text'] != question_text:
                continue
            
            item_answers = item_data['answers']
            if len(item_answers) != len(answers_data):
                continue
            
            all_match = True
            for j in range(len(answers_data)):
                if (item_answers[j]['text'] != answers_data[j]['text'] or 
                    item_answers[j]['is_correct'] != answers_data[j]['is_correct']):
                    all_match = False
                    break
            
            if all_match:
                return True
        
        return False

    def save_test(self):
        if not self.validate_test_data():
            return
        
        try:
            cursor = conn.cursor()
            
            test_name = self.test_name_input.text().strip()
            
            cursor.execute("""
                SELECT id_name FROM test_name WHERE name = ?
            """, (test_name,))
            existing_name = cursor.fetchone()

            if existing_name:
                name_id = existing_name[0]
            else:
                cursor.execute("""
                    INSERT INTO test_name (name) VALUES (?)
                """, (test_name,))
                name_id = cursor.execute("SELECT @@IDENTITY").fetchone()[0]
            
            group_id = self.get_selected_group_id()
        
            deadline_date = self.deadline_date.date().toString("yyyy-MM-dd")
            upload_date = QDate.currentDate().toString("yyyy-MM-dd")

            cursor.execute("""
                INSERT INTO test (id_name, id_name_class, upload, deadline)
                VALUES (?, ?, ?, ?)
            """, (name_id, group_id, upload_date, deadline_date))
            
            test_id = cursor.execute("SELECT @@IDENTITY").fetchone()[0]
            
            for i in range(self.questions_list.count()):
                item = self.questions_list.item(i)
                item_data = item.data(Qt.UserRole)

                if item_data:
                    question_text = item_data['question_text']
                    
                    cursor.execute("""
                        SELECT id_question FROM test_question WHERE text = ?
                    """, (question_text,))
                    existing_question = cursor.fetchone()
                    
                    if existing_question:
                        question_id = existing_question[0]

                        for answer in item_data['answers']:
                            cursor.execute("""
                                SELECT id_answer FROM test_answer 
                                WHERE id_question = ? AND answer = ? AND is_true = ?
                            """, (question_id, answer['text'], 1 if answer['is_correct'] else 0))
                            
                            answer_row = cursor.fetchone()
                            if answer_row:
                                answer_id = answer_row[0]
                    else:
                        cursor.execute("""
                            INSERT INTO test_question (text) VALUES (?)
                        """, (question_text,))
                        question_id = cursor.execute("SELECT @@IDENTITY").fetchone()[0]
                        
                        for answer in item_data['answers']:
                            cursor.execute("""
                                INSERT INTO test_answer (id_question, answer, is_true)
                                VALUES (?, ?, ?)
                            """, (question_id, answer['text'], 1 if answer['is_correct'] else 0))
                    
                    for answer in item_data['answers']:
                        cursor.execute("""
                            SELECT id_answer FROM test_answer 
                            WHERE id_question = ? AND answer = ? AND is_true = ?
                        """, (question_id, answer['text'], 1 if answer['is_correct'] else 0))
                        
                        answer_row = cursor.fetchone()
                        if answer_row:
                            answer_id = answer_row[0]
                            
                            cursor.execute("""
                                SELECT id_que_ans FROM question_answer 
                                WHERE id_question = ? AND id_answer = ? 
                            """, (question_id, answer_id)) ## перепроверить ---------------------------------------------------------------------------------

                            que_ans_row = cursor.fetchone()
                            if que_ans_row:
                                que_ans_id = que_ans_row[0]
                            else:
                                cursor.execute("""
                                    INSERT INTO question_answer (id_question, id_answer)
                                    VALUES (?, ?)
                                """, (question_id, answer_id))
                                
                                que_ans_id = cursor.execute("SELECT @@IDENTITY").fetchone()[0]
                            
                            cursor.execute("""
                                SELECT id_content FROM test_content 
                                WHERE id_test = ? AND id_que_ans = ?
                            """, (test_id, que_ans_id))
                            
                            if not cursor.fetchone():
                                cursor.execute("""
                                    INSERT INTO test_content (id_test, id_que_ans)
                                    VALUES (?, ?)
                                """, (test_id, que_ans_id))
        
            conn.commit()
            cursor.close()
            
            QMessageBox.information(
                self,
                "Успех",
                f"Тест '{test_name}' успешно сохранен"
            )
            
            self.clear_form()

        except Exception as e:
            QMessageBox.critical(
                self,
                "Ошибка",
                f"Не удалось сохранить тест: {str(e)}"
            )

    def validate_test_data(self):
        test_name = self.test_name_input.text().strip()
        if not test_name:
            QMessageBox.warning(self, "Предупреждение", "Введите название теста")
            return False
        
        group_id = self.get_selected_group_id()
        if not group_id:
            QMessageBox.warning(self, "Предупреждение", "Выберите группу")
            return False
        
        if self.questions_list.count() == 0:
            QMessageBox.warning(self, "Предупреждение", "Добавьте хотя бы один вопрос в тест")
            return False
        
        deadline_date = self.deadline_date.date()
        if deadline_date < QDate.currentDate():
            reply = QMessageBox.question(
                self,
                "Подтверждение",
                "Срок выполнения теста уже прошел.\n"
                "Вы уверены, что хотите продолжить?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if reply == QMessageBox.No:
                return False
        
        return True
    
    def get_selected_group_id(self):
        current_index = self.group_combo.currentIndex()
        if current_index > 0:
            return self.group_combo.itemData(current_index)
        return None
    
    def clear_form(self):
        self.test_name_input.clear()
        self.group_combo.setCurrentIndex(0)
        self.deadline_date.setDate(QDate.currentDate().addDays(7))
        self.question_text_edit.clear()
        
        for checkbox, line_edit in self.answer_widgets:
            checkbox.setChecked(False)
            line_edit.clear()
        
        self.questions_list.clear()
        self.update_questions_count()

    def load_groups_from_db(self): # группы для списка
        try:
            cursor = conn.cursor()
            
            query = ("""
                SELECT DISTINCT
                    nc.id_name_class,
                    nc.num,
                    nc.letter
                FROM name_class nc
                ORDER BY nc.num, nc.letter
            """)
        
            cursor.execute(query)
            groups_data = cursor.fetchall()
            
            self.group_combo.clear()
            
            if groups_data:
                self.group_combo.addItem("Выберите группу")
                for group in groups_data:
                    class_num = group[1]
                    class_letter = group[2]
                    group_name = f"{class_num}{class_letter}"
                    self.group_combo.addItem(group_name, group[0])
            else:
                self.group_combo.addItem("Нет доступных групп")
                self.group_combo.setEnabled(False)
                
            cursor.close()
            
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить группы: {str(e)}")
            self.group_combo.clear()
            self.group_combo.addItem("Ошибка загрузки")
            self.group_combo.setEnabled(False)

    def clear_questions_list(self): # очистка questions_list
        if self.questions_list.count() == 0:
            QMessageBox.information(
                self,
                "Очистка",
                "Список вопросов пуст."
            )
            return

        msg_box = QMessageBox(QMessageBox.Question, 
            "Очистка", 
            "Вы уверены, что хотите удалить все вопросы из теста?",
            QMessageBox.Yes | QMessageBox.No
        )
        yes_button = msg_box.button(QMessageBox.Yes)
        no_button = msg_box.button(QMessageBox.No)
        if yes_button:
            yes_button.setText("Да")
        if no_button:
            no_button.setText("Нет")
        msg_box.setDefaultButton(QMessageBox.No)
        
        if msg_box.exec_() == QMessageBox.Yes:
            self.questions_list.clear()
            self.update_questions_count()

    def update_questions_count(self):
        count = self.questions_list.count()
        self.questions_count_label.setText(f"Вопросов: {count}")

    def open_que_ans_db(self): # открытие окна для выбора вопросов из бд
        dialog = QuestionAnswerFromDB(self)
        if dialog.exec_() == QDialog.Accepted:
            question_details = dialog.get_selected_question_details()

            if question_details:
                self.question_text_edit.setText(question_details['text'])
                answers_list = question_details['answers']
                
                for checkbox, line_edit in self.answer_widgets:
                    checkbox.setChecked(False)
                    line_edit.clear()

                for i, (checkbox, line_edit) in enumerate(self.answer_widgets):
                    if i < len(answers_list):
                        answer = answers_list[i]
                        line_edit.setText(answer['text'])
                        checkbox.setChecked(answer['is_correct'])
                    else:
                        checkbox.setChecked(False)
                        line_edit.clear()

                # pass
                # count = self.questions_list.count() + 1
                # self.questions_list.addItem(f"Задание {count}\n"
                #     f"Вопрос: {question_text}\n"
                #     f"Варианты ответов: {answers_text}"
                # )
                # self.questions_count_label.setText(f"Вопросов: {count}")

    def add_question_to_test(self): # добавление теста по кнопке
        question_text = self.question_text_edit.toPlainText().strip()
        
        if not question_text:
            QMessageBox.warning(self, "Предупреждение", "Введите текст вопроса")
            return
        
        answers_data = []

        for checkbox, line_edit in self.answer_widgets:
            answer_text = line_edit.text().strip()
            if answer_text:
                is_correct = checkbox.isChecked()
                answers_data.append({
                    'text': answer_text,
                    'is_correct': is_correct
                })

        has_correct_answer = any(answer['is_correct'] for answer in answers_data)
        if not has_correct_answer:
            QMessageBox.warning(self, "Предупреждение", "Добавьте хотя бы один вариант ответа")
            return
        
        if self.is_question_in_test_list(question_text, answers_data):
            QMessageBox.warning(
                self,
                "Вопрос уже добавлен",
                "Такой вопрос уже есть в тесте."
            )
            return

        question_number = self.questions_list.count() + 1
        
        answers_display = []
        for answer in answers_data:
            marker = " + " if answer['is_correct'] else " - "
            answers_display.append(f"{answer['text']}{marker}")
        
        answers_text = "; ".join(answers_display)
        
        item_text = (f"Задание {question_number}\n"
                    f"Вопрос: {question_text}\n"
                    f"Варианты ответов: {answers_text}")
        list_item = QListWidgetItem(item_text)

        list_item.setData(Qt.UserRole, {
            'question_text': question_text,
            'answers': answers_data,
            'question_number': question_number
        })
        
        self.questions_list.addItem(list_item)
        self.update_questions_count()
        self.clear_question_fields()

    def update_questions_count(self):
        count = self.questions_list.count()
        self.questions_count_label.setText(f"Вопросов: {count}")

    def clear_question_fields(self):
        self.question_text_edit.clear()
        
        for checkbox, line_edit in self.answer_widgets:
            checkbox.setChecked(False)
            line_edit.clear()


class QuestionAnswerFromDB(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.selected_question_id = None
        self.setWindowTitle("Банк вопросов")
        self.setFixedSize(500, 400)
        self.setModal(True)
        self.setWindowFlags(Qt.Dialog | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        
        # таблица для вывода вопросов и ответов
        self.questions_table = QTableWidget()
        self.questions_table.setFixedSize(480, 320)
        self.questions_table.setColumnCount(2)
        self.questions_table.setHorizontalHeaderLabels(["Вопрос", "Ответы"])
        self.questions_table.horizontalHeader().setStretchLastSection(True)
        self.questions_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.questions_table.setSelectionMode(QTableWidget.SingleSelection)
        self.questions_table.setStyleSheet("""
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
        main_layout.addWidget(self.questions_table, alignment=Qt.AlignCenter)
        
        # кнопка выбора вопроса
        self.select_button = QPushButton("Выбрать вопрос")
        self.select_button.setFixedSize(150, 35)
        self.select_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 12px;
                font-family: Roboto;
                font-weight: bold;
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
        self.select_button.clicked.connect(self.accept_selection)
        self.select_button.setEnabled(False)
        main_layout.addStretch()
        main_layout.addWidget(self.select_button, alignment=Qt.AlignCenter)
        main_layout.addStretch()

        self.load_questions_from_db() # загрузка из бд
        self.questions_table.itemSelectionChanged.connect(self.on_selection_changed) # выбор строки

    def load_questions_from_db(self): # загрузка вопросов и ответов из бд
        try:
            cursor = conn.cursor()
            
            query = ("""
                select 
                    q.id_question,
                    q.text as question_text,
                    STRING_AGG(a.answer + 
                        CASE WHEN a.is_true = 1 THEN ' + ' ELSE ' - ' END, 
                        ', ') as answers_list
                from test_question q
                left join test_answer a ON q.id_question = a.id_question
                group by q.id_question, q.text
                order by q.id_question
            """)
            
            cursor.execute(query)
            questions_data = cursor.fetchall()
            
            self.questions_table.setRowCount(len(questions_data))
            
            
            for row, question in enumerate(questions_data):
                question_id = question[0]
                question_text = question[1]
                answers_text = question[2] if question[2] else "Нет вариантов ответов"
                
                # вопрос
                question_item = QTableWidgetItem(question_text)
                question_item.setData(Qt.UserRole, question_id)
                question_item.setFlags(question_item.flags() & ~Qt.ItemIsEditable)
                self.questions_table.setItem(row, 0, question_item)
                
                # ответ
                answers_item = QTableWidgetItem(answers_text)
                answers_item.setFlags(answers_item.flags() & ~Qt.ItemIsEditable)
                self.questions_table.setItem(row, 1, answers_item)
            
            # размеры столбцов
            self.questions_table.resizeColumnsToContents()
            self.questions_table.verticalHeader().setDefaultSectionSize(60)
            self.questions_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
            
            cursor.close()
            
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить вопросы: {str(e)}")

    def on_selection_changed(self):
        selected_items = self.questions_table.selectedItems()
        self.select_button.setEnabled(len(selected_items) > 0)
    
    def accept_selection(self):
        selected_row = self.questions_table.currentRow()
        if selected_row >= 0:
            question_item = self.questions_table.item(selected_row, 0)
            self.selected_question_id = question_item.data(Qt.UserRole)
            self.accept()
    
    def get_selected_question_id(self): # id вопроса
        return self.selected_question_id
    
    def get_selected_question_text(self): # текст вопроса
        selected_row = self.questions_table.currentRow()
        if selected_row >= 0:
            return self.questions_table.item(selected_row, 0).text()
        return None
    
    def get_selected_question_answers(self): # ответы
        selected_row = self.questions_table.currentRow()
        if selected_row >= 0:
            return self.questions_table.item(selected_row, 1).text()
        return None
    
    def get_selected_question_details(self):
        selected_row = self.questions_table.currentRow()
        if selected_row >= 0:
            question_id = self.selected_question_id
            question_text = self.questions_table.item(selected_row, 0).text()
            
            answers_details = self.get_question_answers_details(question_id)
            
            return {
                'id': question_id,
                'text': question_text,
                'answers': answers_details
            }
        return None
    
    def get_question_answers_details(self, question_id):
        try:
            cursor = conn.cursor()
            
            query = ("""
                SELECT 
                    answer,
                    is_true,
                    id_answer
                FROM test_answer
                WHERE id_question = ?
                ORDER BY id_answer
            """)
            
            cursor.execute(query, (question_id,))
            answers_data = cursor.fetchall()
            
            answers_list = []
            for answer_row in answers_data:
                answer_text = answer_row[0]
                is_correct = bool(answer_row[1])
                answer_id = answer_row[2]
                
                answers_list.append({
                    'text': answer_text,
                    'is_correct': is_correct,
                    'id': answer_id
                })
            
            cursor.close()
            return answers_list
            
        except Exception as e:
            print(f"Ошибка при загрузке ответов: {str(e)}")
            return []


class MainMenuAdmin(QMainWindow):
    def __init__(self, id_user = None, fio = None):
        super().__init__()
        self.id_user = id_user
        self.fio = fio

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

        self.load_users()
        
        self.users_table.itemSelectionChanged.connect(self.update_buttons_state)

    def logout(self): # выход из учетки
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()

    def load_users(self): # загрузка пользователей
        try:
            cursor = conn.cursor()
            
            query = ("""
                SELECT 
                    u.id_user,
                    u.surname,
                    u.name,
                    u.patronymic,
                    u.login,
                    r.title as role_name,
                    u.is_active
                FROM users u
                INNER JOIN role r ON u.id_role = r.id_role
                ORDER BY u.surname, u.name
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
        dialog = AddEditUserDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.load_users()

    def open_edit_user_dialog(self): # редактирование пользователя
        selected_row = self.users_table.currentRow()
        if selected_row >= 0:
            login = self.users_table.item(selected_row, 3).text()
            dialog = AddEditUserDialog(self, login=login)
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
                    cursor = conn.cursor()
                    cursor.execute("""
                        UPDATE users
                        SET is_active = 0
                        WHERE login = ?
                    """, (login,))
                    conn.commit()
                    cursor.close()
                    QMessageBox.information(self, "Успех", "Пользователь отключен")
                    self.load_users()
                except Exception as e:
                    QMessageBox.critical(self, "Ошибка", f"Не удалось отключить пользователя: {str(e)}")


class AddEditUserDialog(QDialog):
    def __init__(self, parent=None, user_id=None, login=None):
        super().__init__(parent)
        self.user_id = user_id
        self.login = login
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
            cursor = conn.cursor()
            cursor.execute("SELECT id_role, title FROM role ORDER BY id_role")
            roles = cursor.fetchall()
            
            for role_id, role_name in roles:
                self.role_combo.addItem(role_name, role_id)
            
            cursor.close()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить роли: {str(e)}")

    def load_user_data(self): 
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT surname, name, patronymic, login, id_role, is_active
                FROM users WHERE id_user = ?
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
            cursor = conn.cursor()
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
                        UPDATE users
                        SET surname = ?, name = ?, patronymic = ?,
                            login = ?, password = ?, id_role = ?, is_active = ?
                        WHERE id_user = ?
                    """, (surname, name, patronymic, login, password_hash, role_id, is_active, self.user_id))
                else:
                    cursor.execute("""
                        UPDATE users
                        SET surname = ?, name = ?, patronymic = ?,
                            login = ?, id_role = ?, is_active = ?
                        WHERE id_user = ?
                    """, (surname, name, patronymic, login, role_id, is_active, self.user_id))
            else:
                password = self.password_edit.text()
                if not password:
                    QMessageBox.warning(self, "Ошибка", "Укажите пароль")
                    return
                
                password_hash = hashlib.sha256(password.encode()).hexdigest()
                cursor.execute("""
                    INSERT INTO users (surname, name, patronymic, login, password, id_role, is_active)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (surname, name, patronymic, login, password_hash, role_id, is_active))
            
            conn.commit()
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
            cursor = conn.cursor()
            query = "SELECT COUNT(*) FROM users WHERE login = ?"
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
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id_user, surname, name, patronymic, login, id_role, is_active
                FROM users WHERE login = ?
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


def main():
    
    query = f"select * from users"

    cursor = conn.cursor()

    cursor.execute(query)
    results = cursor.fetchall()

    schedule = []
    for row in results:
        schedule.append({
            "id_user":row.id_user,
            "id_role":row.id_role,
            "surname":row.surname,
            "name":row.name,
            "patronymic":row.patronymic,
            "login":row.login,
            "password":row.password,
            "is_active":row.is_active
        })

    print(schedule)


    # cmd = pd.read_sql_query(query, conn)
    # cmd.head()
    # print(cmd)

    # ip = "192.168.0.32";
    # database = "столовая2";
    # uname = "youruser";
    # pass = "password";
    # port = "52446";


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    login_window = LoginWindow()
    login_window.show()

    sys.exit(app.exec_())
    
    # main()
