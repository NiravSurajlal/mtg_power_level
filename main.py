import re
import os
import requests

from util.deck import MyDeck
from sites import cmm_spellbook

__MAKE_API_CALLS__ = False
__OVERWRITE_COMBOS_TXT = False

def update_deck_combos(mydeck: MyDeck) -> int:
    """ This decks takes the deck class (reference) and updates the possible combos.
        It will return a success or error at end, indicating if the deck was updated OK.

    Args:
        mydeck (MyDeck): deck class

    Returns:
        int: success or errors
    """

    for card_name in mydeck.decklist.keys():
        combos_at_start = len(mydeck.combos)

        print(f"Checking: {card_name}")
        if not mydeck.color_id:
            mydeck.color_id = mydeck.all_card_data[card_name]['colorIdentity']
            print(f'ColorID from: {card_name} - {mydeck.color_id}')
        query = cmm_spellbook.CardComboQuery(card_name)

        if __MAKE_API_CALLS__:
            response = requests.get(query.query, timeout=20)
            # here we construct the list of combos + combo cards needed
            # if a card in the deck is already in the combo list, skip it
            # if it is used in more than the current combos additional combos
            # should appear with the subsequent cards
            # will append to MyDeck.combos as a list --> list of lists ( [[], [], [] ...] )
            cmm_spellbook.filter_response(response, mydeck)

        combos_at_end = len(mydeck.combos)
        combos_delta = combos_at_end - combos_at_start
        print(f"Added Combos: {combos_delta}")

    return 0

def load_test_combo_list(mydeck: MyDeck) -> int:
    """_summary_

    Args:
        mydeck (MyDeck): _description_

    Returns:
        int: _description_
    """

    if not mydeck.combos:
        with open(os.path.join('data', 'combos.txt'), 'r', encoding='utf-8') as f:
            cmbs = f.readlines()
        for i, cmb in enumerate(cmbs):
            l1 = re.findall(r"'(.*?)'", cmb)
            l2 = re.findall(r'"(.*?)"', cmb)
            cmbs[i] = l1+l2

        mydeck.combos = cmbs.copy()
    return 0

def update_combos_text_file(mydeck: MyDeck) -> int:
    """_summary_

    Args:
        mydeck (MyDeck): _description_

    Returns:
        int: _description_
    """

    if __OVERWRITE_COMBOS_TXT and __MAKE_API_CALLS__:
        with open(os.path.join('data', 'combos.txt'), 'w+', encoding='utf-8') as f:
            s = str(mydeck.combos).replace('],', ']\n')
            f.write(s)
    return 0

def main():
    """_summary_
    """

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

    update_deck_combos_status = update_deck_combos(mydeck)
    load_test_combo_list_status = load_test_combo_list(mydeck)
    update_combos_text_file_status = update_combos_text_file(mydeck)

    mydeck.check_all_combos(mydeck.combos)
    probs = mydeck.updated_combo_info['general']['prob_of_combos']
    print(f"Prob forcombos in deck: {probs}")

if __name__ == "__main__":

    main()
