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
            game_seating[section] = int(f"{info["capacity"] * fill_chance:.0f}")
        else:
            game_seating[section] = get_seat_generation(fill_chance, info)
    return game_seating



def get_seat_generation(fill_chance, info):
    layout = []
    for rows in range(info["rows"]):
        row = []
        for seats in range(info["seats_per_row"]):
            is_taken = random.random() < fill_chance
            row.append(is_taken)
        layout.append(row)
    return layout


def customer_menu(gameplan):
    display_gameplan(gameplan)
    option = select_game(gameplan)
    ticket_buy(option, gameplan)


def select_game(gameplan):
    option = int_input("Enter Game number: ", "Game not found, please try again", range(1, len(gameplan) + 1))
    option = count_to_index(option)
    print(f"Game vs {gameplan[option]["club"]} on the {gameplan[option]["date"]}") 
    return option


def display_gameplan(gameplan):
    print(f"{"UPCOMING GAMES":.^60}")
    count = 1
    for clubs in gameplan:
        print(f"GAME {count} {clubs["club"]} {clubs["date"]}")
        count += 1 


def ticket_buy(game, gameplan):
    while True:
        print(f"{"Stadium overview":.^60}")
        print(f"|{"Option 0":<10}{"cancel order":>50}|")
        print(f"|{"Option 1":<10}{"Juergen Grabowski Tribuene":>50}|")
        print(f"|{"OPTION 2":<10}{"Hauptribuene":>50}|")
        print(f"|{"OPTION 3":<10}{"Nordwestkurve":>50}|")
        option = int_input("Enter your preferred seating class: ", "Invalid option, Enter (1-3)", range(0, 4))
        if option == 0:
            break
        elif option == 1:
            seat_ticket_buy(game, gameplan, "JUERGEN_GRABOWSKI_TRIBUENE")
        elif option == 2:
            seat_ticket_buy(game, gameplan, "HAUPTTRIBUENE")
        elif option == 3: 
            nwk_ticket_buy(game, gameplan)


def seat_ticket_buy(game, gameplan, section):
    display_free_seating(game, gameplan, section)



def display_free_seating(game, gameplan, section):
    



def nwk_ticket_buy(game, gameplan):
    free_tickets = STADIUM_TEMPLATE["NORDWESTKURVE"]["capacity"] - gameplan[game]["seating"]["NORDWESTKURVE"]
    print(f"There are {free_tickets} free tickets")
    if free_tickets > 0:
        ticket_number = int_input("How many tickets would you like to buy: ", f"Not a valid amount of tickets, there are only {free_tickets} left", range(1, free_tickets + 1))
        demand_level = count_to_index(gameplan[game]["demand"])
        ticket_price = PRICE_LIST["standing"][demand_level]
        price = ticket_number *  ticket_price
        print(f"{ticket_number} tickets in the Nordwestkurve will cost €{price:.2f}")
        confirmation = int_input("To confirm your order enter 1, to cancel enter 0: ", "Not a valid option, enter (1 or 0)", range(0, 2))
        if confirmation == 1:
            print("Thank you for your order!")
        else:
            print("Order has been canceled")

    
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
            modify_demand(gameplan)
        else:
            print("Option is not available, please try again")


def modify_demand(gameplan):
    display_gameplan(gameplan)
    option = select_game(gameplan)
    demand = demand_input()
    gameplan[option]["demand"] = demand


def add_new_game(gameplan):
    opponent =  string_input("Enter the opponent: ", "Name is too short, please try again")
    date = get_game_date()
    demand = demand_input()
    match = {"club" : opponent, "date" : date, "demand" : demand, "seating" : generate_seating(0, STADIUM_TEMPLATE)}
    gameplan.append(match)
    print(gameplan)


def demand_input():
    demand = int_input("Enter the demand level (1-5): ", "Invalid demand level, enter a number from 1 to 5", range(1, 6))
    return demand


def get_game_date():
    year = int_input("Enter year of the game: ", "Year is not valid, please try again", range(2026, 2028))
    if year == 2026:
        month_range = range(5, 13) 
        month_error = "For 2026, please enter a month from May (5) onwards."
    else:
        month_range = range(1, 13)  
        month_error = "Invalid month (1-12)."
    month = int_input("Enter month of the gamee: ", month_error, month_range)
    max_days = DAYS_IN_MONTHS[month] + 1
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