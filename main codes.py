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
    QToolTip,
    QMessageBox,
    QGraphicsView,
    QGraphicsScene,
    QGraphicsPixmapItem,
    QGraphicsItem
)

from PyQt5.QtCore import (
    QSize,
    Qt,
    pyqtSignal
)

from PyQt5.QtGui import (
    QPixmap,
    QIcon,
    QFont,
    QFontDatabase
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)

# ============================================================
# INVENTORY
# ============================================================

inventory = {}

coins = 2000

# ============================================================
# SHOP WINDOW
# ============================================================

class AnotherWindow(QDialog):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Shopping Cart")
        self.setFixedSize(900, 650)


    
    # ====================================================
    # MAIN WINDOW STYLE
    

        self.setStyleSheet("""
            QDialog {
                background-color: #a3cfe6;
            }

            QLabel {
                color: Black;
            }

            QPushButton {
                font-family: Cave Story;
                font-size: 20%
            }
        """)


        # ====================================================
        # MAIN LAYOUT
        # ====================================================

        main_layout = QVBoxLayout()

        main_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        main_layout.setSpacing(0)


        # ====================================================
        # TOP HEADER

        header = QWidget()

        header.setFixedHeight(
            145
        )

        header.setStyleSheet("""
            QWidget {
                background-color: #aed6eb;
            }
        """)


        header_layout = QVBoxLayout()

        header_layout.setContentsMargins(
            20,
            10,
            20,
            10
        )

        header_layout.setSpacing(0)


        # ====================================================
        # TOP ROW
        # ====================================================

        top_row = QHBoxLayout()


        # ----------------------------------------------------
        # CLOSE BUTTON
        # ----------------------------------------------------

        close_button = QPushButton("x")

        close_button.setFixedSize(
            55,
            55
        )


        # X BUTTON
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #1b4c66;
                border: 3px solid #104059;
                border-radius: 27px;
                font-size: 40px;
                font-weight: bold;
                color: #2c0c38;
            }

            QPushButton:hover {
                background-color: #d979c4;
            }
        """)


        close_button.clicked.connect(
            self.close
        )


        top_row.addWidget(
            close_button
        )


        # ----------------------------------------------------
        # SHOP TITLE
        # ----------------------------------------------------

        shop_title = QLabel(
            "The Room Store"
        )

        shop_title.setAlignment(
            Qt.AlignCenter
        )


        font_id = QFontDatabase.addApplicationFont(
            "Cave-Story.ttf"
        )


        if font_id != -1:

            font_family = QFontDatabase.applicationFontFamilies(
                font_id
            )[0]

            shop_title.setFont(
                QFont(
                    font_family,
                    60
                )
            )


        top_row.addWidget(
            shop_title,
            1
        )


        # Empty space on right

        empty = QLabel()

        empty.setFixedWidth(
            55
        )

        top_row.addWidget(
            empty
        )


        header_layout.addLayout(
            top_row
        )


        # ====================================================
        # CURRENCY
        # ====================================================

        currency_layout = QHBoxLayout()

        currency_layout.setAlignment(
            Qt.AlignCenter
        )

        currency_layout.setSpacing(
            35
        )


        # ====================================================
        # COINS
        # ====================================================

        coin_layout = QHBoxLayout()

        coin_layout.setSpacing(
            5
        )


        coin_image = QLabel()

        coin_pixmap = QPixmap(
            "Ida/images/items/coins.png"
        )


        if not coin_pixmap.isNull():

            coin_pixmap = coin_pixmap.scaled(
                60,
                50,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )

            coin_image.setPixmap(
                coin_pixmap
            )


        coin_image.setFixedSize(
            55,
            55
        )

        coin_image.setAlignment(
            Qt.AlignCenter
        )


        self.coin_text = QLabel(
            "2000"
        )


        font_id = QFontDatabase.addApplicationFont(
            "Cave-Story.ttf"
        )


        if font_id != -1:

            font_family = QFontDatabase.applicationFontFamilies(
                font_id
            )[0]

            self.coin_text.setFont(
                QFont(
                    font_family,
                    30
                )
            )


        coin_layout.addWidget(
            coin_image
        )

        coin_layout.addWidget(
            self.coin_text
        )


        # ====================================================
        # DIAMONDS
        # ====================================================

        gem_layout = QHBoxLayout()

        gem_layout.setSpacing(
            5
        )


        gem_image = QLabel()

        gem_pixmap = QPixmap(
            "Ida/images/items/diamonds.png"
        )


        if not gem_pixmap.isNull():

            gem_pixmap = gem_pixmap.scaled(
                70,
                70,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )

            gem_image.setPixmap(
                gem_pixmap
            )


        gem_image.setFixedSize(
            35,
            35
        )

        gem_image.setAlignment(
            Qt.AlignCenter
        )


        gem_text = QLabel(
            "300"
        )


        font_id = QFontDatabase.addApplicationFont(
            "Cave-Story.ttf"
        )


        if font_id != -1:

            font_family = QFontDatabase.applicationFontFamilies(
                font_id
            )[0]

            gem_text.setFont(
                QFont(
                    font_family,
                    30
                )
            )


        gem_layout.addWidget(
            gem_image
        )

        gem_layout.addWidget(
            gem_text
        )


        # ====================================================
        # ADD CURRENCY
        # ====================================================

        currency_layout.addLayout(
            coin_layout
        )

        currency_layout.addLayout(
            gem_layout
        )


        header_layout.addLayout(
            currency_layout
        )


        header.setLayout(
            header_layout
        )


        main_layout.addWidget(
            header
        )


        # ====================================================
        # CONTENT AREA
        # ====================================================

        content = QWidget()

        content_layout = QHBoxLayout()

        content_layout.setContentsMargins(
            15,
            15,
            15,
            15
        )

        content_layout.setSpacing(
            15
        )


        # ====================================================
        # LEFT CATEGORY BAR
        # ====================================================

        category_bar = QFrame()

        category_bar.setFixedWidth(
            90
        )


        category_bar.setStyleSheet("""
            QFrame {
                background-color: #426a80;
                border-radius: 20px;
            }
        """)


        category_layout = QVBoxLayout()

        category_layout.setContentsMargins(
            12,
            12,
            12,
            12
        )

        category_layout.setSpacing(
            12
        )


        # ====================================================
        # CATEGORY BUTTONS
        # ====================================================

        categories = [
            "Ida/images/sidebar/E1.png",
            "Ida/images/sidebar/E2.png",
            "Ida/images/sidebar/E3.png",
            "Ida/images/sidebar/E4.png",
            "Ida/images/sidebar/E5.png",
            "Ida/images/sidebar/E6.png"
        ]


        for index, icon in enumerate(categories):

            button = QPushButton()


            button.setIcon(
                QIcon(icon)
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


            button.setStyleSheet("""
                QPushButton {
                    background-color: #769db3;
                    border: 2px solid #000000;
                    border-radius: 15px;
                }

                QPushButton:hover {
                    background-color: #c7afb8;
                }

                QPushButton:pressed {
                    background-color: #bd8096;
                }
            """)


        # =================================================
        # CATEGORY CONNECTION SIDE BAR/ HOVER INFORMATION
        # =================================================

            if index == 0:

                button.setToolTip( "<b>Characters</b><br>"
                    "Find your perfect study buddy and Loked In!!"
                )

                button.clicked.connect(
                    lambda checked=False:
                    self.show_category("characters")
                )


            elif index == 1:

                button.setToolTip( "<b>Wallpapers</b><br>"
                    "A cozy space to keep you Locked In!!"
                )

                button.clicked.connect(
                    lambda checked=False:
                    self.show_category("wallpaper")
                )

            elif index == 2:

                button.setToolTip( "<b>Pets</b><br>"
                    "Felling Stressed? Adopt a pet and make your study space feel more alive!!")
                
                button.clicked.connect(
                    lambda checked=False:
                    self.show_category("pets")
                )

            elif index == 3:

                button.setToolTip( "<b>Furnitures</b><br>"
                    "Upgrade your room, Upgrade your study vibe!!"
                )
                        
                button.clicked.connect(
                    lambda checked=False:
                    self.show_category("furniture")
                )

            elif index == 4:

                button.setToolTip( "<b>Foods</b><br>"
                    "Fuel Up!! and Stay Locked In"
                )

                button.clicked.connect(
                    lambda checked=False:
                    self.show_category("foods")
                )

            elif index == 5:

                button.setToolTip( "<b>Special</b><br>"
                    "Something special to keep you Locked In"
                )
                        
                button.clicked.connect(
                    lambda checked=False:
                    self.show_category("Special")
                )

            category_layout.addWidget(
                button
            )


        category_layout.addStretch()


        category_bar.setLayout(
            category_layout
        )


        content_layout.addWidget(
            category_bar
        )


    # ====================================================
    # ITEMS AREA
    # ====================================================

        self.items_area = QWidget()

        self.items_layout = QGridLayout()


        self.items_layout.setContentsMargins(
            5,
            5,
            5,
            5
        )

        self.items_layout.setHorizontalSpacing(
            30
        )

        self.items_layout.setVerticalSpacing(
            15
        )

        self.items_area.setLayout(
            self.items_layout
        )

        # ====================================================
        # SCROLL AREA
        
        scroll_area = QScrollArea()

        scroll_area.setWidgetResizable(
            True
        )


        scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff
        )


        scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarAsNeeded
        )


        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }

            QScrollBar:vertical {
                width: 12px;
                background: #d7e8ef;
            }

            QScrollBar::handle:vertical {
                background: #426a80;
                border-radius: 6px;
                min-height: 30px;
            }

            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)


        scroll_area.setWidget(
            self.items_area
        )


        content_layout.addWidget(
            scroll_area
        )


        # ====================================================
        # CONTENT
        # ====================================================

        content.setLayout(
            content_layout
        )


        main_layout.addWidget(
            content
        )


        self.setLayout(
            main_layout
        )


        # ====================================================
        # SHOW CHARACTERS FIRST
        # ====================================================

        self.show_category(
            "characters"
        )

    def buy_item(self, name, image, price):

        global coins

        if coins >= price:

            coins -= price

            inventory[name] = {
                "image": image,
                "price": price
            }

            self.coin_text.setText(
                str(coins)
            )

            QMessageBox.information(
                self,
                "Purchased!",
                f"{name} has been added to your inventory!"
            )

        else:

            QMessageBox.warning(
                self,
                "Not Enough Coins",
                "You don't have enough coins!!"
            )
    
    # ========================================================
    # CREATE ITEM
    # ========================================================

    def create_item(self, name, image, price):

        card = QFrame()


        card.setFixedSize(
            350,
            225
        )


        card.setStyleSheet("""
            QFrame {
                background-color: #F8F6EE;
                border: 3px solid #555555;
                border-radius: 20px;
            }
        """)


        card_layout = QVBoxLayout()


        card_layout.setContentsMargins(
            10,
            8,
            10,
            8
        )


        card_layout.setSpacing(
            4
        )


    # =================================================
    # ITEM NAME
    # =================================================

        name_label = QLabel(
            name
        )


        name_label.setAlignment(
            Qt.AlignCenter
        )


        name_label.setFont(
            QFont(
                "Cave Story",
                30,
                QFont.Bold
            )
        )


        name_label.setStyleSheet(
            "border: none;"
        )


        card_layout.addWidget(
            name_label
        )

        # =================================================
        # ITEM IMAGE
        
        image_label = QLabel()


        image_label.setAlignment(
            Qt.AlignCenter
        )


        image_label.setStyleSheet(
            "border: none;"
        )


        pixmap = QPixmap(
            image
        )


        if not pixmap.isNull():

            pixmap = pixmap.scaled(
                140,
                130,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )


            image_label.setPixmap(
                pixmap
            )



            image_label.setFont(
                QFont(
                    "Cave Story",
                    40
                )
            )


        card_layout.addWidget(
            image_label
        )


        # =================================================
        # PRICE
        price_layout = QHBoxLayout()


        price_layout.setAlignment(
            Qt.AlignCenter
        )


        price_layout.setSpacing(
            5
        )
        # -------------------------------------------------
        # COIN IMAGE
        
        price_image = QLabel()


        price_pixmap = QPixmap(
            "Ida/images/items/coins.png"
        )


        if not price_pixmap.isNull():

            price_pixmap = price_pixmap.scaled(
                25,
                25,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )


            price_image.setPixmap(
                price_pixmap
            )


        price_image.setFixedSize(
            25,
            25
        )


        price_image.setAlignment(
            Qt.AlignCenter
        )


        price_image.setStyleSheet(
            "background-color: transparent; border: none;"
        )


        # -------------------------------------------------
        # PRICE NUMBER
        # -------------------------------------------------

        price_label = QLabel(
            str(price)
        )


        price_label.setAlignment(
            Qt.AlignCenter
        )


        # Use Cave Story font
        font_id = QFontDatabase.addApplicationFont(
            "Cave-Story.ttf"
        )


        if font_id != -1:

            font_family = QFontDatabase.applicationFontFamilies(
                font_id
            )[0]


            price_label.setFont(
                QFont(
                    font_family,
                    20,
                    QFont.Bold
                )
            )


        price_label.setStyleSheet(
            "border: none;"
        )


        price_layout.addWidget(
            price_image
        )


        price_layout.addWidget(
            price_label
        )


        card_layout.addLayout(
            price_layout
        )


        # =================================================
        # BUY BUTTON
        buy_button = QPushButton(
            "BUY"
        )


        buy_button.setFixedHeight(
            30
        )


    # ONLY BUY USES CAVE STORY
        buy_button.setStyleSheet("""
            QPushButton {
                background-color: #b38897;
                border: 2px solid black;
                border-radius: 12px;

                font-family: "Cave Story";
                font-size: 30px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #A8DCF3;
            }

            QPushButton:pressed {
                background-color: black;
            }
        """)

        
        buy_button.clicked.connect(
            lambda: self.buy_item(name, image, price)
        )

        card_layout.addWidget(
            buy_button
        )


        card.setLayout(
            card_layout
        )


        return card
    # ========================================================
    # SHOW CATEGORY
    def show_category(
        self,
        category
    ):
        # ====================================================
        # REMOVE CURRENT ITEMS
        while self.items_layout.count():

            layout_item = self.items_layout.takeAt(
                0
            )


            widget = layout_item.widget()


            if widget is not None:

                widget.deleteLater()


        # ====================================================
        # CHARACTERS
        # ====================================================

        if category == "characters":

            items = [

                (
                    "Yeejing",
                    "Ida/images/characters/C1.png",
                    20
                ),

                (
                    "Haikal",
                    "Ida/images/characters/C2.png",
                    10
                ),

                (
                    "Khaled",
                    "Ida/images/characters/CCC3.png",
                    10
                ),

                (
                    "Coco",
                    "Ida/images/characters/C4.png",
                    45
                ),

                (
                    "Sean",
                    "Ida/images/characters/C6.png",
                    10
                ),

                (
                    "Siew Che",
                    "Ida/images/characters/C5.png",
                    59
                ),

                (
                    "Dani",
                    "Ida/images/characters/C7.png",
                    50
                ),

                (
                    "Ida",
                    "Ida/images/characters/C8.png",
                    50
                )

            ]


        # ====================================================
        # WALLPAPER
        # ====================================================

        elif category == "wallpaper":

            items = [

                (
                    "Aesthethic",
                    "Ida/images/background.png",
                    10
                ),

                (
                    "Pink Wallpaper",
                    "Ida/images/W2.png",
                    10
                ),

                (
                    "Night Wallpaper",
                    "Ida/images/W3.png",
                    15
                ),

                (
                    "Cozy Wallpaper",
                    "Ida/images/W4.png",
                    15
                ),

                (
                    "Modern Wallpaper",
                    "Ida/images/W5.png",
                    18
                ),

                (
                    "Study Wallpaper",
                    "Ida/images/W6.png",
                    20
                )

            ]

        # ====================================================
        # Pets
        # ====================================================

        elif category == "pets":

            items = [

                (
                    "Siamese Cat",
                    "Ida/images/pets/cat1.png",
                    13
                ),

                (
                    "Beagle Dog",
                    "Ida/images/pets/dog1.png",
                    20
                ),

                (
                    "Yellow Bird",
                    "Ida/images/pets/bird1.png",
                    15
                ),

                (
                    "Gary",
                    "Ida/images/pets/snail1.png",
                    15
                ),

                (
                    "Froggy",
                    "Ida/images/pets/frog1.png",
                    18
                ),

                (
                    "Donald Duck",
                    "Ida/images/pets/duck1.png",
                    20
                ),

                (
                    "Nemo",
                    "Ida/images/pets/fish1.png",
                    23
                ),

                (
                    "Rabbit",
                    "Ida/images/pets/rabbit1.png",
                    50
                )
            ]

        # ======================================================
        # Furniture
        # ======================================================

        elif category == "furniture":

            items = [
            
                (
                    "Ida/Book Rack",
                    "images/furnitures/bookrack.png",
                    10
                ),

                (
                    "TV",
                    "Ida/images/furnitures/TV.png",
                    20
                ),

                (
                    "Flower Vase",
                    "Ida/images/furnitures/Vast.png",
                    10
                ),

                (
                    "Guitar",
                    "Ida/images/furnitures/guitar.png",
                    70
                ),

                (
                    "Radio",
                    "Ida/images/furnitures/radio.png",
                    10
                ),

                (
                    "Cat Tree",
                    "Ida/images/furnitures/cattoys.png",
                    5
                )

            ]

        # ======================================================
        # Furniture
        # ======================================================

        elif category == "foods":

            items = [
            
                (
                    "Croissant",
                    "Ida/images/foods/f1.png",
                    10
                ),

                (
                    "Coffee",
                    "Ida/images/foods/d1.png",
                    50
                ),

                (
                    "Sandwich",
                    "Ida/images/foods/f2.png",
                    1
                ),

                (
                    "Coca Cola",
                    "Ida/images/foods/d2.png",
                    5
                ),

                (
                    "Doritos",
                    "Ida/images/foods/f3.png",
                    1
                ),

                (
                    "Strawberry Mojito",
                    "Ida/images/foods/d3.png",
                    5
                ),

                (
                    "Sushi",
                    "Ida/images/foods/f4.png",
                    3
                ),

                (
                    "Boba Tea",
                    "Ida/images/foods/d4.png",
                    7
                ),

                (
                    "Donut",
                    "Ida/images/foods/f5.png",
                    10
                ),

                (
                    "Lime Milkshake",
                    "Ida/images/foods/d5.png",
                    50
                ),

                (
                    "Pizza",
                    "Ida/images/foods/f6.png",
                    10
                ),

                (
                    "Root Beer",
                    "Ida/images/foods/d6.png",
                    5
                ),

                (
                    "Ramen",
                    "Ida/images/foods/f7.png",
                    10
                ),

                (
                    "Coconut",
                    "Ida/images/foods/d7.png",
                    5
                ),

                (
                    "Spaghetti",
                    "Ida/images/foods/f8.png",
                    4
                ),

                (
                    "Sundae Ice Cream",
                    "Ida/images/foods/d8.png",
                    2
                ),

                (
                    "Pancake",
                    "Ida/images/foods/f9.png",
                    10
                ),

                (
                    "Magnum",
                    "Ida/images/foods/d9.png",
                    500
                )

            ]

        # ======================================================
        # Furniture
        # ======================================================

        elif category == "Special":

            items = [
            
                (
                    "Statue Fountain",
                    "Ida/images/special/sp1.png",
                    10
                ),

                (
                    "THE Flower",
                    "Ida/images/special/sp2.png",
                    50
                ),

                (
                    "Meme Poster",
                    "Ida/images/special/sp3.png",
                    10
                ),

                (
                    "Fountain",
                    "Ida/images/special/sp4.png",
                    50
                ),

                (
                    "Special Frame",
                    "Ida/images/special/sp5.png",
                    10
                ),

                (
                    "Wall-E Friends",
                    "Ida/images/special/sp6.png",
                    50
                )

            ]

        # ====================================================
        # OTHER CATEGORIES
        # ====================================================

        else:

            items = []


        # ====================================================
        # ADD ITEMS TO GRID
        # ====================================================

        for index, (
            name,
            image,
            price
        ) in enumerate(items):


            item = self.create_item(
                name,
                image,
                price
            )


            # 2 items per row

            row = index // 2

            column = index % 2


            self.items_layout.addWidget(
                item,
                row,
                column
            )


        # ====================================================
        # START SCROLLING FROM TOP
        # ====================================================

        self.items_area.adjustSize()

class InventoryWindow(QDialog):

    item_selected = pyqtSignal(str, str)

    #SEND SIGNAL TO MAIN WINDOW (MOVE ITEM TO WINDOWS)
    def __init__(self, parent=None):

        super().__init__(parent)

        self.setWindowTitle( "Inventory"
        )

        self.setFixedSize(900, 650
        )

    # =======================================================
    # MAIN LAYOUT (INVENTORY)
    # =======================================================

        main_layout = QVBoxLayout()

        main_layout.setContentsMargins(
            20,
            20,
            20,
            20
        )

    # TITLE BAR

        title_bar = QFrame()

        title_bar.setFixedHeight(
            80
        )

        title_bar.setStyleSheet("""
            QFrame {
                background-color: #aed6eb;
                border-radius: 15px;
            }
        """)

        # TITLE CONTENT
        title = QLabel(
            "My Inventory"
        )

        title.setAlignment(
            Qt.AlignCenter
        )

        font_id = QFontDatabase.addApplicationFont(
            "Cave-Story.ttf"
        )

        title.setFont(
            QFont(
                "Cave Story",
                60
            )
        )

        title_bar_layout = QVBoxLayout()

        title_bar_layout.addWidget(
            title
        )

        title_bar.setLayout(
            title_bar_layout
        )


        main_layout.addWidget(
            title_bar
        )

# ITEMS AREA

        self.items_area = QWidget()

        self.items_layout = QGridLayout()

        self.items_layout.setSpacing(
            20
        )

        self.items_area.setLayout(
            self.items_layout
        )

    # SCROLL AREA
        scroll_area =QScrollArea()

        scroll_area.setWidgetResizable(
            True
        )

        scroll_area.setWidget(
            self.items_area
        )

        main_layout.addWidget(
            scroll_area
        )

        self.setLayout(
            main_layout
        )

    # BOUGHT ITEM POP-UP 

        self.show_inventory()

    def show_inventory(self):
        # Remove Old Items

        while self.items_layout.count():

            item = self.items_layout.takeAt(0)

            widget = item.widget()

            if widget is not None:
                widget.deleteLater()

    # ADDED BOUGHT ITEMS

        for index, (name, data) in enumerate(
            inventory.items()
        ):

            image = data["image"]

            # ITEM CARD

            item_card = QFrame()

            item_card.setFixedSize(
                180,
                200
            )

        # FOR RESTORE CARD ITEMS
            item_card.setStyleSheet("""
                QFrame {
                    background-color: #F8F6EE;
                    border: 2px solid black;
                    border-radius: 15px;
                }
            """)


            # CARD LAYOUT

            card_layout = QVBoxLayout()

            card_layout.setContentsMargins(
                8,
                8,
                8,
                8
            )

            card_layout.setSpacing(
                5
            )


            # NAME

            name_label = QLabel(
                name
            )

            name_label.setAlignment(
                Qt.AlignCenter
            )

            name_label.setStyleSheet("""
                QLabel {
                    border: none;
                    background: transparent;
                    font-family: "Cave Story";
                    font-size: 22px;
                    font-weight: bold;
                }
            """)

            card_layout.addWidget(
                name_label
            )


            # PICTURE

            image_button = QPushButton()

            image_button.setFixedSize(
                150,
                145
            )

            image_button.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border: none;
                }

                QPushButton:hover {
                    background-color: rgba(170, 220, 243, 80);
                    border-radius: 10px;
                }
            """)

            pixmap = QPixmap(
                image
            )

            if not pixmap.isNull():

                pixmap = pixmap.scaled(
                    120,
                    120,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )

                image_button.setIcon(
                    QIcon(pixmap)
                )

                image_button.setIconSize(
                    QSize(
                        120,
                        120
                    )
                )


            # CLICK IMAGE

            image_button.clicked.connect(
                lambda checked=False,
                item_name=name,
                item_image=image:
                self.put_in_room(
                    item_name,
                    item_image
                )
            )


            card_layout.addWidget(
                image_button,
                alignment=Qt.AlignCenter
            )

            item_card.setLayout(
                card_layout
            )


            # ADD TO GRID

            row = index // 4

            column = index % 4

            self.items_layout.addWidget(
                item_card,
                row,
                column
            )


    def put_in_room(self, name, image):

        # Remove from inventory
        if name in inventory:
            del inventory[name]

        # Send item to main window
        self.item_selected.emit(
            name,
            image
        )

        # Refresh inventory
        self.show_inventory()

        # Close inventory
        self.close()

