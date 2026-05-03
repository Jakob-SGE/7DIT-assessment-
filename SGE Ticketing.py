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
    "VIP": (8, 12)}


def main_menu():
    """The Main menu to access all the different funtions of the program and to store important variable like the gameplan with the seating and dthe shopping cart"""
    gameplan = [{"club" : "FC Bayern München", "date" : "12/09/2026", "demand" : 5, "seating" : generate_seating(5, STADIUM_TEMPLATE)},
                {"club" : "TSG Hoffenheim", "date" : "26/09/2026", "demand" : 2, "seating" : generate_seating(2, STADIUM_TEMPLATE)},
                {"club" : "Hamburger SV", "date" : "5/10/2026", "demand" : 3, "seating" : generate_seating(3, STADIUM_TEMPLATE)},
                {"club" : "Borussia Dortmund", "date" : "14/10/2026", "demand" : 5, "seating" : generate_seating(5, STADIUM_TEMPLATE)},
                {"club" : "1. FC Heidenheim", "date" : "28/10/2026", "demand" : 1, "seating" : generate_seating(1, STADIUM_TEMPLATE)}]
    shopping_cart = [] 
    while True:
        print(f"{"EINTRACHT FRANKFURT TICKETING":.^60}")
        print("*" * 60)
        print(f"|{"OPTION 0":<10}{"Stop the program":>50}|")
        print(f"|{"OPTION 1":<10}{"Customer Area":>50}|")
        print(f"|{"OPTION 2":<10}{"Admin Area":>50}|")
        option = input("Enter option: ")
        if option == "0":
            break
        elif option == "1":
            customer_menu(gameplan, shopping_cart)
        elif option == "2":
            admin_menu(gameplan)
        else:
            print("Option is not available, please try again")


def generate_seating(demand, stadium):
    """Generates the seating for each game in the gameplan and append that to a dictionary."""
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
    """Generates the seating are which seats are taken and which are not and returns that back to the seating"""
    layout = []
    for rows in range(info["rows"]):
        row = []
        for seats in range(info["seats_per_row"]):
            is_taken = random.random() < fill_chance
            row.append(is_taken)
        layout.append(row)
    return layout


def customer_menu(gameplan, shopping_cart):
    """The customer menu where all the functions that are meant for customers can be accessed"""
    while True:
        print(f"{"CUSTOMER MENU":.^60}")
        print(f"|{"OPTION 0":<10}{"Back to Main Menu":>50}|")
        print(f"|{"OPTION 1":<10}{"Select a Game & Buy Tickets":>50}|")
        print(f"|{"OPTION 2":<10}{f"Go to Checkout":>50}|")
        print(f"|{"OPTION 3":<10}{f"Clear Shopping cart":>50}|")
        print("*" * 60)
        option = int_input("\nEnter option: ", "Invalid option, enter (0-3)", range(0, 4))
        if option == 0:
            break
        elif option == 1:
            display_gameplan(gameplan)
            game = select_game(gameplan)
            ticket_buy(game, gameplan, shopping_cart) 
        elif option == 2:
            checkout(shopping_cart)
        elif option == 3:
            clear_shopping_cart(shopping_cart, gameplan)


def clear_shopping_cart(shopping_cart, gameplan):
    """This clears the shopping cart and marks the ordered seats back to free"""
    if not shopping_cart:
        print("\nShopping cart is empty\n")
        return
    for item in shopping_cart:
        if item["section"] == "NORDWESTKURVE":
            gameplan[item["game_index"]]["seating"]["NORDWESTKURVE"] -= item["amount"]
        else:
            for seat in item["seats"]:
                gameplan[item["game_index"]]["seating"][item["section"]][count_to_index(seat[0])][count_to_index(seat[1])] = False
    shopping_cart.clear()
    print("\nSHOPPING CART CLEARED\n")  


def checkout(shopping_cart):
    """The checkout shows an overview of the shopping cart before asking for last confirmation before the purchase"""
    if not shopping_cart:
        print("\nShopping cart is empty\n")
        return
    total_price = 0
    print(f"{"YOUR SHOPPING CART":^60}")
    for item in shopping_cart:
        if item["section"] == "NORDWESTKURVE":
            print(f"VS {item["game"]} {item["amount"]} tickets for {item["price"]} in the Nordwestkurve")
        else:
            print(f"VS {item["game"]} {len(item["seats"])} tickets for {item["price"]}€ in the {item["section"]}") 
        total_price += item["price"]
    print(f"\n{"GRAND TOTAL:":<15} {total_price}€")
    confirmation = int_input("\nEnter 1 to confirm purchase, 0 to cancel order: ", "Invalid option (1 or 0)", range(0, 2))
    if confirmation == 1:
        print("\nPURCHASE CONFIRMED!\n")
        shopping_cart.clear() 
    else:
        print("\nCheckout canceled. Items are still in your cart.\n")

       
