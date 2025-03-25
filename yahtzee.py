

import random


class Board:
        def __init__(self):
            self.scores = {"Aces": None, "Twos": None, "Threes": None, "Fours": None, "Fives": None, "Sixes": None, 
                           "Chance": None, "Three Of A Kind": None, "Four Of A Kind": None, "Full House": None, "Small Straight": None, 
                           "Large Straight": None, "Yatchy": None}  
            self.total_sum = 0

        
        #def to check what the score is for each category
        def check_category_board(self, dices, board):
            for category in self.scores:
                if board.scores[category] is None:
                    self.scores[category] = self.calculate_score(category, dices)
                    
            self.print_board()

        def calculate_score(self, category, dices):
            if category == "Aces":
                self.total_sum += dices.count(1) * 1
                return dices.count(1) * 1
            elif category == "Twos":
                self.total_sum += dices.count(2) * 2
                return dices.count(2) * 2
            elif category == "Threes":
                self.total_sum += dices.count(3) * 3
                return dices.count(3) * 3
            elif category == "Fours":
                self.total_sum += dices.count(4) * 4
                return dices.count(4) * 4
            elif category == "Fives":
                self.total_sum += dices.count(5) * 5
                return dices.count(5) * 5
            elif category == "Sixes":
                self.total_sum += dices.count(6) * 6
                return dices.count(6) * 6
            
        
            elif category == "Chance":
                self.total_sum += sum(dices)
                return sum(dices)   
            #if three or four of a kind, sum all dices
            elif category == "Three Of A Kind":
                for dice in dices:
                    if dices.count(dice) >= 3:
                        self.total_sum += sum(dices)
                        return sum(dices)
                return 0
            elif category == "Four Of A Kind":  
                for dice in dices:
                    if dices.count(dice) >= 4:
                        self.total_sum += sum(dices)
                        return sum(dices)
                return 0
            

            #if theres two numbers (len(set) == 2) and theres either three or two of each number
            elif category == "Full House":  
                if len(set(dices)) == 2 and (dices.count(dices[0]) == 2 or dices.count(dices[0]) == 3):
                    self.total_sum += 25
                    return 25
                return 0
            
            #four sequential dices, 1 2 3 4 or 2 3 4 5 or 3 4 5 6
            #
            elif category == "Small Straight":
                small_straights = [[1, 2, 3, 4], [2, 3, 4, 5], [3, 4, 5, 6]]
                #if sorted(dices)[:3] or sorted(dices)[1:] in small_straights:
                sorted_dices = sorted(set(dices))
                #checks if first 4 or last 4 dices are in small_straights
                if sorted_dices[:4] in small_straights or sorted_dices[1:] in small_straights:
                    self.total_sum += 30
                    return 30
                return 0
            
            #five sequential dices, 1 2 3 4 5 or 2 3 4 5 6
            elif category == "Large Straight":
                large_straights = [[1, 2, 3, 4, 5], [2, 3, 4, 5, 6]]
                if sorted(set(dices)) in large_straights:
                    self.total_sum += 40
                    return 40
                return 0
            
            #all the same
            elif category == "Yatchy":
                if len(set(dices)) == 1:
                    self.total_sum += 50
                    return 50
                return 0
            

        def update_score(self, category, dices):
            self.scores[category] = self.calculate_score(category, dices)
            

        #returns true if game is over
        def is_game_over(self):
            for category in self.scores:
                if self.scores[category] is None:
                    return False
            return True

        #prints scoresheet. Used for actual game scoresheet and for temporary board to show each rolls possible scores
        def print_board(self):
            print("Category\tScore")
            print("------------------------------------")
            for category, score in self.scores.items():
                if score is None:
                    print(f"{category:<20}| -")
                else:
                    print(f"{category:<20}| { score}")
            print("------------------------------------")
            
        
#five random numbers between 1 and 6, return list
def roll_dice():
    dices = []
    for i in range(5):
        dices.append(random.randint(1, 6))
    return dices

