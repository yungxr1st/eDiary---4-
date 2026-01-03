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


class MainMenuStudent(QMainWindow): # главное меню для ученика
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
        from main import LoginWindow
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
            cursor = self.conn.cursor()

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
            cursor = self.conn.cursor()

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
            cursor = self.conn.cursor()

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
            cursor = self.conn.cursor()

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
            cursor = self.conn.cursor()

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
            cursor = self.conn.cursor()
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
            cursor = self.conn.cursor()
            
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
            cursor = self.conn.cursor()
            
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
            
            cursor = self.conn.cursor()
            
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
            
            self.conn.commit()
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
            cursor = self.conn.cursor()
            
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
            
            self.conn.commit()
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