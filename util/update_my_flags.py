"""
abc
"""

import os
import json
import re

from ramp_checker import RampChecker

__MY_CARDLIST_LOCATION__ = os.path.join('data', 'my_cardlist.json')
__FLAGS_UPDATE_LOCATION__ = os.path.join('data', 'mtg_defs.json')
__DEBUG__ = True

def check_if_card_is_perm(card_types: list, permenant_types: list) -> bool:
    """Checks if a card is of the permenant type

    Args:
        card_types (list): _description_

    Returns:
        bool: _description_
    """
    for c_type in card_types:
        for perm_type in permenant_types:
            if c_type == perm_type:
                return True
    return False


def update_card_list_flags():
    """ Updates a cards flags to be used by us.
        These will be used to srot and give scores to cards.
    """
    with open(__MY_CARDLIST_LOCATION__, 'r', encoding='utf-8') as f:
        cardlist = json.load(f)

    with open(__FLAGS_UPDATE_LOCATION__, 'r', encoding='utf-8') as f:
        flags_list = json.load(f)

    permanent_types = flags_list['permanent_types']

    for card_name,card_details in cardlist.items():

        if __DEBUG__:
            card_name = 'Undead Warchief'
            # card_name = 'Sol Ring'
            # card_name = 'Gruul Signet'
            card_name = "Kodama's Reach"
            card_details = cardlist[card_name]

        permanent_types_copy = permanent_types.copy()
        permanent_types_copy.remove('Land')
        is_card_perm = check_if_card_is_perm(card_details['types'], permanent_types_copy)

        for json_tag,json_tag_description in flags_list['tags'].items():
            if json_tag == 'ramp':

                # ramp_score = ramp_check(card_details, tag_description,
                #                         is_card_perm)
                r = RampChecker(card_details, json_tag_description, is_card_perm, card_name)
                r.assign_score()
                print(f"Card {card_name} | score {r.avg_ramp_weight}|")

        break

    print('here')

if __name__ == "__main__":
    update_card_list_flags()