#rerolls dices. dices is a list of dices to reroll, index will be dices -1
def reroll_dice(dices, reroll):

    #user wants to reroll all dices, returns new list of dices
    if(reroll == "0"):
        return roll_dice()
    
    #dice in reroll is indexes. -1 because we ask user for 1-5 
    for dice in reroll:
        dices[int(dice) - 1] = random.randint(1, 6)
    return dices

#asks user if they want to reroll, checks if input is valid
def want_to_reroll_input():
    user_reroll = input("Reroll the dice? [Y/N]")
    if user_reroll.upper() != "Y" and user_reroll.upper() != "N":
        print("Invalid input")
        return want_to_reroll_input()
    return user_reroll


#choose category input, checks if input is valid
def choose_category_input(board):
    category = input("Choose a category to record the score:")
    if category not in board.scores:
        print("You input wrong category name. Please enter again")
        return choose_category_input( board)
    
    elif board.scores[category] is not None:
        print("Category already scored, choose another one")
        return choose_category_input( board)

    return category

#implemented with asking user for which dices to reroll, not which ones to keep
#asks for dices to reroll, checks if input is valid. Innput should be in form "1 2 3 4 5"
def dices_to_reroll_input():
    dices_to_reroll = input("Enter the dices you want to reroll. Seperate numbers with space. If you want to reroll all dices, enter 0")
    
    if dices_to_reroll != "0":
        dices_to_reroll = dices_to_reroll.split()
        for dice in dices_to_reroll:
            if dice not in ["1", "2", "3", "4", "5"]:
                print("Invalid input")
                return dices_to_reroll_input()
            dice.strip()
            
    return dices_to_reroll


#ask user if they wanna roll or see scoresheet, validates input
def get_input():
    user_choice = input("Choose the option:\n1. Roll the dice\n2. Check the scoresheet")
    if user_choice != "1" and user_choice != "2":
        print("Invalid input")
        return get_input()
    return user_choice


#shows user scoresheet with scores for every category not scored with this rounds dices
#asks for category to score
#updates scoresheet
def full_choose_category(dices, board):
    temp_board = Board()
    temp_board.check_category_board(dices, board)
    print(dices)
    category = choose_category_input(board)
    board.update_score(category, dices)


  #rolls dices, if user wants to reroll, rerolls dices and calls on same function again with updated dices
    #otherwise lets user choose category 
def full_roll_dice(dices, board, reroll_count):
    #if first roll
    if len(dices) == 0:
        dices = roll_dice()
        #prints scoresheet with scores for every category for this roll
        temp_board = Board()
        temp_board.check_category_board(dices, board)
        print(dices)

    #we can only reroll twice
    #wants_to_reroll checks for legal input
    want_to_reroll = want_to_reroll_input()
    if want_to_reroll == "N":
        full_choose_category(dices, board)

    #if we want to reroll
    else:
        dices_to_reroll = dices_to_reroll_input()
        dices = reroll_dice(dices, dices_to_reroll)
        #prints scoresheet with scores for every category for this roll
        reroll_count += 1
        #if we rerolled twice, we have to choose category
        if reroll_count == 2:
            full_choose_category(dices, board)
        else:
            temp_board = Board()
            temp_board.check_category_board(dices, board)
            print(dices)
            #otherwise we can reroll again
            full_roll_dice(dices, board, reroll_count)  

    


#"main" function
#initiates game, and runs game until all categories are scored and game is over
def play_game():
    print("Welcome to the game of yatchy!")
    board = Board()
    round = 1
    while True:
        if board.is_game_over():
            break

        print(f"Round {round}")
        user_choice = get_input()
        if user_choice == "1":

            full_roll_dice([], board, 0)
            round += 1

        elif user_choice == "2":    
            board.print_board()
            print("Current score:", board.total_sum)
            

        # else:
        #     print("Invalid input. Choose to roll dice or check scoresheet")
            
    print("Game over. Total score:", board.total_sum)   


if __name__ == "__main__":
    play_game()