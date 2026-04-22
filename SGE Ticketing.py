def main_menu():
    gameplan = {"FC Bayern München" : {"date" : "12/09/2026", "demand" : "5"}}
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
    for clubs, details in gameplan.items():
        print(f"{clubs} {details["date"]}")
    while True:
        option = input("Enter club or 0 to cancel")
        if option == "0":
            return
        elif option in gameplan:
            ticket_buy()
        else:
            print("Club not found in Gameplan, please enter again")

    
def ticket_buy():
    print("1")
    

def admin_menu(gameplan):
    print(f"{"ADMIN MENU":.^60}")






main_menu()