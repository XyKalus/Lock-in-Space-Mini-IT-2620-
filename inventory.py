import sys
import os

from PyQt5.QtWidgets import (
    QApplication,
    QDialog,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QFrame,
    QWidget,
    QScrollArea,
    QMessageBox,
    QGraphicsView,
    QGraphicsScene,
    QGraphicsPixmapItem,
    QGraphicsItem
)

from PyQt5.QtGui import (
    QPixmap,
    QIcon,
    QFont,
    QFontDatabase,
    QPainter,
    QPen
)

from PyQt5.QtCore import (
    QSize,
    Qt,
    QRectF
)


# ============================================================
# PATH
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def img(file):
    return os.path.join(BASE_DIR, file)


# ============================================================
# GAME DATA
# ============================================================

coins = 50000

inventory = {}


# ============================================================
# SHOP ITEMS
# ============================================================

ITEMS = [

    # ---------------- CHARACTERS ----------------

    {
        "name": "Yeejing",
        "image": "characters/C1.png",
        "price": 1000,
        "category": "characters"
    },

    {
        "name": "Haikal",
        "image": "characters/C2.png",
        "price": 500,
        "category": "characters"
    },

    {
        "name": "Khaled",
        "image": "characters/CCC3.png",
        "price": 1000,
        "category": "characters"
    },

    {
        "name": "Coco",
        "image": "characters/C4.png",
        "price": 500,
        "category": "characters"
    },

    {
        "name": "Sean","image": "characters/C6.png","price": 1000,"category": "characters"
    },

    {
        "name": "Siew Che",
        "image": "characters/C5.png",
        "price": 500,
        "category": "characters"
    },

    {
        "name": "Dani",
        "image": "characters/C7.png",
        "price": 500,
        "category": "characters"
    },

    {
        "name": "Ida",
        "image": "characters/C8.png",
        "price": 500,
        "category": "characters"
    },


    # ---------------- WALLPAPER ----------------

    {
        "name": "Aesthetic",
        "image": "background.png",
        "price": 1000,
        "category": "wallpaper"
    },

    {
        "name": "Pink Wallpaper",
        "image": "W2.png",
        "price": 1200,
        "category": "wallpaper"
    },

    {
        "name": "Night Wallpaper",
        "image": "W3.png",
        "price": 1500,
        "category": "wallpaper"
    },

    {
        "name": "Cozy Wallpaper",
        "image": "W4.png",
        "price": 1500,
        "category": "wallpaper"
    },

    {
        "name": "Modern Wallpaper",
        "image": "W5.png",
        "price": 1800,
        "category": "wallpaper"
    },

    {
        "name": "Study Wallpaper",
        "image": "W6.png",
        "price": 2000,
        "category": "wallpaper"
    },


    # ---------------- PETS ----------------

    {
        "name": "Siamese Cat",
        "image": "pets/cat1.png",
        "price": 1300,
        "category": "pets"
    },

    {
        "name": "Beagle Dog",
        "image": "pets/dog1.png",
        "price": 2000,
        "category": "pets"
    },

    {
        "name": "Yellow Bird",
        "image": "pets/bird1.png",
        "price": 1500,
        "category": "pets"
    },

    {
        "name": "Gary",
        "image": "pets/snail1.png",
        "price": 1500,
        "category": "pets"
    },

    {
        "name": "Froggy",
        "image": "pets/frog1.png",
        "price": 1800,
        "category": "pets"
    },

    {
        "name": "Donald Duck",
        "image": "pets/duck1.png",
        "price": 2000,
        "category": "pets"
    },

    {
        "name": "Nemo",
        "image": "pets/fish1.png",
        "price": 2300,
        "category": "pets"
    },

    {
        "name": "Rabbit",
        "image": "pets/rabbit1.png",
        "price": 5000,
        "category": "pets"
    },


    # ---------------- FURNITURE ----------------

    {
        "name": "Book Rack",
        "image": "furnitures/bookrack.png",
        "price": 1000,
        "category": "furniture"
    },

    {
        "name": "TV",
        "image": "furnitures/TV.png",
        "price": 2000,
        "category": "furniture"
    },

    {
        "name": "Flower Vase",
        "image": "furnitures/Vast.png",
        "price": 1000,
        "category": "furniture"
    },

    {
        "name": "Guitar",
        "image": "furnitures/guitar.png",
        "price": 7000,
        "category": "furniture"
    },

    {
        "name": "Radio",
        "image": "furnitures/radio.png",
        "price": 1000,
        "category": "furniture"
    },

    {
        "name": "Cat Tree",
        "image": "furnitures/cattoys.png",
        "price": 500,
        "category": "furniture"
    },


    # ---------------- FOODS ----------------

    {
        "name": "Croissant",
        "image": "foods/f1.png",
        "price": 1000,
        "category": "foods"
    },

    {
        "name": "Coffee",
        "image": "foods/d1.png",
        "price": 500,
        "category": "foods"
    },

    {
        "name": "Sandwich",
        "image": "foods/f2.png",
        "price": 1000,
        "category": "foods"
    },

    {
        "name": "Coca Cola",
        "image": "foods/d2.png",
        "price": 500,
        "category": "foods"
    },

    {
        "name": "Doritos",
        "image": "foods/f3.png",
        "price": 1000,
        "category": "foods"
    },

    {
        "name": "Strawberry Mojito",
        "image": "foods/d3.png",
        "price": 500,
        "category": "foods"
    },

    {
        "name": "Sushi",
        "image": "foods/f4.png",
        "price": 1000,
        "category": "foods"
    },

    {
        "name": "Boba Tea",
        "image": "foods/d4.png",
        "price": 500,
        "category": "foods"
    },

    {
        "name": "Donut",
        "image": "foods/f5.png",
        "price": 1000,
        "category": "foods"
    },

    {
        "name": "Lime Milkshake",
        "image": "foods/d5.png",
        "price": 500,
        "category": "foods"
    },

    {
        "name": "Pizza",
        "image": "foods/f6.png",
        "price": 1000,
        "category": "foods"
    },

    {
        "name": "Root Beer",
        "image": "foods/d6.png",
        "price": 500,
        "category": "foods"
    },

    {
        "name": "Ramen",
        "image": "foods/f7.png",
        "price": 1000,
        "category": "foods"
    },

    {
        "name": "Coconut",
        "image": "foods/d7.png",
        "price": 500,
        "category": "foods"
    },

    {
        "name": "Spaghetti",
        "image": "foods/f8.png",
        "price": 1000,
        "category": "foods"
    },

    {
        "name": "Sundae Ice Cream",
        "image": "foods/d8.png",
        "price": 500,
        "category": "foods"
    },

    {
        "name": "Pancake",
        "image": "foods/f9.png",
        "price": 1000,
        "category": "foods"
    },

    {
        "name": "Magnum",
        "image": "foods/d9.png",
        "price": 500,
        "category": "foods"
    },


    # ---------------- SPECIAL ----------------

    {
        "name": "HIM",
        "image": "C1.png",
        "price": 1000,
        "category": "Special"
    },

    {
        "name": "Rex",
        "image": "C2.png",
        "price": 500,
        "category": "Special"
    },

    {
        "name": "Rose",
        "image": "C1.png",
        "price": 1000,
        "category": "Special"
    },

    {
        "name": "Dex",
        "image": "C2.png",
        "price": 500,
        "category": "Special"
    }
]


