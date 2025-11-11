from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QScrollArea,
                               QLabel, QLineEdit, QPushButton, QFrame, QSpacerItem,
                               QSizePolicy, QGraphicsOpacityEffect, QDialog, QTextEdit)
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QPoint, Signal, QObject
from PySide6.QtGui import QFont
import threading

from chatbot.follow_up import follow_up
from chatbot.question_gen import generate_question
from chatbot.evaluate_answer import evaluate_answer


class FollowUpWorker(QObject):

    finished = Signal(str)


    def __init__(self, messages):
        super().__init__()
        self.messages = messages


    def run(self):
        try:
            follow_up_text = follow_up(self.messages)
            self.finished.emit(follow_up_text)
        except Exception as e:
            self.finished.emit(f'Error: {str(e)}')


class QuestionGeneratorWorker(QObject):

    finished = Signal(str)


    def __init__(self, topic):
        super().__init__()
        self.topic = topic


    def run(self):
        try:
            question = generate_question(self.topic)
            self.finished.emit(question)
        except Exception as e:
            self.finished.emit(f'Error: {str(e)}')


class AnswerEvaluatorWorker(QObject):

    finished = Signal(dict)


    def __init__(self, question, answer):
        super().__init__()
        self.question = question
        self.answer = answer


    def run(self):
        try:
            result = evaluate_answer(self.question, self.answer)
            self.finished.emit(result)
        except Exception as e:
            self.finished.emit({'score': 0, 'feedback': f'Error: {str(e)}'})


class ProblemDescriptionDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Generate Question')
        self.setModal(True)
        self.resize(400, 200)

        layout = QVBoxLayout(self)

        label = QLabel('Enter a topic or problem description:')
        layout.addWidget(label)

        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText('e.g., quadratic equations, Newton\'s laws, Python loops...')
        layout.addWidget(self.text_edit)

        button_layout = QHBoxLayout()
        self.generate_button = QPushButton('Generate')
        self.generate_button.clicked.connect(self.accept)
        self.cancel_button = QPushButton('Cancel')
        self.cancel_button.clicked.connect(self.reject)

        button_layout.addStretch()
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.generate_button)

        layout.addLayout(button_layout)


    def get_description(self):
        return self.text_edit.toPlainText().strip()


class DuelDialog(QDialog):

    answer_submitted = Signal(str)


    def __init__(self, question, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Duel Challenge!')
        self.setModal(True)
        self.resize(500, 350)
        self.question = question
        self.my_score = None
        self.partner_score = None

        self.setup_ui()


    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        title = QLabel('Duel Challenge!')
        title.setObjectName('duelTitle')
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        question_label = QLabel('Question:')
        question_label.setObjectName('duelQuestionLabel')
        layout.addWidget(question_label)

        self.question_text = QLabel(self.question)
        self.question_text.setObjectName('duelQuestionText')
        self.question_text.setWordWrap(True)
        layout.addWidget(self.question_text)

        answer_label = QLabel('Your Answer:')
        answer_label.setObjectName('duelAnswerLabel')
        layout.addWidget(answer_label)

        self.answer_input = QTextEdit()
        self.answer_input.setObjectName('duelAnswerInput')
        self.answer_input.setPlaceholderText('Type your answer here...')
        self.answer_input.setMaximumHeight(100)
        layout.addWidget(self.answer_input)

        self.status_label = QLabel('')
        self.status_label.setObjectName('duelStatusLabel')
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.hide()
        layout.addWidget(self.status_label)

        self.score_label = QLabel('')
        self.score_label.setObjectName('duelScoreLabel')
        self.score_label.setAlignment(Qt.AlignCenter)
        self.score_label.setWordWrap(True)
        self.score_label.hide()
        layout.addWidget(self.score_label)

        button_layout = QHBoxLayout()
        self.submit_button = QPushButton('Submit Answer')
        self.submit_button.clicked.connect(self.on_submit)
        self.close_button = QPushButton('Close')
        self.close_button.clicked.connect(self.accept)
        self.close_button.setEnabled(False)

        button_layout.addStretch()
        button_layout.addWidget(self.submit_button)
        button_layout.addWidget(self.close_button)

        layout.addLayout(button_layout)


    def on_submit(self):
        answer = self.answer_input.toPlainText().strip()
        if not answer:
            return

        self.answer_input.setEnabled(False)
        self.submit_button.setEnabled(False)

        self.status_label.setText('Evaluating your answer...')
        self.status_label.show()

        self.answer_submitted.emit(answer)


    def display_score(self, score, feedback):
        self.my_score = score
        self.status_label.hide()

        score_text = f'Your Score: {score}/10\n{feedback}'

        if self.partner_score is not None:
            score_text += f'\n\nPartner\'s Score: {self.partner_score}/10'
            if score > self.partner_score:
                score_text += '\nYou win!'
            elif score < self.partner_score:
                score_text += '\nImagine loosing!'
            else:
                score_text += '\nIt\'s a tie!'
        else:
            score_text += '\n\nWaiting for partner\'s score...'

        self.score_label.setText(score_text)
        self.score_label.show()

        if self.partner_score is not None:
            self.close_button.setEnabled(True)


    def set_partner_score(self, partner_score):
        self.partner_score = partner_score

        if self.my_score is not None:
            score_text = f'Your Score: {self.my_score}/10'
            score_text += f'\n\nPartner\'s Score: {partner_score}/10'

            if self.my_score > partner_score:
                score_text += '\nYou win!'
            elif self.my_score < partner_score:
                score_text += '\nImagine loosing!'
            else:
                score_text += '\nIt\'s a tie!'

            self.score_label.setText(score_text)
            self.close_button.setEnabled(True)


class MessageBubble(QFrame):

    def __init__(self, text, bubble_type='own', parent=None):
        super().__init__(parent)
        self.bubble_type = bubble_type

        self.setup_ui(text)

        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)

        self.animate_in()


    def setup_ui(self, text):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 8, 10, 8)

        self.label = QLabel(text)
        self.label.setWordWrap(True)
        self.label.setTextInteractionFlags(Qt.TextSelectableByMouse)

        if self.bubble_type == 'own':
            self.setObjectName('ownBubble')
            self.label.setObjectName('ownText')
            self.label.setAlignment(Qt.AlignRight)
        elif self.bubble_type == 'partner':
            self.setObjectName('partnerBubble')
            self.label.setObjectName('partnerText')
            self.label.setAlignment(Qt.AlignLeft)
        elif self.bubble_type == 'ai':
            self.setObjectName('aiBubble')
            self.label.setObjectName('aiText')
            self.label.setAlignment(Qt.AlignLeft)
        elif self.bubble_type == 'status':
            self.setObjectName('statusBubble')
            self.label.setObjectName('statusText')
            self.label.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.label)
        self.setMinimumWidth(400)
        self.setMaximumWidth(700)


    def animate_in(self):
        self.fade_anim = QPropertyAnimation(self.opacity_effect, b'opacity')
        self.fade_anim.setDuration(400)
        self.fade_anim.setStartValue(0.0)
        self.fade_anim.setEndValue(1.0)
        self.fade_anim.setEasingCurve(QEasingCurve.OutCubic)
        self.fade_anim.finished.connect(lambda: self.setGraphicsEffect(None))
        self.fade_anim.start()


