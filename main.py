import requests
import re
import os

from util.deck import MyDeck
import sites.cmm_spellbook as cmm_spellbook

__MAKE_API_CALLS__ = False
__OVERWRITE_COMBOS_TXT = False

def main():

    mydeck = MyDeck()
    # mydeck.decklist will contain {'number': , 'info': {...}}
    # see update_my_cardlist for more info
    errors = mydeck.load_deck_from_file()

    if len(errors) > 0:
        print("--- ERRORS ---")
        for err in errors:
            print(err)
    else:
        print('All cards in deck found in database.')
    print()
    
    for card_name in mydeck.decklist.keys():
        combos_at_start = len(mydeck.combos)

        print(f"Checking: {card_name}")
        if not mydeck.colorID:
            mydeck.colorID = mydeck.all_card_data[card_name]['colorIdentity']
            print(f'ColorID from: {card_name} - {mydeck.colorID}')
        query = cmm_spellbook.CardComboQuery(card_name)

        if __MAKE_API_CALLS__:
            response = requests.get(query.query) 
            # here we construct the list of combos + combo cards needed
            # if a card in the deck is already in the combo list, skip it
            # if it is used in more than the current combos additional combos
            # should appear with the subsequent cards
            # will append to MyDeck.combos as a list --> list of lists ( [[], [], [] ...] )
            cmm_spellbook.filter_response(response, mydeck)
        
        combos_at_end = len(mydeck.combos)
        combos_delta = combos_at_end - combos_at_start
        print(f"Added Combos: {combos_delta}")
    
    if __OVERWRITE_COMBOS_TXT:
        with open(os.path.join('data', 'combos.txt'), 'w+') as f:
            s = str(mydeck.combos).replace('],', ']\n')
            f.write(s)
    
    # loads if 
    if not mydeck.combos:
        with open(os.path.join('data', 'combos.txt'), 'r') as f:
            cmbs = f.readlines()
        for i in range(0, len(cmbs)):
            # THIS WILL NOT WORK if a card has an apostrophe in name
            cmbs[i] = re.findall(r"'(.*?)'", cmbs[i])
        mydeck.combos = cmbs.copy()
    
    mydeck.check_all_combos(mydeck.combos)
    probs = mydeck.updated_combo_info['general']['prob_of_combos']
    print(f"Prob forcombos in deck: {probs}")

if __name__ == "__main__":

    main()
