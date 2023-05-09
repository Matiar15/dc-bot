import random


list_of_words: set = ['maslo', 'makar', 'melin']
emotes_instead_of_letters: dict = {"a": "regional_indicator_a",
                                    "b": "regional_indicator_b",
                                    "c": "regional_indicator_c",
                                    "d": "regional_indicator_d",
                                    "e": "regional_indicator_e",
                                    "f": "regional_indicator_f",
                                    "g": "regional_indicator_g",
                                    "h": "regional_indicator_h",
                                    "i": "regional_indicator_i",
                                    "j": "regional_indicator_j",
                                    "k": "regional_indicator_k",
                                    "l": "regional_indicator_m", 
                                    "m": "regional_indicator_m",
                                    "n": "regional_indicator_n", 
                                    "o": "regional_indicator_o",
                                    "p": "regional_indicator_p",
                                    "r": "regional_indicator_r",
                                    "s": "regional_indicator_s:",
                                    "t": "regional_indicator_t", 
                                    "u": "regional_indicator_u", 
                                    "w": "regional_indicator_w", 
                                    "y": "regional_indicator_y", 
                                    "z": "regional_indicator_z", 
                                    
                                    }


def game():
    chosen_word: str = random.choice(list_of_words)
    chances: int = 6
    
    correct_letters = ['x' for _ in range(5)]
    
    
    while(chances != 0):
        player_word: str = input("Wprowadź słowo 5 literowe: ").lower()
        print(f'{chosen_word} <- szukane, podane -> {player_word}')
        
        if player_word == chosen_word:
            return print(f'{chosen_word}\nWYGRALES!')
        
        list_letters_word = [x for x in chosen_word]
        list_letters_player = [y for y in player_word]
        
        for i in range(len(list_letters_word)):
            
            if list_letters_word[i] == list_letters_player[i]:
                correct_letters[i] = emotes_instead_of_letters[list_letters_word[i]]
                
            for j in range(len(list_letters_player)):
                
                if ((list_letters_word[j] == list_letters_player[j]) and 
                    (correct_letters[i] not in emotes_instead_of_letters.values())):
                    if list_letters_player[i] in list_letters_word:
                        correct_letters[i] = list_letters_player[i].upper()
                    else:
                        correct_letters[i] = list_letters_player[i]
                    
                    
        
        if player_word != chosen_word:
            chances -= 1
        
        print(f'correct_letters >>> {correct_letters}')
        print(f'chances >>> {chances}')
    return 'Szanse sie skonczyly, sprobuj ponownie!'

if __name__ == '__main__':
    game()