# Create inventory count for every item

for item in ITEMS:
    inventory[item["name"]] = 0


# ============================================================
# ROOM ITEM
# ============================================================

class RoomItem(QGraphicsPixmapItem):

    def __init__(self, item_data):

        super().__init__()

        self.item_data = item_data
        self.locked = False

        pixmap = QPixmap(
            img(item_data["image"])
        )

        if not pixmap.isNull():

            pixmap = pixmap.scaled(
                160,
                160,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )

            self.setPixmap(pixmap)

        else:

            print(
                "IMAGE NOT FOUND:",
                img(item_data["image"])
            )

        # Can drag
        self.setFlag(
            QGraphicsItem.ItemIsMovable,
            True
        )

        # Can select
        self.setFlag(
            QGraphicsItem.ItemIsSelectable,
            True
        )


    # ========================================================
    # RESIZE USING MOUSE WHEEL
    # ========================================================

    def wheelEvent(self, event):

        if self.locked:
            return

        if event.delta() > 0:

            new_scale = self.scale() * 1.1

        else:

            new_scale = self.scale() * 0.9

        # Minimum and maximum size

        new_scale = max(
            0.9,
            min(new_scale, 3.0)
        )

        self.setScale(
            new_scale
        )

        event.accept()


    # ========================================================
    # LOCK / UNLOCK
    # ========================================================

    def lock(self):

        self.locked = True

        self.setFlag(
            QGraphicsItem.ItemIsMovable,
            False
        )

        self.setFlag(
            QGraphicsItem.ItemIsSelectable,
            False
        )


    def unlock(self):

        self.locked = False

        self.setFlag(
            QGraphicsItem.ItemIsMovable,
            True
        )

        self.setFlag(
            QGraphicsItem.ItemIsSelectable,
            True
        )


