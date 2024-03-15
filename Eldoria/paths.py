import random


def paths(left_path, straight_path, right_path):
    path_1 = f"""

            _________________
            _________________ ({straight_path})

            """

    path_2 = f"""
                ({left_path})       
                    | |
                    | |
            ________| |_________
            ____________________ ({straight_path})
            """

    path_3 = f"""
                ({left_path})        
                    | |
                    | |
            ________| |_________
            ________   _________ ({straight_path})
                    | |
                    | |
                    | |
                ({right_path})
            """

    path_4 = f"""
            __________
            ________  |
                    | |
                    | |
                    | |
                ({right_path})
            """

    path_5 = f"""
                ({left_path})        
                    | |
                    | |
            ________| |
            ________  |
                    | |
                    | |
                    | |
                ({right_path})
            """

    path_6 = f"""
                ({left_path})        
                    | |
                    | |
            ________| |
            __________|

            """

    return random.choice([path_1, path_2, path_3, path_4, path_5, path_6])
