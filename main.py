import hashlib
import sys
import pyodbc
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                                QPushButton, QLabel, QLineEdit)
from PyQt5.QtCore import (Qt)
from PyQt5.QtGui import QIcon
from teachers import MainMenuTeacher
from admin import MainMenuAdmin
from students import MainMenuStudent
from administration import MainMenuAdministration

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
    ';DATABASE=' + database1 + ';Trusted_Connection=yes;' + 'TrustServerCertificate=yes;'
)


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        central_widget = QWidget()

        self.setWindowTitle("Авторизация")
        self.setFixedSize(600, 400)
        self.setCentralWidget(central_widget)
        self.setWindowIcon(QIcon("diary_120704.ico"))
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
        """ # стиль для ввода текста в элементы

        # логин
        login_label = QLabel("Логин:")
        login_label.setStyleSheet("""
            font-size: 12px;
            font: bold;
            color: black;
            font-family: Roboto;
        """)
        self.login_input = QLineEdit()
        self.login_input.setMaxLength(20)
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
        self.pswd_input.setMaxLength(20)
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

        # строка ошибки 
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

    def hash_password(self, password): # хэширование пароля
        return hashlib.sha256(password.encode('utf-8')).hexdigest() 

    def check_(self): # проверка логина и пароля
        login = self.login_input.text()
        pswd = self.pswd_input.text()
        self.error_label.setText("")

        if not login or not pswd:
            self.error_label.setText("Введите логин и пароль")
            return
        
        try:
            cursor = conn.cursor()

            hashed_pswd = self.hash_password(pswd)

            query = ("""
                select u.id_user, u.surname, left(u.name, 1) + '.', left(u.patronymic, 1) + '.',
                    u.id_role, r.title
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
                role = user_data[5]
                
                fio = f"{surname} {name} {patronymic} ({role})".strip()
                
                if id_role == 1: # ученик
                    self.open_main_menu_for_student(id_user, fio)
                if id_role == 2: # преподаватель
                    self.open_main_menu_for_teacher(id_user, fio)
                if id_role == 3: # администратор
                    self.open_main_menu_for_admin(id_user, fio)
                if id_role == 4: # администрация центра
                    self.open_main_menu_for_administration(id_user, fio)
                
                    
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

            elif login == "2" and pswd == "2":
                id_user = 4
                fio = "сотрудник администрации"
                self.open_main_menu_for_administration(id_user, fio)

            else:
                self.error_label.setText("Неверный логин или пароль")
            
            cursor.close()
            
        except Exception as e:
            self.error_label.setText(f"Ошибка при аутентификации: {str(e)}")
    
    def open_main_menu_for_student(self, id_user, fio): # главное меню для ученика
        self.close()

        self.main_menu_student = MainMenuStudent(id_user, fio, conn)
        self.main_menu_student.show()

    def open_main_menu_for_teacher(self, id_user, fio): # главное меню для учителя
        self.close()

        self.main_menu_teacher = MainMenuTeacher(id_user, fio, conn)
        self.main_menu_teacher.show()

    def open_main_menu_for_admin(self, id_user, fio): # главное меню для администратора
        self.close()

        self.main_menu_admin = MainMenuAdmin(id_user, fio, conn)
        self.main_menu_admin.show()

    def open_main_menu_for_administration(self, id_user, fio): # главное меню для администрации центра
        self.close()

        self.main_menu_administration = MainMenuAdministration(id_user, fio, conn)
        self.main_menu_administration.show()


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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    login_window = LoginWindow()
    login_window.show()

    sys.exit(app.exec_())
    
    # main()