def select_game(gameplan):
    """Select a game out of the gameplan and turns that into and index so that you can access it in the gameplan list"""
    option = int_input("\nEnter Game number: ", "Game not found, please try again", range(1, len(gameplan) + 1))
    option = count_to_index(option)
    print(f"Game vs {gameplan[option]["club"]} on the {gameplan[option]["date"]}") 
    return option


def display_gameplan(gameplan):
    """This displays the gameplan"""
    print(f"{"UPCOMING GAMES":.^60}")
    count = 1
    for clubs in gameplan:
        print(f"GAME {count} {clubs["club"]} {clubs["date"]}")
        count += 1 
    print("\n")


def ticket_buy(game, gameplan, shopping_cart):
    """The mmenu where you can select in which section you want to buy the tickets"""
    while True:
        print(f"{f"\nStadium overview vs {gameplan[game]["club"]}":.^60}")
        print(f"|{"Option 0":<10}{"Back to customer Menu":>50}|")
        print(f"|{"Option 1":<10}{"Juergen Grabowski Tribuene":>50}|")
        print(f"|{"OPTION 2":<10}{"Hauptribuene":>50}|")
        print(f"|{"OPTION 3":<10}{"Nordwestkurve":>50}|")
        option = int_input("\nEnter your preferred seating class: ", "Invalid option, Enter (1-3)", range(0, 4))
        if option == 0:
            break
        elif option == 1:
            seat_ticket_buy(game, gameplan, "JUERGEN_GRABOWSKI_TRIBUENE", "Juergen Grabowski Tribuene", shopping_cart)
        elif option == 2:
            seat_ticket_buy(game, gameplan, "HAUPTTRIBUENE", "Haupttribuene", shopping_cart)
        elif option == 3: 
            nwk_ticket_buy(game, gameplan, shopping_cart)


def seat_ticket_buy(game, gameplan, section, section_name, shopping_cart):
    """The function where you can order the seat tickets by entering row and seat"""
    display_seating(game, gameplan, section, section_name)
    ordered_seats = []
    while True:
        seat = []
        option = int_input("Enter 0 to stop ordering or enter the row: ", "Not a valid option, enter 0 or an existing row", range(0, len(gameplan[game]["seating"][section]) + 1))
        if option == 0:
            break 
        seat.append(option)
        row_idx = count_to_index(option)
        seat_number = int_input("Enter the seat: ", "Not a valid seat number", range(0, len(gameplan[game]["seating"][section][row_idx]) + 1))
        seat_idx = count_to_index(seat_number)
        seat.append(seat_number)
        if not gameplan[game]["seating"][section][row_idx][seat_idx]:
            gameplan[game]["seating"][section][row_idx][seat_idx] = True
            ordered_seats.append(seat)
            print(f"Seat r{option}/s{seat_number} added to your order!")
        else:
            print("This seat is not free, please select another")
    if len(ordered_seats) > 0:
        order_confirmation(ordered_seats, gameplan, game, section, section_name, shopping_cart)



def order_confirmation(ordered_seats, gameplan, game, section, section_name, shopping_cart):
    """For confirmation of the selected seats they then get added to the shopping cart"""
    print("\nSELECTED SEATS:")
    for s in ordered_seats:
        print(f"r{s[0]}/s{s[1]}")
    confirmation = int_input("\nTo add your order to the shopping cart enter 1, to cancel enter 0: ", "Not a valid option, enter (1 or 0)", range(0, 2))
    if confirmation == 1:
        demand_index = count_to_index(gameplan[game]["demand"])
        ticket_price = PRICE_LIST[STADIUM_TEMPLATE[section]["class"]][demand_index]
        ticket_amount = len(ordered_seats)
        price = ticket_price *  ticket_amount
        order = {"game" : gameplan[game]["club"],
                    "section" : section_name,
                    "seats" : ordered_seats,
                    "price" : price,
                    "game_index" : game
        }
        shopping_cart.append(order)
    else:
        for seat in ordered_seats:
            gameplan[game]["seating"][section][count_to_index(seat[0])][count_to_index(seat[1])] = False
        print("Order has been canceled")


