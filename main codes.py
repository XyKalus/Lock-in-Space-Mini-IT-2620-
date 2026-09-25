import sys
import os

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

from Ida.shoppingcart import ShoppingCart
from Ida.inventory import InventoryWindow, RoomItem, inventory
#from Yeejing.countdown timer import   

class Window(QDialog):

    def __init__(self):
        super().__init__()

        self.setWindowIcon(
            QIcon(
                os.path.join(BASE_DIR,"Ida","images","Icons","officialbg.png")
            )       
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
            BASE_DIR,
            "Ida",
            "images",
            "audio",
            "intro.mp4"
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
        self.pages.addWidget(self.room_page)
        self.pages.addWidget(self.shop_page)
        self.pages.addWidget(self.inventory_page)

        self.pages.setGeometry(
            0,
            0,
            1100,
            800
        )

        # ====================================================
        # CLOSE BUTTONS
        # ====================================================

        self.shop_page.close_button.clicked.connect(
            self.show_room
        )

        self.inventory_page.close_button.clicked.connect(
            self.show_room
        )

        # ====================================================
        # ROOM

        self.current_wallpaper = {
            "name": "Default",
            "image": os.path.join(
                BASE_DIR,
                "Ida",
                "images",
                "wallpaper",
                "background.png"
            )
        }

        self.InitWindow()

        # ====================================================
        # START INTRO VIDEO
        # ====================================================

        self.pages.setCurrentWidget(
            self.intro_page
        )

        self.intro_player.mediaStatusChanged.connect(
            self.intro_finished
        )

        self.intro_player.play()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            if self.pages.currentWidget() == self.intro_page:
                self.intro_player.stop()
                self.pages.setCurrentWidget(self.room_page)
            else:
                super().keyPressEvent(event)


    def InitWindow(self):

        # ====================================================
        # BACKGROUND

        self.image = QLabel(
            self.room_page
        )

        pixmap = QPixmap(
            os.path.join(
                BASE_DIR,
                "Ida",
                "images",
                "wallpaper",
                "background.png"
            )
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

        self.menu_button.setGeometry(
            940,
            50,
            100,
            100
        )

        self.menu_button.setToolTip(
            "<b>Menu</b><br>"
            "Open the menu to access your needs"
        )

        self.menu_button.setIcon(
            QIcon(
                os.path.join(
                    BASE_DIR,
                    "Ida",
                    "images",
                    "Icons",
                    "menuicon.png"
                )
            )
        )

        self.menu_button.setIconSize(
            QSize(
                150,
                150
            )
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

        # ====================================================
        # INVENTORY BUTTON
        # ====================================================

        self.inventory_button = QPushButton(
            self.room_page
        )

        self.inventory_button.setGeometry(
            820,
            150,
            100,
            100
        )

        self.inventory_button.setToolTip(
            "<b>Inventory</b><br>"
            "View your items and decorate your study space!"
        )

        self.inventory_button.setIcon(
            QIcon(
                os.path.join(
                    BASE_DIR,
                    "Ida",
                    "images",
                    "Icons",
                    "invenicon.png"
                )
            )
        )

        self.inventory_button.setIconSize(
            QSize(
                150,
                150
            )
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

        self.inventory_button.clicked.connect(
            self.show_inventory
        )


        # ====================================================
        # SHOPPING CART BUTTON
        # ====================================================

        self.shop_button = QPushButton(
            self.room_page
        )

        self.shop_button.setGeometry(
            920,
            150,
            100,
            100
        )

        self.shop_button.setToolTip(
            "<b>Shopping Cart</b><br>"
            "Spend your coins and find new items for your room!"
        )

        self.shop_button.setIcon(
            QIcon(
                os.path.join(
                    BASE_DIR,
                    "Ida",
                    "images",
                    "Icons",
                    "shopicon.png"
                )
            )
        )

        self.shop_button.setIconSize(
            QSize(
                150,
                150
            )
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

        self.shop_button.clicked.connect(
            self.show_shop
        )


        # ====================================================
        # HIDE BUTTONS AT START
        # ====================================================

        self.inventory_button.hide()
        self.shop_button.hide()

        self.menu_button.clicked.connect(
            self.toggle_menu
        )

    def toggle_menu(self):

        if self.inventory_button.isVisible():

            self.inventory_button.hide()
            self.shop_button.hide()

        else:

            self.inventory_button.show()
            self.shop_button.show()

    def intro_finished(self, status):

        if status == QMediaPlayer.MediaStatus.EndOfMedia:

            self.intro_player.stop()

            self.pages.setCurrentWidget(
                self.room_page
            )
    
    def show_shop(self):

        self.pages.setCurrentWidget(
            self.shop_page 
        )

    def show_inventory(self):

        self.inventory_page.show_inventory()

        self.pages.setCurrentWidget(
            self.inventory_page
        )

    def handle_item_selected(self, category, name, image):

        if category == "wallpaper":

            # Return previous wallpaper to inventory
            if self.current_wallpaper["name"] != "Default":

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

        self.scene.addItem(
            item
        )

        item.setPos(
            400,
            300
        )

        item.setZValue(
            10
        )

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