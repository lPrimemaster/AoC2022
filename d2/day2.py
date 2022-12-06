# A | X - Rock    -> 0
# B | Y - Paper   -> 1
# C | Z - Scissor -> 2

def hand_value(hand: str):
    return ord(hand) - ord('X')

def convert_hand(hand: str):
    return chr(ord('X') - ord('A') + ord(hand))

def round_value(opponent: str, you: str):
    hand1 = hand_value(you)
    hand2 = hand_value(convert_hand(opponent))

    if hand2 == (hand1 - 1) % 3:
        return hand1 + 1 + 6 # Win
    elif hand2 == (hand1 + 1) % 3:
        return hand1 + 1     # Loss
    else:
        return hand1 + 1 + 3 # Draw

def reverse_round_value(opponent: str, wdl: str):
    hand = hand_value(convert_hand(opponent))
    
    if wdl == 'Z':
        return (hand + 1) % 3 + 1 + 6 # Win
    elif wdl == 'Y':
        return hand + 1 + 3           # Draw
    else:
        return (hand - 1) % 3 + 1     # Loss

with open('day2.txt') as f:
    lines = f.readlines()
    rounds = [round_value(*round.split()) for round in lines]
    reverse_rounds = [reverse_round_value(*round.split()) for round in lines]

print(sum(rounds))
print(sum(reverse_rounds))