def display_seating(game, gameplan, section, section_name):
    """Displays the seating in a section for a specific game"""
    print(f"{section_name}:")
    print("Legend: [ ] = Free | [X] = Taken\n")
    row = 1
    for r in gameplan[game]["seating"][section]:    
        seating = [f"Row {row}:"]
        for s in r:        
            if not s:
                seating.append("[ ]")
            else:
                seating.append("[X]")
        row += 1
        print(" ".join(seating))
    print("")



def nwk_ticket_buy(game, gameplan, shopping_cart):
    """Function to buy tickets from the standing area appends the selected seats to the shopping cart"""
    free_tickets = STADIUM_TEMPLATE["NORDWESTKURVE"]["capacity"] - gameplan[game]["seating"]["NORDWESTKURVE"]
    print(f"There are {free_tickets} free tickets")
    if free_tickets > 0:
        ticket_number = int_input("How many tickets would you like to buy: ", f"Not a valid amount of tickets, there are only {free_tickets} left", range(1, free_tickets + 1))
        demand_level = count_to_index(gameplan[game]["demand"])
        ticket_price = PRICE_LIST["standing"][demand_level]
        price = ticket_number *  ticket_price
        print(f"{ticket_number} tickets in the Nordwestkurve will cost €{price:.2f}")
        confirmation = int_input("To add your order to the shopping cart enter 1, to cancel enter 0: ", "Not a valid option, enter (1 or 0)", range(0, 2))
        if confirmation == 1:
            gameplan[game]["seating"]["NORDWESTKURVE"] += ticket_number
            order = {"game" : gameplan[game]["club"],
                "section" : "NORDWESTKURVE",
                "amount" : ticket_number,
                "price" : price,
                "game_index" : game}
            print("Order has been added to the shopping cart")
            shopping_cart.append(order)
        else:
            print("Order has been canceled")

    
def admin_menu(gameplan):
    """The admin menu where you can add a new game or modify the demand"""
    while True:
        print(f"{"ADMIN MENU":.^60}")
        print("*" * 60)
        print(f"|{"OPTION 0":<10}{"Go back to main menu":>50}|")
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
    """You can modify the demand of a specific game which impacts prices"""
    display_gameplan(gameplan)
    option = select_game(gameplan)
    demand = demand_input()
    gameplan[option]["demand"] = demand


def add_new_game(gameplan):
    """Adds a new game to the gameplan"""
    opponent =  string_input("Enter the opponent: ", "Name is too short, please try again")
    date = get_game_date()
    demand = demand_input()
    match = {"club" : opponent, "date" : date, "demand" : demand, "seating" : generate_seating(0, STADIUM_TEMPLATE)}
    gameplan.append(match)
    print(f"\nGame vs {opponent} on {date} has been added\n")


def demand_input():
    """demand input function to make the code more readable"""
    demand = int_input("Enter the demand level (1-5): ", "Invalid demand level, enter a number from 1 to 5", range(1, 6))
    return demand


def get_game_date():
    """Gets the date of the game and input validates it, so it is on a correct date"""
    year = int_input("Enter year of the game: ", "Year is not valid, please try again", range(2026, 2028))
    if year == 2026:
        month_range = range(5, 13) 
        month_error = "For 2026, please enter a month from May (5) onwards."
    else:
        month_range = range(1, 13)  
        month_error = "Invalid month (1-12)."
    month = int_input("Enter month of the game: ", month_error, month_range)
    max_days = DAYS_IN_MONTHS[month] + 1
    day = int_input("Enter day of the game: ", "Day is not valid, please try again", range(1, max_days))
    game_date = f"{day:02d}/{month:02d}/{year}"
    return game_date


def int_input(prompt, errormessage, valid_range):
    """function that input validates integer inputs can be adjusted using the parameters"""
    while True:
        try:
            num = int(input(prompt))
            if num in valid_range:
                return num
            else:
                print(errormessage)
        except ValueError:
            print(errormessage)
        

def count_to_index(count):
    """Makes an index out of a count like in the gameplan for example Bayern game 1, index 0. To make the code more readable"""
    count -= 1
    return count


def string_input(prompt, errormessage):
    """string input to validate the input of strings can be adjusted using the parameters"""
    while True: 
        name = input(prompt)
        if len(name) >= 3:
            return name
        else:
            print(errormessage)


main_menu()