# coding: utf-8

import random
import collections

NO_FOOT, LEFT_FOOT, RIGHT_FOOT = range(3)
NO_SWORD, SWORD_ORG, SWORD_DST = range(3)
NO_TYPE, TYPE_ATTACK, TYPE_DEFENSE = range(3)

DESCENDANT, HORIZONTAL, ASCENDANT = range(3)
FRONT, FRONT_MID, MID, MID_BACK, BACK = range(5)
SHORT, LONG = range(2)
REGULAR, INVERSE = range(2)
ALIGNED, SEMI_ALIGNED, NOT_ALIGNED = range(3)

MAX_DECK_POWER = 0
MAX_DECK_COHESION = 0
MAX_DECK_FACTOR = 0

class Card(object):

    def __init__(self):
        self.feet = [NO_FOOT for i in range(5)]
        self.sword = [NO_SWORD for i in range(5)]
        self.type = NO_TYPE

    def __eq__(self, other):
        return (self.feet == other.feet and
                self.sword == other.sword and
                self.type == other.type)

    def __str__(self):
        foot_texts = ['·', 'L', 'R']
        sword_texts = [' ', 'O', 'X']
        card_type_texts = ['Unknown', 'Attack', 'Defense']
        direction_texts = ['Descendant', 'Horizontal', 'Ascendant']
        position_texts = ['Front', 'Front-Mid', 'Mid', 'Mid-Back', 'Back']
        orientation_texts = ['Regular', 'Inverse']
        length_texts = ['Short', 'Long']
        alignment_texts = ['Total', 'Partial', 'None']
        text = "===============\n"
        text += "Type: %s\n" % card_type_texts[self.type]
        text += "Power: %s\n" % self.power
        text += "---------------\n"
        text += "       %s\n" % foot_texts[self.feet[4]]
        text += "   %s       %s\n" % (
            sword_texts[self.sword[4]],
            sword_texts[self.sword[0]],
        )
        text += " %s           %s\n" % (
            foot_texts[self.feet[3]],
            foot_texts[self.feet[0]],
        )
        text += "\n"
        text += "  %s         %s\n" % (
            sword_texts[self.sword[3]],
            sword_texts[self.sword[1]],
        )
        text += "   %s   %s   %s\n" % (
            foot_texts[self.feet[2]],
            sword_texts[self.sword[2]],
            foot_texts[self.feet[1]],
        )
        text += "---------------\n"
        text += "Sword Dir: %s\n" % direction_texts[self.sword_direction]
        text += "Guard Pos: %s\n" % position_texts[self.guard_position]
        text += "Guard Ori: %s\n" % orientation_texts[self.guard_orientation]
        text += "T. Length: %s\n" % length_texts[self.trajectory_length]
        text += "Alignment: %s\n" % alignment_texts[self.sword_guard_alignment]
        text += "===============\n"
        return text

    def set_auto_values(self):
        self.sword_direction = self._sword_direction()
        self.guard_position = self._guard_position()
        self.trajectory_length = self._trajectory_length()
        self.guard_orientation = self._guard_orientation()
        self.sword_guard_alignment = self._sword_guard_alignment()
        self.power = self._power()

    def _power(self):
        total = 0
        if self.type == TYPE_ATTACK:
            total += 5 - self.guard_position
        else:
            total += self.guard_position + 1
        total += 3 - self.sword_direction
        if self.trajectory_length == LONG: total += 2
        total += 4 - self.sword_guard_alignment * 2
        if self.guard_orientation == REGULAR: total += 3
        return total / 17.0

    def _sword_direction(self):
        if SWORD_ORG in [self.sword[0], self.sword[4]]:
            if SWORD_DST in [self.sword[0], self.sword[4]]: return HORIZONTAL
            else: return DESCENDANT
        elif SWORD_ORG in [self.sword[1], self.sword[3]]:
            if SWORD_DST == self.sword[2]: return DESCENDANT
            elif SWORD_DST in [self.sword[0], self.sword[4]]: return ASCENDANT
            else: return HORIZONTAL
        else: return ASCENDANT

    def _guard_position(self):
        if self.feet[4] != NO_FOOT:
            if self.feet[0] + self.feet[3] != NO_FOOT: return FRONT
            else: return MID
        elif self.feet[0] + self.feet[3] != NO_FOOT:
            if self.feet[1] + self.feet[2] != NO_FOOT: return MID_BACK
            else: return FRONT_MID
        else: return BACK

    def _trajectory_length(self):
        if SWORD_ORG == self.sword[0]:
            if SWORD_DST in [self.sword[1], self.sword[4]]: return SHORT
            else: return LONG
        elif SWORD_ORG == self.sword[1]:
            if SWORD_DST in [self.sword[2], self.sword[0]]: return SHORT
            else: return LONG
        elif SWORD_ORG == self.sword[2]:
            if SWORD_DST in [self.sword[3], self.sword[1]]: return SHORT
            else: return LONG
        elif SWORD_ORG == self.sword[3]:
            if SWORD_DST in [self.sword[4], self.sword[2]]: return SHORT
            else: return LONG
        else:
            if SWORD_DST in [self.sword[0], self.sword[3]]: return SHORT
            else: return LONG

    def _guard_orientation(self):
        if LEFT_FOOT == self.feet[4]:
            if RIGHT_FOOT in [self.feet[0], self.feet[1]]: return REGULAR
            else: return INVERSE
        elif LEFT_FOOT == self.feet[2]:
            if RIGHT_FOOT != self.feet[3]: return REGULAR
            else: return INVERSE
        elif LEFT_FOOT == self.feet[1]:
            if RIGHT_FOOT == self.feet[0]: return REGULAR
            else: return INVERSE
        elif LEFT_FOOT == self.feet[0]: return INVERSE
        else: return REGULAR

    def _sword_guard_alignment(self):
        guard_alignment = self._guard_alignment()
        sword_alignment = self._sword_alignment()
        compatibility = abs(guard_alignment - sword_alignment)
        if compatibility == 0: return ALIGNED
        elif compatibility in [1, 4]: return SEMI_ALIGNED
        else: return NOT_ALIGNED

    def _sword_alignment(self):
        table = [
            [None, 4, 0, 1, 2],
            [4, None, 1, 2, 3],
            [0, 1, None, 3, 4],
            [1, 2, 3, None, 0],
            [2, 3, 4, 0, None],
        ]
        sword_org_index = self.sword.index(SWORD_ORG)
        sword_dst_index = self.sword.index(SWORD_DST)
        return table[sword_org_index][sword_dst_index]

    def _guard_alignment(self):
        table = [
            [None, 0, 1, 2, 3],
            [0, None, 2, 3, 4],
            [1, 2, None, 4, 0],
            [2, 3, 4, None, 1],
            [3, 4, 0, 1, None],
        ]
        left_foot_index = self.feet.index(LEFT_FOOT)
        right_foot_index = self.feet.index(RIGHT_FOOT)
        return table[left_foot_index][right_foot_index]

    def distance_to(self, card):
        distance = 0
        a, b = self, card
        a_left_foot = a.feet.index(LEFT_FOOT)
        a_right_foot = a.feet.index(RIGHT_FOOT)
        a_sword_dst = a.sword.index(SWORD_DST)
        b_left_foot = b.feet.index(LEFT_FOOT)
        b_right_foot = b.feet.index(RIGHT_FOOT)
        b_sword_org = b.sword.index(SWORD_ORG)
        if a_left_foot != b_left_foot: distance += 1
        if a_right_foot != b_right_foot: distance += 1
        if a_sword_dst != b_sword_org: distance += 1
        return distance / 3.0

