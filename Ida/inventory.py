import os

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

inventory = {}


class InventoryWindow(QWidget):

    item_selected = pyqtSignal(str, str)


    #SEND SIGNAL TO MAIN WINDOW (MOVE ITEM TO WINDOWS)
    def __init__(self, parent=None):

        super().__init__(parent)

        # ====================================================
        # BACKGROUND WALLPAPER
        # ====================================================

        self.background = QLabel(
            self
        )

        self.background.setGeometry(
            0,
            0,
            1100,
            800
        )

        self.background.setPixmap(
            QPixmap(
                os.path.join(
                    BASE_DIR,
                    "Ida",
                    "images",
                    "Icons",
                    "inventorybg.png"
                )
            )
        )

        self.background.setScaledContents(
            True
        )

        self.background.lower()

        self.setStyleSheet("""
                    QPushButton {
                        font-family: Cave Story;
                    }
                """)

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
        # INVENTORY TITLE
        # ----------------------------------------------------

        inventory_title = QLabel(
            "My Inventory"
        )

        inventory_title.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        font_id = QFontDatabase.addApplicationFont(
            "Cave-Story.ttf"
        )

        if font_id != -1:

            font_family = QFontDatabase.applicationFontFamilies(
                font_id
            )[0]

            inventory_title.setFont(
                QFont(
                    font_family,
                    50
                )
            )

        else:

            inventory_title.setFont(
                QFont(
                    "Arial",
                    50
                )
            )

        inventory_title.setStyleSheet("""
            QLabel {
                color: black;
                background-color: transparent;
            }
        """)


        # ----------------------------------------------------
        # ADD TITLE TO TOP ROW
        # ----------------------------------------------------

        top_row.addWidget(
            inventory_title
        )


        # ----------------------------------------------------
        # RIGHT SPACE
        # ----------------------------------------------------

        top_row.addStretch()


        # ----------------------------------------------------
        # CLOSE BUTTON
        # ----------------------------------------------------

        self.close_button = QPushButton(
            "X"
        )

        self.close_button.setFixedSize(
            55,
            55
        )

        self.close_button.setStyleSheet("""
            QPushButton {
                background-color: #c5a979;
                border: 3px solid #a98d5c;
                border-radius: 27px;
                font-size: 30px;
                font-weight: bold;
                color: #2c0c38;
            }

            QPushButton:hover {
                background-color: #d979c4;
            }
        """)




        # ----------------------------------------------------
        # ADD X TO TOP ROW
        # ----------------------------------------------------

        x_layout = QVBoxLayout()

        x_layout.setContentsMargins(
            0,
            3,
            0,
            10
        )

        x_layout.addWidget(
            self.close_button
        )

        top_row.addLayout(
            x_layout
        )


        # ----------------------------------------------------
        # ADD TOP ROW TO HEADER
        # ----------------------------------------------------

        header_layout.addLayout(
            top_row
        )

        header.setLayout(
            header_layout
        )

    

    # =======================================================
    # MAIN LAYOUT (INVENTORY)
    # =======================================================

        main_layout = QVBoxLayout()

        #Position Layout
        main_layout.setContentsMargins(
            20,
            20,
            20,
            20
        )

        main_layout.setSpacing(15)

        main_layout.addWidget(
            header
        )

        self.setLayout(
            main_layout
        )



# ITEMS AREA

        self.items_area = QWidget()

        self.items_area.setStyleSheet("""
            QWidget {
                background-color: transparent;
            }
        """)

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

        scroll_area.setStyleSheet("""
            QScrollArea {
                background-color: transparent;
                border: none;
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

            QScrollArea > QWidget > QWidget {
                background-color: transparent;
            }
        """)

        scroll_area.setWidget(
            self.items_area
        )

        main_layout.addWidget(
            scroll_area
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
                160,
                175
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
                6,
                6,
                6,
                6
            )

            card_layout.setSpacing(
                2
            )


            # NAME

            name_label = QLabel(
                name
            )

            name_label.setAlignment(
                Qt.AlignmentFlag.AlignCenter
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
                135,
                130
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
                    110,
                    110,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation  
                )

                image_button.setIcon(
                    QIcon(pixmap)
                )

                image_button.setIconSize(
                    QSize(
                        110,
                        110
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
                alignment=Qt.AlignmentFlag.AlignCenter
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
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )

            self.setPixmap(pixmap)
        # Make it Move
        self.setFlag(
            QGraphicsItem.GraphicsItemFlag.ItemIsMovable,
            True
        )

        self.setFlag(
            QGraphicsItem.GraphicsItemFlag.ItemIsSelectable,
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
            QGraphicsItem.GraphicsItemFlag.ItemIsMovable,
            False
        )

        self.setFlag(
            QGraphicsItem.GraphicsItemFlag.ItemIsSelectable,
            False
        )

    # Unlock Items
    def unlock(self):

        self.locked = False

        self.setFlag(
            QGraphicsItem.GraphicsItemFlag.ItemIsMovable,
            True
        )

        self.setFlag(
            QGraphicsItem.GraphicsItemFlag.ItemIsSelectable,
            True
        )

    def mousePressEvent(self, event):

        if event.button() == Qt.MouseButton.RightButton:

            self.main_window.return_to_inventory(
                self.item_name,
                self.image
            )

            self.main_window.scene.removeItem(
                self
            )

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