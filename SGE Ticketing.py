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
import random

DAYS_IN_MONTHS = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

STADIUM_TEMPLATE = {"NORDWESTKURVE" : {"capacity" : 30, "class" : "standing"},
                    "HAUPTTRIBUENE" : {"rows" : 2, "seats_per_row" : 8, "class" : "VIP"},
                    "JUERGEN_GRABOWSKI_TRIBUENE" : {"rows" : 3, "seats_per_row": 10, "class" : "standard"}}


PRICE_LIST = {"standard" : [30, 40, 50, 60, 70],
              "VIP" : [150, 175, 200, 250, 300],
              "standing" : [8, 8, 10, 12, 15]}


SECTION_WEIGHTS = {
    "standing": (18, 20),   
    "standard": (15, 18),  
    "VIP": (8, 12)         
}



def main_menu():
    gameplan = [{"club" : "FC Bayern München", "date" : "12/09/2026", "demand" : 5, "seating" : generate_seating(5, STADIUM_TEMPLATE)},
                {"club" : "TSG Hoffenheim", "date" : "26/09/2026", "demand" : 2, "seating" : generate_seating(2, STADIUM_TEMPLATE)}]
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


def generate_seating(demand, stadium):
    game_seating = {}
    for section, info in stadium.items():
        min, max = SECTION_WEIGHTS[info["class"]]
        fill_chance = random.randint(demand * min, demand * max) / 100
        if info["class"] == "standing":
            game_seating[section] = info["capacity"] * fill_chance
        else:
            game_seating[section] = get_seat_generation(fill_chance, info)
    return game_seating


def get_seat_generation(fill_chance, info):
    layout = []
    for r in range(info["rows"]):
        row = []
        for s in range(info["seats_per_row"]):
            is_taken = random.random() < fill_chance
            row.append(is_taken)
        layout.append(row)
    return layout


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
    print(f"{gameplan[game]["seating"]}")

    
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
    date = get_game_date()
    demand = int_input("Enter the demand level (1-5): ", "Invalid demand level, enter a number from 1 to 5", range(1, 6))
    match = {"club" : {opponent}, "date" : {date}, "demand" : {demand}, "seating" : generate_seating(0, gameplan)}
    gameplan.append(match)


def get_game_date():
    year = int_input("Enter year of the game: ", "Year is not valid, please try again", range(2026, 2028))
    if year == 2026:
        month_range = range(5, 13) 
        month_error = "For 2026, please enter a month from May (5) onwards."
    else:
        month_range = range(1, 13)  
        month_error = "Invalid month (1-12)."
    month = int_input("Enter month of the gamee: ", month_error, month_range)
    max_days = DAYS_IN_MONTHS[month]
    day = int_input("Enter day of the game: ", "Day is not valid, please try again", range(1, max_days))
    game_date = f"{day}/{month}/{year}"
    return game_date


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