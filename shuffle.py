import random
import re
import pandas as pd
import pyarrow as arrow
import streamlit as st


arishem = [
    "Arishem",
    "At the start of the game, +1 Max Energy. Shuffle 12 random cards into your deck.",
    "https://snap.fan/cards/Arishem/"
]

cards = pd.read_parquet("cards.parquet")
cards.loc[max(cards.index)+1] = arishem

with open("sample_deck.txt") as f:
    deck_lines = f.readlines()

deck_names = []
for i in deck_lines:
    deck_card = re.findall("\(\d\) (.*)", i)
    if deck_card:
        deck_names.append(deck_card[0])
    

deck = cards[cards["name"].isin(deck_names)]

deck_index = deck.index.to_list()

new_cards_index = random.sample(cards.index.to_list(), k=12)
arishem_index = deck_index + new_cards_index

random.shuffle(arishem_index)
arishem_deck = cards.loc[arishem_index,:]


### Markdown
st.title("Arishem mini simulator")

### Decks
col_deck_1, col_deck_2 = st.columns(2)

with col_deck_1:
    st.markdown("### Starting deck")
    starting_deck = []
    for sd in deck_index:
        sd_name = cards.iloc[sd]["name"]
        sd_url  = cards.iloc[sd]["url"]
        starting_deck.append(f"[{sd_name}]({sd_url})")
    st.markdown(", ".join(starting_deck))

with col_deck_2:
    st.markdown("### Arishem cards")
    new_cards = []
    for nc in new_cards_index:
        nc_name = cards.iloc[nc]["name"]
        nc_url  = cards.iloc[nc]["url"]
        new_cards.append(f"[{nc_name}]({nc_url})")
    st.markdown(", ".join(new_cards))


### Hands ###
st.markdown("### Card draws")

col_draw_1, col_draw_2 = st.columns([1, 5])
opening_cards = []
for op in range(0, 3):
    op_name = arishem_deck.iloc[op]["name"]
    op_url  = arishem_deck.iloc[op]["url"]
    opening_cards.append(f"[{op_name}]({op_url})")
opening_cards = ", ".join(opening_cards)
with col_draw_1:
    st.markdown("**Opening hand**")
with col_draw_2:
    st.markdown(f"{opening_cards}")


for draw in range(3, 10):
    turn = draw - 2
    draw_name = arishem_deck.iloc[draw]["name"]
    draw_url  = arishem_deck.iloc[draw]["url"]
    draw_card = f"[{draw_name}]({draw_url})"
    with col_draw_1:
        if turn == 7:
            st.markdown(f"**Turn {turn} (if any)**")
        else:
            st.markdown(f"**Turn {turn}**")
    with col_draw_2:
        st.markdown(f"{draw_card}")


not_drawn_cards = []
for not_drawn in range(10, len(arishem_deck.index)):
    nd_name = arishem_deck.iloc[not_drawn]["name"]
    nd_url = arishem_deck.iloc[not_drawn]["url"]
    not_drawn_cards.append(f"[{nd_name}]({nd_url})")
not_drawn_cards = ", ".join(not_drawn_cards)
with col_draw_1:
    st.markdown("**Not drawn**")
with col_draw_2:
    st.markdown(f"{not_drawn_cards}")
