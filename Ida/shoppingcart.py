import os

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
from Ida.inventory import inventory
from PyQt6.QtMultimedia import QSoundEffect

purchased_items = set()

class ShoppingCart(QWidget):
    coins_changed = pyqtSignal(int)

    def __init__(self):

        super().__init__()
        
        self.click_sound = QSoundEffect(self)

        self.click_sound.setSource(
            QUrl.fromLocalFile(os.path.join(BASE_DIR,"Ida","images","audio","clicked.wav")))

        self.click_sound.setVolume(0.3)

        # Shared coin system

        self.setStyleSheet("""
            QPushButton {
                font-family: Cave Story;
            }
        """)
        # ====================================================
        # BACKGROUND IMAGE
        # ====================================================

        self.background = QLabel(self)

        background_path = os.path.join(BASE_DIR,"Ida","images", "Icons","stallbg.jpg")

        background_pixmap = QPixmap(background_path)

        self.background.setPixmap(
            background_pixmap
        )

        self.background.setScaledContents(
            True
        )

        self.background.setGeometry(
            self.rect()
        )

        self.background.lower()

        # Sound Effect

        self.coin_sound = QSoundEffect()

        self.coin_sound.setSource(
            QUrl.fromLocalFile(
                os.path.join(
                    BASE_DIR,
                    "Ida",
                    "images",
                    "audio",
                    "purchased.wav"
                )
            )
        )

        # Softer volume
        self.coin_sound.setVolume(0.25)

    
        # ====================================================
        # MAIN LAYOUT
        # ====================================================

        main_layout = QVBoxLayout()

        main_layout.setContentsMargins(
            20,
            20,
            20,
            20
        )

        main_layout.setSpacing(15)


        # ====================================================
        # TOP HEADER

        header = QWidget()

        header.setFixedHeight(
            120
        )

        header.setStyleSheet("""
            QWidget {
                background-color: #d4be9f;
                border-radius: 50px;
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

        top_row.setContentsMargins(
            10,
            5,
            10,
            0
        )

        top_row.setSpacing(10)


        # ----------------------------------------------------
        # LEFT SPACE
        # ----------------------------------------------------

        top_row.addStretch()


        # ----------------------------------------------------
        # TITLE
        # ----------------------------------------------------

        shop_title = QLabel(
            "The Room Store"
        )

        shop_title.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        top_row.setContentsMargins(
            60,
            -5,
            1,
            0
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
                    50
                )
            )

        else:

            shop_title.setFont(
                QFont(
                    "Cave Story",
                    50
                )
            )

        shop_title.setStyleSheet("""
            QLabel {
                color: black;
                background-color: transparent;
            }
        """)


        # ----------------------------------------------------
        # ADD TITLE TO TOP ROW
        # ----------------------------------------------------

        top_row.addWidget(
            shop_title
        )


        # ----------------------------------------------------
        # RIGHT SPACE
        # ----------------------------------------------------

        top_row.addStretch()


        # ----------------------------------------------------
        # CLOSE BUTTON
        # ----------------------------------------------------

        self.close_button = QPushButton(
            "X",
            header
        )

        self.close_button.setGeometry(
            970,
            30,
            55,
            55
        )

        self.close_button.setStyleSheet("""
            QPushButton {
                background-color: #1b4c66;
                border: 3px solid #104059;
                border-radius: 27px;
                font-family: Cave Story;
                font-size: 30px;
                font-weight: bold;
                color: #2c0c38;
                padding: 0px;
            }

            QPushButton:hover {
                background-color: #d979c4;
            }
        """)


        # ----------------------------------------------------
        # X BUTTON POSITION
        # ----------------------------------------------------

        x_container = QWidget()

        x_container.setFixedWidth(20)


        # ----------------------------------------------------
        # ADD TOP ROW TO HEADER
        # ----------------------------------------------------

        header_layout.addLayout(
            top_row
        )
        # ====================================================
        # CURRENCY
        # ====================================================

        currency_layout = QHBoxLayout()

        currency_layout.setAlignment(
            Qt.AlignmentFlag.AlignCenter
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

        coin_pixmap = QPixmap(os.path.join(BASE_DIR, "Ida", "images", "items", "coins.png"))

        coin_path = os.path.join(BASE_DIR, "Ida", "images", "items", "coins.png")

        print("COIN PATH:", coin_path)
        print("EXISTS:", os.path.exists(coin_path))

        coin_pixmap = QPixmap(coin_path)

        print("NULL:", coin_pixmap.isNull())

        if not coin_pixmap.isNull():

            coin_pixmap = coin_pixmap.scaled(
                60,
                50,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )

            coin_image.setPixmap(
                coin_pixmap
            )


        coin_image.setFixedSize(
            55,
            55
        )

        coin_image.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.coins = 0
        self.coin_text = QLabel(str(self.coins))
        



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
        # ADD CURRENCY
        # ====================================================

        currency_layout.addLayout(
            coin_layout
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

        main_layout.addSpacing(
            20
        )

        # ====================================================
        # CONTENT AREA
        # ====================================================

        content = QWidget()
        content.setStyleSheet("""
            QWidget {
                background: transparent;
            }
        """)

        # Background Outside Card Item

        content_layout = QHBoxLayout()

        content_layout.setContentsMargins(
            20,
            20,
            20,
            20
        )

        content_layout.setSpacing(
            60
        )


        # ====================================================
        # LEFT CATEGORY BAR
        # ====================================================

        category_bar = QFrame()
        category_layout = QVBoxLayout()

        #icon position
        category_layout.setContentsMargins(
            30,
            13,
            1,
            100
        )

        category_layout.setSpacing(
            90
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
                    70,
                    70
                )
            )


            button.setFixedSize(
                85,
                85
            )


            button.setStyleSheet("""
                QPushButton {
                    background-color: #d4be9f;
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

                button.setToolTip(
                    "<b>Characters</b><br>"
                    "Find your perfect study buddy and Loked In!!"
                )

                button.clicked.connect(
                    lambda checked=False: self.show_category("characters")
                )

                button.clicked.connect(
                    self.play_click_sound
                )

            elif index == 1:

                button.setToolTip(
                    "<b>Wallpapers</b><br>"
                    "A cozy space to keep you Locked In!!"
                )

                button.clicked.connect(
                    lambda checked=False: self.show_category("wallpaper")
                )

                button.clicked.connect(
                    self.play_click_sound
                )


            elif index == 2:

                button.setToolTip(
                    "<b>Pets</b><br>"
                    "Felling Stressed? Adopt a pet and make your study space feel more alive!!"
                )

                button.clicked.connect(
                    lambda checked=False: self.show_category("pets")
                )

                button.clicked.connect(
                    self.play_click_sound
                )


            elif index == 3:

                button.setToolTip(
                    "<b>Furnitures</b><br>"
                    "Upgrade your room, Upgrade your study vibe!!"
                )

                button.clicked.connect(
                    lambda checked=False: self.show_category("furniture")
                )

                button.clicked.connect(
                    self.play_click_sound
                )


            elif index == 4:

                button.setToolTip(
                    "<b>Foods</b><br>"
                    "Fuel Up!! and Stay Locked In"
                )

                button.clicked.connect(
                    lambda checked=False: self.show_category("foods")
                )

                button.clicked.connect(
                    self.play_click_sound
                )


            elif index == 5:

                button.setToolTip(
                    "<b>Special</b><br>"
                    "Something special to keep you Locked In"
                )

                button.clicked.connect(
                    lambda checked=False: self.show_category("Special")
                )

                button.clicked.connect(
                    self.play_click_sound
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

        scroll_area.setStyleSheet("""
            QScrollArea {
                background: transparent;
                border: none;
            }

            QScrollArea > QWidget > QWidget {
                background: transparent;
            }
        """)

        scroll_area.viewport().setStyleSheet("""
            background: transparent;
            border: none;
        """)

        scroll_area.setWidgetResizable(
            True
        )


        scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )


        scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )


        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }

            QScrollBar:vertical {
                width: 12px;
                background: #61360c;
            }

            QScrollBar::handle:vertical {
                background: #61360c;
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
        print("SHOPPING CART FILE:", __file__)
        print("HAS ITEMS LAYOUT:", hasattr(self, "items_layout"))
        self.show_category("characters")

    def play_click_sound(self):
        self.click_sound.play()    

    def resizeEvent(self, event):

        self.background.setGeometry(
            self.rect()
        )

        self.background.lower()

        super().resizeEvent(event)

    def set_coins(self, coins):
        self.coins = coins
        self.coin_text.setText(str(coins))

    def buy_item(self, name, image, price):

        if self.coins >= price:

            # Deduct coins
            self.coins -= price

            self.coin_text.setText(
                str(self.coins)
            )

            # Add item to inventory
            inventory[name] = {
                "image": image,
                "price": price,
                "category": self.current_category
            }

            purchased_items.add(name)

            # Tell main window about new coin amount
            self.coins_changed.emit(
                self.coins
            )

            self.coin_sound.play()

            QMessageBox.information(
                self,
                "Purchased!",
                f"{name} has been added to your inventory!"
            )

            self.show_category(
                self.current_category
            )

        else:

            QMessageBox.warning(
                self,
                "Not enough coins!",
                "You don't have enough coins."
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

        #Item Box
        card.setStyleSheet("""
            QFrame {
                background-color: #d4be9f;
                border: 3px solid #000000;
                border-radius: 20px;
            }
        """)


        card_layout = QVBoxLayout()


        card_layout.setContentsMargins(
            50,
            8,
            50,
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
            Qt.AlignmentFlag.AlignCenter
        )


        name_label.setFont(
            QFont(
                "Cave Story",
                30,
                QFont.Weight.Bold
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
            Qt.AlignmentFlag.AlignCenter
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
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
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
            Qt.AlignmentFlag.AlignCenter
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
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )


            price_image.setPixmap(
                price_pixmap
            )


        price_image.setFixedSize(
            25,
            25
        )


        price_image.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )


        price_image.setStyleSheet("background-color: transparent; border: none;")

        # PRICE NUMBER

        price_label = QLabel(str(price))
        price_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
        # USE CAVE STORY FONT
        font_id = QFontDatabase.addApplicationFont("Cave-Story.ttf")

        if font_id != -1:

            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]

            price_label.setFont(QFont(font_family,20,QFont.Weight.Bold))
                
        price_label.setStyleSheet("border: none;")
        price_layout.addWidget(price_image)
        price_layout.addWidget(price_label)
        card_layout.addLayout(price_layout)

        # BUY BUTTON
        buy_button = QPushButton("BUY")
        buy_button.setFixedHeight(30)

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
        
        buy_button.clicked.connect(lambda: self.buy_item(name, image, price))
        card_layout.addWidget(buy_button)
        card.setLayout(card_layout)

        return card
  
    # SHOW CATEGORY
    def show_category(self, category):

        self.current_category = category

        # REMOVE CURRENT ITEMS
        while self.items_layout.count():

            layout_item = self.items_layout.takeAt(0)
            widget = layout_item.widget()

            if widget is not None:

                widget.deleteLater()

        # CHARACTERS
 
        if category == "characters":

            items = [

                ("Yeejing","Ida/images/characters/C1.png", 10),

                ("Haikal","Ida/images/characters/C2.png", 10),

                ("Coco","Ida/images/characters/C3.png", 10),

                ("Khaled","Ida/images/characters/C4.png", 30),

                ("Siew Che","Ida/images/characters/C5.png", 30),

                ("Sean","Ida/images/characters/C6.png", 30),

                ("Ida","Ida/images/characters/C8.png", 30),

                ("Dani","Ida/images/characters/C7.png", 30),

                ("Sofia","Ida/images/characters/C9.png", 50),

                ("Rafe","Ida/images/characters/C10.png", 50)

            ]

        # WALLPAPER

        elif category == "wallpaper":

            items = [

                ("Brown Wall","Ida/images/wallpaper/w1.png",2),

                ("Blue Wall","Ida/images/wallpaper/w2.png",5),

                ("Mr.Bean Wall","Ida/images/wallpaper/w3.png",15),

                ("Fantasy Wall","Ida/images/wallpaper/w4.png",15),

                ("Polka Wall","Ida/images/wallpaper/w5.png",20),

                ("Blue Stripz Wall","Ida/images/wallpaper/w6.png",20),

                ("Lullaby Wall","Ida/images/wallpaper/w7.png",20),

                ("Starry Night Wall","Ida/images/wallpaper/w8.png",20),

                ("Sorrow Wall","Ida/images/wallpaper/w9.png",30),

                ("Adventure Time Wall","Ida/images/wallpaper/w10.png",50),

                ("Kachow Wall","Ida/images/wallpaper/w11.png",50),

                ("Modern Wall","Ida/images/wallpaper/w12.png",50)

            ]

        # PETS

        elif category == "pets":

            items = [

                ("Siamese Cat","Ida/images/pets/cat1.png", 10),
        
                ("Beagle Dog","Ida/images/pets/dog1.png", 15),

                ("Yellow Bird","Ida/images/pets/bird1.png", 25),

                ("Gary","Ida/images/pets/snail1.png", 25),

                ("Froggy","Ida/images/pets/frog1.png", 25),

                ("Donald Duck","Ida/images/pets/duck1.png", 30),

                ("Nemo","Ida/images/pets/fish1.png", 30),

                ("Rabbit","Ida/images/pets/rabbit1.png", 30)
                
            ]

        # FURNITURE

        elif category == "furniture":

            items = [
            
                ("Book Rack","Ida/images/furnitures/bookrack.png", 10),

                ("TV","Ida/images/furnitures/TV.png", 10),

                ("Flower Vase","Ida/images/furnitures/Vast.png", 5),
             
                ("Guitar","Ida/images/furnitures/guitar.png", 10),

                ("Radio","Ida/images/furnitures/radio.png", 10),
                
                ("Cat Tree","Ida/images/furnitures/cattoys.png", 15),

                ("Morning Day","Ida/images/furnitures/morning.png", 15),
                 
                ("Night Day","Ida/images/furnitures/night.png", 20),
        
                ("Harry Potter Books","Ida/images/furnitures/hpbook.png", 20)
            ]

        # FOODS
        elif category == "foods":

            items = [
            
                ("Croissant","Ida/images/foods/f1.png", 2),

                ("Coffee","Ida/images/foods/d1.png", 3),

                ("Sandwich","Ida/images/foods/f2.png",1),

                ("Coca Cola","Ida/images/foods/d2.png",5),

                ("Doritos","Ida/images/foods/f3.png",5),

                ("Strawberry Mojito","Ida/images/foods/d3.png",5),

                ("Sushi","Ida/images/foods/f4.png",3),

                ("Boba Tea","Ida/images/foods/d4.png",7),

                ("Donut","Ida/images/foods/f5.png",4),

                ("Lime Milkshake","Ida/images/foods/d5.png",50),

                ("Pizza","Ida/images/foods/f6.png",10),

                ("Root Beer","Ida/images/foods/d6.png",5),

                ("Ramen","Ida/images/foods/f7.png",10),

                ("Coconut","Ida/images/foods/d7.png",5),

                ("Spaghetti","Ida/images/foods/f8.png",4),

                ("Sundae Ice Cream","Ida/images/foods/d8.png",2),

                ("Pancake","Ida/images/foods/f9.png",10),

                ("Magnum","Ida/images/foods/d9.png",10)

            ]

        # SPECIAL ITEMS

        elif category == "Special":

            items = [
            
                ("Statue Fountain","Ida/images/special/sp1.png",50),

                ("THE Flower","Ida/images/special/sp2.png",50),

                ("Meme Poster","Ida/images/special/sp3.png",50),

                ("Fountain","Ida/images/special/sp4.png",50),

                ("Special Frame","Ida/images/special/sp5.png",50),

                ("Wall-E Friends","Ida/images/special/sp6.png",50),

                ("EBWISE","Ida/images/special/sp7.png",40)

            ]

        else:

            items = []

        # ADD ITEMS TO GRID

        grid_index = 0

        for name, image, price in items:

            if name in purchased_items:
                continue

            item = self.create_item(
                name,
                image,
                price
            )

            row = grid_index // 2
            column = grid_index % 2

            self.items_layout.addWidget(
                item,
                row,
                column
            )

            grid_index += 1