class ChatWidget(QWidget):

    question_generated = Signal(str)
    duel_requested = Signal(str)
    duel_answer_submitted = Signal(str, str)


    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Modern Chat UI')
        self.resize(600, 800)

        self.messages = []
        self.partner_connected = False
        self.active_duel_dialog = None

        self.setup_ui()


    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        content_layout = QHBoxLayout()
        content_layout.setSpacing(0)
        content_layout.setContentsMargins(0, 0, 0, 0)

        chat_container = QWidget()
        chat_layout = QVBoxLayout(chat_container)
        chat_layout.setContentsMargins(0, 0, 0, 0)
        chat_layout.setSpacing(0)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setObjectName('scrollArea')

        self.message_container = QWidget()
        self.message_layout = QVBoxLayout(self.message_container)
        self.message_layout.setContentsMargins(20, 20, 20, 20)
        self.message_layout.setSpacing(15)
        self.message_layout.addStretch()

        self.scroll_area.setWidget(self.message_container)
        chat_layout.addWidget(self.scroll_area)

        input_frame = QFrame()
        input_frame.setObjectName('inputFrame')
        input_v_layout = QVBoxLayout(input_frame)
        input_v_layout.setContentsMargins(20, 15, 20, 15)

        input_layout = QHBoxLayout()
        input_layout.setContentsMargins(20, 15, 20, 15)
        input_layout.setSpacing(10)
        input_v_layout.addLayout(input_layout)

        self.message_input = QLineEdit()
        self.message_input.setObjectName('messageInput')
        self.message_input.setPlaceholderText('Type a message...')
        self.message_input.returnPressed.connect(self.on_send_clicked)

        self.send_button = QPushButton('Send')
        self.send_button.setObjectName('sendButton')
        self.send_button.clicked.connect(self.on_send_clicked)
        self.send_button.setCursor(Qt.PointingHandCursor)

        input_layout.addWidget(self.message_input)
        input_layout.addWidget(self.send_button)

        self.follow_up_button = QPushButton('Follow-ups will appear here')
        self.follow_up_button.setObjectName('followUpButton')
        self.follow_up_button.clicked.connect(lambda: self.message_input.setText(self.follow_up_button.text()))
        self.follow_up_button.clicked.connect(lambda: self.update())

        input_v_layout.addWidget(self.follow_up_button)

        chat_layout.addWidget(input_frame)

        content_layout.addWidget(chat_container)

        sidebar = QFrame()
        sidebar.setObjectName('sidebar')
        sidebar.setMinimumWidth(200)
        sidebar.setMaximumWidth(250)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(15, 20, 15, 20)
        sidebar_layout.setSpacing(10)

        sidebar_title = QLabel('Tools')
        sidebar_title.setObjectName('sidebarTitle')
        sidebar_title.setAlignment(Qt.AlignCenter)
        sidebar_layout.addWidget(sidebar_title)

        self.generate_question_button = QPushButton('Generate Question')
        self.generate_question_button.setObjectName('generateQuestionButton')
        self.generate_question_button.clicked.connect(self.on_generate_question_clicked)
        self.generate_question_button.setEnabled(False)
        self.generate_question_button.setCursor(Qt.PointingHandCursor)
        sidebar_layout.addWidget(self.generate_question_button)

        self.duel_button = QPushButton('Duel')
        self.duel_button.setObjectName('duelButton')
        self.duel_button.clicked.connect(self.on_duel_clicked)
        self.duel_button.setEnabled(False)
        self.duel_button.setCursor(Qt.PointingHandCursor)
        sidebar_layout.addWidget(self.duel_button)

        sidebar_layout.addStretch()

        content_layout.addWidget(sidebar)

        main_layout.addLayout(content_layout)


    def send_own_message(self, text):
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addStretch()

        bubble = MessageBubble(text, 'own')
        layout.addWidget(bubble)

        self.message_layout.insertWidget(self.message_layout.count() - 1, container)
        self.scroll_to_bottom()

        self.messages.append([text, 'own'])
        self.generate_follow_up()


    def send_partner_message(self, text):
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)

        bubble = MessageBubble(text, 'partner')
        layout.addWidget(bubble)
        layout.addStretch()

        self.message_layout.insertWidget(self.message_layout.count() - 1, container)
        self.scroll_to_bottom()

        self.messages.append([text, 'partner'])


    def send_status(self, text):
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addStretch()

        bubble = MessageBubble(text, 'status')
        bubble.setMinimumWidth(300)
        bubble.setMaximumWidth(400)
        layout.addWidget(bubble)
        layout.addStretch()

        self.message_layout.insertWidget(self.message_layout.count() - 1, container)
        self.scroll_to_bottom()


    def send_ai_message(self, text):
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)

        bubble = MessageBubble(text, 'ai')
        layout.addWidget(bubble)
        layout.addStretch()

        self.message_layout.insertWidget(self.message_layout.count() - 1, container)
        self.scroll_to_bottom()

        self.messages.append([text, 'ai'])


    def on_send_clicked(self):
        text = self.message_input.text().strip()
        if text:
            self.send_own_message(text)
            self.message_input.clear()


    def generate_follow_up(self):
        worker = FollowUpWorker(self.messages.copy())
        worker.finished.connect(self._on_follow_up_generated)

        thread = threading.Thread(target=worker.run, daemon=True)
        thread.start()


    def _on_follow_up_generated(self, follow_up_text):
        self.follow_up_button.setText(follow_up_text)


    def scroll_to_bottom(self):
        self.scroll_area.verticalScrollBar().setValue(
            self.scroll_area.verticalScrollBar().maximum()
        )


    def on_generate_question_clicked(self):
        if not self.partner_connected:
            self.send_status('Cannot generate question: No partner connected')
            return

        dialog = ProblemDescriptionDialog(self)
        if dialog.exec() == QDialog.Accepted:
            topic = dialog.get_description()
            if topic:
                self.send_status('Generating question...')
                self.generate_question_button.setEnabled(False)

                worker = QuestionGeneratorWorker(topic)
                worker.finished.connect(self._on_question_generated)

                thread = threading.Thread(target=worker.run, daemon=True)
                thread.start()


    def _on_question_generated(self, question):
        self.generate_question_button.setEnabled(self.partner_connected)

        if question.startswith('Error:'):
            self.send_status(question)
        else:
            self.question_generated.emit(question)


    def set_partner_connected(self, connected):
        self.partner_connected = connected
        self.generate_question_button.setEnabled(connected)
        self.duel_button.setEnabled(connected)


    def on_duel_clicked(self):
        if not self.partner_connected:
            self.send_status('Cannot start duel: No partner connected')
            return

        dialog = ProblemDescriptionDialog(self)
        dialog.setWindowTitle('Start a Duel')
        if dialog.exec() == QDialog.Accepted:
            topic = dialog.get_description()
            if topic:
                self.send_status('Generating duel question...')
                self.duel_button.setEnabled(False)

                self.duel_requested.emit(topic)


    def show_duel_dialog(self, question):
        self.active_duel_dialog = DuelDialog(question, self)
        self.active_duel_dialog.answer_submitted.connect(self.on_duel_answer_submitted)
        self.active_duel_dialog.exec()
        self.active_duel_dialog = None


    def on_duel_answer_submitted(self, answer):
        if self.active_duel_dialog:
            question = self.active_duel_dialog.question
            self.duel_answer_submitted.emit(question, answer)


    def display_duel_score(self, score, feedback):
        if self.active_duel_dialog:
            self.active_duel_dialog.display_score(score, feedback)


    def display_partner_duel_score(self, partner_score):
        if self.active_duel_dialog:
            self.active_duel_dialog.set_partner_score(partner_score)


    def enable_duel_button(self):
        self.duel_button.setEnabled(self.partner_connected)
