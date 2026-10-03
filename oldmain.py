import sys
import os
import json

# Make it a daily log in ( gain coins)
# Reset 
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput, QSoundEffect
from PyQt6.QtMultimediaWidgets import QVideoWidget

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

from Ida.shoppingcart import ShoppingCart
from Ida.inventory import InventoryWindow, RoomItem, inventory
from Ida.playerecords import PlayerRecords
from Ida.dailylogin import DailyLogin
from Yeejing.countdowntimer import CountdownTimer   
from Haikal.calendarsystem import CalendarMainWindow
from Haikal.MusicPlayer import *
from Haikal.EventSystem import Events
from Haikal.calendarsystem import CalendarMainWindow
from Haikal.todo_list import * # << the main class is the only one that needs to be imported, no specify

#from Haikal........ import ....... 
# haikal u need to change something line 2294 to called your function, you can see example like the timer
# btw you guys need to change a bit to your codes if you want to make it it run in the same window

class HomePage(QWidget):

    def __init__(self):
        self.reward = 10
        super().__init__()

        calendardate = CalendarMainWindow()
        dater = Events(calendardate)

        dater.date_fetcher()
        

        
        self.music = MusicController()

        # Button click sound
        self.click_sound = QSoundEffect(self)
        self.player_records = PlayerRecords(BASE_DIR)

        self.click_sound.setSource(
            QUrl.fromLocalFile(os.path.join(BASE_DIR,"Ida","images","audio","clicked.wav"))
        )

        self.click_sound.setVolume(0.5)

        # Daily login system
        self.daily_login = DailyLogin(self.player_records)
        self.coins = 100

        self.setWindowFlags(
        Qt.WindowType.Window |
        Qt.WindowType.WindowMinimizeButtonHint |
        Qt.WindowType.WindowMaximizeButtonHint |
        Qt.WindowType.WindowCloseButtonHint
        )

        self.setWindowIcon(
            QIcon(
                os.path.join(BASE_DIR,"Ida","images","Icons","officialbg.png"))       
        )    

        self.setWindowTitle("Lock In Space")
        self.setFixedSize(QSize(1100, 800))

        # ====================================================
        # PAGES

        self.pages = QStackedWidget(self)

        # ====================================================
        # INTRO VIDEO PAGE
        # ====================================================

        self.intro_page = QWidget()

        # ====================================================
        # NAME / CHARACTER / WELCOME PAGES
        # ====================================================

        self.name_page = QWidget()
        self.character_page = QWidget()
        self.welcome_page = QWidget()

        # Player information
        self.player_name = ""
        self.player_gender = ""
        self.room_layout = {}

        self.intro_video = QVideoWidget(self.intro_page)
        self.intro_video.setGeometry(0, 0, 1170, 800)

        self.intro_video.setAspectRatioMode(
            Qt.AspectRatioMode.KeepAspectRatioByExpanding
)

        self.intro_player = QMediaPlayer(self)
        self.intro_audio = QAudioOutput(self)

        self.intro_player.setAudioOutput(self.intro_audio)
        self.intro_player.setVideoOutput(self.intro_video)

        self.intro_audio.setVolume(1.0)

        video_path = os.path.join(
            BASE_DIR,"Ida","images","audio","intro.mp4"
        )

        print("VIDEO PATH:", video_path)
        print("VIDEO EXISTS:", os.path.exists(video_path))

        self.intro_player.setSource(
            QUrl.fromLocalFile(video_path)
        )

        # ====================================================
        # ROOM / SHOP / INVENTORY PAGES
        # ====================================================

        self.room_page = QWidget()

        # CREATE THESE BEFORE USING THEM
        self.shop_page = ShoppingCart()
        self.shop_page.coins_changed.connect(self.update_coin_display)

        self.inventory_page = InventoryWindow()

        self.inventory_page.item_selected.connect(
            self.handle_item_selected
        )

        
        self.calendar_page = CalendarMainWindow()

        self.todolist_popup = TodoList()

        # ====================================================
        # ADD PAGES
        # ====================================================

        self.pages.addWidget(self.intro_page)
        self.pages.addWidget(self.name_page)
        self.pages.addWidget(self.character_page)
        self.pages.addWidget(self.welcome_page)
        self.pages.addWidget(self.room_page)
        self.pages.addWidget(self.shop_page)
        self.pages.addWidget(self.inventory_page)
        self.pages.addWidget(self.calendar_page)
        # self.pages.addWidget(self.todolist_popup)

        self.pages.setGeometry(0,0,1100,800)

        # ====================================================
        # CLOSE BUTTONS
        # ====================================================

        self.shop_page.close_button.clicked.connect(self.show_room)

        self.inventory_page.close_button.clicked.connect(self.show_room)

        self.calendar_page.close_button.clicked.connect(self.show_room)


        # Changing current wallpaper with a new one
        self.current_wallpaper = {
            "name": "White and Wood",
            "image": os.path.join(BASE_DIR,"Ida","images","wallpaper","mainbackground.png")
        }

        self.create_name_page()
        self.create_character_page()
        self.create_welcome_page()

        coin_path = os.path.join(BASE_DIR,"Ida","images","items","coins.png")

        self.coin_label = QLabel(self.room_page)
        self.coin_label.setPixmap(QPixmap(coin_path))
        self.coin_label.setScaledContents(True)
        self.coin_label.setGeometry(810, 60, 80, 80)

        self.coin_amount = QLabel(str(self.coins), self.room_page)
        self.coin_amount.setGeometry(900, 45, 100, 100)

        self.coin_amount.setFont(
            QFont("Cave Story", 25, QFont.Weight.Bold)
        )

        self.coin_amount.setStyleSheet("""
            QLabel {
                color: white;
                background: transparent;
            }
        """)

        self.InitWindow()

        # ====================================================
        # START INTRO VIDEO
        # ====================================================

        self.pages.setCurrentWidget(self.intro_page)


        self.intro_player.mediaStatusChanged.connect(self.intro_finished)

        self.intro_player.play()

    

    def show_daily_reward(self):

        # Don't create another popup if one already exists
        if getattr(self, "daily_reward_popup", None) is not None:
            try:
                if self.daily_reward_popup.isVisible():
                    return
            except RuntimeError:
                self.daily_reward_popup = None

        self.daily_reward_popup = QFrame(self.room_page)

        self.daily_reward_popup.setGeometry(
            300,
            250,
            500,
            250
        )

        self.daily_reward_popup.setStyleSheet("""
            QFrame {
                background-color: #d4be9f;
                border: 5px solid #11152d;
                border-radius: 20px;
            }
        """)

        # =========================
        # TITLE
        # =========================

        self.daily_reward_title = QLabel(
            "DAILY REWARD!",
            self.daily_reward_popup
        )

        self.daily_reward_title.setGeometry(
            30,
            20,
            440,
            60
        )

        self.daily_reward_title.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.daily_reward_title.setStyleSheet("""
            QLabel {
                color: #11152d;
                background: transparent;
                border: none;
            }
        """)

        self.daily_reward_title.setFont(
            QFont("Cave Story", 30, QFont.Weight.Bold)
        )

        # =========================
        # MESSAGE
        # =========================

        self.daily_reward_message = QLabel(
            "You just received\n10 coins!",
            self.daily_reward_popup
        )

        self.daily_reward_message.setGeometry(
            30,
            80,
            440,
            80
        )

        self.daily_reward_message.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.daily_reward_message.setStyleSheet("""
            QLabel {
                color: #11152d;
                background: transparent;
                border: none;
            }
        """)

        self.daily_reward_message.setFont(
            QFont("Cave Story", 22, QFont.Weight.Bold)
        )

        # =========================
        # CLAIM BUTTON
        # =========================

        self.claim_button = QPushButton(
            "CLAIM",
            self.daily_reward_popup
        )

        self.claim_button.setGeometry(
            175,
            175,
            150,
            50
        )

        self.claim_button.setStyleSheet("""
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

        self.claim_button.setFont(
            QFont("Cave Story", 20, QFont.Weight.Bold)
        )

        self.claim_button.clicked.connect(
            self.claim_daily_login
        )

        self.claim_button.clicked.connect(
            self.play_click_sound
        )

        self.daily_reward_popup.raise_()
        self.daily_reward_popup.show()

    def show_daily_notification(self, message):

        self.daily_notification = QLabel(
            message,
            self.room_page
        )

        self.daily_notification.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.daily_notification.setStyleSheet("""
            QLabel {
                background-color: #d4be9f;
                color: black;
                border: 3px solid black;
                border-radius: 15px;
                padding: 10px;
                font-family: "Cave Story";
                font-size: 25px;
                font-weight: bold;
            }
        """)

        self.daily_notification.setGeometry(
            300, 250, 500, 100
        )

        self.daily_notification.raise_()
        self.daily_notification.show()

        QTimer.singleShot(
            2000,
            self.daily_notification.deleteLater
        )

    def claim_daily_login(self):
        success, coins = self.daily_login.claim(self.player_name)

        # Safely close the daily reward popup
        popup = getattr(self, "daily_reward_popup", None)

        if popup is not None:
            try:
                popup.close()
                popup.deleteLater()
            except RuntimeError:
                pass

            self.daily_reward_popup = None

        if success:
            self.coins = coins
            self.coin_amount.setText(str(coins))
             # Update Shopping Cart coins
            self.shop_page.set_coins(self.coins)
            self.show_daily_notification("+10 COINS!")

        else:
            self.show_daily_notification("Already Claimed Today!") 

    def set_coins(self, coins):
        self.coins = coins
        self.coin_text.setText(str(coins))

    # ENTER button func.
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            if self.pages.currentWidget() == self.intro_page:
                self.intro_player.stop()
                self.pages.setCurrentWidget(self.name_page)
            else:
                super().keyPressEvent(event)

    def play_click_sound(self):
        self.click_sound.play()

    def update_coin_display(self, coins):

        self.coins = coins

        self.coin_amount.setText(
            str(coins)
        )

        player = self.player_records.get_player(
            self.player_name
        )

        if player is not None:

            player["coins"] = coins

            player["inventory"] = dict(
                inventory
            )

            self.player_records.save_data()

            print("PLAYER DATA SAVED")
            print("COINS:", coins)
            print("INVENTORY:", player["inventory"])

    def update_shop_coins(self):
        self.shop_page.set_coins(self.coins)

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

        # ====================================================
        # POPUP TITLE
        # ====================================================

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
                color: #202e63d;
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

        # ====================================================
        # NO BUTTON
        # ====================================================

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

    def create_player_list_page(self):

        # Create the page only once
        if hasattr(self, "player_list_page"):
            return

        self.player_list_page = QWidget()

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
            "border.png"
        )

        popup.setPixmap(QPixmap(border_path))
        popup.setScaledContents(True)

        popup.setGeometry(
            -70,
            100,
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
            70,
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

        y_position = 180

        for player in players:

            name = player.get(
                "name",
                "Unknown"
            )

            player_button = QPushButton(
                name,
                popup
            )

            player_button.setGeometry(
                350,
                y_position,
                400,
                60
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

            y_position += 75

        # =========================
        # BACK BUTTON
        # =========================

        back_button = QPushButton(
            "BACK",
            popup
        )

        back_button.setGeometry(
            450,
            500,
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
                background-color: #ffd6d6;
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

        # =========================
        # ADD PAGE
        # =========================

        self.pages.addWidget(
            self.player_list_page
        )

    def load_existing_player(self, player_name):
        player = self.player_records.get_player(player_name)

        if player is None:
            return

        self.player_name = player["name"]
        self.player_gender = player.get("gender", "girl")

        # Load saved coins
        self.coins = player.get("coins", 100)
        self.coin_amount.setText(str(self.coins))

        # =========================
        # LOAD PLAYER INVENTORY
        # =========================

        inventory.clear()

        saved_inventory = player.get("inventory", {})

        inventory.update(saved_inventory)

        print("LOADED INVENTORY:", inventory)

        self.inventory_page.show_inventory()

        # Load saved wallpaper
        wallpaper = player.get("wallpaper")

        if isinstance(wallpaper, dict):
            self.current_wallpaper = {
                "name": wallpaper.get("name", "White and Wood"),
                "image": wallpaper.get(
                    "image",
                    os.path.join(
                        BASE_DIR,
                        "Ida",
                        "images",
                        "wallpaper",
                        "mainbackground.png"
                    )
                )
            }

        else:
            # Existing save uses a string for wallpaper
            self.current_wallpaper = {
                "name": str(wallpaper) if wallpaper else "White and Wood",
                "image": os.path.join(
                    BASE_DIR,
                    "Ida",
                    "images",
                    "wallpaper",
                    "mainbackground.png"
                )
            }

        # Apply the saved wallpaper to the room
        self.change_wallpaper(
            self.current_wallpaper["image"]
        )

        print("LOADED PLAYER:")
        print("Name:", self.player_name)
        print("Gender:", self.player_gender)
        print("Coins:", self.coins)
        print("Wallpaper:", self.current_wallpaper["name"])

        self.enter_room()

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

        # =========================
        # TITLE
        # =========================

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

    def enter_room(self):

        if self.player_gender == "boy":

            character_path = os.path.join(BASE_DIR,"Ida","images","characters","boy.png"
            )

        elif self.player_gender == "girl":

            character_path = os.path.join(BASE_DIR,"Ida","images","characters","girl.png"
            )

        print("CHARACTER PATH:", character_path)
        print("CHARACTER EXISTS:", os.path.exists(character_path))

        if os.path.exists(character_path):

            self.character_item = RoomItem(
                "player_character",
                character_path,
                self
            )

            self.scene.addItem(
                self.character_item
            )

            self.character_item.setPos(400,380)

            self.character_item.setScale(2.0)

            self.character_item.setZValue(10)


        # =========================
        # ADD BED
        # =========================

        bed_path = os.path.join(BASE_DIR,"Ida","images","furnitures","bed.png"
        )

        print("BED PATH:", bed_path)
        print("BED EXISTS:", os.path.exists(bed_path))

        if os.path.exists(bed_path):

            self.bed_item = RoomItem(
                "bed",
                bed_path,
                self
            )

            self.scene.addItem(
                self.bed_item
            )

            self.bed_item.setPos(5,500)

            #Size
            self.bed_item.setScale(2.5)

            self.bed_item.setZValue(10)

        # =========================
        # CURTAIN
        # =========================

        curtain_path = os.path.join(BASE_DIR,"Ida","images","furnitures","curtain.png")

        print("CURTAIN PATH:", curtain_path)
        print("CURTAIN EXISTS:", os.path.exists(curtain_path))

        if os.path.exists(curtain_path):

            self.curtain_item = RoomItem(
                "curtain",
                curtain_path,
                self
            )

            self.scene.addItem(
                self.curtain_item
            )

            self.curtain_item.setPos(50,200)

            #Size
            self.curtain_item.setScale(2.5)

            self.curtain_item.setZValue(10)

        # =========================
        # DOOR
        # =========================

        door_path = os.path.join(BASE_DIR,"Ida","images","furnitures","door.png"
        )

        print("DOOR PATH:", door_path)
        print("DOOR EXISTS:", os.path.exists(door_path))

        if os.path.exists(door_path):

            self.door_item = RoomItem(
                "door",
                door_path,
                self
            )

            self.scene.addItem(
                self.door_item
            )

            self.door_item.setPos(700,280)

            #Size
            self.door_item.setScale(2.5)

            self.door_item.setZValue(10)

        # =========================
        # LOAD SAVED ROOM ITEMS
        # =========================

        player = self.player_records.get_player(self.player_name)

        if player is not None:

            saved_items = player.get("room_items", {})

            print("SAVED ROOM ITEMS:", saved_items)

            for name, data in saved_items.items():

                image = data.get("image")

                if not image:
                    continue

                # Convert saved relative path to full path
                if not os.path.isabs(image):
                    image = os.path.join(BASE_DIR, image)

                print("LOADING SAVED ITEM:", name)
                print("IMAGE PATH:", image)
                print("IMAGE EXISTS:", os.path.exists(image))

                if not os.path.exists(image):
                    continue

                item = RoomItem(
                    name,
                    image,
                    self
                )

                self.scene.addItem(item)

                item.setPos(
                    data.get("x", 400),
                    data.get("y", 300)
                )

                item.setScale(
                    data.get("scale", 1.0)
                )

                item.setZValue(10)

                self.room_layout[name] = item

        # Go to room
        self.pages.setCurrentWidget(self.room_page)

        # SHOW TEMPORARY NOTE
        self.show_room_note()
        # SHOW DAILY REWARD AFTER 1 SECOND
        QTimer.singleShot(
            1000,
            self.show_daily_reward
        )

        print(f"Welcome {self.player_name}!")



    def no_name_clicked(self):

        self.create_player_list_page()
        self.pages.setCurrentWidget(self.player_list_page)


    def back_to_name(self):
        self.pages.setCurrentWidget(self.name_page)

    # Page Select Gender
    def create_character_page(self):

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
            80,
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

        # =========================
        # STARTING COINS
        # =========================

        self.coins = 50
        self.coin_amount.setText(str(self.coins))

        # Save 50 coins to this new player
        player = self.player_records.get_player(
            self.player_name
        )

        if player is not None:
            player["coins"] = 50
            self.player_records.save_data()

        self.enter_room()

        print("PLAYER NAME:", self.player_name)
        print("PLAYER GENDER:", self.player_gender)
        print("STARTING COINS:", self.coins)

        # UPDATE WELCOME MESSAGE
        self.welcome_label.setText(
            f"Are You Ready To Lock In, {self.player_name}?"
        )

        # Go to welcome page
        self.pages.setCurrentWidget(
            self.welcome_page
        )

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

        self.welcome_yes.clicked.connect(
            self.enter_room
        )

        self.welcome_yes.clicked.connect(
            self.play_click_sound
        )



        # ====================================================
        # NO BUTTON
        # ====================================================

        self.welcome_no = QPushButton(
            "NO",
            self.welcome_popup
        )

        self.welcome_no.setGeometry(
            245,
            215,
            140,
            60
        )

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

        self.welcome_no.clicked.connect(self.back_to_name)

    def show_room_note(self):

        self.room_note = QLabel(
            "This is your space to lock in!\n"
            "Customize your room and make it yours!",
            self.room_page)

        self.room_note.setGeometry(
            300,
            30,
            500,
            110
        )

        self.room_note.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.room_note.setWordWrap(True)

        self.room_note.setStyleSheet("""
            QLabel {
                background-color: rgba(17, 21, 45, 235);
                color: white;
                border: 5px solid #11152d;
                padding: 10px;
            }
        """)

        self.room_note.setFont(
            QFont("Cave Story", 20, QFont.Weight.Bold)
        )

        self.room_note.raise_()
        self.room_note.show()

        QTimer.singleShot(
            4000,
            self.room_note.deleteLater
        )

    def save_player_inventory(self):

        player = self.player_records.get_player(
            self.player_name
        )

        if player is None:
            return

        player["inventory"] = dict(inventory)

        self.player_records.save_data()

        print("INVENTORY SAVED:")
        print(player["inventory"])

    def save_room_layout(self):

        player = self.player_records.get_player(
            self.player_name
        )

        if player is None:
            return

        saved_items = {}

        # Items that belong to the default room
        default_items = {
            "player_character",
            "bed",
            "curtain",
            "door"
        }

        for item in self.scene.items():

            if not isinstance(item, RoomItem):
                continue

            name = item.item_name

            # Don't save default room furniture
            if name in default_items:
                continue

            saved_items[name] = {

                "image": item.image,

                "x": item.pos().x(),

                "y": item.pos().y(),

                "scale": item.scale(),

                "category": "furniture"
            }

        player["room_items"] = saved_items

        # Save inventory too
        player["inventory"] = dict(
            inventory
        )

        # Save coins
        player["coins"] = self.coins

        # Save wallpaper
        player["wallpaper"] = self.current_wallpaper

        self.player_records.save_data()

        print("================================")
        print("ROOM SAVED")
        print("ROOM ITEMS:", saved_items)
        print("INVENTORY:", player["inventory"])
        print("COINS:", player["coins"])
        print("================================")

    def save_current_player_state(self):

        player = self.player_records.get_player(
            self.player_name
        )

        if player is None:
            return

        # =========================
        # COINS
        # =========================

        player["coins"] = self.coins

        # =========================
        # INVENTORY
        # =========================

        player["inventory"] = dict(
            inventory
        )

        # =========================
        # ROOM
        # =========================

        saved_items = {}

        default_items = {
            "player_character",
            "bed",
            "curtain",
            "door"
        }

        for item in self.scene.items():

            if not isinstance(item, RoomItem):
                continue

            name = item.item_name

            if name in default_items:
                continue

            saved_items[name] = {
                "image": item.image,
                "x": item.pos().x(),
                "y": item.pos().y(),
                "scale": item.scale(),
                "category": "furniture"
            }

        player["room_items"] = saved_items

        # =========================
        # WALLPAPER
        # =========================

        player["wallpaper"] = self.current_wallpaper

        # =========================
        # SAVE JSON
        # =========================

        self.player_records.save_data()

        print("PLAYER STATE SAVED")

    def InitWindow(self, controller=None):
        self.controller = controller

        # ====================================================
        # BACKGROUND

        self.image = QLabel(self.room_page)

        pixmap = QPixmap(os.path.join(BASE_DIR,"Ida","images","wallpaper","mainbackground.png")
        )

        self.image.setPixmap(pixmap)

        self.image.setScaledContents(
            True
        )

        self.image.setGeometry(
            0,
            0,
            1100,
            800
        )

        self.image.lower()
        # ====================================================
        # ROOM ITEM AREA
        # ====================================================

        self.scene = QGraphicsScene()

        self.scene.setSceneRect(
            0,
            0,
            1100,
            800
        )

        self.view = QGraphicsView(
            self.scene,
            self.room_page
        )

        self.view.setGeometry(
            0,
            0,
            1100,
            800
        )

        self.view.setStyleSheet("""
            QGraphicsView {
                background: transparent;
                border: none;
            }
        """)

        self.view.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        self.view.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        self.view.setFrameShape(
            QFrame.Shape.NoFrame
        )

        # Make the view show the whole scene
        self.view.setSceneRect(
            0,
            0,
            1100,
            800
        )

        # ====================================================
        # MENU BUTTON
        # ====================================================

        self.menu_button = QPushButton(
            self.room_page
        )

        self.menu_button.setGeometry(940,50,100,100)

        self.menu_button.setToolTip(
            "<b>Menu</b><br>"
            "Open the menu to access your needs"
        )

        self.menu_button.setIcon(
            QIcon(
                os.path.join(BASE_DIR,"Ida","images","Icons","menuicon.png")
            )
        )

        self.menu_button.setIconSize(
            QSize(150,150)
        )

        self.menu_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
            }

            QPushButton:hover {
                background-color: rgba(255, 255, 255, 50);
                border-radius: 50px;
            }
        """)

        self.menu_button.clicked.connect(self.play_click_sound)
        self.menu_button.clicked.connect(self.toggle_menu)

        # ====================================================
        # INVENTORY BUTTON
        # ====================================================

        self.inventory_button = QPushButton(self.room_page)

        self.inventory_button.setGeometry(820,150,100,100)
        
        
        self.inventory_button.setToolTip(
         "<b>Inventory</b><br>"
            "View your items and decorate your study space!"
        )

        self.inventory_button.setIcon(
            QIcon(
                os.path.join(BASE_DIR,"Ida","images","Icons","invenicon.png")
            )
        )

        self.inventory_button.setIconSize(
            QSize(150,150)
        )

        self.inventory_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
            }

            QPushButton:hover {
                background-color: rgba(255, 255, 255, 50);
                border-radius: 50px;
            }
        """)

        self.inventory_button.clicked.connect(self.show_inventory)
        self.inventory_button.clicked.connect(self.play_click_sound)


        # ====================================================
        # SHOPPING CART BUTTON
        # ====================================================

        self.shop_button = QPushButton(
            self.room_page
        )

        self.shop_button.setGeometry(1000,150,100,100)

        self.shop_button.setToolTip(
            "<b>Shopping Cart</b><br>"
            "Spend your coins and find new items for your room!"
        )

        self.shop_button.setIcon(
            QIcon(
                os.path.join(BASE_DIR,"Ida","images","Icons","shopicon.png")
            )
        )

        self.shop_button.setIconSize(
            QSize(150, 150)
        )

        self.shop_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
            }

            QPushButton:hover {
                background-color: rgba(255, 255, 255, 50);
                border-radius: 50px;
            }
        """)

        self.shop_button.clicked.connect(self.show_shop)
        self.shop_button.clicked.connect(self.play_click_sound)
        

        # ====================================================
        # TO-DO LIST BUTTON
        # ====================================================

        self.tdlist_button = QPushButton(
            self.room_page
        )

        self.tdlist_button.setGeometry(910,150,100,100)

        self.tdlist_button.setToolTip(
            "<b>To-Do List</b><br>"
            "Keep track of your tasks and goals"
        )

        self.tdlist_button.setIcon(
            QIcon(
                os.path.join(BASE_DIR,"Ida","images","Icons","todoicon.png")
            )
        )

        self.tdlist_button.setIconSize(
            QSize(150, 150)
        )

        self.tdlist_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
            }

            QPushButton:hover {
                background-color: rgba(255, 255, 255, 50);
                border-radius: 50px;
            }
        """)

        self.tdlist_button.clicked.connect(self.show_todolist)
        self.tdlist_button.clicked.connect(self.play_click_sound)

        # TIMER/COUNTDOWN BUTTON

        self.timer_button = QPushButton(
            self.room_page
        )

        self.timer_button.setGeometry(820,235,100,100)

        self.timer_button.setToolTip(
            "<b>Timer</b><br>"
            "Start your study session and stay Locked In!"
        )

        self.timer_button.setIcon(
            QIcon(
                os.path.join(BASE_DIR,"Ida","images","Icons","timericon.png")
            )
        )

        self.timer_button.setIconSize(
            QSize(150, 150)
        )

        self.timer_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
            }

            QPushButton:hover {
                background-color: rgba(255, 255, 255, 50);
                border-radius: 50px;
            }
        """)

        self.timer_button.clicked.connect(self.show_timer)
        self.timer_button.clicked.connect(self.play_click_sound)


        # STATISTICS BUTTON

        self.statistics_button = QPushButton(
            self.room_page
        )

        self.statistics_button.setGeometry(910,235,100,100)

        self.statistics_button.setToolTip(
            "<b>Statistics</b><br>"
            "View your study progress and achievements!!"
        )

        self.statistics_button.setIcon(
            QIcon(
                os.path.join(BASE_DIR,"Ida","images","Icons","staticon.png")
            )
        )

        self.statistics_button.setIconSize(
            QSize(150, 150)
        )

        self.statistics_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
            }

            QPushButton:hover {
                background-color: rgba(255, 255, 255, 50);
                border-radius: 50px;
            }
        """)

        self.statistics_button.clicked.connect(self.show_statistics)
        self.statistics_button.clicked.connect(self.play_click_sound)

        # CALENDAR BUTTON

        self.calendar_button = QPushButton(
            self.room_page
        )

        self.calendar_button.setGeometry(1000,235,100,100)

        self.calendar_button.setToolTip(
            "<b>Calendar</b><br>"
            "Plan your study sessions and keep track of important dates!"
        )

        self.calendar_button.setIcon(
            QIcon(
                os.path.join(BASE_DIR,"Ida","images","Icons","calenicon.png")
            )
        )

        self.calendar_button.setIconSize(
            QSize(150, 150)
        )

        self.calendar_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
            }

            QPushButton:hover {
                background-color: rgba(255, 255, 255, 50);
                border-radius: 50px;
            }
        """)

        self.calendar_button.clicked.connect(self.show_calendar)
        self.calendar_button.clicked.connect(self.play_click_sound)


        "Haikal was here <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<"

        self.music_settings = QPushButton(
                    self.room_page
                )
        
        self.music_settings.setGeometry(1000,320,100,100)

        self.music_settings.setToolTip(
            "<b>Background Music</b><br>"
            "Set your application background music!"
        )

        self.music_settings.setIcon(
            QIcon(
                os.path.join(BASE_DIR,"Ida","images","Icons","musicicon.png")
            )
        )

        self.music_settings.setIconSize(
            QSize(150, 150)
        )

        self.music_settings.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
            }

            QPushButton:hover {
                background-color: rgba(255, 255, 255, 50);
                border-radius: 50px;
            }
        """)

        self.music_settings.clicked.connect(self.open_music_settings)
        self.music_settings.clicked.connect(self.play_click_sound)
        

        # ====================================================
        # HIDE BUTTONS AT START
        # ====================================================

        self.inventory_button.hide()
        self.shop_button.hide()
        self.tdlist_button.hide()
        self.timer_button.hide()
        self.statistics_button.hide()
        self.calendar_button.hide()
        self.music_settings.hide()




    def toggle_menu(self):

        if self.inventory_button.isVisible():

            self.inventory_button.hide()
            self.shop_button.hide()
            self.tdlist_button.hide()
            self.timer_button.hide()
            self.statistics_button.hide()
            self.calendar_button.hide()
            self.music_settings.hide()


        else:

            self.inventory_button.show()
            self.shop_button.show()
            self.tdlist_button.show()
            self.timer_button.show()
            self.statistics_button.show()
            self.calendar_button.show()
            self.music_settings.show()

    def intro_finished(self, status):

        if status == QMediaPlayer.MediaStatus.EndOfMedia:

            self.intro_player.stop()

            self.pages.setCurrentWidget(
                self.name_page
            )

        ###EXAMPLE###
    def show_shop(self):
        self.shop_page.set_coins(self.coins)
        self.pages.setCurrentWidget(self.shop_page)

    def show_inventory(self):
        self.shop_page.set_coins(self.coins)
        self.inventory_page.show_inventory()

        self.pages.setCurrentWidget(self.inventory_page)
######## WAITING FOR FULLCODES####### (FROM DIFF FILE)
    def show_tdlist(self):
        print("To-Do List clicked!")

    def show_timer(self):
        self.timer_window = CountdownTimer()
        self.timer_window.show()

    def show_statistics(self):
        print("WHERE IS YOUR PROGRESSIONNN")

    def show_calendar(self):
        self.pages.setCurrentWidget(self.calendar_page)

    def open_music_settings(self):
        MusicDialog(self.music, parent=self).exec()

    def show_todolist(self):
        self.todolist_popup.show()


    

    # Change wallpaper and save previous to inventory

    def handle_item_selected(self, category, name, image):

        if category == "wallpaper":

            # Return previous wallpaper to inventory
            previous_name = self.current_wallpaper["name"]
            previous_image = self.current_wallpaper["image"]

            inventory[previous_name] = {
                "image": previous_image,
                "category": "wallpaper"
            }

            # Remove new wallpaper from inventory
            if name in inventory:
                del inventory[name]

            # Set new wallpaper as currently used
            self.current_wallpaper = {
                "name": name,
                "image": image
            }

            self.change_wallpaper(image)

            # Refresh inventory
            self.inventory_page.show_inventory()

        else:
            self.add_item_to_room(name, image)

    def change_wallpaper(self, image):

        print("WALLPAPER PATH:", image)
        print("EXISTS:", os.path.exists(image))

        pixmap = QPixmap(image)

        if pixmap.isNull():
            print("ERROR: Wallpaper could not be loaded")
            return

        self.image.setPixmap(pixmap)
        self.image.setScaledContents(True)
        self.image.show()

        self.pages.setCurrentWidget(self.room_page)

    def add_item_to_room(self, name, image, category="furniture"):

        print("ADDING:", name, image)

        # Get item information before removing it
        item_data = inventory.get(
            name,
            {}
        )

        item = RoomItem(
            name,
            image,
            self
        )

        self.scene.addItem(item)

        item.setPos(
            400,
            300
        )

        item.setZValue(10)

        # Remember room item
        self.room_layout[name] = item

        # Remove item from inventory
        if name in inventory:
            del inventory[name]

        # Save everything immediately
        self.save_current_player_state()

        self.pages.setCurrentWidget(
            self.room_page
        )

        self.view.show()

    def return_to_inventory(self, name, image):

        inventory[name] = {
            "image": image,
            "category": "furniture"
        }

        # Save inventory permanently
        player = self.player_records.get_player(
            self.player_name
        )

        if player is not None:
            player["inventory"] = dict(inventory)
            self.player_records.save_data()

        self.inventory_page.show_inventory()

    def show_room(self):

        self.pages.setCurrentWidget(
            self.room_page
        )



    def closeEvent(self, event):

        print("WINDOW CLOSING...")

        self.save_current_player_state()

        event.accept()

# if 
# app = QApplication(sys.argv)

# window = Window()
# window.show()
def open_music_settings(self):
#         MusicDialog(self.music, parent=self).exec()
# sys.exit(app.exec())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HomePage()
    window.show()
    sys.exit(app.exec())