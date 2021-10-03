
pushButtonStyleSheet = """
    QPushButton{
        border-style: solid;
        border-top-color: transparent;
        border-right-color: transparent;
        border-left-color: transparent;
        border-bottom-color: transparent;
        border-width: 1px;
        border-style: solid;
        font: 14pt bold;
        color: #a9b7c6;
        padding: 2px;
        background-color: #000000;
    }
    QPushButton::default{
        border-style: solid;
        border-top-color: transparent;
        border-right-color: transparent;
        border-left-color: transparent;
        border-bottom-color: #e67e22;
        border-width: 1px;
        color: #a9b7c6;
        padding: 2px;
        background-color: #000000;
    }
    QPushButton:hover{
        border-style: solid;
        border-top-color: transparent;
        border-right-color: transparent;
        border-left-color: transparent;
        border-bottom-color: #e67e22;
        border-bottom-width: 1px;
        border-style: solid;
        color: #FFFFFF;
        padding-bottom: 2px;
        background-color: #000000;
    }
    QPushButton:pressed{
        border-style: solid;
        border-top-color: transparent;
        border-right-color: transparent;
        border-left-color: transparent;
        border-bottom-color: #e67e22;
        border-bottom-width: 2px;
        border-style: solid;
        color: #e67e22;
        padding-bottom: 1px;
        background-color: #000000;
    }
    QPushButton:disabled{
        border-style: solid;
        border-top-color: transparent;
        border-right-color: transparent;
        border-left-color: transparent;
        border-bottom-color: transparent;
        border-bottom-width: 2px;
        border-style: solid;
        color: #808086;
        padding-bottom: 1px;
        background-color: #000000;
    }
    """

toolButtonStyleSheet = """
    QToolButton {
        border-style: solid;
        border-top-color: #e67e22;
        border-right-color: #e67e22;
        border-left-color: #e67e22;
        border-bottom-color: #e67e22;
        border-bottom-width: 1px;
        border-style: solid;
        color: #a9b7c6;
        padding: 2px;
        background-color: #444;
    }
    QToolButton:hover{
        border-style: solid;
        border-top-color: transparent;
        border-right-color: transparent;
        border-left-color: transparent;
        border-bottom-color: #e67e22;
        border-bottom-width: 2px;
        border-style: solid;
        color: #FFFFFF;
        padding-bottom: 1px;
        background-color: #000000;
    }"""


checkBoxStyleSheet ="""
    QCheckBox {
        color: #000;
        padding: 6px;
    }
    QCheckBox:disabled {
        color: #808086;
        padding: 6px;
    }

    QCheckBox:hover {
        border-radius: 4px;
        border-style: #611 solid;
        padding: 4px;
        border-width: 2px;
        border-color: rgb(0, 0, 0);
        background-color:#dddddd;
    }
    QCheckBox::indicator:checked {

        height: 13px;
        width: 13px;
        border-style:solid;
        border-width: 2px;
        border-color: #e67e22;
        color: #a9b7c6;
        background-color: #d63d12;
    }
    QCheckBox::indicator:unchecked {

        height: 11px;
        width: 11px;
        border-style:solid;
        border-width: 2px;
        border-color: #e67e22;
        color: #a9b7c6;
        background-color: transparent;
    }"""


tabBarStyleSheet = """
    QTabWidget {
        color:rgb(0,0,0);
        background-color:#000000;
        font: bold 100pt;
    }
    QTabWidget::pane {
            border-color: rgb(77,77,77);
            background-color:#000000;
            border-style: solid;
            border-width: 1px;
            border-radius: 6px;
            font: bold 100pt;
    }
    QTabBar::tab {
        border-style: solid;
        border-top-color: transparent;
        border-right-color: transparent;
        border-left-color: transparent;
        border-bottom-color: transparent;
        font: bold 100pt;
        border-bottom-width: 1px;
        border-style: solid;
        color: #808086;
        padding: 3px;
        margin-left:3px;
        background-color:#000000;
    }
    QTabBar::tab:selected, QTabBar::tab:last:selected, QTabBar::tab:hover {
        border-style: solid;
        border-top-color: transparent;
        border-right-color: transparent;
        border-left-color: transparent;
        font: 100pt bold;
        border-bottom-color: #e67e22;
        border-bottom-width: 2px;
        border-style: solid;
        color: #FFFFFF;
        padding-left: 3px;
        padding-bottom: 2px;
        margin-left:3px;
        background-color:#000000;
    }
    QRadioButton {
        color: #a9b7c6;
        background-color:#000000;
        padding: 1px;
    }
    QRadioButton::indicator:checked {
        height: 10px;
        width: 10px;
        border-style:solid;
        border-radius:5px;
        border-width: 1px;
        border-color: #e67e22;
        color: #a9b7c6;
        background-color: #e67e22;
    }
    QRadioButton::indicator:!checked {
        height: 10px;
        width: 10px;
        border-style:solid;
        border-radius:5px;
        border-width: 1px;
        border-color: #e67e22;
        color: #a9b7c6;
        background-color: transparent;
    }
    """

lineEditStyleSheet = """
    QLineEdit {
        border-color: #1a1a1a;
        border-width: 1px;
        border-radius: 4px;
        border-style: inset;
        padding: 0 8px;
        color: #fff;
        background: #646464;
        selection-background-color: #411;
        selection-color: #0ff;
    }
    QLineEdit::disabled {
        background-color: #222;
        color: #ddd;
    }
    """

altLineEditStyleSheet = """
    QLineEdit {
        border-color: #3a3a3a;
        border-bottom-width: 2px;
        border-radius: 0px;
        border-style: inset;
        padding: 0 8px;
        font: 10pt italic;
        color: #000;
        background: #fff;
        selection-background-color: #bbbbbb;
        selection-color: #3c3f41;
    }
    QLineEdit::disabled {
        background-color: #fff;
        color: #000;
    }
    """

editStyleSheet = """
    QLineEdit {
        border-width: 1px; border-radius: 4px;
        border-color: rgb(58, 58, 58);
        border-style: inset;
        padding: 0 8px;
        color: #f5f5f5;
        background:#000000;
        selection-background-color:#007b50;
        selection-color: #FFFFFF;
    }"""


comboBoxStyleSheet = """
    QComboBox {
        color: #a9b7c6;
        background: #1e1d23;
    }
    QComboBox:editable {
        background: #1e1d23;
        color: #a9b7c6;
        selection-background-color:#000000;
    }
    QComboBox QAbstractItemView {
        color: #a9b7c6;
        background: #1e1d23;
        selection-color: #FFFFFF;
        selection-background-color:#000000;
    }
    QComboBox:!editable:on, QComboBox::drop-down:editable:on {
        color: #a9b7c6;
        background: #1e1d23;
    }
    QFontComboBox {
        color: #a9b7c6;
        background-color:#000000;
    }"""


textEditStyleSheet = """
    QPlainTextEdit {
        color: #0F0;
        background-color: #2a2a2a;
    }"""


labelStyleSheet = """
    QLabel {
        color: #191716;
    }
    """
