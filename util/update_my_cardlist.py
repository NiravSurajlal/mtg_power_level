import json
import os
import shutil

__DEBUG__ = False
__DATA_FOLDER__ = os.path.join('data')

def update_my_cardlist():
    # dict_keys(['artist', 'artistIds', 'availability', 'boosterTypes', 'borderColor', 
    # 'colorIdentity', 'colors', 'convertedManaCost', 'edhrecRank', 'finishes', 'flavorText', 
    # 'foreignData', 'frameVersion', 'hasFoil', 'hasNonFoil', 'identifiers', 'keywords', 
    # 'language', 'layout', 'legalities', 'manaCost', 'manaValue', 'name', 'number', 'originalText', 
    # 'originalType', 'power', 'printings', 'purchaseUrls', 'rarity', 'setCode', 'sourceProducts', 
    # 'subtypes', 'supertypes', 'text', 'toughness', 'type', 'types', 'uuid', 'variations'])

    pth = os.path.join(__DATA_FOLDER__, "AllPrintings.json") 
    with open(pth, encoding='utf-8') as f:
        all_card_data = json.load(f, )

    cardlist = {}
    num = 0
    # card_0 = all_card_data['data']['ALL']['cards'][0]['manaCost']
    for set in all_card_data['data'].keys():
        for card_data in all_card_data['data'][set]['cards']:
            card_name = card_data['name']

            if __DEBUG__:
                num = num + 1

            if num > 5:
                break
            try:
                processing_card = cardlist[card_name]
            except KeyError:
                try:
                    card_colors = card_data['colors']
                except KeyError:
                    card_colors = 'Nan'

                try:
                    card_colorIdentity = card_data['colorIdentity']
                except KeyError:
                    card_colorIdentity = 'Nan'

                try:
                    card_manaCost = card_data['manaCost'] 
                except KeyError:
                    card_manaCost = 'Nan'
                
                try:
                    card_manaValue = card_data['manaValue']
                except KeyError:
                    card_manaValue = 'Nan'
                
                try:
                    card_convertedManaCost = card_data['convertedManaCost']
                except KeyError:
                    card_convertedManaCost = 'Nan'

                try:
                    card_type = card_data['type']
                except KeyError:
                    card_type = 'Nan'
    
                try:
                    card_types = card_data['types']
                except KeyError:
                    card_types = 'Nan'

                try:
                    card_text = card_data['text']
                except KeyError:
                    card_text = 'Nan'

                cardlist[card_name] = {'name':card_name,
                                'colors':card_colors,
                                'colorIdentity':card_colorIdentity,
                                'manaCost': card_manaCost, 
                                'manaValue': card_manaValue,
                                'convertedManaCost':card_convertedManaCost,
                                'type': card_type,
                                'types': card_types,
                                'text': card_text
                                }
            
    my_cardlist_filename = os.path.join(__DATA_FOLDER__, f"my_cardlist")  
    try:     
        pth = f"{my_cardlist_filename}.json"
        with open(pth, encoding='utf-8', mode='x+') as f:
            f.write(json.dump(cardlist, sort_keys=True))
    except FileExistsError:
        try:
            my_cardlist_filename2 = f"{my_cardlist_filename}_old"
            os.remove(my_cardlist_filename2+'.json')
        except FileNotFoundError:
            pass
        shutil.copy(f"{my_cardlist_filename}.json",
                    f"{my_cardlist_filename2}.json")
        os.remove(my_cardlist_filename+'.json')
        with open(f"{my_cardlist_filename}.json", encoding='utf-8', mode='x+') as f:
            json.dump(cardlist, f, sort_keys=True)

def check_card_data():
    pth = os.path.join(__DATA_FOLDER__, "AllPrintings.json") 
    with open(pth, encoding='utf-8') as f:
        all_card_data = json.load(f, )

    # card_0 = all_card_data['data']['ALL']['cards'][0]['manaCost']
    for set in all_card_data['data'].keys():
        for card_data in all_card_data['data'][set]['cards']:
            card_name = card_data['name']
            print("Debug Here")

if __name__ == "__main__":
    update_my_cardlist()
    # check_card_data()
    print()