def get_all_cards():
    all_cards = {TYPE_ATTACK: [], TYPE_DEFENSE: []}
    for type in [TYPE_ATTACK, TYPE_DEFENSE]:
        for left_foot in range(5):
            for right_foot in range(5):
                if left_foot != right_foot:
                    for sword_org in range(5):
                        for sword_dst in range(5):
                            if sword_org != sword_dst:
                                c = Card()
                                c.type = type
                                c.feet[left_foot] = LEFT_FOOT
                                c.feet[right_foot] = RIGHT_FOOT
                                c.sword[sword_org] = SWORD_ORG
                                c.sword[sword_dst] = SWORD_DST
                                c.set_auto_values()
                                all_cards[type].append(c)
    return all_cards

def get_power_mean(deck):
    total = 0
    for card in deck:
        total += card.power
    return float(total) / len(deck)

def get_cohesion(deck):
    feet_count = [0, 0, 0, 0, 0]
    for card in deck:
        for i in range(5):
            if card.feet[i] == RIGHT_FOOT:
                feet_count[i] += 1
            elif card.feet[i] == LEFT_FOOT:
                feet_count[i] -= 1
    feet_count = map(lambda x: x*x, feet_count)
    feet_cohesion = sum(feet_count) / 800.0
    sword_count = [0, 0, 0, 0, 0]
    for card in deck:
        for i in range(5):
            if card.sword[i] == SWORD_ORG:
                sword_count[i] += 1
            elif card.sword[i] == SWORD_DST:
                sword_count[i] -= 1
    sword_count = map(lambda x: abs(x), sword_count)
    sword_cohesion = 1 - sum(sword_count) / 80.0
    return feet_cohesion * sword_cohesion
    # distance = 0
    # for card1 in deck:
    #     for card2 in deck:
    #         distance += card1.distance_to(card2)
    # return 1 - (distance / 400.0)

