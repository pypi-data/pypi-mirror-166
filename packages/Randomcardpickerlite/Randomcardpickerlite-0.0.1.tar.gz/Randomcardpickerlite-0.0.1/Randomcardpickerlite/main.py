import random
def Pick_a_card():
    card_number =['A','K','Q','J','2','3','4','5','6','7','8','9','10']
    card_signs =['Heart','CLUB','DIAMOND','SPADE']
    random_point = random.choice(card_number)
    random_sign = random.choice(card_signs)
    random_card = random_point, random_sign
    return(random_card)

if __name__ == "__main__":
    print(Pick_a_card())