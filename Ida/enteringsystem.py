import os 
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtMultimedia import QSoundEffect
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class LoginSystem(QWidget):

    login_success = pyqtSignal(str, str)

    def __init__(self, player_records):
        super().__init__()

        self.click_sound = QSoundEffect(self)

        self.click_sound.setSource(
            QUrl.fromLocalFile(os.path.join(BASE_DIR,"Ida","images","audio","clicked.wav")))

        self.click_sound.setVolume(0.5)

        self.player_records = player_records

        self.player_name = ""
        self.player_gender = ""

        self.pages = QStackedWidget()

        self.name_page = QWidget()
        self.character_page = QWidget()
        self.player_list_page = QWidget()
        self.welcome_page = QWidget()

        self.pages.addWidget(self.name_page)
        self.pages.addWidget(self.character_page)
        self.pages.addWidget(self.player_list_page)
        self.pages.addWidget(self.welcome_page)

        self.create_name_page()
        self.create_character_page()
        self.create_player_list_page()
        self.create_welcome_page()

        self.pages.setCurrentWidget(self.name_page)


        # IMPORTANT: display the stacked widget
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.pages)



    def play_click_sound(self):
        self.click_sound.play()

    def create_name_page(self):

        # ====================================================
        # NAME PAGE BACKGROUND
        # ====================================================

        self.name_background = QLabel(self.name_page)

        background_path = os.path.join(BASE_DIR,"Ida","images","background","loginbg.png")

        pixmap = QPixmap(background_path)

        self.name_background.setPixmap(pixmap)
        self.name_background.setScaledContents(True)
        self.name_background.setGeometry(0, 0, 1100, 800)

        # Make sure background stays behind everything
        self.name_background.lower()

        # ====================================================
        # NAME POPUP - CUSTOM PNG BORDER
        # ====================================================

        self.name_popup = QLabel(self.name_page)

        border_path = os.path.join(BASE_DIR,"Ida","images","background","border.png")

        border_pixmap = QPixmap(border_path)

        self.name_popup.setPixmap(border_pixmap)
        self.name_popup.setScaledContents(True)

        # Center of 1100 x 800 screen
        self.name_popup.setGeometry(-70,100,1200,600)


        # POPUP TITLE     

        self.name_title = QLabel(
            "ARE YOU A NEWBIE?",
            self.name_popup
        )

        self.name_title.setGeometry(90,90,1000,70)


        self.name_title.setStyleSheet("""
            QLabel {
                color: white;
                background: transparent;
                border: none;
            }
        """)

        self.name_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.name_title.setFont(QFont("Cave Story", 39, QFont.Weight.Bold))
        # ====================================================
        # ENTER YOUR NAME
        # ====================================================

        self.name_title = QLabel(
            "ENTER YOUR NAME",
            self.name_popup
        )

        self.name_title.setGeometry(100,190,1000,60)

        self.name_title.setAlignment(Qt.AlignmentFlag.AlignCenter)


        self.name_title.setStyleSheet("""
            QLabel {
                6color: #202e63;
                background: transparent;
                border: none;
            }
        """)

        self.name_title.setFont(
            QFont("Cave Story", 30, QFont.Weight.Bold))


        # ====================================================
        # NAME INPUT
        # ====================================================

        self.name_input = QLineEdit(self.name_popup)

        self.name_input.setGeometry(410,260,350,60)

        self.name_input.setPlaceholderText(
            "Enter your name..."
        )

        self.name_input.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.name_input.setStyleSheet("""
            QLineEdit {
                background-color: #eeeeee;
                color: #111111;
                border: 6px solid #11152d;
                padding: 5px;
            }

            QLineEdit:focus {
                background-color: white;
            }
        """)

        self.name_input.setFont(
            QFont("Cave Story", 30, QFont.Weight.Bold)
        )


        # ====================================================
        # NEXT BUTTON
        # ====================================================

        self.name_next_button = QPushButton(
            "NEXT",
            self.name_popup
        )

        self.name_next_button.setGeometry(
            610,
            350,
            150,
            60
        )

        self.name_next_button.setStyleSheet("""
            QPushButton {
                background-color: #eeeeee;
                color: #111111;
                border: 6px solid #11152d;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #d6e5ff;
            }

            QPushButton:pressed {
                background-color: #b8c9ec;
            }
        """)

        self.name_next_button.setFont(
            QFont("Cave Story", 20, QFont.Weight.Bold)
        )

        self.name_next_button.clicked.connect(
            self.name_next_clicked
        )

        self.name_next_button.clicked.connect(
            self.play_click_sound
        )
        # NO BUTTON
        self.name_no_button = QPushButton(
            "NO",
            self.name_popup
        )

        self.name_no_button.setGeometry(
            410,
            350,
            150,
            60
        )

        self.name_no_button.setStyleSheet("""
            QPushButton {
                background-color: #eeeeee;
                color: #111111;
                border: 6px solid #11152d;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #ffd6d6;
            }

            QPushButton:pressed {
                background-color: #f0b8cd;
            }
        """)

        self.name_no_button.setFont(
            QFont("Cave Story", 20, QFont.Weight.Bold)
        )

        self.name_no_button.clicked.connect(
            self.no_name_clicked
        )

        self.name_no_button.clicked.connect(
            self.play_click_sound
        )

    def name_next_clicked(self):

        name = self.name_input.text().strip()

        # Check if name is empty
        if not name:
            self.name_input.setPlaceholderText(
                "Please enter your name!"
            )
            return

        # Check if username already exists
        if self.player_records.player_exists(name):

            self.show_name_error(
                "USER FOUND!\n"
                "This username is already in use.\n"
                "Please choose another name."
            )

            return

        # Name is available
        self.player_name = name

        self.pages.setCurrentWidget(
            self.character_page
        )

    def show_name_error(self, message):

        self.name_error_popup = QFrame(self.name_page)

        self.name_error_popup.setGeometry(
            300,
            270,
            500,
            260
        )

        self.name_error_popup.setStyleSheet("""
            QFrame {
                background-color: #d4be9f;
                border: 5px solid #11152d;
                border-radius: 20px;
            }
        """)

        # TITLE
    
        self.name_error_title = QLabel(
            "USER FOUND!",
            self.name_error_popup
        )

        self.name_error_title.setGeometry(
            30,
            25,
            440,
            55
        )

        self.name_error_title.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.name_error_title.setStyleSheet("""
            QLabel {
                color: #11152d;
                background: transparent;
                border: none;
            }
        """)

        self.name_error_title.setFont(
            QFont("Cave Story", 30, QFont.Weight.Bold)
        )

        # =========================
        # MESSAGE
        # =========================

        self.name_error_message = QLabel(
            message,
            self.name_error_popup
        )

        self.name_error_message.setGeometry(
            30,
            85,
            440,
            80
        )

        self.name_error_message.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.name_error_message.setWordWrap(True)

        self.name_error_message.setStyleSheet("""
            QLabel {
                color: #11152d;
                background: transparent;
                border: none;
            }
        """)

        self.name_error_message.setFont(
            QFont("Cave Story", 19, QFont.Weight.Bold)
        )

        # =========================
        # OK BUTTON
        # =========================

        self.name_error_button = QPushButton(
            "OK",
            self.name_error_popup
        )

        self.name_error_button.setGeometry(
            175,
            180,
            150,
            50
        )

        self.name_error_button.setStyleSheet("""
            QPushButton {
                background-color: #eeeeee;
                color: #111111;
                border: 5px solid #11152d;
                border-radius: 10px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #cfe5ff;
            }

            QPushButton:pressed {
                background-color: #a9c9ef;
            }
        """)

        self.name_error_button.setFont(
            QFont("Cave Story", 20, QFont.Weight.Bold)
        )

        self.name_error_button.clicked.connect(
            self.name_error_popup.deleteLater
        )

        self.name_error_button.clicked.connect(
            self.play_click_sound
        )

        self.name_error_popup.raise_()
        self.name_error_popup.show()

