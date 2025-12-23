from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QPushButton, 
                             QVBoxLayout, QHBoxLayout, QWidget, QMessageBox, 
                             QDialog, QDialogButtonBox, QMenuBar, QMenu, QGraphicsOpacityEffect, QSlider, QWidgetAction)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QUrl
from PyQt6.QtGui import QPixmap, QFont, QFontDatabase, QAction
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
        self.resize(600, 700)

        # Center the window on screen
        screen = QApplication.primaryScreen().geometry()
        window_geometry = self.frameGeometry()
        center_point = screen.center()
        window_geometry.moveCenter(center_point)
        self.move(window_geometry.topLeft())

        self.game = Game21()
        
        # Initialize card display helper
        self.card_display = CardDisplay()
        
        # Track dealer card labels for flip animation
        self.dealer_card_labels = []
        self.dealer_had_hidden_card = False

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
        
        # Set audio volume to match slider (30%)
        if hasattr(self, 'volume_slider') and self.audio_output:
            slider_value = self.volume_slider.value()
            self.audio_output.setVolume(slider_value / 100.0)

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
        dealer_cards_widget.setMinimumHeight(180)  # Reserve space for cards
        main_layout.addWidget(dealer_cards_widget)
        
        self.dealerTotalLabel = QLabel("Total: 0")
        self.dealerTotalLabel.setObjectName("totalLabel")
        main_layout.addWidget(self.dealerTotalLabel)
        
        main_layout.addSpacing(5)
        
        # Player Section
        player_label = QLabel("Player:")
        player_label.setObjectName("sectionLabel")
        main_layout.addWidget(player_label)
        
        self.playerCardsLayout = QHBoxLayout()
        player_cards_widget = QWidget()
        player_cards_widget.setLayout(self.playerCardsLayout)
        player_cards_widget.setMinimumHeight(180)  # Reserve space for cards
        main_layout.addWidget(player_cards_widget)
        
        self.playerTotalLabel = QLabel("Total: 0")
        self.playerTotalLabel.setObjectName("totalLabel")
        main_layout.addWidget(self.playerTotalLabel)
        
        main_layout.addSpacing(5)
        
        # Feedback label
        self.feedbackLabel = QLabel("Click 'New Round' to start!")
        self.feedbackLabel.setObjectName("feedbackLabel")
        self.feedbackLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.feedbackLabel)
        
        # Add pulsating animation to feedback label
        self.feedback_opacity_effect = QGraphicsOpacityEffect()
        self.feedbackLabel.setGraphicsEffect(self.feedback_opacity_effect)
        self.feedback_animation = QPropertyAnimation(self.feedback_opacity_effect, b"opacity")
        self.feedback_animation.setDuration(3000)
        self.feedback_animation.setStartValue(0.8)
        self.feedback_animation.setKeyValueAt(0.5, 1.0)
        self.feedback_animation.setEndValue(0.8)
        self.feedback_animation.setEasingCurve(QEasingCurve.Type.InOutSine)
        self.feedback_animation.setLoopCount(-1)
        self.feedback_animation.start()
        
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
        
        self.newRoundButton = QPushButton("New round!")
        self.newRoundButton.setObjectName("newRoundButton")
        self.newRoundButton.clicked.connect(self.on_new_round)
        button_layout.addWidget(self.newRoundButton)
        
        main_layout.addLayout(button_layout)
        
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
        
        main_menu_action = game_menu.addAction("Main Menu")
        main_menu_action.triggered.connect(self.quit_to_main_menu)
        
        game_menu.addSeparator()
        
        quit_action = game_menu.addAction("Quit")
        quit_action.setMenuRole(QAction.MenuRole.NoRole)
        quit_action.triggered.connect(self.close)
        
        # Settings menu
        settings_menu = menubar.addMenu("Settings")
        
        # Volume control in settings menu
        volume_widget = QWidget()
        volume_widget.setObjectName("volumeWidget")
        volume_layout = QHBoxLayout()
        volume_layout.setContentsMargins(15, 8, 15, 8)
        volume_layout.setSpacing(8)
        
        volume_label = QLabel("Volume:")
        volume_label.setObjectName("volumeLabel")
        volume_layout.addWidget(volume_label)
        
        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setObjectName("volumeSlider")
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(30)
        self.volume_slider.setFixedWidth(150)
        self.volume_slider.valueChanged.connect(self.update_volume)
        volume_layout.addWidget(self.volume_slider)
        
        self.volume_value_label = QLabel("30%")
        self.volume_value_label.setObjectName("volumeValueLabel")
        volume_layout.addWidget(self.volume_value_label)
        
        volume_widget.setLayout(volume_layout)
        
        volume_action = QWidgetAction(self)
        volume_action.setDefaultWidget(volume_widget)
        settings_menu.addAction(volume_action)
        
        settings_menu.addSeparator()
        
        card_back_menu = settings_menu.addMenu("Back of card color")
        
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
        
        help_menu.addSeparator()
        
        about_action = help_menu.addAction("About")
        about_action.setMenuRole(QAction.MenuRole.NoRole)
        about_action.triggered.connect(self.show_about)

    def update_volume(self, value):
        #convert slider value (0-100) to volume (0.0-1.0)
        volume = value / 100.0
        if self.audio_output:
            self.audio_output.setVolume(volume)
        #update the label
        if hasattr(self, 'volume_value_label'):
            self.volume_value_label.setText(f"{value}%")
    
    def quit_to_main_menu(self):
        #close the game window and show the welcome window with existing music player
        self.welcome_window = WelcomeWindow(music_player=self.music_player, audio_output=self.audio_output)
        self.welcome_window.show()
        self.close()
    
    def change_card_back(self, card_back_file):
        #change the card back style and refresh dealer cards if hidden
        self.card_display.set_card_back_style(card_back_file)
        #refresh the display if there are hidden dealer cards
        if hasattr(self.game, 'dealer_hand') and len(self.game.dealer_hand) > 0:
            if not self.game.dealer_hidden_revealed:
                self.update_dealer_cards(full=False)


    # Button actions

    def on_hit(self):
        # Player takes a card
        card = self.game.player_hit()
        self.card_display.add_card(self.playerCardsLayout, card, animate=True)
        
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
        #show dealer cards, hide the first card until revealed
        # If animate the flip
        should_flip = (full and self.dealer_had_hidden_card and len(self.dealer_card_labels) > 0 and 
                      len(self.game.dealer_hand) > 0)
        
        if should_flip:
            #flip the first card with animation
            first_card_label = self.dealer_card_labels[0]
            actual_card = self.game.dealer_hand[0]
            self.card_display.animate_card_flip(first_card_label, actual_card)
            self.dealer_had_hidden_card = False
            
            #add any new cards that were dealt during dealer's turn
            existing_count = len(self.dealer_card_labels)
            for i in range(existing_count, len(self.game.dealer_hand)):
                card = self.game.dealer_hand[i]
                label = self.card_display.add_card(self.dealerCardsLayout, card, animate=True)
                self.dealer_card_labels.append(label)
        else:
            #clear
            self.card_display.clear_layout(self.dealerCardsLayout)
            self.dealer_card_labels = []

            for i, card in enumerate(self.game.dealer_hand):
                if i == 0 and not full and not self.game.dealer_hidden_revealed:
                    label = self.card_display.add_card(self.dealerCardsLayout, "??", animate=True)   # face-down
                    self.dealer_card_labels.append(label)
                    self.dealer_had_hidden_card = True
                else:
                    label = self.card_display.add_card(self.dealerCardsLayout, card, animate=True)
                    self.dealer_card_labels.append(label)
                    if i == 0:
                        self.dealer_had_hidden_card = False

        #update dealer total label
        if full or self.game.dealer_hidden_revealed:
            dealer_total = self.game.dealer_total()
            self.dealerTotalLabel.setText(f"Total: {dealer_total}")
        else:
            #only show the visible cards value
            if len(self.game.dealer_hand) > 1:
                visible_card = self.game.dealer_hand[1]
                visible_value = self.game.card_value(visible_card)
                self.dealerTotalLabel.setText(f"Total: {visible_value} + ?")
            else:
                self.dealerTotalLabel.setText("Total: ?")

    def new_round_setup(self):
        #new visual layout
        self.card_display.clear_layout(self.playerCardsLayout)
        self.card_display.clear_layout(self.dealerCardsLayout)
        self.dealer_card_labels = []
        self.dealer_had_hidden_card = False
        
        #update labels
        player_total = self.game.player_total()
        self.playerTotalLabel.setText(f"Total: {player_total}")
        
        #display new cards for dealers and players
        for card in self.game.player_hand:
            self.card_display.add_card(self.playerCardsLayout, card, animate=True)
        
        self.update_dealer_cards(full=False)
        
        # Enable buttons for Stand and Hit
        self.hitButton.setEnabled(True)
        self.standButton.setEnabled(True)
        self.newRoundButton.setEnabled(False)
        self.feedback_animation.stop()
        self.feedback_opacity_effect.setOpacity(1.0)
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
        dialog.setFixedSize(600, 450)
        
        # Center the dialog
        screen = QApplication.primaryScreen().geometry()
        dialog_geometry = dialog.frameGeometry()
        center_point = screen.center()
        dialog_geometry.moveCenter(center_point)
        dialog.move(dialog_geometry.topLeft())
        
        layout = QVBoxLayout()
        dialog.setLayout(layout)
        
        rules_text = QLabel("""
        <h2 style='font-size: 20px;'>Game of 21 (Blackjack) Rules:</h2>
        <ul style='font-size: 16px; line-height: 1.6;'>
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
        rules_text.setStyleSheet("padding: 15px; background-color: white; border-radius: 5px;")
        layout.addWidget(rules_text)
        
        ok_button = QPushButton("OK")
        ok_button.setObjectName("resultButton")
        ok_button.setFixedSize(120, 45)
        ok_button.clicked.connect(dialog.accept)
        layout.addWidget(ok_button, alignment=Qt.AlignmentFlag.AlignCenter)
        
        dialog.exec()
    
    def show_about(self):
        # Show about dialog
        dialog = QDialog(self)
        dialog.setWindowTitle("About")
        dialog.setFixedSize(500, 300)
        
        # Center the dialog
        screen = QApplication.primaryScreen().geometry()
        dialog_geometry = dialog.frameGeometry()
        center_point = screen.center()
        dialog_geometry.moveCenter(center_point)
        dialog.move(dialog_geometry.topLeft())
        
        layout = QVBoxLayout()
        dialog.setLayout(layout)
        
        about_text = QLabel(
            "<h2 style='font-size: 24px;'>Game of 21 (Blackjack)</h2>"
            "<p style='font-size: 16px; margin-top: 10px;'>A classic card game built with PyQt6</p>"
            "<p style='font-size: 16px; margin-top: 10px;'>Made by Nichita Chirtoaca and Antonio Madrid</p>"
            "<p style='font-size: 16px;'>Try to beat the dealer!</p>"
        )
        about_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        about_text.setWordWrap(True)
        about_text.setStyleSheet("padding: 30px; background-color: white; border-radius: 5px;")
        layout.addWidget(about_text)
        
        ok_button = QPushButton("OK")
        ok_button.setObjectName("resultButton")
        ok_button.setFixedSize(120, 45)
        ok_button.clicked.connect(dialog.accept)
        layout.addWidget(ok_button, alignment=Qt.AlignmentFlag.AlignCenter)
        
        dialog.exec()



if __name__ == '__main__':
    app = QApplication(sys.argv)

    # macOS only fix for icons appearing
    app.setAttribute(Qt.ApplicationAttribute.AA_DontShowIconsInMenus, False)

    # Show welcome window first
    welcome = WelcomeWindow()
    welcome.show()
    sys.exit(app.exec())