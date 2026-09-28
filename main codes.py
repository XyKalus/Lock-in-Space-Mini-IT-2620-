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
#from Yeejing.countdown timer import   

class Window(QDialog):

    def __init__(self):
        super().__init__()

        # Button click sound
        self.click_sound = QSoundEffect(self)
        self.player_records = PlayerRecords(BASE_DIR)

        self.click_sound.setSource(
            QUrl.fromLocalFile(os.path.join(BASE_DIR,"Ida","images","audio","clicked.wav"))
        )

        self.click_sound.setVolume(0.5)

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

        self.inventory_page = InventoryWindow()

        self.inventory_page.item_selected.connect(
            self.handle_item_selected
        )

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

        self.pages.setGeometry(0,0,1100,800)

        # ====================================================
        # CLOSE BUTTONS
        # ====================================================

        self.shop_page.close_button.clicked.connect(self.show_room)

        self.inventory_page.close_button.clicked.connect(self.show_room)

        # Changing current wallpaper with a new one
        self.current_wallpaper = {
            "name": "White and Wood",
            "image": os.path.join(BASE_DIR,"Ida","images","wallpaper","mainbackground.png")
        }

        self.create_name_page()
        self.create_character_page()
        self.create_welcome_page()

        self.InitWindow()

        # ====================================================
        # START INTRO VIDEO
        # ====================================================

        self.pages.setCurrentWidget(
            self.intro_page
        )

        self.show_room_note()

        self.intro_player.mediaStatusChanged.connect(self.intro_finished)

        self.intro_player.play()

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

    def name_next_clicked(self):

        name = self.name_input.text().strip()

        if not name:
            self.name_input.setPlaceholderText(
                "Please enter your name!"
            )
            return

        self.player_name = name

        self.pages.setCurrentWidget(
            self.character_page
        )

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

        curtain_path = os.path.join(BASE_DIR,"Ida","images","furnitures","curtain.png"
        )

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

        print("DOOR PATH:", curtain_path)
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

        # Go to room
        self.pages.setCurrentWidget(
            self.room_page
        )

        # SHOW TEMPORARY NOTE
        self.show_room_note()

        print(f"Welcome {self.player_name}!")



    def no_name_clicked(self):

        self.pages.setCurrentWidget(
            self.room_page
        )


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

        # SAVE NEW PLAYER
        self.player_records.create_player(
            self.player_name,
            self.player_gender
        )

        print("PLAYER NAME:", self.player_name)
        print("PLAYER GENDER:", self.player_gender)

        # UPDATE WELCOME MESSAGE WITH PLAYER NAME
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

        self.welcome_no.setFont(
            QFont("Cave Story", 15, QFont.Weight.Bold)
        )

        self.welcome_no.clicked.connect(
            self.back_to_name
        )

        self.welcome_no.clicked.connect(
            self.play_click_sound
        )

        self.welcome_no.clicked.connect(
            self.back_to_name
        )

    def show_room_note(self):

        self.room_note = QLabel(
            "This is your space to lock in!\n"
            "Customize your room and make it yours!",
            self.room_page
        )

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

    def save_room_layout(self):

        self.room_layout = {}

        for item in self.scene.items():

            if isinstance(item, RoomItem):

                self.room_layout[item.item_name] = {
                    "x": item.pos().x(),
                    "y": item.pos().y()
                }

        self.save_room_button = QPushButton(
            "SAVE ROOM",
            self.room_page
        )

        self.save_room_button.setGeometry(
            850,
            30,
            180,
            60
        )

        self.save_room_button.clicked.connect(
            self.save_room_layout
)

        print("ROOM SAVED:")
        print(self.room_layout)

    def InitWindow(self):

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

        self.tdlist_button.clicked.connect(self.show_tdlist)
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


        # ====================================================
        # HIDE BUTTONS AT START
        # ====================================================

        self.inventory_button.hide()
        self.shop_button.hide()
        self.tdlist_button.hide()
        self.timer_button.hide()
        self.statistics_button.hide()
        self.calendar_button.hide()




    def toggle_menu(self):

        if self.inventory_button.isVisible():

            self.inventory_button.hide()
            self.shop_button.hide()
            self.tdlist_button.hide()
            self.timer_button.hide()
            self.statistics_button.hide()
            self.calendar_button.hide()


        else:

            self.inventory_button.show()
            self.shop_button.show()
            self.tdlist_button.show()
            self.timer_button.show()
            self.statistics_button.show()
            self.calendar_button.show()

    def intro_finished(self, status):

        if status == QMediaPlayer.MediaStatus.EndOfMedia:

            self.intro_player.stop()

            self.pages.setCurrentWidget(
                self.name_page
            )

        ###EXAMPLE###
    def show_shop(self):

        self.pages.setCurrentWidget(
            self.shop_page 
        )

    def show_inventory(self):

        self.inventory_page.show_inventory()

        self.pages.setCurrentWidget(
            self.inventory_page
        )
######## WAITING FOR FULLCODES####### (FROM DIFF FILE)
    def show_tdlist(self):
        print("To-Do List clicked!")

    def show_timer(self):
        print("DONT WASTE TIME LAA")

    def show_statistics(self):
        print("WHERE IS YOUR PROGRESSIONNN")

    def show_calendar(self):
        print("NOT BADD")

    

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

    def add_item_to_room(self, name, image):

        print("ADDING:", name, image)

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

        # Remember this furniture item
        self.room_layout[name] = item

        self.pages.setCurrentWidget(
            self.room_page
        )

        self.view.show()


    def return_to_inventory(self, name, image):
        inventory[name] = {
            "image": image,
            "category": "characters"
        }

        self.inventory_page.show_inventory()
    def show_room(self):

        self.pages.setCurrentWidget(
            self.room_page
        )



app = QApplication(sys.argv)

window = Window()
window.show()

sys.exit(app.exec())