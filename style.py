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

/* Text Edit in Dialogs */
QTextEdit {
    background-color: #3a3a3a;
    color: #ffffff;
    border: 2px solid #4a4a4a;
    border-radius: 8px;
    padding: 10px;
    font-size: 14px;
}

QTextEdit:focus {
    border: 2px solid #6a6a6a;
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

/* Upload/Attach Button */
QPushButton#attachButton {
    background-color: #4a7c59;
    color: #ffffff;
    border: none;
    border-radius: 5px;
    padding: 10px 20px;
    font-weight: bold;
    font-size: 14px;
}

QPushButton#attachButton:hover {
    background-color: #5a8d6a;
}

QPushButton#attachButton:pressed {
    background-color: #3a6b49;
}

/* Send Button */
QPushButton#sendButton {
    background-color: #ffffff;
    color: #1a1a1a;
    border: none;
    border-radius: 5px;
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

/* Follow-Up Button */
QPushButton#followUpButton {
    background-color: #ffffff;
    color: #1a1a1a;
    border: none;
    border-radius: 5px;
    padding: 10px 25px;
    font-size: 12px;
    font-weight: 500;
}

QPushButton#followUpButton:hover {
    background-color: #e0e0e0;
}

QPushButton#followUpButton:pressed {
    background-color: #d0d0d0;
}


/* ==================== Sidebar ==================== */

QFrame#sidebar {
    background-color: #2a2a2a;
    border-left: 1px solid #3a3a3a;
}

QLabel#sidebarTitle {
    font-size: 16px;
    font-weight: bold;
    color: #ffffff;
    padding: 10px 0px;
    background-color: transparent;
}

QPushButton#generateQuestionButton {
    background-color: #3a3a3a;
    color: #ffffff;
    border: 2px solid #4a4a4a;
    border-radius: 8px;
    padding: 12px 15px;
    font-weight: bold;
    font-size: 13px;
    text-align: center;
}

QPushButton#generateQuestionButton:hover {
    background-color: #4a4a4a;
    border: 2px solid #6a6a6a;
}

QPushButton#generateQuestionButton:pressed {
    background-color: #5a5a5a;
}

QPushButton#generateQuestionButton:disabled {
    background-color: #2a2a2a;
    color: #5a5a5a;
    border: 2px solid #3a3a3a;
}

QPushButton#duelButton {
    background-color: #3a3a3a;
    color: #ffffff;
    border: 2px solid #4a4a4a;
    border-radius: 8px;
    padding: 12px 15px;
    font-weight: bold;
    font-size: 13px;
    text-align: center;
}

QPushButton#duelButton:hover {
    background-color: #4a4a4a;
    border: 2px solid #6a6a6a;
}

QPushButton#duelButton:pressed {
    background-color: #5a5a5a;
}

QPushButton#duelButton:disabled {
    background-color: #2a2a2a;
    color: #5a5a5a;
    border: 2px solid #3a3a3a;
}


/* ==================== Duel Dialog ==================== */

QLabel#duelTitle {
    font-size: 20px;
    font-weight: bold;
    color: #ffffff;
    padding: 10px;
    background-color: transparent;
}

QLabel#duelQuestionLabel, QLabel#duelAnswerLabel {
    font-size: 13px;
    color: #ffffff;
    font-weight: bold;
    background-color: transparent;
}

QLabel#duelQuestionText {
    font-size: 14px;
    color: #ffffff;
    background-color: #3a3a3a;
    padding: 10px;
    border-radius: 8px;
    border: 1px solid #4a4a4a;
}

QTextEdit#duelAnswerInput {
    background-color: #3a3a3a;
    color: #ffffff;
    border: 2px solid #4a4a4a;
    border-radius: 8px;
    padding: 10px;
    font-size: 14px;
}

QTextEdit#duelAnswerInput:focus {
    border: 2px solid #6a6a6a;
}

QTextEdit#duelAnswerInput:disabled {
    background-color: #2a2a2a;
    color: #6a6a6a;
}

QLabel#duelStatusLabel {
    font-size: 13px;
    color: #888888;
    font-style: italic;
    padding: 5px;
    background-color: transparent;
}

QLabel#duelScoreLabel {
    font-size: 14px;
    color: #ffffff;
    background-color: #3a3a3a;
    padding: 15px;
    border-radius: 8px;
    border: 2px solid #4a4a4a;
    font-weight: bold;
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


/* ==================== File Attachment Bubbles ==================== */

/* File Bubble - Own */
QFrame#ownBubble QLabel {
    color: #1a1a1a;
    padding: 5px;
    background-color: transparent;
    font-size: 14px;
}

/* File Bubble - Partner */
QFrame#partnerBubble QLabel {
    color: #ffffff;
    padding: 5px;
    background-color: transparent;
    font-size: 14px;
}

/* Download Button */
QPushButton#downloadButton {
    background-color: #3b82f6;
    color: #ffffff;
    border: none;
    border-radius: 6px;
    padding: 8px 20px;
    font-weight: bold;
    font-size: 13px;
    margin-top: 5px;
}

QPushButton#downloadButton:hover {
    background-color: #2563eb;
}

QPushButton#downloadButton:pressed {
    background-color: #1d4ed8;
}
'''


def get_stylesheet():
    return STYLESHEET