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
