def position_check(current_plyer):
    move = None
    while type(move) != int:
        move = input(f"Player {current_plyer} move: ")
        try:
            move = int(move)
        except ValueError:
            continue
    return move


def calculate_sums(positions):
    return ["".join(positions[0]),
            "".join(positions[1]),
            "".join(positions[2]),
            positions[0][0] + positions[1][0] + positions[2][0],
            positions[0][1] + positions[1][1] + positions[2][1],
            positions[0][2] + positions[1][2] + positions[2][2],
            positions[0][0] + positions[1][1] + positions[2][2],
            positions[0][2] + positions[1][1] + positions[2][0]
            ]


def print_board(positions):
    print("-------------")
    print(f"| {positions[0][0]} | {positions[0][1]} | {positions[0][2]} |")
    print("-------------")
    print(f"| {positions[1][0]} | {positions[1][1]} | {positions[1][2]} |")
    print("-------------")
    print(f"| {positions[2][0]} | {positions[2][1]} | {positions[2][2]} |")
    print("-------------")


def check_for_two_symbols(sums, symbol):
    for sub in sums:
        counter = 0
        for i in sub:
            if i == symbol:
                counter += 1

        if counter == 2 and "XO".replace(symbol, "") not in sub:
            return int(sub.replace(symbol, ""))

    return False


def ttt_ai(positions, sums):

    if positions[1][1] == "4":
        return 4

    elif check_for_two_symbols(sums, "O"):
        return check_for_two_symbols(sums, "O")

    elif check_for_two_symbols(sums, "X"):
        return check_for_two_symbols(sums, "X")

    elif positions[0][0] != "X":
        return 0

    elif positions[0][2] != "X":
        return 2

    elif positions[2][0] != "X":
        return 6

    elif positions[2][2] != "X":
        return 9


def tic_tac_toe(ai=False):
    positions = [["0", "1", "2"], ["3", "4", "5"], ["6", "7", "8"]]

    symbols = ["X", "O"]
    player = 0
    moves = 0
    sums = []

    # Choosing game type
    game_type = 0
    while not game_type == "1" or game_type == "2":
        game_type = input("Press 1 for one player press 2 for two players: ")

    while ("XXX" not in sums) and ("OOO" not in sums) and (moves != 9):
        sums = calculate_sums(positions)

        print_board(positions)

        if "XXX" in sums:
            return print("player 1 won")
        elif "OOO" in sums:
            return print("player 2 won")
        else:

            if game_type == "1":
                current_plyer = 1
                player_symbol = "X"
            else:
                current_plyer = player % 2 + 1
                player_symbol = symbols[player % 2]

            move = position_check(current_plyer)

            while (not 0 <= move <= 8 and
                   positions[move // 3][move % 3] != "O" and
                   positions[move // 3][move % 3] != "X"):

                print("wrong position")
                move = position_check(current_plyer)

            positions[move // 3][move % 3] = player_symbol
            player += 1
            moves += 1

            if moves == 9:
                print("TIE")
                break

            if game_type == "1":
                sums = calculate_sums(positions)
                move = ttt_ai(positions, sums)
                positions[move // 3][move % 3] = "O"
                moves += 1


tic_tac_toe()
