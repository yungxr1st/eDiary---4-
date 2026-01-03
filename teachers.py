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
        from main import LoginWindow
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
            cursor = self.conn.cursor()
            
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
            cursor = self.conn.cursor()
            
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
            cursor = self.conn.cursor()
            
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
            cursor = self.conn.cursor()
            
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