from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QPushButton, 
                             QVBoxLayout, QHBoxLayout, QWidget, QMessageBox, 
                             QDialog, QDialogButtonBox, QMenuBar, QMenu, QGraphicsOpacityEffect)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve
import sys
import os

# this project should use a modular approach - try to keep UI logic and game logic separate
from game_logic import Game21

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
        # Create and show the main game window
        self.game_window = MainWindow()
        self.game_window.show()
        # Close the welcome window
        self.close()
    
    def exit_game(self):
        # Close the application
        QApplication.quit()

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("LUDO")

        # set the windows dimensions
        self.setGeometry(200, 200, 600, 500)

        self.game = Game21()

        self.initUI()
        self.load_stylesheet()

    def initUI(self):
        # Create menu bar
        self.create_menu_bar()
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Dealer Section
        dealer_label = QLabel("Dealer:")
        dealer_label.setObjectName("sectionLabel")
        main_layout.addWidget(dealer_label)
        
        self.dealerCardsLayout = QHBoxLayout()
        dealer_cards_widget = QWidget()
        dealer_cards_widget.setLayout(self.dealerCardsLayout)
        main_layout.addWidget(dealer_cards_widget)
        
        self.dealerTotalLabel = QLabel("Total: 0")
        self.dealerTotalLabel.setObjectName("totalLabel")
        main_layout.addWidget(self.dealerTotalLabel)
        
        main_layout.addSpacing(20)
        
        # Player Section
        player_label = QLabel("Player:")
        player_label.setObjectName("sectionLabel")
        main_layout.addWidget(player_label)
        
        self.playerCardsLayout = QHBoxLayout()
        player_cards_widget = QWidget()
        player_cards_widget.setLayout(self.playerCardsLayout)
        main_layout.addWidget(player_cards_widget)
        
        self.playerTotalLabel = QLabel("Total: 0")
        self.playerTotalLabel.setObjectName("totalLabel")
        main_layout.addWidget(self.playerTotalLabel)
        
        main_layout.addSpacing(20)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.hitButton = QPushButton("HIT ME")
        self.hitButton.setObjectName("actionButton")
        self.hitButton.clicked.connect(self.on_hit)
        button_layout.addWidget(self.hitButton)
        
        self.standButton = QPushButton("Stand :(")
        self.standButton.setObjectName("actionButton")
        self.standButton.clicked.connect(self.on_stand)
        button_layout.addWidget(self.standButton)
        
        self.newRoundButton = QPushButton("NEW ROUND RAHHH")
        self.newRoundButton.setObjectName("newRoundButton")
        self.newRoundButton.clicked.connect(self.on_new_round)
        button_layout.addWidget(self.newRoundButton)
        
        main_layout.addLayout(button_layout)
        
        # Feedback label
        self.feedbackLabel = QLabel("Click 'New Round' to start!")
        self.feedbackLabel.setObjectName("feedbackLabel")
        self.feedbackLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.feedbackLabel)
        
        main_layout.addStretch()
        
        # Initially disable hit and stand buttons until a round starts
        self.hitButton.setEnabled(False)
        self.standButton.setEnabled(False)


    # STYLESHEET
    
    def load_stylesheet(self):
        # Load stylesheet from file
        stylesheet_path = os.path.join(os.path.dirname(__file__), "stylesheet.qss")
        try:
            with open(stylesheet_path, "r") as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print(f"Warning: Stylesheet file not found at {stylesheet_path}")
    
    # MENU BAR
    
    def create_menu_bar(self):
        menubar = self.menuBar()
        
        # Game menu
        game_menu = menubar.addMenu("Game")
        
        main_menu_action = game_menu.addAction("Quit to Main Menu")
        main_menu_action.triggered.connect(self.quit_to_main_menu)
        
        game_menu.addSeparator()
        
        quit_action = game_menu.addAction("Quit")
        quit_action.triggered.connect(self.close)
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        
        rules_action = help_menu.addAction("Rules")
        rules_action.triggered.connect(self.show_rules)
        
        about_action = help_menu.addAction("About")
        about_action.triggered.connect(self.show_about)

    def quit_to_main_menu(self):
        # Close the game window and show the welcome window
        self.welcome_window = WelcomeWindow()
        self.welcome_window.show()
        self.close()

    # Button actions

    def on_hit(self):
        # Player takes a card
        card = self.game.player_hit()
        self.add_card(self.playerCardsLayout, card)
        
        player_total = self.game.player_total()
        self.playerTotalLabel.setText(f"Total: {player_total}")

        if player_total > 21:
            # Player busts - end the round
            self.feedbackLabel.setText("Player busts!")
            self.end_round()
            result = self.game.decide_winner()
            self.show_result_dialog(result)

    def on_stand(self):
        # Player ends turn; dealer reveals their hidden card and plays
        self.game.reveal_dealer_card()
        self.update_dealer_cards(full=True)
        
        # Play dealer's turn
        self.game.play_dealer_turn()
        self.update_dealer_cards(full=True)
        
        dealer_total = self.game.dealer_total()
        self.dealerTotalLabel.setText(f"Total: {dealer_total}")
        
        # Determine winner
        result = self.game.decide_winner()
        self.feedbackLabel.setText(result)
        self.end_round()
        self.show_result_dialog(result)

    def on_new_round(self):
        self.game.new_round()
        self.game.deal_initial_cards()
        self.new_round_setup()

    # HELPER METHODS

    def clear_layout(self, layout):
        # Remove all widgets from a layout
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def add_card(self, layout, card_text):
        # Create a QLabel showing the card value and add it to the chosen layout.
        label = QLabel(card_text)
        label.setObjectName("cardLabel")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        label.setProperty("card", True)

    def update_dealer_cards(self, full=False):
        # Show dealer cards; hide the first card until revealed
        self.clear_layout(self.dealerCardsLayout)

        for i, card in enumerate(self.game.dealer_hand):
            if i == 0 and not full and not self.game.dealer_hidden_revealed:
                self.add_card(self.dealerCardsLayout, "??")   # face-down
            else:
                self.add_card(self.dealerCardsLayout, card)

        # Update dealer total label
        if full or self.game.dealer_hidden_revealed:
            dealer_total = self.game.dealer_total()
            self.dealerTotalLabel.setText(f"Total: {dealer_total}")
        else:
            # Only show the visible card's value
            if len(self.game.dealer_hand) > 1:
                visible_card = self.game.dealer_hand[1]
                visible_value = self.game.card_value(visible_card)
                self.dealerTotalLabel.setText(f"Total: {visible_value} + ?")
            else:
                self.dealerTotalLabel.setText("Total: ?")

    def new_round_setup(self):
        # Prepare a fresh visual layout
        self.clear_layout(self.playerCardsLayout)
        self.clear_layout(self.dealerCardsLayout)
        
        # Update labels (reset dealer and player totals)
        player_total = self.game.player_total()
        self.playerTotalLabel.setText(f"Total: {player_total}")
        
        # Display new cards for dealers and players
        for card in self.game.player_hand:
            self.add_card(self.playerCardsLayout, card)
        
        self.update_dealer_cards(full=False)
        
        # Enable buttons for Stand and Hit
        self.hitButton.setEnabled(True)
        self.standButton.setEnabled(True)
        self.newRoundButton.setEnabled(False)
        self.feedbackLabel.setText("Your turn")

    def end_round(self):
        # Disable button actions after the round ends
        self.hitButton.setEnabled(False)
        self.standButton.setEnabled(False)
        self.newRoundButton.setEnabled(True)
    
    def show_result_dialog(self, result):
        # Dialog box for round result
        dialog = QDialog(self)
        dialog.setWindowTitle("Round Result")
        dialog.setMinimumSize(500, 250)
        
        layout = QVBoxLayout()
        dialog.setLayout(layout)
        
        # Add spacing at top
        layout.addStretch()
        
        # Result text label
        result_label = QLabel(result)
        result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        result_label.setStyleSheet("font-size: 24px; color: #333; font-weight: bold;")
        layout.addWidget(result_label)
        
        # Add spacing in middle
        layout.addStretch()
        
        # Button centered
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        ok_button = QPushButton("OK")
        ok_button.setObjectName("resultButton")
        ok_button.setMinimumSize(150, 50)
        ok_button.clicked.connect(dialog.accept)

        button_layout.addWidget(ok_button)        
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        # Add spacing at bottom
        layout.addSpacing(20)
        
        dialog.exec()
    
    def show_rules(self):
        # Show rules dialog
        dialog = QDialog(self)
        dialog.setWindowTitle("Game Rules")
        dialog.setGeometry(300, 300, 400, 300)
        
        layout = QVBoxLayout()
        dialog.setLayout(layout)
        
        rules_text = QLabel("""
        <h2>Game of 21 (Blackjack) Rules:</h2>
        <ul>
        <li>The goal is to get as close to 21 as possible without going over.</li>
        <li>Face cards (J, Q, K) are worth 10 points.</li>
        <li>Aces are worth 11 points, or 1 point if 11 would cause a bust.</li>
        <li>Number cards are worth their face value.</li>
        <li>Click "Hit" to receive another card.</li>
        <li>Click "Stand" to end your turn and let the dealer play.</li>
        <li>The dealer must hit until they reach 17 or higher.</li>
        <li>If you go over 21, you bust and lose.</li>
        <li>The player closest to 21 without going over wins!</li>
        </ul>
        """)
        rules_text.setWordWrap(True)
        layout.addWidget(rules_text)
        
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        button_box.accepted.connect(dialog.accept)
        layout.addWidget(button_box)
        
        dialog.exec()
    
    def show_about(self):
        # Show about dialog
        QMessageBox.about(self, "About", 
                         "Game of 21 (Blackjack)\n\n"
                         "A classic card game built with PyQt6.\n\n"
                         "Try to beat the dealer!")



if __name__ == '__main__':
    app = QApplication(sys.argv)

    # macOS only fix for icons appearing
    app.setAttribute(Qt.ApplicationAttribute.AA_DontShowIconsInMenus, False)

    # Show welcome window first
    welcome = WelcomeWindow()
    welcome.show()
    sys.exit(app.exec())