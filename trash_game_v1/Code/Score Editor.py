import pickle

Scores = pickle.load(open("../Scores", "rb"))

while True:
    UserInput = input().casefold().split(" ")

    if UserInput[0] == "list":
        for Score in Scores.items():
            print(f"{Score[0]}: {Score[1]}")

    if UserInput[0] == "del":
        if len(UserInput) == 3:
            Scores[int(UserInput[1])].remove(UserInput[2])
            print(f'Deleted "{UserInput[2]}" from "{UserInput[1]}"')

        elif len(UserInput) == 2:
            del Scores[int(UserInput[1])]
            print(f'Deleted "{UserInput[1]}"')

        else:
            print("Deletion failed")

    if UserInput[0] == "add":
        if len(UserInput) == 3:
            Scores[int(UserInput[1])].append(UserInput[2])
            print(f'Added "{UserInput[2]}" to "{UserInput[1]}"')

        elif len(UserInput) == 2:
            if UserInput[1] not in list(Scores.keys()):
                Scores[int(UserInput[1])] = []
                print(f'Added "{UserInput[1]}"')

            else:
                print(f'{UserInput[1]} already exists')

        else:
            print("Addition failed")

    if UserInput[0] == "replace":
        if len(UserInput) == 4:
            Scores[int(UserInput[1])][Scores[int(UserInput[1])].index(UserInput[2])] = UserInput[3]

            print(f'Replaced "{UserInput[2]}" with "{UserInput[3]}"')

        elif len(UserInput) == 3:
            Scores[int(UserInput[2])] = Scores[int(UserInput[1])]
            del Scores[int(UserInput[1])]

            print(f'Replaced "{UserInput[1]}" with "{UserInput[2]}"')

    if UserInput[0] == "save":
        pickle.dump(Scores, open("../Scores", "wb"))

        print("Saved successfully")

    if UserInput[0] == "load":
        pickle.load(open("../Scores", "rb"))

        print("Loaded successfully")

    if UserInput[0] == "stop":
        print("Stopped")

        break

    if UserInput[0] == "help":
        print("Commands:")
        print("- list")
        print("- del")
        print("- add")
        print("- replace")
        print("- save")
        print("- load")
        print("- stop")
        print("- help")