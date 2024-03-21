import numpy as np
import random


class Player:
    def __init__(self, player_number, place, price, quality):
        self.player_number = player_number
        self.place = place
        self.price = price
        self.quality = quality
        self.cost = 0
        self.utility = 0

    def calculate_cost(self, i):
        self.cost = (np.e ** ((abs(i - self.place) + 1) / 100)) * 0.1\
                    + (np.e ** (self.price / 10)) * 0.5\
                    - (np.e ** (self.quality / 10)) * 0.4

    def calculated_utility(self, utility):
        self.utility = utility

    def new_place(self, last_place, l):
        left = self.place - (last_place + 1) * 20
        right = self.place + (last_place + 1) * 20

        if left < 0:
            left = 0
        if right > l:
            right = l

        self.place = random.randint(left, right)

    def new_price(self, last_price):
        left = self.price - (last_price + 1) * 4
        right = self.price + (last_price + 1) * 4

        if left < 10:
            left = 10
        if right > 30:
            right = 30

        self.price = random.randint(left, right)

    def __copy__(self):
        return Player(self.player_number, self.place, self.price, self.quality)

    def write(self):
        return self.place, self.price, self.quality, self.utility


def utilhelp(players_list, l):

    utility = []

    player_number_list = []

    for i in range(1, l + 1):

        for player in players_list:
            player.calculate_cost(i)

        min_nr = players_list[0].player_number
        min_cost = players_list[0].cost

        for k in range(1, len(players_list)):
            if players_list[k].cost < min_cost:
                min_nr = players_list[k].player_number
                min_cost = players_list[k].cost

            elif players_list[k].cost == min_cost:
                los = random.randint(1, 2)
                if los == 1:
                    min_nr = players_list[k].player_number
                    min_cost = players_list[k].cost

        player_number_list.append(min_nr)

    for element in players_list:
        count = player_number_list.count(element.player_number)
        element.calculated_utility(count)

    return players_list


def util(poz, l):

    dist_poz = []
    dist_all_poz = []
    full_sublist = []

    for sublist in poz:
        full_sublist.append([sublist.place, sublist.price, sublist.quality])
        if [sublist.place, sublist.price, sublist.quality] not in dist_poz:
            dist_poz.append([sublist.place, sublist.price, sublist.quality])
            dist_all_poz.append(sublist)

    if len(dist_poz) == len(poz):
        utility_final = utilhelp(poz, l)
        return utility_final

    else:
        dist_players_list = utilhelp(dist_all_poz, l)

        cnt_list = []

        for pozycja in dist_poz:
            count = full_sublist.count(pozycja)
            cnt_list.append([pozycja[0], pozycja[1], pozycja[2], count])

        for player in dist_players_list:
            for cnt in cnt_list:
                if player.place == cnt[0] and player.price == cnt[1] and player.quality == cnt[2]:
                    val = player.utility / cnt[3]
                    player.calculated_utility(val)

        for player in poz:
            for dist_player in dist_players_list:
                if player.place == dist_player.place and player.price == dist_player.price and player.quality == dist_player.quality:
                    player.calculated_utility(dist_player.utility)

        return poz


