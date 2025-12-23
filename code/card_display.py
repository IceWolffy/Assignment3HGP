from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
import os

class CardDisplay:
    def __init__(self, card_back_style="cardBack_red2.png"):
        self.card_back_style = card_back_style
    
    def get_card_image_path(self, card_text):
        """Convert card text like 'A♠' to image filename like 'cardSpadesA.png'"""
        if card_text == "??":
            # Use selected card back style
            return os.path.join(os.path.dirname(__file__), "assets", "cards", self.card_back_style)
        
        # Extract rank and suit from card text
        rank = card_text[:-1]  # Everything except last character
        suit_symbol = card_text[-1]  # Last character is the suit
        
        # Map suit symbols to names (capitalized)
        suit_map = {
            '♠': 'Spades',
            '♥': 'Hearts',
            '♦': 'Diamonds',
            '♣': 'Clubs'
        }
        
        suit_name = suit_map.get(suit_symbol, 'Spades')
        
        # New format: cardSpadesA.png, cardHearts10.png, etc.
        filename = f"card{suit_name}{rank}.png"
        return os.path.join(os.path.dirname(__file__), "assets", "cards", filename)
    
    def clear_layout(self, layout):
        """Remove all widgets and spacers from a layout"""
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                if item.widget():
                    widget = item.widget()
                    widget.setParent(None)
                    widget.deleteLater()
                elif item.layout():
                    self.clear_layout(item.layout())
    
    def add_card(self, layout, card_text):
        """Create a QLabel showing the card image and add it to the chosen layout."""
        label = QLabel()
        label.setObjectName("cardLabel")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Load the card image
        card_path = self.get_card_image_path(card_text)
        pixmap = QPixmap(card_path)
        if not pixmap.isNull():
            label.setPixmap(pixmap)
        else:
            # Fallback to text if image not found
            label.setText(card_text)
        
        layout.addWidget(label)
        label.setProperty("card", True)
    
    def set_card_back_style(self, card_back_file):
        """Change the card back style"""
        self.card_back_style = card_back_file