# ============================================================
# ROOM ITEM

class RoomItem(QGraphicsPixmapItem):

    def __init__(self, name, image, main_window):
        super().__init__()

        self.item_name = name
        self.image = image
        self.main_window = main_window
        pixmap = QPixmap(image)

        if not pixmap.isNull():

            pixmap = pixmap.scaled(
                160,
                160,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )

            self.setPixmap(pixmap)

        self.setFlag(
            QGraphicsItem.ItemIsMovable,
            True
        )

        self.setFlag(
            QGraphicsItem.ItemIsSelectable,
            True
        )

    def wheelEvent(self, event):

        if event.delta() > 0:

            new_scale = self.scale() * 1.1

        else:

            new_scale = self.scale() * 0.9

        new_scale = max(
            0.3,
            min(new_scale, 3.0)
        )

        self.setScale(
            new_scale
        )
        event.accept()

    # ========================================================
    # LOCK / UNLOCK

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

    def mousePressEvent(self, event):

        if event.button() == Qt.RightButton:

            self.put_back_to_inventory()

            event.accept()

            return

        super().mousePressEvent(event)

    # SENDING ITEM BACK TO INVENTORY
    def put_back_to_inventory(self):

        self.main_window.return_to_inventory(
            self.item_name,
            self.image
        )

        self.main_window.scene.removeItem(
            self
        )

