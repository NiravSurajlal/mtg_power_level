import re
import html
from urllib.parse import quote_plus
import requests

from util.deck import MyDeck

colour_identies = ['B', 'G', 'R', 'U', 'W']

class CardComboQuery:
    """_summary_
    """
    def __init__(self, cardName) -> None:
        self.cardName: str = cardName
        card_name_enc = quote_plus(cardName)
        q1 = f'card%3A"{card_name_enc}"'
        self.query: str = f'https://commanderspellbook.com/search/?q={q1}'

def filter_response(response: requests.models.Response, mydeck: MyDeck) -> None:
    """_summary_

    Args:
        response (requests.models.Response): _description_
        mydeck (MyDeck): _description_
    """
    all_combos: list = mydeck.combos
    color_id_req: list = mydeck.color_id

    txt = response.text
    ls = txt.split('comboResults_comboResultsWrapper')
    try:
        list_of_combos = ls[1].split('comboResults_comboResult__')[1:]
    except IndexError:
        # No combos found
        return

    for combo in list_of_combos:

        # combo_colours = get_combo_colours(combo)
        # combo_colors_ok = True
        # for c in combo_colours:
        #     if not c in colorID_req:
        #         combo_colors_ok = False
        combo_colors_ok = color_test(combo, color_id_req)
        # cards = re.findall(r'alt=(.*?)/', combo)
        # cards = re.findall(r'alt=("[\w\s]*?")/', combo)
        if combo_colors_ok:
            cards = re.findall(r'alt="(.*?)"', html.unescape(combo))
            cards = [card for card in cards if card != 'Mana Symbol']
            if not cards in all_combos:
                # check if all cards are in decklist, otherwise, do not add
                all_cards_in_deck = True
                for card in cards:
                    all_cards_in_deck = mydeck.check_card_in_deck(card)
                    if not all_cards_in_deck:
                        break
                if all_cards_in_deck:
                    all_combos.append(cards)

def color_test(combo: str, color_id_req: list) -> bool:
    """_summary_

    Args:
        combo (str): _description_
        colorID_req (list): _description_

    Returns:
        bool: _description_
    """
    combo_colours = get_combo_colours(combo)
    combo_colors_ok = True
    for c in combo_colours:
        if not c in color_id_req:
            combo_colors_ok = False
            break
    return combo_colors_ok

def get_combo_colours(s: str) -> list:
    """_summary_

    Args:
        s (str): _description_

    Returns:
        list: _description_
    """
    combo_colours = ''

    colours = re.search(r'Color Identity(.*?)img', s).group(1)

    for letter in colours:
        if letter.isalpha():
            if letter.upper() in colour_identies:
                combo_colours = combo_colours + letter.upper()
    return sorted(combo_colours)
