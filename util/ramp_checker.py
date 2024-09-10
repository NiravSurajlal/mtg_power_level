"""_summary_

    Args:
        card_details (dict): _description_
        ramp_checks (dict): _description_
        permanent_types (list): _description_

    Returns:
        float: _description_

    - SolRing - score 2.0
    - Dimir Signet - score 1.12
    """


import re

class RampChecker:
    def __init__ (self, card_details: dict, json_tag_description: dict, \
            is_card_perm: bool, cardname: str):

        self.card_details: dict = card_details
        self.json_tag_description: dict = json_tag_description
        self.is_card_perm: bool = is_card_perm
        self.cardname: str = cardname
        self.avg_ramp_weight: float = 0.0
        self.card_text: str = self.card_details['text']

    def assign_score(self):
        json_text_flags = self.json_tag_description['card_description_flags']


        for flag_desc, normal_M_to_CC in json_text_flags['perm'].items():
            flags_desc_updated =  r'(.*?)'.join(flag_desc.split('&'))
            print(flags_desc_updated)
            if re.search(flags_desc_updated, self.card_text):
                self.__select_ramp_function__(flag_desc)
            # elif True:
            #     print(f"Unchecked ramp text:\n{self.card_text}")

        return 0

    def __select_ramp_function__(self, flag_description):
        match flag_description:
            case "{T}&Add":
                self.tap_to_add()
            case "create&treasure":
                pass
            case "search&land":
                pass
            case "additional&land":
                pass
            case "cost&less":
                self.cost_less()
            case "put&land":
                pass
            case "!when&cast":
                pass
            case "!when&enters|leaves&battelfield":
                pass
            case _:
                print("None to match")

    def tap_to_add(self):
        num_colours = 0
        colour_fixing_total = 0
        taps_for = re.findall(r"{[C, B, U, R, G, W]}", self.card_text)
        mana_to_cc_ratio = len(taps_for)/self.card_details['manaValue']

        for color in ['{B}', '{U}', '{R}', '{G}', '{W}']:
            num_of_coloured_mana = taps_for.count(color)
            if num_of_coloured_mana > 0:
                num_colours = num_colours + 1
            colour_fixing_total = colour_fixing_total + num_of_coloured_mana

        colour_fixing_weight = 1 + num_colours/50 + colour_fixing_total/25

        self.avg_ramp_weight = self.avg_ramp_weight + mana_to_cc_ratio*colour_fixing_weight

    def cost_less(self):
        num_colours = 0
        colour_fixing_total = 0
        mana_reduction_colour = re.findall(r"{[C, B, U, R, G, W]}", self.card_text)
        mana_reduction = re.findall(r"{[0-9]}", self.card_text)


        pass