# ============================================================
# SHOP WINDOW
# ============================================================


class AnotherWindow(QDialog):

    def __init__(self, room_window):

        super().__init__()

        self.room_window = room_window

        self.setWindowTitle(
            "The Room Store"
        )

        self.setFixedSize(
            900,
            650
        )

        self.setWindowIcon(
            QIcon(img("Logos1.png"))
        )

        self.main_layout = QVBoxLayout()

        self.setLayout(
            self.main_layout
        )

        self.create_header()
        self.create_content()

        self.show_category(
            "characters"
        )


    # ========================================================
    # HEADER
    # ========================================================

    def create_header(self):

        header = QWidget()

        header.setFixedHeight(
            100
        )

        header_layout = QHBoxLayout()

        header.setLayout(
            header_layout
        )

        close_button = QPushButton("x")

        close_button.setFixedSize(
            55,
            55
        )

        close_button.clicked.connect(
            self.close
        )

        title = QLabel(
            "The Room Store"
        )

        title.setAlignment(
            Qt.AlignCenter
        )

        title.setFont(
            QFont(
                "Arial",
                28,
                QFont.Bold
            )
        )

        self.coin_label = QLabel()

        self.coin_label.setFont(
            QFont(
                "Arial",
                20,
                QFont.Bold
            )
        )

        header_layout.addWidget(
            close_button
        )

        header_layout.addWidget(
            title,
            1
        )

        header_layout.addWidget(
            self.coin_label
        )

        self.main_layout.addWidget(
            header
        )

        self.update_coins()


    # ========================================================
    # CONTENT
    # ========================================================

    def create_content(self):

        content = QWidget()

        content_layout = QHBoxLayout()

        content.setLayout(
            content_layout
        )

        # CATEGORY BAR

        category_bar = QFrame()

        category_bar.setFixedWidth(
            90
        )

        category_layout = QVBoxLayout()

        category_bar.setLayout(
            category_layout
        )

        categories = [
            ("sidebar/E1.png", "characters"),
            ("sidebar/E2.png", "wallpaper"),
            ("sidebar/E3.png", "pets"),
            ("sidebar/E4.png", "furniture"),
            ("sidebar/E5.png", "foods"),
            ("sidebar/E6.png", "Special")
        ]

        for icon, category in categories:

            button = QPushButton()

            button.setIcon(
                QIcon(
                    img(icon)
                )
            )

            button.setIconSize(
                QSize(
                    45,
                    45
                )
            )

            button.setFixedSize(
                65,
                65
            )

            button.clicked.connect(
                lambda checked=False,
                value=category:
                self.show_category(value)
            )

            category_layout.addWidget(
                button
            )

        category_layout.addStretch()

        content_layout.addWidget(
            category_bar
        )


        # ITEMS

        self.items_area = QWidget()

        self.items_layout = QGridLayout()

        self.items_area.setLayout(
            self.items_layout
        )

        scroll = QScrollArea()

        scroll.setWidgetResizable(
            True
        )

        scroll.setWidget(
            self.items_area
        )

        content_layout.addWidget(
            scroll
        )

        self.main_layout.addWidget(
            content
        )


    # ========================================================
    # CREATE SHOP ITEM
    # ========================================================

    def create_item(self, item):

        card = QFrame()

        card.setFixedSize(
            350,
            225
        )

        card.setStyleSheet("""
            QFrame {
                background-color: #b950c7;
                border: 3px solid #555555;
                border-radius: 20px;
            }
        """)

        layout = QVBoxLayout()

        name = QLabel(
            item["name"]
        )

        name.setAlignment(
            Qt.AlignCenter
        )

        name.setFont(
            QFont(
                "Arial",
                18,
                QFont.Bold
            )
        )

        image_label = QLabel()

        image_label.setAlignment(
            Qt.AlignCenter
        )

        pixmap = QPixmap(
            img(item["image"])
        )

        if not pixmap.isNull():

            pixmap = pixmap.scaled(
                140,
                110,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )

            image_label.setPixmap(
                pixmap
            )

        else:

            image_label.setText(
                "Image not found"
            )


        price = QLabel(
            f"🪙 {item['price']}"
        )

        price.setAlignment(
            Qt.AlignCenter
        )

        price.setFont(
            QFont(
                "Arial",
                16,
                QFont.Bold
            )
        )


        buy_button = QPushButton(
            "BUY"
        )

        buy_button.setFixedHeight(
            35
        )

        buy_button.clicked.connect(
            lambda checked=False,
            item_data=item:
            self.buy_item(item_data)
        )


        layout.addWidget(
            name
        )

        layout.addWidget(
            image_label
        )

        layout.addWidget(
            price
        )

        layout.addWidget(
            buy_button
        )

        card.setLayout(
            layout
        )

        return card


    # ========================================================
    # SHOW CATEGORY
    # ========================================================

    def show_category(self, category):

        while self.items_layout.count():

            item = self.items_layout.takeAt(
                0
            )

            widget = item.widget()

            if widget:
                widget.deleteLater()


        category_items = [

            item for item in ITEMS

            if item["category"] == category

        ]


        for index, item in enumerate(
            category_items
        ):

            card = self.create_item(
                item
            )

            self.items_layout.addWidget(
                card,
                index // 2,
                index % 2
            )


    # ========================================================
    # BUY
    # ========================================================

    def buy_item(self, item):

        global coins

        name = item["name"]
        price = item["price"]


        if coins < price:

            QMessageBox.warning(
                self,
                "Not Enough Coins",
                "You don't have enough coins!"
            )

            return


        coins -= price

        inventory[name] += 1


        self.update_coins()


        QMessageBox.information(
            self,
            "Purchase Successful",
            f"You bought {name}!\n\n"
            f"You own: {inventory[name]}"
        )


    def update_coins(self):

        self.coin_label.setText(
            f"🪙 {coins}"
        )


