def main():
    while True:
        direction = input("Which direction?\n\n>>> ")
        if direction == "north":
            print("You went north.")
        elif direction == "west":
            print("You went west.")
        elif direction == "south":
            print("You went south.")
        elif direction == "east":
            print("You went east.")
        else:
            print("Commands: ['north', 'south', 'east', 'west']")
        continue

main()

