import os
import re
import json
import math

__CARDLIST_LOCATION__ = os.path.join("data", "my_cardlist.json")
__TEST_DECKLIST__ = os.path.join("data", 'decklist_test_old.txt')
class MyDeck:
    def __init__(self) -> None:
        with open(__CARDLIST_LOCATION__, encoding='utf-8') as f:
            self.all_card_data = json.load(f, )
        
        self.decklist: dict = {}
        self.combos: list = []
        self.combo_cards: list = []
        self.colorID: list = []
        self.updated_combo_info: dict = {}
        

    def load_deck_from_file(self, filename=__TEST_DECKLIST__):
        with open(filename, 'r') as f:
            deck = f.read()
        deck_items: list = re.findall(r'(.*?)\n', deck)

        self.decklist, errors = self.__process_deck_items__(deck_items)
        return errors
    
    def __process_deck_items__(self, deck_items: list) -> dict:
        decklist = {}
        errors = []

        for item in deck_items:
            num_name = item.split(' ', 1)
            card_name = num_name[1]
            try:
                decklist[card_name]['number'] = decklist[card_name]['number'] + int(num_name[0])
            except KeyError:
                decklist[card_name] = {}
                decklist[card_name]['number'] = int(num_name[0])
                try:
                    decklist[card_name]['info'] = self.all_card_data[card_name]
                except KeyError:
                    errors.append(f'{card_name} : Cannot be found in database')
        return decklist, errors   
    
    def check_all_combos(self, combos: list, num_cards_drawn=20):
        combos_probability = 0

        self.updated_combo_info = {}
        self.updated_combo_info['general'] = {}

        for combo_cards in combos:
            all_cards_in_deck, combo_color_id, total_cmc = self.check_cards_in_combo(combo_cards)

            if all_cards_in_deck:
                combo_id = f'combo_{len(self.updated_combo_info)}'
                self.updated_combo_info[combo_id] = {}
                
                num_of_cards = len(combo_cards)
                self.updated_combo_info[combo_id]['colorID'] = combo_color_id
                self.updated_combo_info[combo_id]['totalCMC'] = total_cmc
                self.updated_combo_info[combo_id]['numCards'] = num_of_cards

                combos_probability = combos_probability + \
                                     self.get_combo_draw_probability_by_cards_drawn(num_cards_drawn=num_cards_drawn,
                                                                                    combo=combo_cards)
        
        self.updated_combo_info['general']['prob_of_combos'] = combos_probability 
                

    def check_cards_in_combo(self, combo_cards: list) -> tuple:
        all_cards_in_deck = True
        combo_color_id = []
        total_cmc = 0

        for card in combo_cards:
            all_cards_in_deck = self.check_card_in_deck(card)
            combo_color_id = sorted(self.build_combo_color_identity(card, combo_color_id))
            total_cmc = total_cmc + self.decklist[card]['info']['manaValue']
            if not all_cards_in_deck:
                break

        return all_cards_in_deck, combo_color_id, total_cmc

    def check_card_in_deck(self, card) -> bool:
        return True if card in self.decklist.keys() else False
    
    def build_combo_color_identity(self, card: str, combo_color_id: list) -> list:
        card_colors = self.decklist[card]['info']['colors']
        new_color_list = combo_color_id + list(set(card_colors) - set(combo_color_id))
        return new_color_list
    
    def get_card_probability(self, num_unique_cards: int, num_of_card_in_deck: int) -> float:
        return num_of_card_in_deck/num_unique_cards*100        
    
    def get_combo_draw_probability_by_cards_drawn(self, num_cards_drawn: int, combo: list, 
                                                  num_of_cards_in_deck=100) -> float:
        
        num_unique_cards_in_combo = len(combo)
        # total number of ways to draw X cards
        p_of_num_unique_hands = math.comb(num_of_cards_in_deck, num_cards_drawn)
        # total number of ways to choose the remaining cards in the hand (not in combo)
        p_of_rem_cards_in_hand = math.comb(num_of_cards_in_deck-num_unique_cards_in_combo, 
                                           num_cards_drawn-num_unique_cards_in_combo)
        # p of favourable outcomes
        p_favourable = p_of_rem_cards_in_hand/p_of_num_unique_hands

        return p_favourable
    