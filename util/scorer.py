import math

class Scorer:
    def get_card_probability(self, num_unique_cards: int, num_of_card_in_deck: int) -> float:
        return num_of_card_in_deck/num_unique_cards*100

    def get_card_draw_probability_by_cards_drawn(self, cards_drawn: int, num_unique_cards: int, 
                                                 num_of_cards_in_deck: int) -> float:
        
        selecting_num = 1
        # num of ways to choose 1 card of suite card name 
        c = math.comb(selecting_num, num_of_cards_in_deck)
        # num of ways to choose remaining card of suite card name 
        r = math.comb(num_of_cards_in_deck-selecting_num, num_of_cards_in_deck)

        # total number of ways to draw X cards
        num_unique_hands = math.comb(num_unique_cards, cards_drawn)

        # prob of the card being drawn by hand X
        p = c*r/num_of_cards_in_deck

        return p
    
    def prob_of_card_in_starting_hand(self, )
        
