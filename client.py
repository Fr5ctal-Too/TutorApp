import sys
import socket
import threading
import json
from datetime import datetime
from enum import Enum

from PySide6.QtWidgets import (QApplication, QMainWindow, QDialog, QVBoxLayout,
                               QHBoxLayout, QLabel, QPushButton, QComboBox,
                               QWidget, QDialogButtonBox)
from PySide6.QtCore import QObject, Signal, Slot, QTimer, Qt
from PySide6.QtGui import QFont

from chat_framework import ChatWidget
import style


class MessageType(Enum):
    CHAT = 'chat'
    STATUS = 'status'
    SYSTEM = 'system'
    REGISTER = 'register'


class SelectionDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Peer Tutoring - Select Subject & Role')
        self.setModal(True)
        self.setMinimumWidth(400)

        self.subject = None
        self.role = None

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        title = QLabel('Welcome to Peer Tutoring')
        title.setObjectName('dialogTitle')
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        subject_label = QLabel('Select Subject:')
        subject_label.setObjectName('dialogLabel')
        layout.addWidget(subject_label)

        self.subject_combo = QComboBox()
        self.subject_combo.setObjectName('dialogCombo')
        self.subject_combo.addItems([
            'Mathematics',
            'Physics',
            'Chemistry',
            'Biology',
            'Computer Science',
            'English',
            'History',
            'Geography'
        ])
        layout.addWidget(self.subject_combo)

        role_label = QLabel('Select Role:')
        role_label.setObjectName('dialogLabel')
        layout.addWidget(role_label)

        self.role_combo = QComboBox()
        self.role_combo.setObjectName('dialogCombo')
        self.role_combo.addItems([
            'Learn (Find a Tutor)',
            'Teach (Be a Tutor)'
        ])
        layout.addWidget(self.role_combo)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.setObjectName('dialogButtons')
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def get_selection(self):
        subject = self.subject_combo.currentText()
        role_text = self.role_combo.currentText()
        role = 'learn' if 'Learn' in role_text else 'teach'
        return subject, role


class SocketChatClient(QObject):

    message_received = Signal(str)
    status_changed = Signal(str)

    def __init__(self, host='localhost', port=5555):
        super().__init__()
        self.host = host
        self.port = port
        self.client_socket = None
        self.connected = False
        self.running = False
        self.registered = False

    def connect_to_server(self):
        try:
            print(f'\nConnecting to server at {self.host}:{self.port}...')
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.host, self.port))
            self.running = True
            print('Connected to server!')

            receive_thread = threading.Thread(target=self.receive_messages)
            receive_thread.daemon = True
            receive_thread.start()

            return True

        except Exception as e:
            print(f'\n[ERROR] Could not connect to server: {e}')
            self.status_changed.emit(f'Connection failed: {e}')
            return False

    def register_with_server(self, subject, role):
        if not self.running:
            print('[ERROR] Cannot register. Not connected to server.')
            return False

        try:
            register_message = {
                'type': MessageType.REGISTER.value,
                'subject': subject,
                'role': role
            }
            message_json = json.dumps(register_message)
            self.client_socket.send(message_json.encode('utf-8'))
            self.registered = True
            print(f'Registered with subject: {subject}, role: {role}')
            self.status_changed.emit(f'Looking for a {("tutor" if role == "learn" else "student")} in {subject}...')
            return True
        except Exception as e:
            print(f'[ERROR] Failed to register: {e}')
            self.status_changed.emit(f'Failed to register: {e}')
            return False

    def receive_messages(self):
        while self.running:
            try:
                data = self.client_socket.recv(4096)
                if not data:
                    break

                message_str = data.decode('utf-8')

                try:
                    msg_dict = json.loads(message_str)

                    if 'type' not in msg_dict:
                        print(f'[WARNING] Invalid message format: missing \'type\' field')
                        continue

                    msg_type = msg_dict.get('type')

                    if msg_type == MessageType.STATUS.value:
                        self.handle_status_message(msg_dict)
                    elif msg_type == MessageType.CHAT.value:
                        self.handle_chat_message(msg_dict)
                    elif msg_type == MessageType.SYSTEM.value:
                        self.handle_system_message(msg_dict)
                    else:
                        print(f'[WARNING] Unknown message type: {msg_type}')

                except json.JSONDecodeError as e:
                    print(f'[ERROR] Invalid JSON received: {e}')
                    continue

            except Exception as e:
                if self.running:
                    print(f'\n[ERROR] Error receiving message: {e}')
                break

        if self.running:
            self.handle_disconnection()

    def handle_status_message(self, msg_dict):
        status_code = msg_dict.get('status', 'unknown')
        status_msg = msg_dict.get('message', 'Status update')

        print(f'\n[STATUS] {status_msg}')
        self.status_changed.emit(status_msg)

        if status_code == 'waiting':
            self.connected = False
        elif status_code == 'connected':
            self.connected = True
        elif status_code == 'disconnected':
            self.connected = False

    def handle_chat_message(self, msg_dict):
        content = msg_dict.get('content', '')
        sender = msg_dict.get('sender', 'Partner')

        timestamp = datetime.now().strftime('%H:%M:%S')
        print(f'[{timestamp}] {sender}: {content}')
        self.message_received.emit(content)

    def handle_system_message(self, msg_dict):
        system_msg = msg_dict.get('message', 'System message')
        print(f'\n[SYSTEM] {system_msg}')
        self.status_changed.emit(f'System: {system_msg}')

    def send_message(self, message):
        if not self.registered:
            print('[INFO] Cannot send message. Not registered yet.')
            return False

        if not self.connected:
            print('[INFO] Cannot send message. Not connected to a partner yet.')
            self.status_changed.emit('Cannot send message. Not connected to a partner yet.')
            return False

        if message:
            try:
                chat_message = {
                    'type': MessageType.CHAT.value,
                    'content': message
                }
                message_json = json.dumps(chat_message)
                self.client_socket.send(message_json.encode('utf-8'))

                timestamp = datetime.now().strftime('%H:%M:%S')
                print(f'[{timestamp}] You: {message}')
                return True
            except Exception as e:
                print(f'[ERROR] Failed to send message: {e}')
                self.status_changed.emit(f'Failed to send message: {e}')
                return False
        return False

    def handle_disconnection(self):
        print('\n[STATUS] Disconnected from server')
        self.status_changed.emit('Disconnected from server')
        self.running = False

    def disconnect_server(self):
        self.running = False
        if self.client_socket:
            try:
                self.client_socket.close()
            except:
                pass


