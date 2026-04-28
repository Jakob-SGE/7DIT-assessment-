"""
Should include at least the next 5 games
Should have different prices for the different areas and blocks
At least 4 different areas
Should include an option to book a parking or train ticket with it
Should have different prices depending on the opponent and competition, the demand level can be modified by the operator, the different levels of demand dictate prices
The seat options should be organized by block, area, price and suitability (family, business, hardcore fan)
After the order information has been displayed the program should be ready to accept another order or end. 
You should have the option between a digital and printed ticket
Optional:
Should have an option to search for seats that are next to each other for families
"""


STADIUM_TEMPLATE = {"NORDWESTKURVE" : {"capacity" : 30, "class" : "standing"},
                    "HAUPTTRIBUENE" : {"rows" : 2, "seats_per_row" : 8, "class" : "VIP"},
                    "JUERGEN_GRABOWSKI_TRIBUENE" : {"rows" : 3, "seats_per_row": 10, "class" : "standard"}}


PRICE_LIST = {"standard" : [30, 40, 50, 60, 70],
              "VIP" : [150, 175, 200, 250, 300],
              "standing" : [8, 8, 10, 12, 15]}



def main_menu():
    gameplan = [{"club" : "FC Bayern München", "date" : "12/09/2026", "demand" : 5},
                {"club" : "TSG Hoffenheim", "date" : "26/09/2026", "demand" : 2}]
    while True:
        print(f"{"EINTRACHT FRANKFURT TICKETING":.^60}")
        print("*" * 60)
        print(f"|{"OPTION 0":<10}{"Stop the program":>50}|")
        print(f"|{"OPTION 1":<10}{"Sell Tickets":>50}|")
        print(f"|{"OPTION 2":<10}{"Modify Program":>50}|")
        option = input("Enter option: ")
        if option == "0":
            break
        elif option == "1":
            customer_menu(gameplan)
        elif option == "2":
            admin_menu(gameplan)
        else:
            print("Option is not available, please try again")


def customer_menu(gameplan):
    print(f"{"UPCOMING GAMES":.^60}")
    count = 1
    for clubs in gameplan:
        print(f"GAME {count} {clubs["club"]} {clubs["date"]}")
        count += 1 
    option = int_input("Enter Game number: ", "Game not found, please try again", (0, len(gameplan)))
    option = count_to_index(option)
    print(f"Game vs {gameplan[option]["club"]} on the {gameplan[option]["date"]}") 
    ticket_buy(option, gameplan)


def ticket_buy(game, gameplan):
    print(f"{gameplan[game]["club"]}")

    
def admin_menu(gameplan):
    while True:
        print(f"{"ADMIN MENU":.^60}")
        print("*" * 60)
        print(f"|{"OPTION 0":<10}{"Stop the program":>50}|")
        print(f"|{"OPTION 1":<10}{"Add a new game":>50}|")
        print(f"|{"OPTION 2":<10}{"Modify demand/prices":>50}|")
        option = input("Enter option: ")
        if option == "0":
            break
        elif option == "1":
            add_new_game(gameplan)
        elif option == "2":
            admin_menu(gameplan)
        else:
            print("Option is not available, please try again")


def add_new_game(gameplan):
    opponent =  string_input("Enter the opponent: ", "Name is too short, please try again")
    year = int_input("Enter year of the game: ", "Year is not valid, please try again", range(2026, 2027))
    month = int_input("Enter month of the game: ", "Month is not valid, please try again", range(1, 12))
    day = int_input("Enter day of the game: ", "Day is not valid, please try again", range(1, 31))




def int_input(prompt, errormessage, range):
    while True:
        try:
            num = int(input(prompt))
            if num in range:
                return num
            else:
                print(errormessage)
        except ValueError:
            print(errormessage)
        

def count_to_index(count):
    count -= 1
    return count

def string_input(prompt, errormessage):
    while True: 
        name = input(prompt)
        if len(name) >= 3:
            return name
        else:
            print(errormessage)


main_menu()