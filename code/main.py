from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QPushButton, 
                             QVBoxLayout, QHBoxLayout, QWidget, QMessageBox, 
                             QDialog, QDialogButtonBox, QMenuBar, QMenu, QGraphicsOpacityEffect)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QUrl
from PyQt6.QtGui import QPixmap
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
import sys
import os

# this project should use a modular approach - try to keep UI logic and game logic separate
from game_logic import Game21
from welcome_window import WelcomeWindow
from music_manager import MusicManager
from card_display import CardDisplay

class MainWindow(QMainWindow):

    def __init__(self, music_player=None, audio_output=None):
        super().__init__()
        self.setWindowTitle("LUDO")

        # Set window size
        self.resize(800, 800)
        
        # Center the window on screen
        screen = QApplication.primaryScreen().geometry()
        window_geometry = self.frameGeometry()
        center_point = screen.center()
        window_geometry.moveCenter(center_point)
        self.move(window_geometry.topLeft())

        self.game = Game21()
        
        # Initialize card display helper
        self.card_display = CardDisplay()

        self.initUI()
        self.load_stylesheet()
        
        # Use existing music manager or create new one
        if music_player and audio_output:
            self.music_player = music_player
            self.audio_output = audio_output
        else:
            music_mgr = MusicManager()
            music_mgr.play()
            self.music_player = music_mgr.get_player()
            self.audio_output = music_mgr.get_audio_output()

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
        
        # Settings menu
        settings_menu = menubar.addMenu("Settings")
        
        card_back_menu = settings_menu.addMenu("Card Back")
        
        # Red card backs
        red_submenu = card_back_menu.addMenu("Red")
        for i in range(1, 6):
            action = red_submenu.addAction(f"Red {i}")
            action.triggered.connect(lambda checked, num=i: self.change_card_back(f"cardBack_red{num}.png"))
        
        # Blue card backs
        blue_submenu = card_back_menu.addMenu("Blue")
        for i in range(1, 6):
            action = blue_submenu.addAction(f"Blue {i}")
            action.triggered.connect(lambda checked, num=i: self.change_card_back(f"cardBack_blue{num}.png"))
        
        # Green card backs
        green_submenu = card_back_menu.addMenu("Green")
        for i in range(1, 6):
            action = green_submenu.addAction(f"Green {i}")
            action.triggered.connect(lambda checked, num=i: self.change_card_back(f"cardBack_green{num}.png"))
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        
        rules_action = help_menu.addAction("Rules")
        rules_action.triggered.connect(self.show_rules)
        
        about_action = help_menu.addAction("About")
        about_action.triggered.connect(self.show_about)

    def quit_to_main_menu(self):
        # Close the game window and show the welcome window with existing music player
        self.welcome_window = WelcomeWindow(music_player=self.music_player, audio_output=self.audio_output)
        self.welcome_window.show()
        self.close()
    
    def change_card_back(self, card_back_file):
        # Change the card back style and refresh dealer cards if hidden
        self.card_display.set_card_back_style(card_back_file)
        # Refresh the display if there are hidden dealer cards
        if hasattr(self.game, 'dealer_hand') and len(self.game.dealer_hand) > 0:
            if not self.game.dealer_hidden_revealed:
                self.update_dealer_cards(full=False)

    # Button actions

    def on_hit(self):
        # Player takes a card
        card = self.game.player_hit()
        self.card_display.add_card(self.playerCardsLayout, card)
        
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
        
        # Play dealer's turn
        self.game.play_dealer_turn()
        
        # Update dealer cards once after dealer finishes playing
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

    def update_dealer_cards(self, full=False):
        # Show dealer cards; hide the first card until revealed
        self.card_display.clear_layout(self.dealerCardsLayout)

        for i, card in enumerate(self.game.dealer_hand):
            if i == 0 and not full and not self.game.dealer_hidden_revealed:
                self.card_display.add_card(self.dealerCardsLayout, "??")   # face-down
            else:
                self.card_display.add_card(self.dealerCardsLayout, card)

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
        self.card_display.clear_layout(self.playerCardsLayout)
        self.card_display.clear_layout(self.dealerCardsLayout)
        
        # Update labels (reset dealer and player totals)
        player_total = self.game.player_total()
        self.playerTotalLabel.setText(f"Total: {player_total}")
        
        # Display new cards for dealers and players
        for card in self.game.player_hand:
            self.card_display.add_card(self.playerCardsLayout, card)
        
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