class PeerTutoringChatWidget(ChatWidget):

    def __init__(self, socket_client):
        super().__init__()
        self.socket_client = socket_client
        self.setWindowTitle('Peer Tutoring Chat')

    def on_send_clicked(self):
        text = self.message_input.text().strip()
        if text:
            if self.socket_client.send_message(text):
                self.send_own_message(text)
            self.message_input.clear()


class ChatWindow(QMainWindow):

    def __init__(self, host='localhost', port=5555):
        super().__init__()
        self.setWindowTitle('Peer Tutoring App')
        self.setGeometry(100, 100, 800, 600)

        self.socket_client = SocketChatClient(host, port)

        self.chat_widget = PeerTutoringChatWidget(self.socket_client)
        self.setCentralWidget(self.chat_widget)

        self.setup_connections()

        self.show_selection_dialog()

    def setup_connections(self):
        self.socket_client.message_received.connect(self.handle_socket_message)
        self.socket_client.status_changed.connect(self.handle_status_change)

    def show_selection_dialog(self):
        dialog = SelectionDialog(self)

        connection_thread = threading.Thread(target=self.connect_to_server_async)
        connection_thread.daemon = True
        connection_thread.start()

        if dialog.exec() == QDialog.Accepted:
            subject, role = dialog.get_selection()
            print(f'User selected: {subject}, {role}')

            self.chat_widget.send_status('Connecting to server...')

            QTimer.singleShot(500, lambda: self.register_with_selection(subject, role))
        else:
            print('User cancelled selection')
            QTimer.singleShot(100, self.close)

    def connect_to_server_async(self):
        if not self.socket_client.connect_to_server():
            print('Failed to connect to server. Please make sure the server is running.')

    def register_with_selection(self, subject, role):
        self.socket_client.register_with_server(subject, role)

    def handle_socket_message(self, message):
        self.chat_widget.send_partner_message(message)

    def handle_status_change(self, status):
        self.chat_widget.send_status(status)

    def closeEvent(self, event):
        self.socket_client.disconnect_server()
        event.accept()


def main():
    app = QApplication(sys.argv)

    app.setStyleSheet(style.get_stylesheet())

    HOST = 'localhost'
    PORT = 5555

    window = ChatWindow(HOST, PORT)
    window.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
