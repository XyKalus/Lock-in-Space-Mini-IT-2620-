import sys
import os

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

from Ida.shoppingcart import ShoppingCart
from Ida.inventory import InventoryWindow, RoomItem, inventory


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

        self.pages.setGeometry(
            0,
            0,
            1100,
            800
        )

        self.room_page = QWidget()

        self.shop_page = ShoppingCart()

        # To Connect item into Main Window

        self.inventory_page = InventoryWindow()
        
        self.inventory_page.item_selected.connect(
            self.add_item_to_room
        )

 
        # ====================================================
        # X BUTTONS → BACK TO ROOM
        # ====================================================

        self.shop_page.close_button.clicked.connect(
            self.show_room
        )

        self.inventory_page.close_button.clicked.connect(
            self.show_room
        )

        # Add Pages
        self.pages.addWidget(
            self.room_page
        )

        self.pages.addWidget(
            self.shop_page
        )

        self.pages.addWidget(
            self.inventory_page
        )
        # ====================================================
        # ROOM

        self.InitWindow()


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
        # SHOP BUTTON

        self.shop_button = QPushButton(
            self.room_page
        )

        self.shop_button.setGeometry(
            930,
            50,
            100,
            100
        )

        self.shop_button.setIcon(
            QIcon(
                os.path.join(
                    BASE_DIR,
                    "Ida",
                    "images",
                    "Icons",
                    "22.png"
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
        # INVENTORY BUTTON

        self.inventory_button = QPushButton(
            self.room_page
        )

        self.inventory_button.setGeometry(
            830,
            50,
            100,
            100
        )

        self.inventory_button.setIcon(
            QIcon(
                os.path.join(
                    BASE_DIR,
                    "Ida",
                    "images",
                    "Icons",
                    "11.png"
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

    def show_shop(self):

        self.pages.setCurrentWidget(
            self.shop_page 
        )

    def show_inventory(self):

        self.inventory_page.show_inventory()

        self.pages.setCurrentWidget(
            self.inventory_page
        )

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
            "image": image
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