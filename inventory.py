import re

character_inventories = {
    'IRONCLAD': {
        'deck': [
            'Strike_R', 'Strike_R', 'Strike_R', 'Strike_R', 'Strike_R', 
            'Defend_R', 'Defend_R', 'Defend_R', 'Defend_R', 'Defend_R', 
            'Bash'
        ],
        'relics': ['Burning Blood'],
    }
}

class Inventory:

    def __init__(self, character, asc):
        if character not in character_inventories:
            print("Character not supported: " + character)
        self.deck = character_inventories[character]['deck'].copy()
        self.relics = character_inventories[character]['relics'].copy()
        if asc >= 10:
            self.add_card("AscendersBane")

    def add_relic(self, item):
        self.relics.append(item)

    def remove_relic(self, item):
        if item in self.relics:
            self.relics.remove(item)
        else:
            print('relic not found: ', item)

    def add_card(self, item):
        self.deck.append(item)

    def remove_card(self, item):
        if item in self.deck:
            self.deck.remove(item)
        else:
            print('card not found (remove): ', item)

    def upgrade_card(self, item):
        if item in self.deck:
            newitem = self.__get_upgrade(item)
            self.deck.remove(item)
            self.deck.append(newitem)
        else:
            print('card not found (upgrade): ', item)

    def __get_upgrade(self, item):
        m = re.match(r'([^+]+)(\+(\d+))?', item)
        if m.group(2) is None:
            newname = m.group(1) + "+1"
        else:
            newname = m.group(1) + "+" + str(int(m.group(3)) + 1)
        return newname

    def export(self):
        return {
            'deck': self.deck.copy(),
            'relics': self.relics.copy(),
        }

def reconstruct_inventory_states(run, allcards, allrelics):
    """reconstruct floor-by-floor inventory states when given a record from the slay the spire data dump"""
    floors = range(0, run['floor_reached'] + 1)
    actions = {}

    # first step: reconstruct all actions performed on the player's inventory
    for floor in floors:
        actions[floor] = []

    # items_purchased
    for idx, floor in enumerate(run['item_purchase_floors']):
        item = run['items_purchased'][idx]
        if item in allcards:
            action = 'addCard'
        elif item in allrelics:
            action = 'addRelic'
        else:
            continue
        actions[floor].append({
            'type': action,
            'name': item,
            'context': 'purchase',
        })

    # card_choices
    for choice in run['card_choices']:
        if choice['picked'] == 'SKIP':
            continue
        if choice['picked'] == 'Singing Bowl':
            continue
        actions[choice['floor']].append({
            'type': 'addCard',
            'name': choice['picked'],
            'context': 'pick',
        })

    # relics_obtained
    for e in run['relics_obtained']:
        actions[e['floor']].append({
            'type': 'addRelic',
            'name': e['key'],
            'context': 'relic_obtained',
        })

    # items_purged
    for idx, floor in enumerate(run['items_purged_floors']):
        item = run['items_purged'][idx]
        if item in allcards:
            action = 'removeCard'
        if item in allrelics:
            action = 'removeRelic'
        actions[floor].append({
            'type': action,
            'name': item,
            'context': 'purge',
        })

    # campfire_choices
    for choice in run['campfire_choices']:
        if choice['key'] == 'SMITH':
            action = {
                'type': 'upgradeCard',
                'name': choice['data'],
                'context': 'campfire',
            }
        elif choice['key'] == 'PURGE':
            action = {
                'type': 'removeCard',
                'name': choice['data'],
                'context': 'campfire',
            }
        else:
            continue
        actions[choice['floor']].append(action)

    # events
    for e in run['event_choices']:
        fe = actions[e['floor']]
        # when a card's tranformed, the old is in cards_transformed, the new is in cards_obtained
        if 'cards_transformed' in e:
            for item in e['cards_transformed']:
                fe.append({
                    'type': 'removeCard',
                    'name': item,
                    'context': 'event_transform_card',
                })
        if 'cards_removed' in e:
            for item in e['cards_removed']:
                fe.append({
                    'type': 'removeCard',
                    'name': item,
                    'context': 'event_remove_card',
                })
        if 'cards_upgraded' in e:
            for item in e['cards_upgraded']:
                fe.append({
                    'type': 'upgradeCard',
                    'name': item,
                    'context': 'event_upgrade_card',
                })
        if 'cards_obtained' in e:
            for item in e['cards_obtained']:
                fe.append({
                    'type': 'addCard',
                    'name': item,
                    'context': 'event_obtain_card',
                })
        if 'relics_lost' in e:
            for item in e['relics_lost']:
                fe.append({
                    'type': 'removeRelic',
                    'name': item,
                    'context': 'event_lost_relic',
                })
        if 'relics_obtained' in e:
            for item in e['relics_obtained']:
                fe.append({
                    'type': 'addRelic',
                    'name': item,
                    'context': 'event_obtain_relic',
                })

    # next step: replay all inventory changes floor-by-floor
    inventory_states = {}
    inv = Inventory('IRONCLAD', asc=run['ascension_level'])

    for floor in floors:
        
        # snapshot current state
        inventory_states[floor] = {
            "floor_reached": run["floor_reached"],
            "ascension_level": run["ascension_level"],
            "character_chosen": run["character_chosen"],
            "play_id": run["play_id"],
            "floor": floor,
            "inventory": inv.export(),
        }

        if floor not in actions or not actions[floor]:
            continue

        # apply changes
        action_list = actions[floor]
        for action in action_list:
            try:
                if action['type'] == 'addCard':
                    inv.add_card(action['name'])
                elif action['type'] == 'removeCard':
                    inv.remove_card(action['name'])
                elif action['type'] == 'upgradeCard':
                    inv.upgrade_card(action['name'])
                elif action['type'] == 'addRelic':
                    inv.add_relic(action['name'])
                elif action['type'] == 'removeRelic':
                    inv.remove_relic(action['name'])
                else:
                    print("OOPS... action not found: ", action['type'])
            except:
                print("exception. action:", action)

    return inventory_states