# ============================================================
# INVENTORY WINDOW
# ============================================================

class InventoryWindow(QDialog):

    def __init__(self, room_window):

        super().__init__()

        self.room_window = room_window

        self.setWindowTitle(
            "My Inventory"
        )

        self.setFixedSize(
            850,
            600
        )

        self.setWindowIcon(
            QIcon(img("Uilogos.png"))
        )

        self.layout = QVBoxLayout()

        self.setLayout(
            self.layout
        )

        title = QLabel(
            "MY INVENTORY"
        )

        title.setAlignment(
            Qt.AlignCenter
        )

        title.setFont(
            QFont(
                "Arial",
                28,
                QFont.Bold
            )
        )

        self.layout.addWidget(
            title
        )


        self.scroll = QScrollArea()

        self.scroll.setWidgetResizable(
            True
        )

        self.container = QWidget()

        self.grid = QGridLayout()

        self.container.setLayout(
            self.grid
        )

        self.scroll.setWidget(
            self.container
        )

        self.layout.addWidget(
            self.scroll
        )


        self.refresh()


    # ========================================================
    # REFRESH INVENTORY
    # ========================================================

    def refresh(self):

        while self.grid.count():

            item = self.grid.takeAt(
                0
            )

            widget = item.widget()

            if widget:
                widget.deleteLater()


        owned_items = [

            item for item in ITEMS

            if inventory[item["name"]] > 0

        ]


        if not owned_items:

            empty = QLabel(
                "Your inventory is empty."
            )

            empty.setAlignment(
                Qt.AlignCenter
            )

            empty.setFont(
                QFont(
                    "Arial",
                    20
                )
            )

            self.grid.addWidget(
                empty,
                0,
                0
            )

            return


        for index, item in enumerate(
            owned_items
        ):

            card = QFrame()

            card.setFixedSize(
                230,
                260
            )

            card.setStyleSheet("""
                QFrame {
                    background-color: #5f9e96;
                    border: 2px solid #ed0202;
                    border-radius: 15px;
                }
            """)

            layout = QVBoxLayout()

            name = QLabel(
                f"{item['name']} x {inventory[item['name']]}"
            )

            name.setAlignment(
                Qt.AlignCenter
            )

            name.setFont(
                QFont(
                    "Arial",
                    14,
                    QFont.Bold
                )
            )


            image = QLabel()

            image.setAlignment(
                Qt.AlignCenter
            )

            pixmap = QPixmap(
                img(item["image"])
            )

            if not pixmap.isNull():

                pixmap = pixmap.scaled(
                    110,
                    110,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )

                image.setPixmap(
                    pixmap
                )


            take_out = QPushButton(
                "TAKE OUT"
            )

            take_out.clicked.connect(
                lambda checked=False,
                item_data=item:
                self.take_out(item_data)
            )


            layout.addWidget(
                name
            )

            layout.addWidget(
                image
            )

            layout.addWidget(
                take_out
            )

            card.setLayout(
                layout
            )


            self.grid.addWidget(
                card,
                index // 3,
                index % 3
            )


    # ========================================================
    # TAKE ITEM OUT
    # ========================================================

    def take_out(self, item):

        name = item["name"]

        if inventory[name] <= 0:
            return


        inventory[name] -= 1

        self.room_window.add_room_item(
            item
        )

        self.refresh()


