import sys
import os

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
from Ida.enteringsystem import LoginSystem
from Yeejing.countdowntimer import CountdownTimer 
from Haikal.calendarsystem import Calendar

class Window(QDialog):

    def __init__(self):
        
        super().__init__()

        self.pages = QStackedWidget(self)

        # Button click sound
        self.click_sound = QSoundEffect(self)
        self.player_records = PlayerRecords(BASE_DIR)

        #
        self.login_system = LoginSystem(self.player_records)
        self.login_system.login_success.connect(self.player_login_success)
        self.pages.addWidget(self.login_system)

        self.click_sound.setSource(QUrl.fromLocalFile(os.path.join(BASE_DIR,"Ida","images","audio","clicked.wav")))
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

        self.setWindowIcon(QIcon(os.path.join(BASE_DIR,"Ida","images","Icons","officialbg.png")))
        self.setWindowTitle("Lock In Space")
        self.setFixedSize(QSize(1100, 800))

        # INTRO VIDEO PAGE
        self.intro_page = QWidget()

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

        # ROOM / SHOP / INVENTORY PAGES

        self.room_page = QWidget()

        # CREATE THESE BEFORE USING THEM
        self.shop_page = ShoppingCart()
        self.shop_page.coins_changed.connect(self.update_coin_display)

        self.inventory_page = InventoryWindow()

        self.inventory_page.item_selected.connect(
            self.handle_item_selected
        )
        self.calendar_page = Calendar()

        # ADD PAGES (QStackWidget) BUTTON

        self.pages.addWidget(self.intro_page)
        self.pages.addWidget(self.room_page)
        self.pages.addWidget(self.shop_page)
        self.pages.addWidget(self.inventory_page)
        self.pages.addWidget(self.calendar_page)

        self.pages.setGeometry(0,0,1100,800)

        # CLOSE BUTTONS
        self.shop_page.close_button.clicked.connect(self.show_room)
        self.inventory_page.close_button.clicked.connect(self.show_room)
        self.calendar_page.close_button.clicked.connect(self.show_room)

        # Changing current wallpaper with a new one
        self.current_wallpaper = {
            "name": "White and Wood",
            "image": os.path.join(BASE_DIR,"Ida","images","wallpaper","mainbackground.png")
        }

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
      
        # START INTRO VIDEO

        self.pages.setCurrentWidget(self.intro_page)

        self.intro_player.mediaStatusChanged.connect(self.intro_finished)

        self.intro_player.play()

    def player_login_success(self, name, gender):

        self.player_name = name
        self.player_gender = gender

        # Get saved player data
        player = self.player_records.get_player(
            self.player_name
        )

        if player is not None:

            # LOAD COINS
            self.coins = player.get("coins",50)

            self.coin_amount.setText(str(self.coins))

            self.shop_page.set_coins(self.coins)

          
            # LOAD INVENTORY
            inventory.clear()

            saved_inventory = player.get("inventory", {})
            inventory.update(saved_inventory)

            print(
                "LOADED INVENTORY:",
                inventory
            )

            # LOAD WALLPAPER

            wallpaper = player.get("wallpaper")

            if isinstance(wallpaper, dict):

                self.current_wallpaper = {
                    "name": wallpaper.get(
                        "name",
                        "White and Wood"
                    ),
                    "image": wallpaper.get(
                        "image",
                        os.path.join(BASE_DIR, "Ida", "images", "wallpaper", "mainbackground.png"))
                }

            else:

                self.current_wallpaper = {"name": "White and Wood",
                                          "image": os.path.join(BASE_DIR, "Ida", "images", "wallpaper", "mainbackground.png")
                }

        # CLEAR OLD ROOM

        self.scene.clear()
        self.room_layout.clear()

        # LOAD ROOM

        self.enter_room()

        # APPLY SAVED WALLPAPER
        if self.current_wallpaper:
            self.change_wallpaper(
                self.current_wallpaper["image"]
            )
        

   # OUTPUT
    def claim_daily_login(self):

        success, coins = self.daily_login.claim(self.player_name)

        if success:
            self.coins = coins
            self.coin_amount.setText(str(coins))

            # Update Shopping Cart coins
            self.shop_page.set_coins(self.coins)

            self.show_daily_notification(
                "+10 COINS!\n"
                "Daily reward claimed!"
            )

        else:
            self.show_daily_notification("Already Claimed Today!")

    def show_daily_notification(self, message):
        self.daily_notification = QLabel(message, self)

        self.daily_notification.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.daily_notification.setGeometry(450,200,200,260)

        self.daily_notification.setFont(QFont("Cave Story", 20, QFont.Weight.Bold))

        self.daily_notification.setStyleSheet("""
            QLabel {
                background-color: #202e63;
                color: white;
                border-radius: 15px;
                padding: 12px 25px;
                font-size: 30px;
                font-weight: bold;
            }
        """)

        self.daily_notification.adjustSize()
        self.daily_notification.show()

        # Automatically disappear after 2 seconds
        QTimer.singleShot(
            2000,
            self.daily_notification.deleteLater
        )

    def set_coins(self, coins):
        self.coins = coins
        self.coin_text.setText(str(coins))

    # ENTER button func.
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:

            if self.pages.currentWidget() == self.intro_page:
                self.intro_player.stop()
                self.pages.setCurrentWidget(self.login_system)
                
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


    def enter_room(self):

        # GET PLAYER'S SAVED ROOM

        player = self.player_records.get_player(self.player_name)

        saved_items = {}

        if player is not None:
            saved_items = player.get(
                "room_items",
                {}
            )

        print("SAVED ROOM ITEMS:", saved_items)

        # LOAD THEIR SAVED ROOM
  
        if saved_items:

            for name, data in saved_items.items():

                image = data.get("image")

                if not image:
                    continue

                # Convert saved relative path to full path
                if not os.path.isabs(image):
                    image = os.path.join(BASE_DIR, image)

                print("LOADING SAVED ITEM:", name)
                print("IMAGE PATH:", image)
                print(
                    "IMAGE EXISTS:",
                    os.path.exists(image)
                )

                if not os.path.exists(image):
                    continue

                item = RoomItem(name, image, self)

                self.scene.addItem(item)

                item.setPos(
                    data.get("x", 400),
                    data.get("y", 300)
                )

                item.setScale(data.get("scale", 1.0))
                item.setZValue(10)
                self.room_layout[name] = item

        else:

            # CHARACTER

            if self.player_gender == "boy":

                character_path = os.path.join(BASE_DIR, "Ida", "images", "characters", "boy.png")

            else:

                character_path = os.path.join(BASE_DIR, "Ida", "images", "characters", "girl.png")

            if os.path.exists(character_path):

                self.character_item = RoomItem(
                    "BOY",
                    character_path,
                    self
                )

                self.scene.addItem(self.character_item)
                self.character_item.setPos(400, 380)
                self.character_item.setScale(2.0)
                self.character_item.setZValue(10)

            # BED
            bed_path = os.path.join(BASE_DIR, "Ida", "images", "furnitures","bed.png")

            if os.path.exists(bed_path):

                self.bed_item = RoomItem("bed", bed_path, self)
                self.scene.addItem(self.bed_item)
                self.bed_item.setPos(5,500)
                self.bed_item.setScale(2.5)
                self.bed_item.setZValue(10)
            
            # CURTAIN

            curtain_path = os.path.join(BASE_DIR,"Ida", "images", "furnitures", "curtain.png")

            if os.path.exists(curtain_path):

                self.curtain_item = RoomItem("curtain", curtain_path, self)
                self.scene.addItem(self.curtain_item)
                self.curtain_item.setPos(50, 200)
                self.curtain_item.setScale(2.5)

                self.curtain_item.setZValue(10)

            # DOOR
            door_path = os.path.join(BASE_DIR, "Ida", "images", "furnitures","door.png")

            if os.path.exists(door_path):

                self.door_item = RoomItem("door", door_path, self)
                self.scene.addItem(self.door_item)
                self.door_item.setPos(700, 280)
                self.door_item.setScale(2.5)
                self.door_item.setZValue(10)

        # GO TO ROOM

        self.pages.setCurrentWidget(
            self.room_page
        )

        self.show_room_note()

        QTimer.singleShot(
            1000,
            self.claim_daily_login
        )

        print(
            f"Welcome {self.player_name}!"
        )

    def show_room_note(self):

        self.room_note = QLabel(
            "This is your space to lock in!\n"
            "Customize your room and make it yours!",
            self.room_page)

        self.room_note.setGeometry(300, 30, 500, 110)

        self.room_note.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.room_note.setWordWrap(True)

        self.room_note.setStyleSheet("""
            QLabel {
                background-color: rgba(17, 21, 45, 235);
                color: white;
                border-radius: 15px;
                padding: 12px 25px;
                font-size: 30px;
                font-weight: bold;  
            }
        """)

        self.room_note.setFont(QFont("Cave Story", 20, QFont.Weight.Bold))

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
        for item in self.scene.items():

            if not isinstance(item, RoomItem):
                continue

            name = item.item_name

            saved_items[name] = {
                "image": item.image,
                "x": item.pos().x(),
                "y": item.pos().y(),
                "scale": item.scale(),
                "category": "furniture"
            }

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
        
        # COINS
        player["coins"] = self.coins

        # INVENTORY
        player["inventory"] = dict(
            inventory
        )

        # ROOM
        saved_items = {}

        for item in self.scene.items():
            if not isinstance(item, RoomItem):
                continue

            name = item.item_name

            saved_items[name] = {
                "image": item.image,
                "x": item.pos().x(),
                "y": item.pos().y(),
                "scale": item.scale(),
                "category": "furniture"
            }

        player["room_items"] = saved_items

        # WALLPAPER
        player["wallpaper"] = self.current_wallpaper

        # SAVE JSON
        self.player_records.save_data()
        print("PLAYER STATE SAVED")

    def InitWindow(self):

        # BACKGROUND
        self.image = QLabel(self.room_page)

        pixmap = QPixmap(os.path.join(BASE_DIR,"Ida","images","wallpaper","mainbackground.png")
        )

        self.image.setPixmap(pixmap)
        self.image.setScaledContents(True)
        self.image.setGeometry(0, 0, 1100,800)
        self.image.lower()
      
        # ROOM ITEM AREA
        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0, 0, 1100,800)
        self.view = QGraphicsView(self.scene, self.room_page)
        self.view.setGeometry(0,0, 1100, 800)

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
        self.view.setSceneRect(0, 0, 1100, 800)

        # MENU BUTTON

        self.menu_button = QPushButton(
            self.room_page
        )

        self.menu_button.setGeometry(940,50,100,100)

        self.menu_button.setToolTip(
            "<b>Menu</b><br>"
            "Open the menu to access your needs"
        )

        self.menu_button.setIcon(QIcon(os.path.join(BASE_DIR,"Ida","images","Icons","menuicon.png")))
        self.menu_button.setIconSize(QSize(150,150))
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

        # INVENTORY BUTTON
        self.inventory_button = QPushButton(self.room_page)
        self.inventory_button.setGeometry(820,150,100,100)
        
        self.inventory_button.setToolTip(
         "<b>Inventory</b><br>"
            "View your items and decorate your study space!"
        )

        self.inventory_button.setIcon(QIcon(os.path.join(BASE_DIR,"Ida","images","Icons","invenicon.png")))
        self.inventory_button.setIconSize( QSize(150,150))
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

        # SHOPPING CART BUTTON
        self.shop_button = QPushButton(self.room_page)
        self.shop_button.setGeometry(1000,150,100,100)
        self.shop_button.setToolTip(
            "<b>Shopping Cart</b><br>"
            "Spend your coins and find new items for your room!"
        )

        self.shop_button.setIcon(QIcon(os.path.join(BASE_DIR,"Ida","images","Icons","shopicon.png")))
        self.shop_button.setIconSize(QSize(150, 150))
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
        
        # TO-DO LIST BUTTON
        self.tdlist_button = QPushButton(self.room_page)
        self.tdlist_button.setGeometry(910,150,100,100)

        self.tdlist_button.setToolTip(
            "<b>To-Do List</b><br>"
            "Keep track of your tasks and goals"
        )

        self.tdlist_button.setIcon(QIcon(os.path.join(BASE_DIR,"Ida","images","Icons","todoicon.png")))
        self.tdlist_button.setIconSize(QSize(150, 150))
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

        self.timer_button.setIcon(QIcon(os.path.join(BASE_DIR,"Ida","images","Icons","timericon.png")))
        self.timer_button.setIconSize(QSize(150, 150))
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

        self.statistics_button = QPushButton(self.room_page)
        self.statistics_button.setGeometry(910,235,100,100)
        self.statistics_button.setToolTip(
            "<b>Statistics</b><br>"
            "View your study progress and achievements!!"
        )

        self.statistics_button.setIcon(QIcon(os.path.join(BASE_DIR,"Ida","images","Icons","staticon.png")))
        self.statistics_button.setIconSize(QSize(150, 150))
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

        self.calendar_button = QPushButton(self.room_page)

        self.calendar_button.setGeometry(1000,235,100,100)

        self.calendar_button.setToolTip("<b>Calendar</b><br>"
                                        "Plan your study sessions and keep track of important dates!"
        )

        self.calendar_button.setIcon(QIcon(os.path.join(BASE_DIR,"Ida","images","Icons","calenicon.png")))
        self.calendar_button.setIconSize(QSize(150, 150))
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

        # HIDE BUTTON
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
            self.pages.setCurrentWidget(self.login_system)

    # Output function 
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

        item = RoomItem(name, image, self)

        self.scene.addItem(item)
        item.setPos(400,300)

        item.setZValue(10)

        # Remember room item
        self.room_layout[name] = item

        # Remove item from inventory
        if name in inventory:
            del inventory[name]

        # Save everything immediately
        self.save_current_player_state()
        self.pages.setCurrentWidget(self.room_page)
        self.view.show()

    def return_to_inventory(self, name, image):

        inventory[name] = {"image": image,
                            "category": "furniture"}

        # Save inventory permanently
        player = self.player_records.get_player(self.player_name)

        if player is not None:
            player["inventory"] = dict(inventory)
            self.player_records.save_data()
        self.inventory_page.show_inventory()

    def show_room(self):

        self.pages.setCurrentWidget(self.room_page)

    # SEND OUTPUT TO CLOSED
    def closeEvent(self, event):

        print("WINDOW CLOSING...")
        self.save_current_player_state()
        event.accept()

app = QApplication(sys.argv)

window = Window()
window.show()

sys.exit(app.exec())