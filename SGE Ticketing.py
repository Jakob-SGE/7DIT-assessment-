def main_menu():
    gameplan = [{"Club" : "FC Bayern München", "date" : "12/09/2026", "demand" : "5"}]
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
        print(f"GAME {count} {clubs["Club"]} {clubs["date"]}")
        count += 1 
    option = int_input("Enter Game number: ", "Game not found, please try again", (0, len(gameplan)))

    

def admin_menu(gameplan):
    print(f"{"ADMIN MENU":.^60}")


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
        



main_menu()