# Page Select Gender
    def create_character_page(self):
        layout = QVBoxLayout(self.character_page)

        # ====================================================
        # BACKGROUND
        # ====================================================

        self.character_background = QLabel(
            self.character_page
        )

        background_path = os.path.join(
            BASE_DIR,
            "Ida",
            "images",
            "background",
            "loginbg.png"
        )

        pixmap = QPixmap(background_path)

        self.character_background.setPixmap(pixmap)
        self.character_background.setScaledContents(True)
        self.character_background.setGeometry(
            0, 0, 1100, 800
        )

        self.character_background.lower()


        # ====================================================
        # POPUP
        # ====================================================

        self.character_popup = QLabel(self.character_page)

        border_path = os.path.join(
            BASE_DIR,
            "Ida",
            "images",
            "background",
            "border.png"
        )

        border_pixmap = QPixmap(border_path)

        self.character_popup.setPixmap(border_pixmap)
        self.character_popup.setScaledContents(True)

        self.character_popup.setGeometry(
            -70,
            100,
            1200,
            600
        )

        # ====================================================
        # TITLE
        # ====================================================

        self.character_title = QLabel(
            "SELECT YOUR CHARACTER",
            self.character_popup
        )

        self.character_title.setGeometry(
            100,
            70,
            1000,
            110
        )
        self.character_title.setStyleSheet("""
            QLabel {
                color: white;
                background: transparent;
                border: none;
            }
        """)

        self.character_title.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )


        self.character_title.setFont(
            QFont("Cave Story", 45, QFont.Weight.Bold)
        )


        # ====================================================
        # BOY BUTTON
        # ====================================================

        self.boy_button = QPushButton(
            "BOY",
            self.character_popup
        )

        self.boy_button.setGeometry(
            420,
            225,
            340,
            75
        )

        self.boy_button.setStyleSheet("""
            QPushButton {
                background-color: #eeeeee;
                color: #111111;
                border: 6px solid #11152d;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #cfe5ff;
            }

            QPushButton:pressed {
                background-color: #a9c9ef;
            }
        """)

        self.boy_button.setFont(
            QFont("Cave Story", 30, QFont.Weight.Bold)
        )

        self.boy_button.clicked.connect(
            lambda: self.select_gender("boy")
        )

        self.boy_button.clicked.connect(
            self.play_click_sound
        )


        # ====================================================
        # GIRL BUTTON
        # ====================================================

        self.girl_button = QPushButton(
            "GIRL",
            self.character_popup
        )

        self.girl_button.setGeometry(
            420,
            320,
            340,
            75
        )

        self.girl_button.setStyleSheet("""
            QPushButton {
                background-color: #eeeeee;
                color: #111111;
                border: 6px solid #11152d;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #ffd6e5;
            }

            QPushButton:pressed {
                background-color: #f0b8cd;
            }
        """)

        self.girl_button.setFont(
            QFont("Cave Story", 30, QFont.Weight.Bold)
        )

        self.girl_button.clicked.connect(
            lambda: self.select_gender("girl")
        )

        self.girl_button.clicked.connect(
            self.play_click_sound
        )

    def select_gender(self, gender):

        self.player_gender = gender

        # Create and save the new player
        self.player_records.create_player(
            self.player_name,
            self.player_gender
        )

        # Starting coins
        player = self.player_records.get_player(
            self.player_name
        )

        if player is not None:
            player["coins"] = 50
            self.player_records.save_data()

        print("PLAYER NAME:", self.player_name)
        print("PLAYER GENDER:", self.player_gender)
        print("STARTING COINS: 50")

        self.welcome_label.setText(
            f"Are You Ready To Lock In, {self.player_name}?"
        )

        self.pages.setCurrentWidget(
            self.welcome_page
        )

    def create_player_list_page(self):

        # Create the page only once

        # =========================
        # BACKGROUND
        # =========================

        background = QLabel(self.player_list_page)

        background_path = os.path.join(
            BASE_DIR,
            "Ida",
            "images",
            "background",
            "loginbg.png"
        )

        background.setPixmap(QPixmap(background_path))
        background.setScaledContents(True)
        background.setGeometry(
            0, 0, 1100, 800
        )

        background.lower()

        # =========================
        # POPUP
        # =========================

        popup = QLabel(self.player_list_page)

        border_path = os.path.join(
            BASE_DIR,
            "Ida",
            "images",
            "background",
            "border2.png"
        )

        popup.setPixmap(QPixmap(border_path))
        popup.setScaledContents(True)

        popup.setGeometry(
            -70,
            80,
            1200,
            600
        )

        # =========================
        # TITLE
        # =========================

        title = QLabel(
            "SELECT YOUR PROFILE",
            popup
        )

        title.setGeometry(
            100,
            40,
            1000,
            80
        )

        title.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        title.setStyleSheet("""
            QLabel {
                color: white;
                background: transparent;
                border: none;
            }
        """)

        title.setFont(
            QFont(
                "Cave Story",
                38,
                QFont.Weight.Bold
            )
        )

        # =========================
        # PLAYER LIST
        # =========================

        players = self.player_records.data.get(
            "players",
            []
        )

        # Scroll area
        scroll_area = QScrollArea(self.player_list_page)

        scroll_area.setGeometry(
            360,
            220,
            400,
            330
        )

        scroll_area.setWidgetResizable(True)

        scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )

        # Make scroll area transparent
        scroll_area.setStyleSheet("""
            QScrollArea {
                background: transparent;
                border: none;
            }

            QScrollArea > QWidget > QWidget {
                background: transparent;
            }

            QScrollBar:vertical {
                background: transparent;
                width: 10px;
                margin: 50px;
            }

        """)

        scroll_area.setFrameShape(
            QFrame.Shape.NoFrame
        )

        # Widget inside scroll area
        player_container = QWidget()

        player_container.setStyleSheet("""
            QWidget {
                background: transparent;
            }
        """)

        scroll_area.setWidget(
            player_container
        )

        # Layout for player buttons
        player_layout = QVBoxLayout(
            player_container
        )

        player_layout.setContentsMargins(
            20,
            10,
            2,
            2
        )

        player_layout.setSpacing(15)

        # Add player buttons
        for player in players:

            name = player.get(
                "name",
                "Unknown"
            )

            player_button = QPushButton(
                name,
                player_container
            )

            player_button.setFixedHeight(
                60
            )

            player_button.setFixedWidth(
                300
            )

            player_button.setFont(
                QFont(
                    "Cave Story",
                    22,
                    QFont.Weight.Bold
                )
            )

            player_button.setStyleSheet("""
                QPushButton {
                    background-color: #eeeeee;
                    color: #111111;
                    border: 5px solid #11152d;
                }

                QPushButton:hover {
                    background-color: #cfe5ff;
                }

                QPushButton:pressed {
                    background-color: #a9c9ef;
                }
            """)

            player_button.clicked.connect(
                lambda checked=False, player_name=name:
                    self.load_existing_player(player_name)
            )

            player_button.clicked.connect(
                self.play_click_sound
            )

            player_layout.addWidget(
                player_button
            )

        # =========================
        # BACK BUTTON
        # =========================

        back_button = QPushButton(
            "BACK",
            self.player_list_page
        )

        back_button.setGeometry(
            430,
            580,
            200,
            60
        )

        back_button.setFont(
            QFont(
                "Cave Story",
                20,
                QFont.Weight.Bold
            )
        )

        back_button.setStyleSheet("""
            QPushButton {
                background-color: #eeeeee;
                color: #111111;
                border: 5px solid #11152d;
            }

            QPushButton:hover {
                background-color: #a6f7f2;
            }

            QPushButton:pressed {
                background-color: #f0b8cd;
            }
        """)

        back_button.clicked.connect(
            lambda: self.pages.setCurrentWidget(
                self.name_page
            )
        )

        back_button.clicked.connect(
            self.play_click_sound
        )

    def load_existing_player(self, player_name):
        player = self.player_records.get_player(player_name)

        if player is None:
            return

        self.player_name = player["name"]
        self.player_gender = player.get("gender", "girl")

        print("EXISTING PLAYER:", self.player_name)
        print("GENDER:", self.player_gender)

        self.login_success.emit(
            self.player_name,
            self.player_gender
    )

    def no_name_clicked(self):
        self.pages.setCurrentWidget(self.player_list_page)


    def create_welcome_page(self):

        # ====================================================
        # BACKGROUND
        # ====================================================

        self.welcome_background = QLabel(
            self.welcome_page
        )

        background_path = os.path.join(
            BASE_DIR,
            "Ida",
            "images",
            "wallpaper",
            "mainbackground.png"
        )

        pixmap = QPixmap(background_path)

        self.welcome_background.setPixmap(pixmap)
        self.welcome_background.setScaledContents(True)
        self.welcome_background.setGeometry(
            0, 0, 1100, 800
        )

        self.welcome_background.lower()


        # ====================================================
        # POPUP
        # ====================================================

        self.welcome_popup = QFrame(
            self.welcome_page
        )

        self.welcome_popup.setGeometry(
            325,
            220,
            450,
            330
        )

        self.welcome_popup.setStyleSheet("""
            QFrame {
                background-color: #29469b;
                border: 7px solid #11152d;
            }
        """)


        # ====================================================
        # WELCOME TEXT
        # ====================================================

        self.welcome_label = QLabel(
            f"Are You Ready To Lock In, {self.player_name}?",
            self.welcome_popup
        )

        self.welcome_label.setGeometry(
            35,
            45,
            380,
            130
        )

        self.welcome_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.welcome_label.setWordWrap(True)

        self.welcome_label.setStyleSheet("""
            QLabel {
                color: white;
                background: transparent;
                border: none;
            }
        """)

        self.welcome_label.setFont(
            QFont("Cave Story", 40, QFont.Weight.Bold)
        )
        # ====================================================
        # YES BUTTON
        # ====================================================

        self.welcome_yes = QPushButton(
            "YES",
            self.welcome_popup
        )

        self.welcome_yes.setGeometry(
            65,
            215,
            140,
            60
        )

        self.welcome_yes.setStyleSheet("""
            QPushButton {
                background-color: #eeeeee;
                color: #111111;
                border: 6px solid #11152d;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #cfe5ff;
            }
        """)

        self.welcome_yes.setFont(
            QFont("Cave Story", 15, QFont.Weight.Bold)
        )

        self.welcome_yes.clicked.connect(self.welcome_yes_clicked)

        self.welcome_yes.clicked.connect(self.play_click_sound)


        # NO BUTTON


        self.welcome_no = QPushButton("NO", self.welcome_popup)
        self.welcome_no.setGeometry(245, 215, 140, 60)

        self.welcome_no.setStyleSheet("""
            QPushButton {
                background-color: #eeeeee;
                color: #111111;
                border: 6px solid #11152d;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #ffd6d6;
            }
        """)

        self.welcome_no.setFont(QFont("Cave Story", 15, QFont.Weight.Bold))
        self.welcome_no.clicked.connect(self.back_to_name)
        self.welcome_no.clicked.connect(self.play_click_sound)


   # SEND THE INFORMATION BACK TO WINDOW
    def welcome_yes_clicked(self):
        self.login_success.emit(self.player_name,self.player_gender)
        
    def back_to_name(self):
        self.pages.setCurrentWidget(self.name_page)