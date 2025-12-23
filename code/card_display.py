from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer
from PyQt6.QtGui import QPixmap
import os

class CardDisplay:
    def __init__(self, card_back_style="cardBack_red2.png"):
        self.card_back_style = card_back_style
        # Store animations to prevent garbage collection
        self._animations = []


    def get_card_image_path(self, card_text):
        # Convert card text like 'A♠' to image filename like 'cardSpadesA.png'
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
        # Remove all widgets and spacers from a layout
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                if item.widget():
                    widget = item.widget()
                    widget.setParent(None)
                    widget.deleteLater()
                elif item.layout():
                    self.clear_layout(item.layout())
    
    def add_card(self, layout, card_text, animate=True):
        # Create a QLabel showing the card image and add it to the chosen layout.
        label = QLabel()
        label.setObjectName("cardLabel")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Load the card image
        card_path = self.get_card_image_path(card_text)
        pixmap = QPixmap(card_path)
        if not pixmap.isNull():
            # Scale the card to 85% of original size
            scaled_pixmap = pixmap.scaled(
                int(pixmap.width() * 0.85), 
                int(pixmap.height() * 0.85),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            label.setPixmap(scaled_pixmap)
        else:
            # Fallback to text if image not found
            label.setText(card_text)
        
        layout.addWidget(label)
        label.setProperty("card", True)
        
        # Ensure label is visible first
        label.show()
        
        # Animate the card if requested
        if animate:
            # Use a small delay to ensure widget is laid out before animating
            QTimer.singleShot(10, lambda: self.animate_card_deal(label))
        else:
            # Without animation, ensure it's fully visible
            label.setStyleSheet("")  # Clear any opacity effects
        
        return label
    
    def animate_card_deal(self, label):
        # Animate card being dealt: fade in
        from PyQt6.QtWidgets import QGraphicsOpacityEffect
        
        # Ensure label is visible and has a parent
        if label.parent() is None:
            return  # Can't animate without parent
        
        label.show()
        
        opacity_effect = QGraphicsOpacityEffect(label)
        label.setGraphicsEffect(opacity_effect)
        
        # Set initial state: transparent
        opacity_effect.setOpacity(0.0)
        
        # Create opacity animation
        opacity_anim = QPropertyAnimation(opacity_effect, b"opacity")
        opacity_anim.setDuration(400)
        opacity_anim.setStartValue(0.0)
        opacity_anim.setEndValue(1.0)
        opacity_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        # Store animation to prevent garbage collection
        self._animations.append(opacity_anim)
        
        # Clean up old animations (keep only last 10)
        if len(self._animations) > 10:
            self._animations.pop(0)
        
        # Safety fallback: ensure card is visible after animation duration
        def ensure_visible():
            if opacity_effect.opacity() < 0.1:
                opacity_effect.setOpacity(1.0)
        
        QTimer.singleShot(500, ensure_visible)
        
        # Start the animation
        opacity_anim.start()
    
    def animate_card_flip(self, label, new_card_text):
        # Animate card being flipped: opacity fade out, change image, fade in
        from PyQt6.QtWidgets import QGraphicsOpacityEffect
        
        if label.parent() is None:
            return  # Can't animate without parent
        
        opacity_effect = label.graphicsEffect()
        if opacity_effect is None:
            opacity_effect = QGraphicsOpacityEffect(label)
            label.setGraphicsEffect(opacity_effect)
            opacity_effect.setOpacity(1.0)
        
        # Fade out
        fade_out = QPropertyAnimation(opacity_effect, b"opacity")
        fade_out.setDuration(150)
        fade_out.setStartValue(1.0)
        fade_out.setEndValue(0.0)
        fade_out.setEasingCurve(QEasingCurve.Type.InQuad)
        
        # Change card image when fade out completes
        def change_card_image():
            card_path = self.get_card_image_path(new_card_text)
            pixmap = QPixmap(card_path)
            if not pixmap.isNull():
                # Scale the card to 85% of original size
                scaled_pixmap = pixmap.scaled(
                    int(pixmap.width() * 0.85), 
                    int(pixmap.height() * 0.85),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                label.setPixmap(scaled_pixmap)
            else:
                label.setText(new_card_text)
        
        # Fade in
        fade_in = QPropertyAnimation(opacity_effect, b"opacity")
        fade_in.setDuration(150)
        fade_in.setStartValue(0.0)
        fade_in.setEndValue(1.0)
        fade_in.setEasingCurve(QEasingCurve.Type.OutQuad)
        
        # Store animations to prevent garbage collection
        self._animations.append(fade_out)
        self._animations.append(fade_in)
        
        # Chain animations
        fade_out.finished.connect(change_card_image)
        fade_out.finished.connect(fade_in.start)
        
        # Start the animation
        fade_out.start()
    
    def set_card_back_style(self, card_back_file):
        # Change the card back style
        self.card_back_style = card_back_file