# ============================================================
# MAIN ROOM
# ============================================================

class Window(QDialog):

    def __init__(self):

        super().__init__()

        self.shop_window = None
        self.inventory_window = None

        self.setWindowTitle(
            "Lock In Space"
        )

        self.setWindowIcon(
            QIcon(
                img("Icons/officialbg.png")
            )
        )

        self.setFixedSize(
            1100,
            800
        )

        self.create_room()


    # ========================================================
    # ROOM
    # ========================================================

    def create_room(self):

        self.scene = QGraphicsScene(
            0,
            0,
            1100,
            800
        )


        background = QPixmap(
            img("background.png")
        )


        if not background.isNull():

            background = background.scaled(
                1100,
                800,
                Qt.IgnoreAspectRatio,
                Qt.SmoothTransformation
            )

            background_item = QGraphicsPixmapItem(
                background
            )

            background_item.setZValue(
                -100
            )

            self.scene.addItem(
                background_item
            )


        self.view = QGraphicsView(
            self.scene,
            self
        )

        self.view.setGeometry(
            0,
            0,
            1100,
            800
        )

        self.view.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff
        )

        self.view.setVerticalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff
        )

        self.view.setFrameShape(
            QGraphicsView.NoFrame
        )


        self.create_buttons()


    # ========================================================
    # ROOM BUTTONS
    # ========================================================

    def create_buttons(self):

        # SHOP BUTTON

        self.shop_button = QPushButton(
            self
        )

        self.shop_button.setGeometry(
            950,
            50,
            100,
            100
        )

        self.shop_button.setIcon(
            QIcon(
                img("Logos2.png")
            )
        )

        self.shop_button.setIconSize(
            QSize(
                80,
                80
            )
        )

        self.shop_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
            }

            QPushButton:hover {
                background-color: rgba(255,255,255,50);
                border-radius: 15px;
            }
        """)

        self.shop_button.clicked.connect(
            self.show_shop
        )


        # INVENTORY BUTTON

        self.inventory_button = QPushButton(
            "INVENTORY LAA",
            self
        )

        self.inventory_button.setGeometry(
            800,
            55,
            130,
            50
        )

        self.inventory_button.clicked.connect(
            self.show_inventory
        )


        # LOCK BUTTON

        self.lock_button = QPushButton(
            "LOCK ITEM",
            self
        )

        self.lock_button.setGeometry(
            650,
            55,
            130,
            50
        )

        self.lock_button.clicked.connect(
            self.lock_item
        )


        # UNLOCK BUTTON

        self.unlock_button = QPushButton(
            "UNLOCK",
            self
        )

        self.unlock_button.setGeometry(
            650,
            110,
            130,
            45
        )

        self.unlock_button.clicked.connect(
            self.unlock_item
        )


        style = """
            QPushButton {
                background-color: white;
                color: black;
                border: 2px solid black;
                border-radius: 10px;
                font-size: 14px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #A8DCF3;
            }
        """

        self.inventory_button.setStyleSheet(
            style
        )

        self.lock_button.setStyleSheet(
            style
        )

        self.unlock_button.setStyleSheet(
            style
        )


    # ========================================================
    # OPEN SHOP
    # ========================================================

    def show_shop(self):

        if self.shop_window is None:

            self.shop_window = AnotherWindow(
                self
            )

        self.shop_window.update_coins()

        self.shop_window.show()

        self.shop_window.raise_()

        self.shop_window.activateWindow()


    # ========================================================
    # OPEN INVENTORY
    # ========================================================

    def show_inventory(self):

        if self.inventory_window is None:

            self.inventory_window = InventoryWindow(
                self
            )

        self.inventory_window.refresh()

        self.inventory_window.show()

        self.inventory_window.raise_()

        self.inventory_window.activateWindow()


    # ========================================================
    # ADD ITEM TO ROOM
    # ========================================================

    def add_room_item(self, item):

        room_item = RoomItem(
            item
        )

        self.scene.addItem(
            room_item
        )

        # Starting position

        room_item.setPos(
            450,
            300
        )

        room_item.setZValue(
            10
        )


    # ========================================================
    # LOCK SELECTED ITEM
    # ========================================================

    def lock_item(self):

        selected = self.scene.selectedItems()

        if not selected:

            QMessageBox.information(
                self,
                "No Item Selected",
                "Select an item first."
            )

            return


        item = selected[0]

        if isinstance(
            item,
            RoomItem
        ):

            item.lock()

            item.setSelected(
                False
            )


    # ========================================================
    # UNLOCK ITEM
    # ========================================================

    def unlock_item(self):

        for item in self.scene.items():

            if isinstance(
                item,
                RoomItem
            ):

                if item.locked:

                    item.unlock()

                    item.setSelected(
                        True
                    )

                    return


        QMessageBox.information(
            self,
            "No Locked Item",
            "There is no locked item."
        )


# ============================================================
# RUN
# ============================================================

app = QApplication(
    sys.argv
)

window = Window()

window.show()

sys.exit(
    app.exec_()
)