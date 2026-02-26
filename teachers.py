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


class MainMenuTeacher(QMainWindow):
    def __init__(self, id_user = None, fio = None, conn = None):
        super().__init__()
        self.id_user = id_user
        self.fio = fio
        self.conn = conn
        self.selected_test_id = None

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

        # кнопка посещаемости
        self.button_attendance = QPushButton("Посещаемость")
        self.button_attendance.setFixedSize(200, 40)
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
        self.button_homework.setFixedSize(200, 40)
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
        self.button_tests.clicked.connect(self.show_tests)
        group_button_layout.addWidget(self.button_tests, alignment=Qt.AlignLeft)
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
        self.button_stats.clicked.connect(self.show_grades)
        group_button_layout.addWidget(self.button_stats, alignment=Qt.AlignLeft)
        group_button_layout.addSpacing(5)

        # кнопка расписания
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

        group_button_layout.addStretch(2)
        main_layout.addStretch(1)

        self.schedule()
        self.homework()
        self.attendance()
        self.grades()
        self.tests()
        self.show_schedule()

    def clear_content_layout(self): # удаление информации из content_layout_v для последующей вставки другого контента
        for i in reversed(range(self.content_layout_v.count())):
            widget = self.content_layout_v.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

    def show_schedule(self): # отображение расписания
        self.clear_content_layout()

        self.content_layout_v.addWidget(self.schedule_widget)

        self.load_schedule()

    def schedule(self): # элемент расписания (таблица, список, как душе угодно)
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
        self.schedule_list.setFixedSize(600, 450)
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
        schedule_layout.addWidget(self.schedule_list)

        self.load_schedule()

    def load_schedule(self): # загрузка расписания
        try:
            cursor = self.conn.cursor()

            query = ("""
                select 
                    s.day_of_week, sub.subject_name, nc.num, nc.letter, cab.num,
                    case s.lesson_num
                        when 1 then '14:00'
                        when 2 then '15:00'
                        when 3 then '16:00'
                        when 4 then '17:00'
                        when 5 then '18:00'
                    end as lesson_time
                from schedule s
                inner join name_class nc ON s.id_name_class = nc.id_name_class
                inner join subject sub ON s.id_subject = sub.id_subject
                inner join cabinet cab on cab.id_cabinet = s.id_cabinet
                where s.id_user = ?
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
                    cabinet = lesson[4]
                    lesson_time = lesson[5]

                    class_group = f"{class_num}{class_letter}"
                    
                    lesson_text = (f"{subject_name}, группа: {class_group}, "
                        f"{cabinet} кабинет\n  Начало в: {lesson_time}")
                    
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

    def show_homework(self): # отображение дз
        self.clear_content_layout()
        self.load_groups_for_homework()

        self.content_layout_v.addWidget(self.homework_widget)

        self.load_homework()

    def homework(self): # элементы для домашнего задания (таблица)
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

        control_layout = QHBoxLayout() # область для элементов группы и обновления таблицы
        
        # выбор группы
        group_label = QLabel("Группа:")
        group_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #333;")
        control_layout.addWidget(group_label)
        
        self.group_combo = QComboBox()
        self.group_combo.addItems(["Выберите группу"])
        self.group_combo.setFixedSize(150, 30)
        self.group_combo.setStyleSheet("""
            border-radius: 5px;
            border: 1px solid #ccc;
            color: #333;
            padding: 5px;
            font-family: Roboto;
        """)
        self.group_combo.currentIndexChanged.connect(self.load_homework)
        control_layout.addWidget(self.group_combo)
        
        control_layout.addStretch()
        
        # кнопка обновить
        refresh_button = QPushButton("Обновить")
        refresh_button.setFixedSize(120, 35)
        refresh_button.setStyleSheet("""
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
        refresh_button.clicked.connect(self.load_homework)
        control_layout.addWidget(refresh_button)
        
        homework_layout.addLayout(control_layout)

        # таблица для дз
        self.homework_table = QListWidget()
        self.homework_table.setFixedSize(600, 304)
        self.homework_table.setStyleSheet("""
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
            }
            QListWidget::item:selected {
                background-color: #e8f4fc;
                color: #2c3e50;
            }                        
            QTableWidget::item:focus {
                outline: none;
                border: none;
            }
            QListWidget::item:last {
                border-bottom: none;
            }
        """)
        self.homework_table.itemSelectionChanged.connect(self.on_homework_selected)
        homework_layout.addWidget(self.homework_table)

        exercise_layout = QHBoxLayout() # область для параметров задания (текст, срок выполнения)
        homework_layout.addLayout(exercise_layout)
        text_layout = QVBoxLayout() # область для текста задания
        exercise_layout.addLayout(text_layout)
        date_layout = QVBoxLayout() # область для срока выполнения
        exercise_layout.addLayout(date_layout)

        # текст задания
        question_text_label = QLabel("Текст задания:")
        question_text_label.setStyleSheet("font-family: Roboto; color: #333;")
        text_layout.addWidget(question_text_label, alignment=Qt.AlignLeft)

        self.question_text_edit = QTextEdit()
        self.question_text_edit.setFixedSize(280, 80)
        self.question_text_edit.setPlaceholderText("Введите текст задания...")
        self.question_text_edit.setStyleSheet("""
            border-radius: 5px;
            border: 1px solid #ccc;
            padding: 5px;
            font-family: Roboto;
        """)
        self.question_text_edit.textChanged.connect(self.validate_homework_text)
        text_layout.addWidget(self.question_text_edit, alignment=Qt.AlignLeft)

        # счетчик символов
        self.char_count_label = QLabel("0/150")
        self.char_count_label.setStyleSheet("font-family: Roboto; color: #333; font-size: 11px;")
        date_layout.addWidget(self.char_count_label, alignment=Qt.AlignLeft)
        
        # выбор срока выполнения
        date_label = QLabel("Срок выполнения:")
        date_label.setStyleSheet("font-family: Roboto; color: #333;")
        self.deadline_date = QDateEdit()
        self.deadline_date.setFixedSize(100, 30)
        self.deadline_date.setCalendarPopup(True)
        self.deadline_date.setDate(QDate.currentDate())
        self.deadline_date.setStyleSheet("""
            border-radius: 5px;
            border: 1px solid #ccc;
            color: #333;
            padding: 5px;
            font-family: Roboto;
        """)
        date_layout.addStretch(1)
        date_layout.addWidget(date_label, alignment=Qt.AlignLeft)
        date_layout.addWidget(self.deadline_date, alignment=Qt.AlignLeft)

        edit_btn_layout = QVBoxLayout() # область для кнопки редактирования дз
        exercise_layout.addLayout(edit_btn_layout)
        edit_btn_layout.addStretch(1)

        self.edit_button = QPushButton("Изменить")
        self.edit_button.setFixedSize(100, 35)
        self.edit_button.setStyleSheet("""
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
                background-color: #95a5a6;
            }
        """)
        self.edit_button.clicked.connect(self.edit_homework)
        self.edit_button.setEnabled(False)
        edit_btn_layout.addWidget(self.edit_button)

        add_del_button = QVBoxLayout() # область для кнопок добавления/удаления
        exercise_layout.addLayout(add_del_button)
        add_del_button.addStretch(1)

        self.del_button = QPushButton("Удалить")
        self.del_button.setFixedSize(100, 35)
        self.del_button.setStyleSheet("""
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
                background-color: #95a5a6;
            }
        """)
        self.del_button.clicked.connect(self.delete_homework)
        self.del_button.setEnabled(False)
        add_del_button.addWidget(self.del_button)

        self.add_button = QPushButton("Добавить")
        self.add_button.setFixedSize(100, 35)
        self.add_button.setStyleSheet("""
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
        self.add_button.clicked.connect(self.add_homework)
        add_del_button.addWidget(self.add_button)

        self.selected_homework_id = None

    def load_homework(self): # загрузка заданий
        try:
            selected_group_id = self.group_combo.currentData()
        
            if not selected_group_id:
                self.homework_table.clear()
                no_group_item = QListWidgetItem("Выберите группу для просмотра заданий")
                no_group_item.setTextAlignment(Qt.AlignCenter)
                no_group_item.setFlags(Qt.NoItemFlags)
                no_group_item.setForeground(QColor("#7f8c8d"))
                self.homework_table.addItem(no_group_item)
                self.selected_homework_id = None
                self.del_button.setEnabled(False)
                return
            
            cursor = self.conn.cursor()

            query = ("""
                select 
                    e.id_exercise,
                    s.subject_name,
                    e.exercise,
                    e.upload,
                    e.deadline
                from exercise e
                inner join subject s on s.id_subject = e.id_subject
                where e.id_name_class = ?
                order by e.deadline desc
            """)

            cursor.execute(query, (selected_group_id))
            homework_data = cursor.fetchall()

            self.homework_table.clear()

            if homework_data: # комбинирование полученной информации в одну ячейку в списке
                current_date = None

                for record in homework_data:
                    id_exercise = record[0]
                    subject_name = record[1]
                    exercise = record[2]
                    upload = record[3]
                    deadline = record[4]

                    formatted_upload = upload.strftime("%d.%m.%Y")
                    formatted_deadline = deadline.strftime("%d.%m.%Y")

                    date_text = f"Задано: {formatted_upload} \nСрок сдачи: {formatted_deadline}"

                    item_text = (f"{subject_name}\n"
                                f"{date_text}\n"
                                f"{exercise}")
                    list_item = QListWidgetItem(item_text)

                    list_item.setData(Qt.UserRole, {
                        'id': id_exercise,
                        'subject_name': subject_name,
                        'exercise': exercise,
                        'upload': upload,
                        'deadline': deadline
                    })
                    
                    self.homework_table.addItem(list_item)

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

    def on_homework_selected(self): # выбор задания в списке для удаления
        selected_items = self.homework_table.selectedItems()
        
        if selected_items:
            item = selected_items[0]
            item_data = item.data(Qt.UserRole)
            
            if item_data:
                self.selected_homework_id = item_data['id']
                self.del_button.setEnabled(True)
                self.edit_button.setEnabled(True)
                
                self.question_text_edit.setPlainText(item_data['exercise'])
                self.deadline_date.setDate(QDate(item_data['deadline'].year, 
                                            item_data['deadline'].month, 
                                            item_data['deadline'].day))
                self.validate_homework_text()
            else:
                self.selected_homework_id = None
                self.del_button.setEnabled(False)
                self.edit_button.setEnabled(False)
                self.question_text_edit.clear()
                self.validate_homework_text()
        else:
            self.selected_homework_id = None
            self.del_button.setEnabled(False)
            self.edit_button.setEnabled(False)
            self.question_text_edit.clear()
            self.validate_homework_text()

    def edit_homework(self): # редактирование домашнего задания
        selected_group_id = self.group_combo.currentData()
        if not selected_group_id:
            QMessageBox.warning(self, "Ошибка", "Выберите группу для добавления задания")
            return
        
        exercise_text = self.question_text_edit.toPlainText().strip()
        if not exercise_text:
            QMessageBox.warning(self, "Ошибка", "Введите текст задания")
            return
        
        if len(exercise_text) > 150:
            QMessageBox.warning(self, "Ошибка", "Текст задания не должен превышать 150 символов")
            return
        
        deadline_date = self.deadline_date.date()
        deadline_date_str = deadline_date.toString("yyyy-MM-dd")
        
        if deadline_date < QDate.currentDate():
            reply = QMessageBox.question(
                self,
                "Подтверждение",
                "Срок выполнения уже прошел. Вы уверены, что хотите изменить задание?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if reply == QMessageBox.No:
                return
        
        try:
            cursor = self.conn.cursor()
            
            update_query = """
                update exercise 
                set exercise = ?, deadline = ? 
                where id_exercise = ?
            """
            cursor.execute(update_query, (exercise_text, deadline_date_str, self.selected_homework_id))
            
            if cursor.rowcount > 0:
                self.conn.commit()
                
                QMessageBox.information(
                    self, 
                    "Успех", 
                    f"Задание успешно обновлено!"
                )
            else:
                QMessageBox.warning(
                    self,
                    "Ошибка",
                    "Задание не найдено."
                )
            
            # очистка полей
            self.question_text_edit.clear()
            self.validate_homework_text()
            self.load_homework()

            cursor.close()
            
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось обновить задание: {str(e)}")
            if 'cursor' in locals():
                self.conn.rollback()

    def add_homework(self): # добавление домашнего задания
        if self.edit_button.isEnabled():
            reply = QMessageBox.question(
                self,
                "Предупреждение",
                "Вы уверены, что хотите добавить задание, а не изменить?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if reply == QMessageBox.No:
                return
        
        selected_group_id = self.group_combo.currentData()
        if not selected_group_id:
            QMessageBox.warning(self, "Ошибка", "Выберите группу для добавления задания")
            return
        
        exercise_text = self.question_text_edit.toPlainText().strip()
        if not exercise_text:
            QMessageBox.warning(self, "Ошибка", "Введите текст задания")
            return
        
        if len(exercise_text) > 150:
            QMessageBox.warning(self, "Ошибка", "Текст задания не должен превышать 150 символов")
            return
        
        deadline_date = self.deadline_date.date()
        deadline_date_str = deadline_date.toString("yyyy-MM-dd")
        
        if deadline_date < QDate.currentDate():
            reply = QMessageBox.question(
                self,
                "Подтверждение",
                "Срок сдачи уже прошел. Вы уверены, что хотите изменить задание?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if reply == QMessageBox.No:
                return
        
        try:
            cursor = self.conn.cursor()
            
            subject_query = """
                select distinct s.id_subject
                from schedule sch
                inner join subject s on sch.id_subject = s.id_subject
                where sch.id_user = ? and sch.id_name_class = ?
            """
            cursor.execute(subject_query, (self.id_user, selected_group_id))
            subject_data = cursor.fetchone()
            
            if not subject_data:
                QMessageBox.warning(self, "Ошибка", "Для выбранной группы не найден предмет")
                cursor.close()
                return
            
            subject_id = subject_data[0]
            
            insert_query = """
                insert into exercise (id_subject, id_name_class, exercise, upload, deadline)
                values (?, ?, ?, GETDATE(), ?)
            """
            
            cursor.execute(insert_query, (subject_id, selected_group_id, exercise_text, deadline_date_str))
            self.conn.commit()
            
            QMessageBox.information(self, "Успех", "Задание успешно добавлено")
            
            # очистка полей
            self.question_text_edit.clear()
            self.validate_homework_text()
            self.load_homework()
            
            cursor.close()
            
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить задание: {str(e)}")

    def delete_homework(self): # удаление домашнего задания
        if not self.selected_homework_id:
            QMessageBox.warning(self, "Ошибка", "Выберите задание для удаления")
            return
        
        reply = QMessageBox.question(
            self,
            "Подтверждение удаления",
            "Вы уверены, что хотите удалить выбранное задание?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                cursor = self.conn.cursor()
                
                delete_query = "delete from exercise where id_exercise = ?"
                cursor.execute(delete_query, (self.selected_homework_id,))
                self.conn.commit()
                
                QMessageBox.information(self, "Успех", "Задание успешно удалено")
                
                # очистка полей
                self.selected_homework_id = None
                self.del_button.setEnabled(False)
                self.question_text_edit.clear()
                self.validate_homework_text()
                self.load_homework()
                
                cursor.close()
                
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось удалить задание: {str(e)}")

    def validate_homework_text(self): # проверка текста задания на кол-во символов
        text = self.question_text_edit.toPlainText()
        char_count = len(text)
        
        # обновление счетчика
        self.char_count_label.setText(f"{char_count}/150")
        
        # активность кнопки в зависимости от символов
        if text.strip() and char_count > 0:
            self.add_button.setEnabled(True)
        else:
            self.add_button.setEnabled(False)

    def load_groups_for_homework(self): # загрузка групп для списка
        try:
            cursor = self.conn.cursor()

            query = """
                select 
                    s_t.id_name_class,
                    convert(varchar, n_c.num) + n_c.letter
                from subj_teachers s_t
                inner join name_class n_c on n_c.id_name_class = s_t.id_name_class
                inner join users u on u.id_user = s_t.id_user
                where u.id_user = ?
                order by n_c.num, n_c.letter
            """
            cursor.execute(query, self.id_user)
            groups_data = cursor.fetchall()
            
            self.group_combo.clear()
            
            if groups_data:
                self.group_combo.addItem("Выберите группу", None)
                for group in groups_data:
                    class_id = group[0]
                    num_letter = group[1]
                    group_name = f"{num_letter}"
                    self.group_combo.addItem(group_name, class_id)
            else:
                self.group_combo.addItem("Нет доступных групп")
                self.group_combo.setEnabled(False)
                
            cursor.close()
            
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить группы: {str(e)}")
            self.group_combo.clear()
            self.group_combo.addItem("Ошибка загрузки")
            self.group_combo.setEnabled(False)

    def show_attendance(self): # отображение посещаемости
        self.clear_content_layout()

        self.content_layout_v.addWidget(self.attendance_widget)

        self.load_groups_for_attendance()
        self.load_status_for_attendance()

    def attendance(self): # элементы для посещаемости
        self.attendance_widget = QWidget()
        attendance_layout = QVBoxLayout()
        self.attendance_widget.setLayout(attendance_layout)

        attendance_label = QLabel("Посещаемость:")
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
        attendance_layout.addSpacing(2)
        
        top_layout = QHBoxLayout() # для группы и кнопки обновить
        
        group_label = QLabel("Группа:")
        group_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #333;")
        top_layout.addWidget(group_label)
        
        self.attendance_group_combo = QComboBox()
        self.attendance_group_combo.addItems(["Выберите группу"])
        self.attendance_group_combo.setFixedSize(150, 30)
        self.attendance_group_combo.setStyleSheet("""
            border-radius: 5px;
            border: 1px solid #ccc;
            color: #333;
            padding: 5px;
            font-family: Roboto;
        """)
        self.attendance_group_combo.currentIndexChanged.connect(self.load_attendance)
        top_layout.addWidget(self.attendance_group_combo)
        
        top_layout.addStretch()
        
        attendance_layout.addLayout(top_layout)
        
        # для таблицы
        self.attendance_table = QTableWidget()
        self.attendance_table.setFixedSize(600, 355)
        self.attendance_table.setColumnCount(3)
        self.attendance_table.setHorizontalHeaderLabels(["Предмет", "ФИО", "Статус посещаемости"])
        self.attendance_table.horizontalHeader().setStretchLastSection(True)
        self.attendance_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.attendance_table.setSelectionMode(QTableWidget.SingleSelection)
        self.attendance_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.attendance_table.itemSelectionChanged.connect(self.on_attendance_selected)
        self.attendance_table.setStyleSheet("""
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
        header = self.attendance_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Fixed)  # предмет
        header.resizeSection(0, 120)
        header.setSectionResizeMode(1, QHeaderView.Fixed)  # фио
        header.resizeSection(1, 300)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # статус посещаемости
        attendance_layout.addWidget(self.attendance_table)
        attendance_layout.addSpacing(2)
        
        # для выбора даты, типа статуса посещения и кнопки добавления 
        bottom_layout = QHBoxLayout()
        
        date_layout = QVBoxLayout()
        date_label = QLabel("Дата занятия:")
        date_label.setStyleSheet("font-family: Roboto; color: #333;")
        date_layout.addWidget(date_label, alignment=Qt.AlignLeft)
        
        self.attendance_date = QDateEdit()
        self.attendance_date.setFixedSize(120, 30)
        self.attendance_date.setCalendarPopup(True)
        self.attendance_date.setDate(QDate.currentDate())
        self.attendance_date.setStyleSheet("""
            border-radius: 5px;
            border: 1px solid #ccc;
            color: #333;
            padding: 5px;
            font-family: Roboto;
        """)
        self.attendance_date.dateChanged.connect(self.load_attendance)
        date_layout.addWidget(self.attendance_date, alignment=Qt.AlignLeft)
        bottom_layout.addLayout(date_layout)
        
        status_layout = QVBoxLayout()
        status_label = QLabel("Статус посещения:")
        status_label.setStyleSheet("font-family: Roboto; color: #333;")
        status_layout.addWidget(status_label, alignment=Qt.AlignLeft)
        
        self.attendance_status_combo = QComboBox()
        self.attendance_status_combo.setFixedSize(200, 30)
        self.attendance_status_combo.setStyleSheet("""
            border-radius: 5px;
            border: 1px solid #ccc;
            color: #333;
            padding: 5px;
            font-family: Roboto;
        """)
        status_layout.addWidget(self.attendance_status_combo, alignment=Qt.AlignLeft)
        bottom_layout.addLayout(status_layout)
        
        bottom_layout.addStretch()
        
        # кнопка изменения
        add_button_layout = QVBoxLayout()
        add_button_layout.addStretch()
        
        self.add_attendance_button = QPushButton("Сохранить")
        self.add_attendance_button.setFixedSize(120, 35)
        self.add_attendance_button.setStyleSheet("""
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
                background-color: #95a5a6;
            }
        """)
        self.add_attendance_button.clicked.connect(self.add_attendance)
        self.add_attendance_button.setEnabled(False)
        add_button_layout.addWidget(self.add_attendance_button)
        
        bottom_layout.addLayout(add_button_layout)
        
        attendance_layout.addLayout(bottom_layout)
        
        # для данных из выбранной строки в таблице
        self.selected_student_id = None
        self.selected_subject_id = None
        self.selected_attendance_id = None

    def load_attendance(self): # загрузка посещаемости
        try:
            selected_group_id = self.attendance_group_combo.currentData()
            attendance_date = self.attendance_date.date()
            attendance_date_str = attendance_date.toString("yyyy-MM-dd")
            
            if not selected_group_id:
                self.attendance_table.setRowCount(0)
                self.selected_student_id = None
                self.selected_subject_id = None
                self.add_attendance_button.setEnabled(False)
                return
                
            cursor = self.conn.cursor()
            query = """
                select 
	                a.id_attendance,
                    s.id_subject,
                    s.subject_name,
                    u.id_user,
                    u.surname + ' ' + u.name + ' ' + u.patronymic as fio,
                    isnull(t_a.title, '') as attendance_status
                from lesson l
                inner join attendance a on a.id_lesson = l.id_lesson
                inner join type_attendance t_a on t_a.id_type_att = a.id_type_att
                inner join name_class n_c on n_c.id_name_class = l.id_name_class
                inner join class c on c.id_name_class = n_c.id_name_class
                inner join users u on u.id_user = c.id_user
                inner join subject s on s.id_subject = l.id_subject
                inner join schedule sch on sch.id_name_class = n_c.id_name_class
                where sch.id_user = ? and sch.id_name_class = ? and l.date = ?
                group by a.id_attendance, s.id_subject, s.subject_name, u.id_user, 
	                u.surname, u.name, u.patronymic, t_a.title
                order by s.subject_name, u.surname, u.name, u.patronymic
            """
            cursor.execute(query, (self.id_user, selected_group_id, attendance_date_str))
            attendance_data = cursor.fetchall()
            
            # вывод в таблице
            self.attendance_table.setRowCount(len(attendance_data))
            
            for row, record in enumerate(attendance_data):
                attendance_id = record[0]
                subject_id = record[1]
                subject_name = record[2]
                student_id = record[3]
                fio = record[4]
                attendance_status = record[5]
                
                # предмет
                subject_item = QTableWidgetItem(subject_name)
                subject_item.setData(Qt.UserRole, {
                    'subject_id': subject_id, 
                    'student_id': student_id, 
                    'attendance_id': attendance_id
                })
                subject_item.setFlags(subject_item.flags() & ~Qt.ItemIsEditable)
                subject_item.setTextAlignment(Qt.AlignCenter)
                self.attendance_table.setItem(row, 0, subject_item)
                
                # фио
                fio_item = QTableWidgetItem(fio)
                fio_item.setData(Qt.UserRole, {
                    'subject_id': subject_id, 
                    'student_id': student_id, 
                    'attendance_id': attendance_id
                })
                fio_item.setFlags(fio_item.flags() & ~Qt.ItemIsEditable)
                fio_item.setTextAlignment(Qt.AlignCenter)
                self.attendance_table.setItem(row, 1, fio_item)
                
                # статус посещаемости
                status_item = QTableWidgetItem(attendance_status)
                status_item.setData(Qt.UserRole, {
                    'subject_id': subject_id, 
                    'student_id': student_id, 
                    'attendance_id': attendance_id
                })
                status_item.setFlags(status_item.flags() & ~Qt.ItemIsEditable)
                status_item.setTextAlignment(Qt.AlignCenter)
                
                # цвет статуса
                if attendance_status == 'Присутствовал':
                    status_item.setForeground(QColor("#27ae60"))
                elif attendance_status == 'Отсутствовал':
                    status_item.setForeground(QColor("#e74c3c"))
                elif attendance_status == 'Уважительная причина':
                    status_item.setForeground(QColor("#f39c12"))
                    
                self.attendance_table.setItem(row, 2, status_item)
                
            self.attendance_table.resizeColumnsToContents()
            self.attendance_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
            
            cursor.close()
            
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить данные о посещаемости: {str(e)}")
            self.attendance_table.setRowCount(0)

    def load_groups_for_attendance(self): # выбор элемента для загрузки групп
        self.load_groups_into_combo(self.attendance_group_combo) # в скобках указан элемент для подстановки

    def load_groups_into_combo(self, combo_box): # загрузка групп
        try:
            cursor = self.conn.cursor()
            
            # query = """
            #     select distinct 
            #         c.id_class,
            #         convert(varchar, nc.num) + nc.letter as [group]
            #     from schedule s
            #     inner join class c on s.id_name_class = c.id_name_class
            #     inner join name_class nc on c.id_name_class = nc.id_name_class
            #     where s.id_user = ?
            #     order by [group]
            # """

            query = """
                select 
                    s_t.id_name_class,
                    convert(varchar, n_c.num) + n_c.letter
                from subj_teachers s_t
                inner join name_class n_c on n_c.id_name_class = s_t.id_name_class
                inner join users u on u.id_user = s_t.id_user
                where u.id_user = ?
                order by n_c.num, n_c.letter
            """
            # cursor.execute(query, (self.id_user,))
            cursor.execute(query, self.id_user)
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
            combo_box.addItem("Ошибка загрузки")
            combo_box.setEnabled(False)

    def load_status_for_attendance(self): # загрузка статусов посещения
        try:
            cursor = self.conn.cursor()
            
            query = """
                select id_type_att, title 
                from type_attendance 
                order by id_type_att
            """
            cursor.execute(query)
            statuses = cursor.fetchall()
            
            self.attendance_status_combo.clear()
            
            if statuses:
                for status in statuses:
                    status_id = status[0]
                    status_title = status[1]
                    self.attendance_status_combo.addItem(status_title, status_id)
            else:
                self.attendance_status_combo.addItem("Нет статуса")
                self.attendance_status_combo.setEnabled(False)
                
            cursor.close()
            
        except Exception as e:
            self.attendance_status_combo.clear()
            self.attendance_status_combo.addItem("Ошибка загрузки")
            self.attendance_status_combo.setEnabled(False)

    def on_attendance_selected(self): # выбор строки в таблице
        selected_items = self.attendance_table.selectedItems()
        
        if selected_items:
            item = selected_items[0]
            item_data = item.data(Qt.UserRole)
            
            if item_data and 'student_id' in item_data and 'subject_id' in item_data:
                self.selected_student_id = item_data['student_id']
                self.selected_subject_id = item_data['subject_id']
                self.selected_attendance_id = item_data['attendance_id']
                self.add_attendance_button.setEnabled(True)
            else:
                self.selected_student_id = None
                self.selected_subject_id = None
                self.selected_attendance_id = None
                self.add_attendance_button.setEnabled(False)
        else:
            self.selected_student_id = None
            self.selected_subject_id = None
            self.selected_attendance_id = None
            self.add_attendance_button.setEnabled(False)

    def add_attendance(self): # изменение записи о посещаемости
        if not self.selected_student_id or not self.selected_subject_id:
            QMessageBox.warning(self, "Ошибка", "Выберите ученика из таблицы")
            return
            
        selected_group_id = self.attendance_group_combo.currentData()
        if not selected_group_id:
            QMessageBox.warning(self, "Ошибка", "Выберите группу")
            return
            
        attendance_date = self.attendance_date.date()
        attendance_date_str = attendance_date.toString("yyyy-MM-dd")
        
        status_type_id = self.attendance_status_combo.currentData()
        if not status_type_id:
            QMessageBox.warning(self, "Ошибка", "Выберите статус посещения")
            return
            
        try:
            cursor = self.conn.cursor()
            
            update_query = """
                update attendance 
                set id_type_att = ? 
                where id_attendance = ?
            """
            cursor.execute(update_query, (status_type_id, self.selected_attendance_id))
            
            self.conn.commit()
            cursor.close()
            
            QMessageBox.information(self, "Успех", "Запись о посещаемости успешно изменена")
            
            self.load_attendance()
            
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось изменить запись о посещаемости: {str(e)}")
            if 'cursor' in locals():
                self.conn.rollback()

    def show_grades(self):
        self.clear_content_layout()

        self.content_layout_v.addWidget(self.grades_widget)

        self.load_groups_for_grades()
        self.load_types_for_grades()

    def grades(self):
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
        grades_layout.addSpacing(2)
        
        top_layout = QHBoxLayout() # для группы и кнопки обновить
        
        group_label = QLabel("Группа:")
        group_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #333;")
        top_layout.addWidget(group_label)
        
        self.grades_group_combo = QComboBox()
        self.grades_group_combo.addItems(["Выберите группу"])
        self.grades_group_combo.setFixedSize(150, 30)
        self.grades_group_combo.setStyleSheet("""
            border-radius: 5px;
            border: 1px solid #ccc;
            color: #333;
            padding: 5px;
            font-family: Roboto;
        """)
        self.grades_group_combo.currentIndexChanged.connect(self.load_grades)
        top_layout.addWidget(self.grades_group_combo)
        
        top_layout.addStretch()

        self.check_stats = QPushButton()
        self.check_stats.setText("Средний балл группы")
        self.check_stats.setFixedSize(140, 30)
        self.check_stats.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border-radius: 5px;
                font-size: 12px;
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
        top_layout.addWidget(self.check_stats)
        
        grades_layout.addLayout(top_layout)
        
        # для таблицы
        self.grades_table = QTableWidget()
        self.grades_table.setFixedSize(600, 355)
        self.grades_table.setColumnCount(4)
        self.grades_table.setHorizontalHeaderLabels(["Предмет", "ФИО", "Оценка", "Тип оценки"])
        self.grades_table.horizontalHeader().setStretchLastSection(True)
        self.grades_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.grades_table.setSelectionMode(QTableWidget.SingleSelection)
        self.grades_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.grades_table.itemSelectionChanged.connect(self.on_grades_selected)
        self.grades_table.setStyleSheet("""
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
        header = self.grades_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Fixed)  # предмет
        header.resizeSection(0, 120)
        header.setSectionResizeMode(1, QHeaderView.Fixed)  # фио
        header.resizeSection(1, 280)
        header.setSectionResizeMode(2, QHeaderView.Fixed)  # оценка
        header.resizeSection(2, 70)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # тип оценки
        grades_layout.addWidget(self.grades_table)
        grades_layout.addSpacing(2)
        
        # для выбора даты, типа статуса посещения и кнопки добавления 
        bottom_layout = QHBoxLayout()
        
        date_layout = QVBoxLayout()
        date_label = QLabel("Дата занятия:")
        date_label.setStyleSheet("font-family: Roboto; color: #333;")
        date_layout.addWidget(date_label, alignment=Qt.AlignLeft)
        
        self.grades_date = QDateEdit()
        self.grades_date.setFixedSize(120, 30)
        self.grades_date.setCalendarPopup(True)
        self.grades_date.setDate(QDate.currentDate())
        self.grades_date.setStyleSheet("""
            border-radius: 5px;
            border: 1px solid #ccc;
            color: #333;
            padding: 5px;
            font-family: Roboto;
        """)
        self.grades_date.dateChanged.connect(self.load_grades)
        date_layout.addWidget(self.grades_date, alignment=Qt.AlignLeft)
        bottom_layout.addLayout(date_layout)
        
        type_grades_layout = QHBoxLayout() # область для элементов, относящихся к оценке
        bottom_layout.addLayout(type_grades_layout)
        grades_from_db_layout = QVBoxLayout() # область для оценки
        type_grades_layout.addLayout(grades_from_db_layout)
        type_gr_from_db_layout = QVBoxLayout() # область для типа оценки
        type_grades_layout.addLayout(type_gr_from_db_layout)

        grades_from_db_label = QLabel("Оценка:")
        grades_from_db_label.setStyleSheet("font-family: Roboto; color: #333;")
        grades_from_db_layout.addWidget(grades_from_db_label, alignment=Qt.AlignLeft)
        
        self.grades_db_combo = QComboBox()
        self.grades_db_combo.addItems(["2", "3", "4", "5"])
        self.grades_db_combo.setFixedSize(70, 30)
        self.grades_db_combo.setStyleSheet("""
            border-radius: 5px;
            border: 1px solid #ccc;
            color: #333;
            padding: 5px;
            font-family: Roboto;
        """)
        grades_from_db_layout.addWidget(self.grades_db_combo, alignment=Qt.AlignLeft)

        type_gr_from_db_label = QLabel("Тип оценки:")
        type_gr_from_db_label.setStyleSheet("font-family: Roboto; color: #333;")
        type_gr_from_db_layout.addWidget(type_gr_from_db_label, alignment=Qt.AlignLeft)
        
        self.type_gr_db_combo = QComboBox()
        self.type_gr_db_combo.setFixedSize(150, 30)
        self.type_gr_db_combo.setStyleSheet("""
            border-radius: 5px;
            border: 1px solid #ccc;
            color: #333;
            padding: 5px;
            font-family: Roboto;
        """)
        type_gr_from_db_layout.addWidget(self.type_gr_db_combo, alignment=Qt.AlignLeft)
        
        bottom_layout.addStretch()
        
        # кнопка изменения
        add_button_layout = QVBoxLayout()
        add_button_layout.addStretch()
        
        self.add_grade_button = QPushButton("Сохранить")
        self.add_grade_button.setFixedSize(120, 35)
        self.add_grade_button.setStyleSheet("""
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
                background-color: #95a5a6;
            }
        """)
        self.add_grade_button.clicked.connect(self.add_grades)
        self.add_grade_button.setEnabled(False)
        add_button_layout.addWidget(self.add_grade_button)
        add_button_layout.addStretch()
        
        bottom_layout.addLayout(add_button_layout)
        
        grades_layout.addLayout(bottom_layout)
        
        # для данных из выбранной строки в таблице
        self.selected_student_id = None
        self.selected_subject_id = None
        self.selected_grade_id = None

    def load_grades(self):
        try:
            selected_group_id = self.grades_group_combo.currentData()
            grades_date = self.grades_date.date()
            grades_date_str = grades_date.toString("yyyy-MM-dd")
            
            if not selected_group_id:
                self.grades_table.setRowCount(0)
                self.selected_student_id = None
                self.selected_subject_id = None
                self.add_grade_button.setEnabled(False)
                self.check_stats.setEnabled(False)
                return
            
            self.check_stats.setEnabled(True)
                
            cursor = self.conn.cursor()
            query = """
                select 
                    g.id_grade,
                    s.id_subject,
                    s.subject_name,
                    g.id_user,
                    u.surname + ' ' + u.name + ' ' + u.patronymic as fio,
                    isnull(g.grade, ' ') as grade,
                    isnull(t_g.title, ' ') as type_grade
                from grade g
                inner join users u on u.id_user = g.id_user
                inner join type_grade t_g on t_g.id_type_gr = g.id_type_gr
                inner join lesson l on l.id_lesson = g.id_lesson
                inner join subject s on s.id_subject = l.id_subject
                inner join name_class n_c on n_c.id_name_class = l.id_name_class
                inner join schedule sch on sch.id_name_class = n_c.id_name_class
                where sch.id_user = ? and sch.id_name_class = ? and l.date = ?
                group by g.id_grade, s.id_subject, s.subject_name, g.id_user, 
                    u.surname, u.name, u.patronymic, g.grade, g.id_type_gr, t_g.title
                order by s.subject_name, u.surname, u.name, u.patronymic
            """
            cursor.execute(query, (self.id_user, selected_group_id, grades_date_str))
            grades_data = cursor.fetchall()
            
            # вывод в таблице
            self.grades_table.setRowCount(len(grades_data))
            
            for row, record in enumerate(grades_data):
                id_grade = record[0]
                subject_id = record[1]
                subject_name = record[2]
                student_id = record[3]
                fio = record[4]
                grade = str(record[5])
                if grade == '0':
                    grade = ''
                type_grade = record[6]
                
                # предмет
                subject_item = QTableWidgetItem(subject_name)
                subject_item.setData(Qt.UserRole, {
                    'subject_id': subject_id, 'student_id': student_id, 'grade_id': id_grade
                })
                subject_item.setFlags(subject_item.flags() & ~Qt.ItemIsEditable)
                subject_item.setTextAlignment(Qt.AlignCenter)
                self.grades_table.setItem(row, 0, subject_item)
                
                # фио
                fio_item = QTableWidgetItem(fio)
                fio_item.setData(Qt.UserRole, {
                    'subject_id': subject_id, 'student_id': student_id, 'grade_id': id_grade
                })
                fio_item.setFlags(fio_item.flags() & ~Qt.ItemIsEditable)
                fio_item.setTextAlignment(Qt.AlignCenter)
                self.grades_table.setItem(row, 1, fio_item)
                
                # оценка
                grade_item = QTableWidgetItem(grade)
                grade_item.setData(Qt.UserRole, {
                    'subject_id': subject_id, 'student_id': student_id, 'grade_id': id_grade
                })
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
                
                self.grades_table.setItem(row, 2, grade_item)

                # тип оценки
                type_item = QTableWidgetItem(type_grade)
                type_item.setData(Qt.UserRole, {
                    'subject_id': subject_id, 'student_id': student_id, 'grade_id': id_grade
                })
                type_item.setFlags(type_item.flags() & ~Qt.ItemIsEditable)
                type_item.setTextAlignment(Qt.AlignCenter)
                self.grades_table.setItem(row, 3, type_item)
                
            self.grades_table.resizeColumnsToContents()
            self.grades_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
            
            cursor.close()
            
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить данные об оценках: {str(e)}")
            self.grades_table.setRowCount(0)

    def load_groups_for_grades(self): # выбор элемента для загрузки групп
        self.load_groups_into_combo(self.grades_group_combo) # в скобках указан элемент для подстановки

    def load_types_for_grades(self): # загрузка типов оценки
        try:
            cursor = self.conn.cursor()
            
            query = """
                select id_type_gr, title 
                from type_grade
                order by id_type_gr
            """
            cursor.execute(query)
            types = cursor.fetchall()
            
            self.type_gr_db_combo.clear()
            
            if types:
                for type in types:
                    id_type = type[0]
                    type_title = type[1]
                    self.type_gr_db_combo.addItem(type_title, id_type)
            else:
                self.type_gr_db_combo.addItem("Нет типа оценки")
                self.type_gr_db_combo.setEnabled(False)
                
            cursor.close()
            
        except Exception as e:
            self.type_gr_db_combo.clear()
            self.type_gr_db_combo.addItem("Ошибка загрузки")
            self.type_gr_db_combo.setEnabled(False)

    def on_grades_selected(self): # выбор строки в таблице
        selected_items = self.grades_table.selectedItems()
        
        if selected_items:
            item = selected_items[0]
            item_data = item.data(Qt.UserRole)
            
            if item_data and 'student_id' in item_data and 'subject_id' in item_data:
                self.selected_student_id = item_data['student_id']
                self.selected_subject_id = item_data['subject_id']
                self.selected_grade_id = item_data['grade_id']
                self.add_grade_button.setEnabled(True)
            else:
                self.selected_student_id = None
                self.selected_subject_id = None
                self.selected_grade_id = None
                self.add_grade_button.setEnabled(False)
        else:
            self.selected_student_id = None
            self.selected_subject_id = None
            self.selected_grade_id = None
            self.add_grade_button.setEnabled(False)

    def add_grades(self): # изменение записи об оценке
        if not self.selected_student_id or not self.selected_subject_id:
            QMessageBox.warning(self, "Ошибка", "Выберите ученика из таблицы")
            return
            
        selected_group_id = self.grades_group_combo.currentData()
        if not selected_group_id:
            QMessageBox.warning(self, "Ошибка", "Выберите группу")
            return
            
        grades_date = self.grades_date.date()
        grades_date_str = grades_date.toString("yyyy-MM-dd")
        
        type_id = self.type_gr_db_combo.currentData()
        if not type_id:
            QMessageBox.warning(self, "Ошибка", "Выберите статус посещения")
            return
            
        try:
            cursor = self.conn.cursor()
            
            grade = int(self.grades_db_combo.currentText())
            
            update_query = """
                update grade
                set id_type_gr = ?, grade = ?
                where id_grade = ?
            """
            cursor.execute(update_query, (type_id, grade, self.selected_grade_id))
            
            update_avg_query = """
                declare @avg_grade varchar(4); declare @id_user int = ?;
                declare @id_subject int = ?;
                select @avg_grade = cast(round(avg(cast(g.grade as float)), 2) as varchar(4))
                from grade g 
                inner join lesson l on l.id_lesson = g.id_lesson
                where g.id_user = @id_user and l.id_subject = @id_subject
                begin
                    update subj_students
                    set avg_grade = @avg_grade
                    where id_user = @id_user and id_subject = @id_subject;
                end
            """
            cursor.execute(update_avg_query, (self.selected_student_id, self.selected_subject_id))
            
            self.conn.commit()
            cursor.close()
            
            QMessageBox.information(self, "Успех", "Запись об оценке успешно изменена")
            
            self.load_grades()
            
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось изменить запись об оценке: {str(e)}")
            if 'cursor' in locals():
                self.conn.rollback()

    def check_user_stats(self):
        try:
            dialog = QDialog(self)
            dialog.setWindowTitle(f"{self.grades_group_combo.currentText()}")
            dialog.setFixedSize(350, 300)
            dialog.setWindowFlags(Qt.Dialog | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
            
            layout = QVBoxLayout()
            dialog.setLayout(layout)
            
            avg_grade_table = QTableWidget()
            avg_grade_table.setColumnCount(2)
            avg_grade_table.setHorizontalHeaderLabels(["Ученик", "Средний балл"])
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
            
            avg_grades_query = """
                select
                    u.surname + ' ' + u.name + ' ' + u.patronymic as fio,
                    isnull(s_s.avg_grade, 'н/а') as avg_grade
                from subj_teachers s_t
                inner join subject s on s.id_subject = s_t.id_subject
                inner join name_class n_c on n_c.id_name_class = s_t.id_name_class
                inner join class c on c.id_name_class = n_c.id_name_class
                inner join users u on u.id_user = c.id_user
                inner join subj_students s_s on s_s.id_subject = s.id_subject
                where n_c.id_name_class = ?
                order by u.surname + ' ' + u.name + ' ' + u.patronymic
            """
            cursor.execute(avg_grades_query, (self.grades_group_combo.currentData()))
            grades_data = cursor.fetchall()
            
            cursor.close()
            
            avg_grade_table.setRowCount(len(grades_data))
            
            for row, record in enumerate(grades_data):
                fio = record[0]
                avg_grade = record[1]
                
                # группа
                student_name = QTableWidgetItem(fio)
                student_name.setFlags(student_name.flags() & ~Qt.ItemIsEditable)
                student_name.setTextAlignment(Qt.AlignCenter)
                avg_grade_table.setItem(row, 0, student_name)
                
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
                
                avg_grade_table.setItem(row, 1, avg)
            
            avg_grade_table.resizeColumnsToContents()
            layout.addWidget(avg_grade_table)
            
            dialog.exec_()
            
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить средний балл группы: {str(e)}")

    def show_tests(self):
        self.clear_content_layout()

        self.content_layout_v.addWidget(self.tests_widget)

        self.load_groups_for_tests()

    def tests(self):
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
        tests_layout.addSpacing(2)
        
        top_layout = QHBoxLayout() # для группы, даты и кнопки обновить
        
        group_label = QLabel("Группа:")
        group_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #333;")
        top_layout.addWidget(group_label)
        
        self.tests_group_combo = QComboBox()
        self.tests_group_combo.addItems(["Выберите группу"])
        self.tests_group_combo.setFixedSize(150, 30)
        self.tests_group_combo.setStyleSheet("""
            border-radius: 5px;
            border: 1px solid #ccc;
            color: #333;
            padding: 5px;
            font-family: Roboto;
        """)
        self.tests_group_combo.currentIndexChanged.connect(self.load_tests)
        top_layout.addWidget(self.tests_group_combo)
        
        top_layout.addStretch()

        # date_label = QLabel("Дата занятия:")
        # date_label.setStyleSheet("font-family: Roboto; color: #333;")
        # top_layout.addWidget(date_label, alignment=Qt.AlignLeft)
        
        # self.tests_date = QDateEdit()
        # self.tests_date.setFixedSize(120, 30)
        # self.tests_date.setCalendarPopup(True)
        # self.tests_date.setDate(QDate.currentDate())
        # self.tests_date.setStyleSheet("""
        #     border-radius: 5px;
        #     border: 1px solid #ccc;
        #     color: #333;
        #     padding: 5px;
        #     font-family: Roboto;
        # """)
        # top_layout.addWidget(self.tests_date, alignment=Qt.AlignLeft)
        
        tests_layout.addLayout(top_layout)
        
        # для таблицы
        self.tests_table = QTableWidget()
        self.tests_table.setFixedSize(600, 355)
        self.tests_table.setColumnCount(5)
        self.tests_table.setHorizontalHeaderLabels(["Предмет", "Группа", "Тест", "Дата загрузки", "Срок сдачи"])
        self.tests_table.horizontalHeader().setStretchLastSection(True)
        self.tests_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.tests_table.setSelectionMode(QTableWidget.SingleSelection)
        self.tests_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tests_table.itemSelectionChanged.connect(self.on_tests_selected)
        self.tests_table.setStyleSheet("""
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
        header = self.tests_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Fixed)  # предмет
        header.resizeSection(0, 120)
        header.setSectionResizeMode(1, QHeaderView.Fixed)  # группа
        header.resizeSection(1, 80)
        header.setSectionResizeMode(2, QHeaderView.Fixed)  # тест
        header.resizeSection(2, 140)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # дата загрузки
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # срок сдачи
        tests_layout.addWidget(self.tests_table)
        tests_layout.addSpacing(18)
        
        # область для нижней части экрана
        bottom_layout = QHBoxLayout()
        
        # кнопки для просмотра оценок, добавления и удаления тестов
        view_add_del_layout = QHBoxLayout()
        view_add_del_layout.addStretch()
        
        self.view_grade_button = QPushButton("Просмотреть оценки")
        self.view_grade_button.setFixedSize(150, 35)
        self.view_grade_button.setStyleSheet("""
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
                background-color: #95a5a6;
            }
        """)
        self.view_grade_button.clicked.connect(self.view_test_grades)
        self.view_grade_button.setEnabled(False)
        view_add_del_layout.addWidget(self.view_grade_button)

        self.add_test_button = QPushButton("Добавить тест")
        self.add_test_button.setFixedSize(130, 35)
        self.add_test_button.setStyleSheet("""
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
        self.add_test_button.clicked.connect(self.test_const_open)
        view_add_del_layout.addWidget(self.add_test_button)

        self.del_test_button = QPushButton("Удалить тест")
        self.del_test_button.setFixedSize(130, 35)
        self.del_test_button.setStyleSheet("""
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
                background-color: #95a5a6;
            }
        """)
        self.del_test_button.clicked.connect(self.del_tests)
        self.del_test_button.setEnabled(False)
        view_add_del_layout.addWidget(self.del_test_button)
        
        bottom_layout.addLayout(view_add_del_layout)
        
        tests_layout.addLayout(bottom_layout)

    def load_tests(self):
        try:
            selected_group_id = self.tests_group_combo.currentData()
            # tests_date = self.tests_date.date()
            # tests_date_str = tests_date.toString("yyyy-MM-dd")
            
            if not selected_group_id:
                self.tests_table.setRowCount(0)
                self.selected_test_id = None
                self.del_test_button.setEnabled(False)
                self.view_grade_button.setEnabled(False)
                return
            
            cursor = self.conn.cursor()
            query = """
                select
                    t.id_test,
                    s.subject_name,
                    convert(varchar, n_c.num) + n_c.letter as group_name,
                    t_n.[name],
                    t.upload,
                    t.deadline
                from test t
                inner join test_name t_n on t_n.id_name = t.id_name
                inner join name_class n_c on n_c.id_name_class = t.id_name_class
                inner join subj_teachers s_t on s_t.id_name_class = n_c.id_name_class
                inner join subject s on s.id_subject = s_t.id_subject
                inner join users u on u.id_user = s_t.id_user
                where s_t.id_user = ? and t.id_name_class = ?
                order by id_test desc
            """
            cursor.execute(query, (self.id_user, selected_group_id))
            tests_data = cursor.fetchall()
            
            # вывод в таблице
            self.tests_table.setRowCount(len(tests_data))
            
            for row, record in enumerate(tests_data):
                test_id = record[0]
                subject_name = record[1]
                group_name = record[2]
                test_name = record[3]
                upload_date = record[4]
                deadline_date = record[5]
                
                formatted_upload = upload_date.strftime("%d.%m.%Y")
                formatted_deadline = deadline_date.strftime("%d.%m.%Y")
                
                # предмет
                subject_item = QTableWidgetItem(subject_name)
                subject_item.setData(Qt.UserRole, {'test_id': test_id, 'test_name': test_name})
                subject_item.setFlags(subject_item.flags() & ~Qt.ItemIsEditable)
                subject_item.setTextAlignment(Qt.AlignCenter)
                self.tests_table.setItem(row, 0, subject_item)
                
                # группа
                group_item = QTableWidgetItem(group_name)
                group_item.setData(Qt.UserRole, {'test_id': test_id, 'test_name': test_name})
                group_item.setFlags(group_item.flags() & ~Qt.ItemIsEditable)
                group_item.setTextAlignment(Qt.AlignCenter)
                self.tests_table.setItem(row, 1, group_item)
                
                # название теста
                test_item = QTableWidgetItem(test_name)
                test_item.setData(Qt.UserRole, {'test_id': test_id, 'test_name': test_name})
                test_item.setFlags(test_item.flags() & ~Qt.ItemIsEditable)
                test_item.setTextAlignment(Qt.AlignCenter)
                self.tests_table.setItem(row, 2, test_item)
                
                # дата загрузки
                upload_item = QTableWidgetItem(formatted_upload)
                upload_item.setData(Qt.UserRole, {'test_id': test_id, 'test_name': test_name})
                upload_item.setFlags(upload_item.flags() & ~Qt.ItemIsEditable)
                upload_item.setTextAlignment(Qt.AlignCenter)
                self.tests_table.setItem(row, 3, upload_item)
                
                # срок сдачи
                deadline_item = QTableWidgetItem(formatted_deadline)
                deadline_item.setData(Qt.UserRole, {'test_id': test_id, 'test_name': test_name})
                deadline_item.setFlags(deadline_item.flags() & ~Qt.ItemIsEditable)
                deadline_item.setTextAlignment(Qt.AlignCenter)
                self.tests_table.setItem(row, 4, deadline_item)
            
            cursor.close()
            
            if len(tests_data) == 0:
                self.view_grade_button.setEnabled(False)
                self.del_test_button.setEnabled(False)
            
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить данные о тестах: {str(e)}")
            self.tests_table.setRowCount(0)
            self.view_grade_button.setEnabled(False)
            self.del_test_button.setEnabled(False)

    def on_tests_selected(self):
        selected_items = self.tests_table.selectedItems()
    
        if selected_items:
            item = selected_items[0]
            item_data = item.data(Qt.UserRole)
            
            if item_data and 'test_id' in item_data:
                self.selected_test_id = item_data['test_id']
                self.view_grade_button.setEnabled(True)
                self.del_test_button.setEnabled(True)
            else:
                self.selected_test_id = None
                self.view_grade_button.setEnabled(False)
                self.del_test_button.setEnabled(False)
        else:
            self.selected_test_id = None
            self.view_grade_button.setEnabled(False)
            self.del_test_button.setEnabled(False)

    def load_groups_for_tests(self): # выбор элемента для загрузки групп
        self.load_groups_into_combo(self.tests_group_combo) # в скобках указан элемент для подстановки

    def view_test_grades(self):
        try:
            selected_items = self.tests_table.selectedItems()
            item = selected_items[0]
            item_data = item.data(Qt.UserRole)
            test_id = item_data['test_id']
            test_name = item_data['test_name']

            dialog = QDialog(self)
            dialog.setWindowTitle(f"{test_name}")
            dialog.setFixedSize(500, 400)
            dialog.setWindowFlags(Qt.Dialog | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
            
            layout = QVBoxLayout()
            dialog.setLayout(layout)
            
            grades_table = QTableWidget()
            grades_table.setColumnCount(3)
            grades_table.setHorizontalHeaderLabels(["Ученик", "Оценка", "% выполнения"])
            grades_table.horizontalHeader().setStretchLastSection(True)
            grades_table.setSelectionBehavior(QTableWidget.SelectRows)
            grades_table.setSelectionMode(QTableWidget.SingleSelection)
            grades_table.setEditTriggers(QTableWidget.NoEditTriggers)
            grades_table.setStyleSheet("""
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
                    u.surname + ' ' + u.[name] + ' ' + u.patronymic as fio,
                    s_t.grade,
                    s_t.grade_percent
                from solved_tests s_t
                inner join users u on u.id_user = s_t.id_user
                where s_t.id_test = ?
                order by fio
            """
            cursor.execute(grades_query, (test_id))
            grades_data = cursor.fetchall()
            
            cursor.close()
            
            grades_table.setRowCount(len(grades_data))
            
            for row, record in enumerate(grades_data):
                fio = record[0]
                grade = record[1] if record[1] is not None else "Не оценено"
                grade_percent = record[2] if record[2] is not None else "0"
                
                # фио ученика
                fio_item = QTableWidgetItem(fio)
                fio_item.setFlags(fio_item.flags() & ~Qt.ItemIsEditable)
                fio_item.setTextAlignment(Qt.AlignCenter)
                grades_table.setItem(row, 0, fio_item)
                
                # оценка
                grade_item = QTableWidgetItem(str(grade))
                grade_item.setFlags(grade_item.flags() & ~Qt.ItemIsEditable)
                grade_item.setTextAlignment(Qt.AlignCenter)
                
                # цвет оценки
                if grade >= 4:
                    grade_item.setForeground(QColor("#27ae60"))  # зеленый
                elif grade == 3:
                    grade_item.setForeground(QColor("#f39c12"))  # оранжевый
                elif grade <= 2:
                    grade_item.setForeground(QColor("#e74c3c"))  # красный
                
                grades_table.setItem(row, 1, grade_item)
                
                # процент выполнения
                percent_item = QTableWidgetItem(f"{grade_percent}%")
                percent_item.setFlags(percent_item.flags() & ~Qt.ItemIsEditable)
                percent_item.setTextAlignment(Qt.AlignCenter)
                
                grades_table.setItem(row, 2, percent_item)
            
            grades_table.resizeColumnsToContents()
            layout.addWidget(grades_table)
            
            dialog.exec_()
            
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить оценки за тест: {str(e)}")

    def del_tests(self): # удаление теста
        selected_items = self.tests_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Ошибка", "Тест не выбран")
            return
        
        row = self.tests_table.row(selected_items[0])
        test_name = self.tests_table.item(row, 2).text()
        
        reply = QMessageBox.question(
            self,
            "Подтверждение удаления",
            f"Вы уверены, что хотите удалить тест?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.No:
            return
        
        try:
            cursor = self.conn.cursor()
            
            # проверка оценок для удаления
            check_grades_query = """
                select count(*) 
                from solved_tests 
                where id_test = ?
            """
            cursor.execute(check_grades_query, (self.selected_test_id,))
            has_grades = cursor.fetchone()[0] > 0
            if has_grades:
                QMessageBox.warning(
                    self,
                    "Ошибка",
                    f"Нельзя удалить тест, так как за него уже есть оценки."
                )
                cursor.close()
                return
            
            try:
                test_name_query = """
                    select id_name
                    from test
                    where id_test = ?
                """
                cursor.execute(test_name_query, (self.selected_test_id))
                id_test_name = cursor.fetchone()[0]

                delete_query = """
                    delete from test_content 
                    where id_test = ?
                    delete from test 
                    where id_test = ?
                    delete from test_name 
                    where id_name = ?
                """ # удаление содержания теста
                cursor.execute(delete_query, (
                    self.selected_test_id, self.selected_test_id, id_test_name
                ))
                self.conn.commit()
                
                QMessageBox.information(
                    self,
                    "Успех",
                    f"Тест '{test_name}' удален."
                )
                
                self.selected_test_id = None
                self.view_grade_button.setEnabled(False)
                self.del_test_button.setEnabled(False)
                
                self.load_tests()
                
            except Exception as e:
                QMessageBox.critical(
                self, "Ошибка", f"Не удалось удалить тест: {str(e)}."
                )
                
            cursor.close()
            
        except Exception as e:
            QMessageBox.critical(
                self, "Ошибка", "Не удалось удалить тест."
            )

    def test_const_open(self):
        self.test_window = TestConstructor(self.id_user, self.fio, self.conn)
        self.test_window.show()

    def logout(self): # выход из учетки
        from main import LoginWindow
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()


class TestConstructor(QDialog):
    def __init__(self, id_user = None, fio = None, conn = None):
        super().__init__()
        self.id_user = id_user
        self.fio = fio
        self.conn = conn
        self.setModal(True)
        self.setWindowFlags(Qt.Dialog | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)

        self.setWindowTitle("Конструктор тестов")
        self.setFixedSize(900, 600)
        self.setStyleSheet("background-color: #f0f0f0;")

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

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
        self.test_name_input.setMaxLength(50)
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
        #self.question_text_edit.
        self.question_text_edit.setMaximumHeight(80)
        self.question_text_edit.setPlaceholderText("Введите текст вопроса...")
        self.question_text_edit.setStyleSheet("""
            border-radius: 5px;
            border: 1px solid #ccc;
            padding: 5px;
            font-family: Roboto;
        """)
        self.question_text_edit.textChanged.connect(self.limit_question_length)
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
            self.answer_input.setMaxLength(50)
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

    def limit_question_length(self): # ограничение символов для текста вопроса
        text = self.question_text_edit.toPlainText()
        
        if len(text) > 150:
            cursor = self.question_text_edit.textCursor()
            position = cursor.position()
            
            self.question_text_edit.setPlainText(text[:150])
            
            new_position = min(position, 150)
            cursor.setPosition(new_position)
            self.question_text_edit.setTextCursor(cursor)

    def check_question_exists(self, question_text, answers_data): # проверка на добавленный вопрос
        try:
            cursor = self.conn.cursor()
            
            cursor.execute("""
                select id_question 
                from test_question 
                where text = ?
            """, (question_text,))
            
            existing_question = cursor.fetchone()
            
            if not existing_question:
                cursor.close()
                return None
            
            question_id = existing_question[0]
            
            cursor.execute("""
                select answer, is_true 
                from test_answer 
                where id_question = ?
                order by id_answer
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

            if item_data['question_text'] == question_text:
                return True
            
            # if item_data['question_text'] != question_text:
            #     continue
            
            # item_answers = item_data['answers']
            # if len(item_answers) != len(answers_data):
            #     continue
            
            # all_match = True
            # for j in range(len(answers_data)):
            #     if (item_answers[j]['text'] != answers_data[j]['text'] or 
            #         item_answers[j]['is_correct'] != answers_data[j]['is_correct']):
            #         all_match = False
            #         break
            
            # if all_match:
            #     return True
        
        return False

    def save_test(self):
        if not self.validate_test_data():
            return
        
        try:
            cursor = self.conn.cursor()
            
            test_name = self.test_name_input.text().strip()
            
            cursor.execute("""
                select id_name from test_name where name = ?
            """, (test_name,))
            existing_name = cursor.fetchone()

            if existing_name:
                name_id = existing_name[0]
            else:
                cursor.execute("""
                    insert into test_name (name) values (?)
                """, (test_name,))
                name_id = cursor.execute("select @@IDENTITY").fetchone()[0]
            
            group_id = self.get_selected_group_id()
        
            deadline_date = self.deadline_date.date().toString("yyyy-MM-dd")
            upload_date = QDate.currentDate().toString("yyyy-MM-dd")

            cursor.execute("""
                insert into test (id_name, id_name_class, upload, deadline)
                values (?, ?, ?, ?)
            """, (name_id, group_id, upload_date, deadline_date))
            
            test_id = cursor.execute("select @@IDENTITY").fetchone()[0]
            
            for i in range(self.questions_list.count()):
                item = self.questions_list.item(i)
                item_data = item.data(Qt.UserRole)
                if item_data:
                    question_text = item_data['question_text']
                    
                    cursor.execute("""
                        select id_question from test_question where text = ?
                    """, (question_text,))
                    existing_question = cursor.fetchone()
                    
                    if existing_question:
                        question_id = existing_question[0]
                    else:
                        cursor.execute("""
                            insert into test_question (text) values (?)
                        """, (question_text,))
                        question_id = cursor.execute("select @@IDENTITY").fetchone()[0]
                    
                    for answer in item_data['answers']:
                        answer_text = answer['text']
                        is_correct = 1 if answer['is_correct'] else 0
                        
                        cursor.execute("""
                            select id_answer from test_answer 
                            where id_question = ? and answer = ? and is_true = ?
                        """, (question_id, answer_text, is_correct))
                        
                        answer_row = cursor.fetchone()
                        if answer_row:
                            answer_id = answer_row[0]
                        else:
                            cursor.execute("""
                                insert into test_answer (id_question, answer, is_true)
                                values (?, ?, ?)
                            """, (question_id, answer_text, is_correct))
                            answer_id = cursor.execute("select @@IDENTITY").fetchone()[0]
                        
                        cursor.execute("""
                            select id_content from test_content 
                            where id_test = ? and id_answer = ?
                        """, (test_id, answer_id))
                        
                        if not cursor.fetchone():
                            cursor.execute("""
                                insert into test_content (id_test, id_answer)
                                values (?, ?)
                            """, (test_id, answer_id))
        
            self.conn.commit()
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
            cursor = self.conn.cursor()
            
            query = ("""
                select 
                    s_t.id_name_class,
                    convert(varchar, n_c.num) + n_c.letter
                from subj_teachers s_t
                inner join name_class n_c on n_c.id_name_class = s_t.id_name_class
                inner join users u on u.id_user = s_t.id_user
                where u.id_user = ?
                order by n_c.num, n_c.letter
            """)
            cursor.execute(query, self.id_user)
            groups_data = cursor.fetchall()
            
            self.group_combo.clear()
            
            if groups_data:
                self.group_combo.addItem("Выберите группу")
                for group in groups_data:
                    group_id = group[0]
                    class_name = group[1]
                    group_name = f"{class_name}"
                    self.group_combo.addItem(group_name, group_id)
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
        dialog = QuestionAnswerFromDB(self, self.conn)
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
            QMessageBox.warning(self, "Предупреждение", "Укажите хотя бы один верный вариант ответа")
            return
        
        if self.is_question_in_test_list(question_text, answers_data):
            QMessageBox.warning(
                self,
                "Ошибка",
                "Данный вопрос уже есть в тесте."
            )
            return
        
        answer_texts = [answer['text'] for answer in answers_data]
        duplicates = []
        seen = set()
        for answer_text in answer_texts:
            if answer_text in seen:
                duplicates.append(answer_text)
            else:
                seen.add(answer_text)
        
        if duplicates:
            QMessageBox.warning(
                self,
                "Ошибка",
                f"Все варианты ответов должны быть уникальными"
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
    def __init__(self, parent=None, conn=None):
        super().__init__(parent)
        self.selected_question_id = None
        self.conn = conn
        self.setWindowTitle("Банк вопросов")
        self.setFixedSize(550, 400)
        self.setModal(True)
        self.setWindowFlags(Qt.Dialog | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        
        # таблица для вывода вопросов и ответов
        self.questions_table = QTableWidget()
        self.questions_table.setFixedSize(500, 320)
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
            cursor = self.conn.cursor()
            
            query = ("""
                select 
                    q.id_question,
                    q.text as question_text,
                    string_agg(a.answer + 
                        case when a.is_true = 1 then ' + ' else ' - ' end, 
                        ', ') as answers_list
                from test_question q
                left join test_answer a on q.id_question = a.id_question
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
            cursor = self.conn.cursor()
            
            query = ("""
                select 
                    answer,
                    is_true,
                    id_answer
                from test_answer
                where id_question = ?
                order by id_answer
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