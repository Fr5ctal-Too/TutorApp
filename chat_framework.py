from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QScrollArea,
                               QLabel, QLineEdit, QPushButton, QFrame, QSpacerItem,
                               QSizePolicy)
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QPoint
from PySide6.QtGui import QFont


class MessageBubble(QFrame):

    def __init__(self, text, bubble_type='own', parent=None):
        super().__init__(parent)
        self.bubble_type = bubble_type
        self._opacity = 0.0

        self.setup_ui(text)

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
        self.setMaximumWidth(500)

    def animate_in(self):
        start_pos = QPoint(0, 20)
        end_pos = QPoint(0, 0)

        self.slide_anim = QPropertyAnimation(self, b'pos')
        self.slide_anim.setDuration(400)
        self.slide_anim.setStartValue(self.pos() + start_pos)
        self.slide_anim.setEndValue(self.pos() + end_pos)
        self.slide_anim.setEasingCurve(QEasingCurve.OutCubic)

        self.fade_anim = QPropertyAnimation(self, b'opacity')
        self.fade_anim.setDuration(400)
        self.fade_anim.setStartValue(0.0)
        self.fade_anim.setEndValue(1.0)
        self.fade_anim.setEasingCurve(QEasingCurve.OutCubic)

        self.fade_anim.start()

    def get_opacity(self):
        return self._opacity

    def set_opacity(self, value):
        self._opacity = value
        self.setStyleSheet(f'QFrame #{self.objectName()} {{ opacity: {value}; }}')

    opacity = Property(float, get_opacity, set_opacity)


class ChatWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Modern Chat UI')
        self.resize(600, 800)

        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

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
        main_layout.addWidget(self.scroll_area)

        input_frame = QFrame()
        input_frame.setObjectName('inputFrame')
        input_layout = QHBoxLayout(input_frame)
        input_layout.setContentsMargins(20, 15, 20, 15)
        input_layout.setSpacing(10)

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

        main_layout.addWidget(input_frame)

    def send_own_message(self, text):
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addStretch()

        bubble = MessageBubble(text, 'own')
        layout.addWidget(bubble)

        self.message_layout.insertWidget(self.message_layout.count() - 1, container)
        self.scroll_to_bottom()

    def send_partner_message(self, text):
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)

        bubble = MessageBubble(text, 'partner')
        layout.addWidget(bubble)
        layout.addStretch()

        self.message_layout.insertWidget(self.message_layout.count() - 1, container)
        self.scroll_to_bottom()

    def send_status(self, text):
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addStretch()

        bubble = MessageBubble(text, 'status')
        bubble.setMaximumWidth(200)
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

    def on_send_clicked(self):
        text = self.message_input.text().strip()
        if text:
            self.send_own_message(text)
            self.message_input.clear()

    def scroll_to_bottom(self):
        self.scroll_area.verticalScrollBar().setValue(
            self.scroll_area.verticalScrollBar().maximum()
        )
