"""
abc
"""

import os
import json
import re

__MY_CARDLIST_LOCATION__ = os.path.join('data', 'my_cardlist.json')
__FLAGS_UPDATE_LOCATION__ = os.path.join('data', 'mtg_defs.json')
__DEBUG__ = True

def check_if_card_is_perm(card_types: list, permenant_types: list) -> bool:
    """_summary_

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

def ramp_check(card_details: dict, tag_description: dict, \
    permanent_types: list, cardlist) -> float:
    """_summary_

    Args:
        card_details (dict): _description_
        ramp_checks (dict): _description_
        permanent_types (list): _description_

    Returns:
        float: _description_
    """
    permanent_types.remove('Land')

    if __DEBUG__:
        card_name = 'Undead Warchief'
        card_details = cardlist[card_name]

    text_flags = tag_description['card_description_flags']
    card_text = card_details['text']
    card_perm = check_if_card_is_perm(card_details['types'], permanent_types)

    avg_ramp_weight = 0

    if card_perm:
        for flag_desc, normal_M_to_CC in text_flags['perm'].items():
            flags =  r'(.*?)'.join(flag_desc.split('&'))
            print(flags)
            if re.search(flags, card_text):
                # tap to add
                taps_for = re.findall(r"{[C, B, U, R, G, W]}", card_text)
                mana_to_cc_ratio = len(taps_for)/card_details['manaValue']
                avg_ramp_weight = avg_ramp_weight + mana_to_cc_ratio

            elif re.search(flags, card_text):
                print(f"Unchecked ramp text:\n\t{card_text}")

    else:
        pass

    return 0


def update_card_list_flags():
    """_summary_
    """
    with open(__MY_CARDLIST_LOCATION__, 'r', encoding='utf-8') as f:
        cardlist = json.load(f)

    with open(__FLAGS_UPDATE_LOCATION__, 'r', encoding='utf-8') as f:
        flags_list = json.load(f)

    permanent_types = flags_list['permanent_types']

    for card_name,card_details in cardlist.items():


        for tag,tag_description in flags_list['tags'].items():
            if tag == 'ramp':

                ramp_score = ramp_check(card_details, tag_description,
                                        permanent_types.copy(), cardlist)

    print('here')


if __name__ == "__main__":
    update_card_list_flags()
