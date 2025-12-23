import random

class Game21:
    def __init__(self):
        # Start immediately with a fresh round
        self.new_round()

    # ROUND MANAGEMENT

    def new_round(self):
        """
        Prepares for a new round
        Suggested process:
        - Create and shuffle a new deck
        - Reset card pointer
        - Empty both hands
        - Reset whether the dealer's hidden card has been revealed
        """
        self.deck = self.create_deck()
        random.shuffle(self.deck)

        # Instead of removing cards from the deck,
        # we keep an index of the "next card" to deal.
        self.deck_position = 0

        # Hands start empty; cards will be dealt after UI calls deal_initial_cards()
        self.player_hand = []
        self.dealer_hand = []

        # The first dealer card starts hidden until Stand is pressed
        self.dealer_hidden_revealed = False

    def deal_initial_cards(self):
        """
        Deal two cards each to player and dealer.
        """
        self.player_hand = [self.draw_card(), self.draw_card()]
        self.dealer_hand = [self.draw_card(), self.draw_card()]

    # DECK AND CARD DRAWING

    def create_deck(self):
        """
        Create a standard 52-card deck represented as text strings, e.g.:
        'A♠', '10♥', 'K♦'.

        Ranks: A, 2–10, J, Q, K
        Suits: spades, hearts, diamonds, clubs (with unicode symbols)
        """
        ranks = ["A"] + [str(n) for n in range(2, 11)] + ["J", "Q", "K"]
        suits = ["♠", "♥", "♦", "♣"]
        return [f"{rank}{suit}" for rank in ranks for suit in suits]

    def draw_card(self):
        """
        Return the next card in the shuffled deck.
        """
        card = self.deck[self.deck_position]
        self.deck_position += 1
        return card

    # HAND VALUES + ACE HANDLING

    def card_value(self, card):
        """
        Convert a card string into its numeric value.

        Rules:
        - Number cards = their number (2–10)
        - J, Q, K = 10
        - A is normally 11, may later count as 1 if needed
        """
        rank = card[:-1]  # everything except the suit symbol

        if rank in ["J", "Q", "K"]:
            return 10

        if rank == "A":
            return 11  # Initially treat Ace as 11

        # Otherwise it's a number from 2 to 10
        return int(rank)

    def hand_total(self, hand):
        """
        Calculates the best possible total for a hand.
        Aces are counted as 11 unless this would bust the hand,
        in which case they are reduced to 1.

        Suggested Process:
        1. Count all Aces as 11 initially.
        2. If total > 21, subtract 10 for each Ace, so it effectively makes them = 1
        """
        total = 0
        aces = 0
        
        for card in hand:
            value = self.card_value(card)
            total += value
            if card[:-1] == "A":
                aces += 1
        
        # If we bust and have aces, reduce them from 11 to 1
        while total > 21 and aces > 0:
            total -= 10
            aces -= 1
        
        return total

    # PLAYER ACTIONS

    def player_hit(self):
        # Add one card to the player's hand and return it, so the UI can display the card.
        card = self.draw_card()
        self.player_hand.append(card)
        return card

    def player_total(self):
        # Return the player's total.
        return self.hand_total(self.player_hand)

    # DEALER ACTIONS

    def reveal_dealer_card(self):
        # Called when the player presses Stand. After this, the UI should show both dealer cards.
        self.dealer_hidden_revealed = True


    def dealer_total(self):
        # Return the dealer's total.
        return self.hand_total(self.dealer_hand)

    def play_dealer_turn(self):
        # Dealer must hit until their total is 17 or more, then stand.
        while self.dealer_total() < 17:
            card = self.draw_card()
            self.dealer_hand.append(card)
        return self.dealer_hand

    # WINNER DETERMINATION

    def decide_winner(self):
        """
        Decide the outcome of the round.
        Returns text messages:
        - "Player busts. Dealer wins!"
        - "Dealer busts. Player wins!"
        - "Player wins!"
        - "Dealer wins!"
        - "Push (tie)."
        """
        player_total = self.player_total()
        dealer_total = self.dealer_total()
        
        if player_total > 21:
            return "player busts. dealer wins, get better bozo"
        if dealer_total > 21:
            return "dealer busts. player wins, gambling always pays off"
        
        if player_total > dealer_total:
            return "player wins"
        elif dealer_total > player_total:
            return "dealer wins"
        else:
            return "push (tie)"