import pandas as pd
import pyarrow as arrow
from bs4 import BeautifulSoup

url_base = "https://snap.fan"
class_name = "card-grid__cell-name"
class_abils = "card-grid__cell-description"
class_url = "card-grid__cell-card"

with open("snap_fan_cards.html", "r") as f:
    cards_text = f.read()
    cards = BeautifulSoup(cards_text, "html")

names = [i.text.replace("\n", "") for i in cards.find_all(class_=class_name)]
abils = [i.text.replace("\n", "") for i in cards.find_all(class_=class_abils)]
links = [i.find("a")["href"] for i in cards.find_all("div", class_=class_url)]
url_links = [f"{url_base}{i}" for i in links]

cards_df = pd.DataFrame(data={"name":names, "ability":abils, "url":url_links})

cards_df.to_parquet("cards.parquet")