def get_inverse_cohesion(deck):
    inverted_count = 0
    for card in deck:
        if card.guard_orientation == INVERSE:
            inverted_count += 1
    inverted_cohesion = pow(1 - inverted_count / 20.0, 5)
    return inverted_cohesion

def get_deck_factor(deck):
    global MAX_DECK_POWER, MAX_DECK_COHESION, MAX_DECK_FACTOR
    power = get_power_mean(deck)
    cohesion = get_cohesion(deck)
    inverse = get_inverse_cohesion(deck)
    factor = power * cohesion * inverse
    if power > MAX_DECK_POWER: MAX_DECK_POWER = power
    if cohesion > MAX_DECK_COHESION: MAX_DECK_COHESION = cohesion
    if factor > MAX_DECK_FACTOR: MAX_DECK_FACTOR = factor
    return factor

def get_power_histogram(decks):
    freqs = {
        TYPE_ATTACK: collections.defaultdict(lambda: 0),
        TYPE_DEFENSE: collections.defaultdict(lambda: 0)
    }
    for deck in decks:
        for card in deck[0]:
            freqs[card.type][card] += 1
    freqs[TYPE_ATTACK] = list(freqs[TYPE_ATTACK].iteritems())
    freqs[TYPE_DEFENSE] = list(freqs[TYPE_DEFENSE].iteritems())
    freqs[TYPE_ATTACK].sort(key=lambda x: x[1], reverse=True)
    freqs[TYPE_DEFENSE].sort(key=lambda x: x[1], reverse=True)
    return {
        TYPE_ATTACK: map(lambda x: x[0], freqs[TYPE_ATTACK]),
        TYPE_DEFENSE: map(lambda x: x[0], freqs[TYPE_DEFENSE])
    }

def sort_by_heuristic(cards, make_histogram=True):
    decks = []
    for i in range(100000):
        deck = []
        selected_attacks, selected_defenses = [None], [None]
        attack_index, defense_index = None, None
        for j in range(10):
            while attack_index in selected_attacks:
                attack_index = int(random.random() * len(cards[TYPE_ATTACK]))
            selected_attacks.append(attack_index)
            deck.append(cards[TYPE_ATTACK][attack_index])
            while defense_index in selected_defenses:
                defense_index = int(random.random() * len(cards[TYPE_DEFENSE]))
            selected_defenses.append(defense_index)
            deck.append(cards[TYPE_DEFENSE][defense_index])
        factor = get_deck_factor(deck)
        decks.append((deck, factor))
    decks.sort(key=lambda x: x[1], reverse=True)
    if make_histogram:
        hist = get_power_histogram(decks[:50000])
        return hist
    else: return decks

def crop_card_set(cards, threshold):
    return {
        TYPE_ATTACK: cards[TYPE_ATTACK][:threshold],
        TYPE_DEFENSE: cards[TYPE_DEFENSE][:threshold]
    }

if __name__ == '__main__':
    all_cards = get_all_cards()
    cards1 = sort_by_heuristic(all_cards)
    cards2 = sort_by_heuristic(crop_card_set(cards1, 350))
    cards3 = sort_by_heuristic(crop_card_set(cards2, 300))
    cards4 = sort_by_heuristic(crop_card_set(cards3, 250))
    cards5 = sort_by_heuristic(crop_card_set(cards4, 200))
    cards6 = sort_by_heuristic(crop_card_set(cards5, 150))
    deck = sort_by_heuristic(crop_card_set(cards6, 100), False)[0][0]

    print get_power_mean(deck), MAX_DECK_POWER
    print get_cohesion(deck), MAX_DECK_COHESION
    print get_power_mean(deck) * get_cohesion(deck), MAX_DECK_FACTOR
    for card in deck: print card
    
    # c = Card()
    # c.type = TYPE_ATTACK
    # c.feet[0] = RIGHT_FOOT
    # c.feet[3] = LEFT_FOOT
    # c.sword[1] = SWORD_ORG
    # c.sword[3] = SWORD_DST
    # c.set_auto_values()
    # print c

    # c2 = Card()
    # c2.type = TYPE_ATTACK
    # c2.feet[1] = RIGHT_FOOT
    # c2.feet[4] = LEFT_FOOT
    # c2.sword[1] = SWORD_ORG
    # c2.sword[3] = SWORD_DST
    # c2.set_auto_values()
    # print c2

    # print c.distance_to(c2)