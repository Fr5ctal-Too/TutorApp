STYLESHEET = '''
/* ==================== Base Styles ==================== */

* {
    font-family: 'Segoe UI', 'Roboto', 'Arial', sans-serif;
}

QWidget {
    background-color: #1a1a1a;
    color: #ffffff;
    font-size: 14px;
}

QDialog {
    background-color: #1a1a1a;
}

QMainWindow {
    background-color: #1a1a1a;
}


/* ==================== Selection Dialog ==================== */

QLabel#dialogTitle {
    font-size: 24px;
    font-weight: bold;
    color: #ffffff;
    padding: 10px;
    background-color: transparent;
}

QLabel#dialogLabel {
    font-size: 14px;
    color: #ffffff;
    font-weight: bold;
    margin-top: 10px;
    background-color: transparent;
}

QComboBox#dialogCombo {
    background-color: #3a3a3a;
    color: #ffffff;
    border: 2px solid #4a4a4a;
    border-radius: 8px;
    padding: 10px;
    font-size: 14px;
}

QComboBox#dialogCombo:hover {
    border: 2px solid #6a6a6a;
}

QComboBox#dialogCombo::drop-down {
    border: none;
    padding-right: 10px;
}

QComboBox#dialogCombo::down-arrow {
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 5px solid #ffffff;
    margin-right: 5px;
}

QComboBox#dialogCombo QAbstractItemView {
    background-color: #3a3a3a;
    color: #ffffff;
    selection-background-color: #4a4a4a;
    border: 1px solid #4a4a4a;
}

QDialogButtonBox QPushButton {
    background-color: #ffffff;
    color: #1a1a1a;
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    font-weight: bold;
    font-size: 14px;
    min-width: 80px;
}

QDialogButtonBox QPushButton:hover {
    background-color: #e0e0e0;
}

QDialogButtonBox QPushButton:pressed {
    background-color: #d0d0d0;
}


/* ==================== Chat Widget ==================== */

/* Scroll Area */
QScrollArea {
    border: none;
    background-color: #1a1a1a;
}

QScrollArea > QWidget > QWidget {
    background-color: #1a1a1a;
}

/* Scrollbar */
QScrollBar:vertical {
    border: none;
    background-color: #1a1a1a;
    width: 8px;
    margin: 0px;
}

QScrollBar::handle:vertical {
    background-color: #3a3a3a;
    border-radius: 4px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background-color: #4a4a4a;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background: none;
}

/* Input Frame */
QFrame#inputFrame {
    background-color: #2a2a2a;
    border-top: 1px solid #3a3a3a;
}

/* Message Input */
QLineEdit#messageInput {
    background-color: #3a3a3a;
    border: 2px solid #4a4a4a;
    border-radius: 20px;
    padding: 10px 15px;
    color: #ffffff;
    font-size: 14px;
}

QLineEdit#messageInput:focus {
    border: 2px solid #ffffff;
}

/* Send Button */
QPushButton#sendButton {
    background-color: #ffffff;
    color: #1a1a1a;
    border: none;
    border-radius: 20px;
    padding: 10px 25px;
    font-weight: bold;
    font-size: 14px;
}

QPushButton#sendButton:hover {
    background-color: #e0e0e0;
}

QPushButton#sendButton:pressed {
    background-color: #d0d0d0;
}


/* ==================== Message Bubbles ==================== */

/* Own Message Bubble */
QFrame#ownBubble {
    background-color: #ffffff;
    border-radius: 18px;
    border-top-right-radius: 4px;
}

QLabel#ownText {
    color: #1a1a1a;
    padding: 5px;
    background-color: transparent;
}

/* Partner Message Bubble */
QFrame#partnerBubble {
    background-color: #3a3a3a;
    border-radius: 18px;
    border-top-left-radius: 4px;
}

QLabel#partnerText {
    color: #ffffff;
    padding: 5px;
    background-color: transparent;
}

/* AI Message Bubble */
QFrame#aiBubble {
    background-color: #4a4a4a;
    border-radius: 18px;
    border-top-left-radius: 4px;
    border: 2px solid #6a6a6a;
}

QLabel#aiText {
    color: #ffffff;
    padding: 5px;
    font-style: italic;
    background-color: transparent;
}

/* Status Bubble */
QFrame#statusBubble {
    background-color: #2a2a2a;
    border-radius: 12px;
    border: 1px solid #3a3a3a;
}

QLabel#statusText {
    color: #888888;
    font-size: 12px;
    padding: 3px 10px;
    background-color: transparent;
}
'''


def get_stylesheet():
    return STYLESHEET