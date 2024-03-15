from bs4 import BeautifulSoup
import requests
import csv

FILE_NAME = 'game_data.csv'

GENRE_LIST = ["Action",
              "Adventure",
              "Action-Adventure",
              "Board+Game",
              "Education",
              "Fighting",
              "Misc",
              "MMO",
              "Music",
              "Party",
              "Platform",
              "Puzzle",
              "Racing",
              "Role-Playing",
              "Sandbox",
              "Shooter",
              "Simulation",
              "Sports",
              "Strategy",
              "Visual+Novel"]


def scrap_vgc(genre, page):
    response = requests.get(
        "https://www.vgchartz.com/games/games.php?page=" + str(page) + "&name=&keyword=&console=&region=All&developer"
        "=&publisher=&goty_year=&genre=" + genre + "&boxart=Both&banner=Both&ownership=Both&showmultiplat=No"
        "&results=200&order=Sales&showtotalsales=0&showtotalsales=1&showpublisher=0&showpublisher=1"
        "&showvgchartzscore=0&showvgchartzscore=1&shownasales=0&showdeveloper=0&showcriticscore=0"
        "&showcriticscore=1&showpalsales=0&showreleasedate=0&showreleasedate=1&showuserscore=0"
        "&showuserscore=1&showjapansales=0&showlastupdate=0&showothersales=0&showshipped=0")
    vgc_page = response.text

    soup = BeautifulSoup(vgc_page, "html.parser")
    x = soup.find_all(name="tr")
    for i in range(27, 227):
        game = x[i]
        # print(game)
        game_texts = [chosen_game.getText() for chosen_game in game if chosen_game.getText() != " "]
        game_texts_2 = [chosen_game.replace("\n", "").replace("Read the review", "").strip() for
                        chosen_game in game_texts if chosen_game.replace("\n", "").strip() != ""]

        if "Results: (" in game_texts_2[0]:
            return False

        game_texts_2.append(genre)
        with open(FILE_NAME, 'a', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(game_texts_2[1:])
    return True


if __name__ == "__main__":
    with open(FILE_NAME, 'w', newline='', encoding='utf-8') as csvfile:
        csvfile.truncate(0)

    for loc_genre in GENRE_LIST:
        for loc_page in range(1, 300):
            print(str(loc_page) + " " + loc_genre)
            if not scrap_vgc(loc_genre, loc_page):
                break
