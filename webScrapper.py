from bs4 import BeautifulSoup
import requests
import json

url = 'http://store.steampowered.com/search/?page=%d'
file = open("a.csv", "w")
file.write("id~url~title~releaseDate~desc~developers~discount~discountCost~realCost~reviewUrl\n")
count = 0
page = 1
while count <= 300:
    raw = requests.get(url % page, 'html.parser')
    data = BeautifulSoup(raw.text)
    game_list = data.find_all("a", {"class": "search_result_row"})
    for game in game_list:
        game_url = game.get("href")
        game_data = BeautifulSoup(requests.get(game_url).text)

        if game_data.find("div", {"class": "glance_ctn"}) is None or game_data.find("div", {"class": "game_purchase_price price"}) is None:
            continue

        try:
            title = game_data.find("div", {"class": "apphub_AppName"})
            title = title.get_text()
            title = "".join(title.split("\n"))
            title = "".join(title.split("\r"))
        except Exception:
            title = ""
        try:
            release_date = game_data.find("div", {"class": "date"})
            release_date = release_date.get_text()
            release_date = "".join(release_date.split("\n"))
            release_date = "".join(release_date.split("\r"))
        except Exception:
            release_date = ""
        try:
            desc = game_data.find("div", {"class": "game_description_snippet"})
            desc = desc.get_text()
            desc = "".join(desc.split("\n"))
            desc = "".join(desc.split("\r"))
        except Exception:
            desc = ""
        try:
            developers = game_data.find("div", {"id": "developers_list"})
            developers = developers.get_text()
            developers = "".join(developers.split("\n"))
            developers = "".join(developers.split("\r"))
        except Exception:
            developers = ""

        try:
            discountData = game_data.find("div", {"class": "discount_block game_purchase_discount"})
            disc = discountData.find("div", {"class": "discount_pct"})
            disc = disc.get_text()
            disc = "".join(disc.split("\n"))
            disc = "".join(disc.split("\r"))
            discCost = discountData.find("div", {"class": "discount_final_price"})
            discCost = discCost.get_text()
            discCost = "".join(discCost.split("\n"))
            discCost = "".join(discCost.split("\r"))
            realCost = discountData.find("div", {"class": "discount_original_price"})
            realCost = realCost.get_text()
        except Exception:
            realCost = game_data.find("div", {"class": "game_purchase_price price"})
            realCost = realCost.get_text()
            disc = discCost = ""
        realCost = "".join(realCost.split("\n"))
        realCost = "".join(realCost.split("\r"))

        try:
            review_url = "http://steamcommunity.com/app/%s/reviews/" % game_url.split("/")[4]
        except Exception:
            review_url = ""

        game_line = "%d~%s~%s~%s~%s~%s~%s~%s~%s~%s\n" % (count, game_url, title, release_date, desc, developers, disc, discCost, realCost, review_url)
        file.write(game_line)
        print(game_line)
        count += 1
    page += 1
file.close()