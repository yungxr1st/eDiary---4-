import hashlib
import sys
import pyodbc
import pandas as pd
import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QStyleFactory, QVBoxLayout,
                             QHBoxLayout, QPushButton, QSpinBox, QLabel, QGridLayout, QComboBox, QLineEdit, QTabWidget,
                             QGroupBox, QListWidget, QDialogButtonBox, QDialog, QFormLayout, QMessageBox,
                             QListWidgetItem, QTextEdit)
from PyQt5.QtGui import QPixmap, QIcon, QPainter, QColor, QPen, QFont, QPalette
from PyQt5.QtCore import Qt, QSize, QTimer, pyqtSignal

uname = "youruser"
pswd = "password"
driver = "{ODBC Driver 17 for SQL Server}"
server = "DESKTOP-Q4NUJUS"
database = "diary"

conn = pyodbc.connect(
    'DRIVER=' + driver + ';SERVER=' + server + "\\MSSQLSERVER02" +
    ';DATABASE=' + database + ';UID=' + uname + ';PWD=' + pswd)


class MainWindow(QMainWindow):
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
        """ # для ввода текста в элементы

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
                    
            if login == "123" and pswd == "123":
                id_user = 1
                fio = "администратор"

                self.open_main_menu_for_student(id_user, fio)

            else:
                self.error_label.setText("Неверный логин или пароль")
            
            cursor.close()
            
        except Exception as e:
            self.error_label.setText(f"Ошибка при аутентификации: {str(e)}")
    
    def open_main_menu_for_student(self, id_user, fio): # главное меню для ученика
        self.close()

        self.main_menu_student = MainMenuStudent(id_user, fio)
        self.main_menu_student.show()


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

        label = QLabel(f"Добро пожаловать, {fio}")
        label.setAlignment(Qt.AlignLeft)
        label.setStyleSheet("""
            font-size: 20px;
            font-family: Roboto;
            color: #333;
        """)
        main_layout.addWidget(label)

        # расположение элементов
        main_layout_h = QHBoxLayout() # основная группа
        group_button_layout = QVBoxLayout() # группа для кнопок
        self.content_layout_v = QVBoxLayout() # группа для расписания/посещаемости/заданий/тестов/успеваемости
        main_layout_h.addLayout(group_button_layout)
        main_layout_h.addStretch(1)
        main_layout_h.addLayout(self.content_layout_v)
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

        self.show_schedule()

        main_layout.addStretch(1)

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

    def show_schedule(self): # отображение расписания
        self.clear_content_layout()

        self.content_layout_v.addWidget(self.schedule_widget)

        self.load_schedule()

    def show_attendance(self): # отображение посещаемости
        self.clear_content_layout()

        self.content_layout_v.addWidget(self.attendance_widget)

        self.load_attendance()

    def clear_content_layout(self): # очистка content_layout_v
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
                    s.cabinet
                from schedule s
                inner join class c ON s.id_class = c.id_class
                inner join name_class nc ON c.id_name_class = nc.id_name_class
                inner join subject sub ON s.id_subject = sub.id_subject
                inner join users u ON s.id_user = u.id_user
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
                SELECT 
                    l.date,
                    sub.subject_name,
                    t_att.title as attendance_status,
                    u.surname + ' ' + LEFT(u.name, 1) + '.' + LEFT(u.patronymic, 1) + '.' as teacher_name
                from lesson l
                inner join subject sub on sub.id_subject = l.id_subject
                inner join attendance a on a.id_lesson = l.id_lesson
                inner join type_attendance t_att ON t_att.id_type_att = a.id_type_att
                inner join subj_teachers s_t on s_t.id_subject = sub.id_subject
                inner join users u on u.id_user = s_t.id_user
                WHERE a.id_user = ?
                ORDER BY l.date DESC
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
                    status_text = f"Статус: {attendance_status}"
                    
                    date_item = QListWidgetItem(f" {attendance_text}")
                    date_item.setFlags(Qt.NoItemFlags)
                    date_item.setFont(QFont("Roboto", 9, QFont.Bold))
                    date_item.setForeground(QColor("#2c3e50"))
                    self.attendance_table.addItem(date_item)
                    
                    status_item = QListWidgetItem(f"   {teacher_name}")
                    status_item.setFlags(Qt.NoItemFlags)
                    status_item.setFont(QFont("Roboto", 8))
                    self.attendance_table.addItem(status_item)
                    
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

    login_window = MainWindow()
    login_window.show()

    sys.exit(app.exec_())
    
    # main()
