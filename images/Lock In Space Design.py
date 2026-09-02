import sys
import os


#BASED_DIR = os.part.dirname(os.path.abspath(__file__))

##def resource_path(path):
#    return os.path.join(BASED_DIR, path)

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
    QToolTip
)

from PyQt5.QtGui import (
    QPixmap,
    QIcon,
    QFont,
    QFontDatabase
)

from PyQt5.QtCore import (
    QSize,
    Qt
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)



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
        # ====================================================

        self.setStyleSheet("""
            QDialog {
                background-color: #a3cfe6;
            }

            QLabel {
                color: Black;
            }

            QPushButton {
                font-family: Arial;
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
        # ====================================================

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
            "items/coins.png"
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


        coin_text = QLabel(
            "200"
        )


        font_id = QFontDatabase.addApplicationFont(
            "Cave-Story.ttf"
        )


        if font_id != -1:

            font_family = QFontDatabase.applicationFontFamilies(
                font_id
            )[0]

            coin_text.setFont(
                QFont(
                    font_family,
                    30
                )
            )


        coin_layout.addWidget(
            coin_image
        )

        coin_layout.addWidget(
            coin_text
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
            "items/diamonds.png"
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
            "sidebar/E1.png",
            "sidebar/E2.png",
            "sidebar/E3.png",
            "sidebar/E4.png",
            "sidebar/E5.png",
            "sidebar/E6.png"
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
        # ====================================================

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


    # ========================================================
    # CREATE ITEM
    # ========================================================

    def create_item(
        self,
        name,
        image,
        price
    ):

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
        # =================================================

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
        # =================================================

        price_layout = QHBoxLayout()


        price_layout.setAlignment(
            Qt.AlignCenter
        )


        price_layout.setSpacing(
            5
        )


        # -------------------------------------------------
        # COIN IMAGE
        # -------------------------------------------------

        price_image = QLabel()


        price_pixmap = QPixmap(
            "coins.png"
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
        # =================================================

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


        card_layout.addWidget(
            buy_button
        )


        card.setLayout(
            card_layout
        )


        return card


    # ========================================================
    # SHOW CATEGORY
    # ========================================================

    def show_category(
        self,
        category
    ):

        # ====================================================
        # REMOVE CURRENT ITEMS
        # ====================================================

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
                    "characters/C1.png",
                    1000
                ),

                (
                    "Haikal",
                    "characters/C2.png",
                    500
                ),

                (
                    "Khaled",
                    "characters/CCC3.png",
                    1000
                ),

                (
                    "Coco",
                    "characters/C4.png",
                    500
                ),

                (
                    "Sean",
                    "characters/C6.png",
                    1000
                ),

                (
                    "Siew Che",
                    "characters/C5.png",
                    500
                ),

                (
                    "Dani",
                    "characters/C7.png",
                    500
                ),

                (
                    "Ida",
                    "characters/C8.png",
                    500
                )

            ]


        # ====================================================
        # WALLPAPER
        # ====================================================

        elif category == "wallpaper":

            items = [

                (
                    "Aesthethic",
                    "background.png",
                    1000
                ),

                (
                    "Pink Wallpaper",
                    "W2.png",
                    1200
                ),

                (
                    "Night Wallpaper",
                    "W3.png",
                    1500
                ),

                (
                    "Cozy Wallpaper",
                    "W4.png",
                    1500
                ),

                (
                    "Modern Wallpaper",
                    "W5.png",
                    1800
                ),

                (
                    "Study Wallpaper",
                    "W6.png",
                    2000
                )

            ]

        # ====================================================
        # Pets
        # ====================================================

        elif category == "pets":

            items = [

                (
                    "Siamese Cat",
                    "pets/cat1.png",
                    1300
                ),

                (
                    "Beagle Dog",
                    "pets/dog1.png",
                    2000
                ),

                (
                    "Yellow Bird",
                    "pets/bird1.png",
                    1500
                ),

                (
                    "Gary",
                    "pets/snail1.png",
                    1500
                ),

                (
                    "Froggy",
                    "pets/frog1.png",
                    1800
                ),

                (
                    "Donald Duck",
                    "pets/duck1.png",
                    2000
                ),

                (
                    "Nemo",
                    "pets/fish1.png",
                    2300
                ),

                (
                    "Rabbit",
                    "pets/rabbit1.png",
                    5000
                )
            ]

        # ======================================================
        # Furniture
        # ======================================================

        elif category == "furniture":

            items = [
            
                (
                    "Book Rack",
                    "furnitures/bookrack.png",
                    1000
                ),

                (
                    "TV",
                    "furnitures/TV.png",
                    2000
                ),

                (
                    "Flower Vase",
                    "furnitures/Vast.png",
                    1000
                ),

                (
                    "Guitar",
                    "furnitures/guitar.png",
                    7000
                ),

                (
                    "Radio",
                    "furnitures/radio.png",
                    1000
                ),

                (
                    "Cat Tree",
                    "furnitures/cattoys.png",
                    500
                )

            ]

        # ======================================================
        # Furniture
        # ======================================================

        elif category == "foods":

            items = [
            
                (
                    "Croissant",
                    "foods/f1.png",
                    1000
                ),

                (
                    "Coffee",
                    "foods/d1.png",
                    500
                ),

                (
                    "Sandwich",
                    "foods/f2.png",
                    1000
                ),

                (
                    "Coca Cola",
                    "foods/d2.png",
                    500
                ),

                (
                    "Doritos",
                    "foods/f3.png",
                    1000
                ),

                (
                    "Strawberry Mojito",
                    "foods/d3.png",
                    500
                ),

                (
                    "Sushi",
                    "foods/f4.png",
                    1000
                ),

                (
                    "Boba Tea",
                    "foods/d4.png",
                    500
                ),

                (
                    "Donut",
                    "foods/f5.png",
                    1000
                ),

                (
                    "Lime Milkshake",
                    "foods/d5.png",
                    500
                ),

                (
                    "Pizza",
                    "foods/f6.png",
                    1000
                ),

                (
                    "Root Beer",
                    "foods/d6.png",
                    500
                ),

                (
                    "Ramen",
                    "foods/f7.png",
                    1000
                ),

                (
                    "Coconut",
                    "foods/d7.png",
                    500
                ),

                (
                    "Spaghetti",
                    "foods/f8.png",
                    1000
                ),

                (
                    "Sundae Ice Cream",
                    "foods/d8.png",
                    500
                ),

                (
                    "Pancake",
                    "foods/f9.png",
                    1000
                ),

                (
                    "Magnum",
                    "foods/d9.png",
                    500
                )

            ]

        # ======================================================
        # Furniture
        # ======================================================

        elif category == "Special":

            items = [
            
                (
                    "HIM",
                    "C1.png",
                    1000
                ),

                (
                    "Rex",
                    "C2.png",
                    500
                ),

                (
                    "Rose",
                    "C1.png",
                    1000
                ),

                (
                    "Dex",
                    "C2.png",
                    500
                ),

                (
                    "LOL",
                    "C1.png",
                    1000
                ),

                (
                    "LOL",
                    "C2.png",
                    500
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


# ============================================================
# MAIN WINDOW
# ============================================================

class Window(QDialog):

    def __init__(self):

        super().__init__()


        self.shop_window = None


        self.setWindowTitle(
            "Lock In Space"
        )


        self.setWindowIcon(
            QIcon(
                "Logos1.png"
            )
        )


        self.setFixedSize(
            QSize(
                1100,
                800
            )
        )


        self.InitWindow()


    # ========================================================
    # MAIN WINDOW SETUP
    # ========================================================

    def InitWindow(self):

        # ====================================================
        # BACKGROUND
        # ====================================================

        self.image = QLabel(
            self
        )


        pixmap = QPixmap(
            "background.png"
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
            1100,
            800
        )


        self.image.lower()


        # ====================================================
        # SHOP BUTTON
        # ====================================================

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
                "Logos2.png"
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
                background-color: rgba(255, 255, 255, 50);
                border-radius: 15px;
            }
        """)


        self.shop_button.clicked.connect(
            self.show_shop
        )


    # ========================================================
    # OPEN SHOP
    # ========================================================

    def show_shop(self):

        if self.shop_window is None:

            self.shop_window = AnotherWindow()


        self.shop_window.show()

        self.shop_window.raise_()

        self.shop_window.activateWindow()


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