# ============================================================
# MAIN WINDOW

class Window(QDialog):

    def __init__(self):

        super().__init__()


        self.shop_window = None

        self.setWindowTitle(
            "Lock In Space"
        )

        self.setWindowIcon(
            QIcon("Ida/images/Icons/officialbg.png")
        )

        self.setFixedSize(
            QSize(1100, 800)
        )

        self.InitWindow()

    # ========================================================
    # MAIN WINDOW SETUP
    

    def InitWindow(self):

        # ====================================================
        # BACKGROUND
        

        self.image = QLabel(
            self
        )


        pixmap = QPixmap(
            "Ida/images/background.png"
        )


        self.image.setPixmap(
            pixmap
        )


        self.image.setScaledContents(
            True
        )


        self.image.setGeometry(
            0,
            0,
            2000,
            800
        )


        self.image.lower()

        # ====================================================
        # ROOM ITEM AREA
        
        self.scene = QGraphicsScene(self)

        self.view = QGraphicsView(
            self.scene,
            self
        )

        self.view.setGeometry(
            0,
            0,
            1100,
            1000
        )

        self.view.setStyleSheet(
            "background: transparent; border: none;"
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

        # ====================================================
        # SHOP BUTTON
        
        self.shop_button = QPushButton(
            self
        )

        #Position Button(W,H,BO.Size)
        self.shop_button.setGeometry(
            850,
            50,
            100,
            100
        )


        self.shop_button.setIcon(
            QIcon("Ida/images/Icons/22.png")
        )

        #Size Button
        self.shop_button.setIconSize(
            QSize(
                200,
                200
            )
        )


        self.shop_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
            }

            QPushButton:hover {
                background-color: rgba(255, 255, 255, 50);
                border-radius: 15px;
            }
        """)


        self.shop_button.clicked.connect(
            self.show_shop
        )

    # =============================================
    # INVENTORY

        self.inventory_button = QPushButton(
            self
        )
        #Position Button(W,H,BO.Size)
        self.inventory_button.setGeometry(
            960,
            50,
            100,
            100
        )

        self.inventory_button.setIcon(
            QIcon(
                "Ida/images/Icons/11.png"
            )
        )
        #Size Button
        self.inventory_button.setIconSize(
            QSize(
                200,
                200
            )
        )

        self.inventory_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
            }

            QPushButton:hover {
                background-color: rgba(255, 255, 255, 50);
                border-radius: 15px;
            }
        """)

        self.inventory_button.clicked.connect(
            self.show_inventory
        )
        
            
    # =============================================
    # OPEN SHOP

    def show_shop(self):

        if self.shop_window is None:
            self.shop_window = AnotherWindow()

        self.shop_window.show()
        self.shop_window.raise_()
        self.shop_window.activateWindow()

    # OPEN INVENTORY

    def show_inventory(self):

        #CALL ITEMS
        if not hasattr(self, "inventory_window") or self.inventory_window is None:

            self.inventory_window = InventoryWindow(self)

            self.inventory_window.item_selected.connect(
                self.add_item_to_room
            )

        self.inventory_window.show_inventory() 

        self.inventory_window.show()
        self.inventory_window.raise_()
        self.inventory_window.activateWindow()

    # ADD ITEM TO ROOM
    def add_item_to_room(self, name, image):

        item = RoomItem(
            name,
            image,
            self
        )

        item.setPos(
            400,
            300
        )

        self.scene.addItem(
            item
        )
    # RETURN ITEM TO INVENTORY
    def return_to_inventory(self, name, image):

        inventory[name] = {
            "image": image
        }

# ============================================================
# RUN

app = QApplication(
    sys.argv
)


window = Window()


window.show()


sys.exit(
    app.exec_()
)