def nash(poz, num_poz, l):

    product = poz

    higher_val = False
    counter = 0

    while not higher_val and counter < 1000:

        if poz[num_poz].utility == 1000:
            print('brak lepszej pozycji!')
            break

        counter += 1
        poz_list_2 = [elem.__copy__() for elem in poz]
        poz_list_2[num_poz].new_place(counter, l)
        poz_list_2[num_poz].new_price(counter)

        full_list_2 = util(poz_list_2, l)

        if full_list_2[num_poz].utility > poz[num_poz].utility:
            # print('zmn')
            main_poz_list = list(range(0, len(poz), 1))
            main_poz_list.remove(num_poz)
            iter_num = 8000
            perc = 0

            for zmienna in range(iter_num):
                p_list = [0] * (len(poz))
                for r in main_poz_list:
                    if full_list_2[r].utility >= poz[r].utility:
                        p_list[r] = full_list_2[r]
                    else:
                        test_poz_list = [elem.__copy__() for elem in poz_list_2]
                        test_poz_list[r].new_place(zmienna, l)
                        test_poz_list[r].new_price(zmienna)
                        test_list = util(test_poz_list, l)

                        if full_list_2[r].utility >= test_list[r].utility:
                            p_list[r] = poz[r]
                        else:
                            p_list[r] = test_list[r]

                p_list[num_poz] = full_list_2[num_poz]

                p_util = util(p_list, l)

                if poz[num_poz].utility > p_util[num_poz].utility:
                    perc += 1
                    break

            less_perc = perc / iter_num

            if less_perc == 0:
                higher_val = True
                product = full_list_2

    if counter == 1000:
        print("Brak lepszej pozycji!")

    return product


def main():
    outcome = []
    outcome_pos = []

    l = 1000

    for i in range(1):

        x_poz = random.randint(1, l)
        x_price = random.randint(10, 30)
        x_quality = 10
        y_poz = random.randint(1, l)
        y_price = random.randint(10, 30)
        y_quality = 10

        z_poz = random.randint(1, l)
        z_price = random.randint(10, 30)
        z_quality = 10

        t_poz = random.randint(1, l)
        t_price = random.randint(10, 30)
        t_quality = 10

        x = Player(1, x_poz, x_price, x_quality)
        y = Player(2, y_poz, y_price, y_quality)
        z = Player(3, z_poz, z_price, z_quality)
        t = Player(4, t_poz, t_price, t_quality)

        # utility = util([x, y], l)
        utility = util([x, y, z, t], l)
        print(f"próba: początek - utility x : {x.write()} - utility y : {y.write()} - utility z : {z.write()} - utility t : {t.write()}")

        print("----------------------------------------------------------")

        util_list = []

        for k in range(0, 10000000):
            this_util = []
            if k > 4:
                if util_list[k - 1] == util_list[k - 2]:
                    break

            utility = nash([x, y, z, t], 0, l)
            x = utility[0]
            y = utility[1]
            z = utility[2]
            t = utility[3]

            print(f"próba:{k} - utility x : {x.write()} - utility y : {y.write()} - utility z : {z.write()} - utility t : {t.write()}")
            utility = nash([x, y, z, t], 1, l)
            x = utility[0]
            y = utility[1]
            z = utility[2]
            t = utility[3]

            print(f"próba:{k} - utility x : {x.write()} - utility y : {y.write()} - utility z : {z.write()} - utility t : {t.write()}")
            utility = nash([x, y, z, t], 2, l)
            x = utility[0]
            y = utility[1]
            z = utility[2]
            t = utility[3]

            print(
                f"próba:{k} - utility x : {x.write()} - utility y : {y.write()} - utility z : {z.write()} - utility t : {t.write()}")
            utility = nash([x, y, z, t], 3, l)
            x = utility[0]
            y = utility[1]
            z = utility[2]
            t = utility[3]

            this_util.append(utility)
            util_list.append(utility)

            print(f"próba:{k} - utility x : {x.write()} - utility y : {y.write()} - utility z : {z.write()} - utility t : {t.write()}")
            print("----------------------------------------------------------")

    print("----------------------------------------------------------")

    print(f'utility x : {x.write()} - utility y : {y.write()}')
    print("----------------------------------------------------------")

    # print('outcome_pos')
    # print(outcome_pos)

    # o1 = []
    # o2 = []
    # for t in util_list:
    #     o1.append(t[0][0][0])
    #     o2.append(t[0][0][0])
    #
    # plt.plot(o1, label="line 1", linestyle="-")
    # plt.plot(o2, label="line 2", linestyle="--")
    # plt.show()


if __name__ == "__main__":
    main()

