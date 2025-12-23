from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QPushButton, 
                             QVBoxLayout, QWidget, QGraphicsOpacityEffect)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve
import os

class WelcomeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LUDO - Ready to gamble?")
        self.setGeometry(300, 300, 400, 300)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Add spacing at top
        layout.addStretch()
        
        # Title
        title = QLabel("LUDO")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = title.font()
        font.setPointSize(36)
        font.setBold(True)
        title.setFont(font)
        layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Game of 21")
        subtitle.setObjectName("subtitleLabel")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = subtitle.font()
        font.setPointSize(16)
        subtitle.setFont(font)
        layout.addWidget(subtitle)
        
        layout.addSpacing(40)
        
        # Start Game button
        start_button = QPushButton("Start Game")
        start_button.setObjectName("welcomeButton")
        start_button.setMinimumHeight(50)
        font = start_button.font()
        font.setPointSize(14)
        start_button.setFont(font)
        start_button.clicked.connect(self.start_game)
        layout.addWidget(start_button)
        
        # Add pulsating animation to start button
        self.start_opacity_effect = QGraphicsOpacityEffect()
        start_button.setGraphicsEffect(self.start_opacity_effect)
        self.start_animation = QPropertyAnimation(self.start_opacity_effect, b"opacity")
        self.start_animation.setDuration(3000)
        self.start_animation.setStartValue(0.6)
        self.start_animation.setKeyValueAt(0.5, 1.0)  # Peak at halfway
        self.start_animation.setEndValue(0.6)  # Back to start
        self.start_animation.setEasingCurve(QEasingCurve.Type.InOutSine)
        self.start_animation.setLoopCount(-1)  # Loops forever
        self.start_animation.start()
        
        layout.addSpacing(10)
        
        # Exit Game button
        exit_button = QPushButton("Exit Game")
        exit_button.setObjectName("welcomeButton")
        exit_button.setMinimumHeight(50)
        font = exit_button.font()
        font.setPointSize(14)
        exit_button.setFont(font)
        exit_button.clicked.connect(self.exit_game)
        layout.addWidget(exit_button)
        
        # Add pulsating animation to exit button (slightly offset)
        self.exit_opacity_effect = QGraphicsOpacityEffect()
        exit_button.setGraphicsEffect(self.exit_opacity_effect)
        self.exit_animation = QPropertyAnimation(self.exit_opacity_effect, b"opacity")
        self.exit_animation.setDuration(3000)  # 2 seconds for full cycle
        self.exit_animation.setStartValue(1.0)
        self.exit_animation.setKeyValueAt(0.5, 0.6)  # Dim at halfway
        self.exit_animation.setEndValue(1.0)  # Back to start
        self.exit_animation.setEasingCurve(QEasingCurve.Type.InOutSine)
        self.exit_animation.setLoopCount(-1)  # Loop forever
        self.exit_animation.start()
        
        # Add spacing at bottom
        layout.addStretch()
        
        # Load stylesheet
        self.load_stylesheet()
        
        # Reference to the game window (will be created when start is clicked)
        self.game_window = None
    
    def load_stylesheet(self):
        # Load stylesheet from file
        stylesheet_path = os.path.join(os.path.dirname(__file__), "stylesheet.qss")
        try:
            with open(stylesheet_path, "r") as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print(f"Warning: Stylesheet file not found at {stylesheet_path}")
    
    def start_game(self):
        # Import here to avoid circular dependency
        from main import MainWindow
        
        # Create and show the main game window
        self.game_window = MainWindow()
        self.game_window.show()
        # Close the welcome window
        self.close()
    
    def exit_game(self):
        # Close the application
        QApplication.quit()
