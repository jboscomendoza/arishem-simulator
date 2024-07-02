import random
import re
import pandas as pd
import pyarrow as arrow
import streamlit as st

icon_arishem = ":earth_africa:"
icon_deck    = ":heavy_check_mark:"

st.set_page_config(page_title="Arishem simulator", page_icon=icon_arishem)

arishem = [
    "Arishem",
    "At the start of the game, +1 Max Energy. Shuffle 12 random cards into your deck.",
    "https://snap.fan/cards/Arishem/"
]

separator = " / "

cards = pd.read_parquet("cards.parquet")
cards.loc[max(cards.index)+1] = arishem


### Markdown
hcol_1, hcol_2, hcol_3 = st.columns([0.5, 2, 0.5])
with hcol_2:
    st.image("arishem_simulator.png")


### Deck input
st.markdown("### Your deck code")
with st.form(key="deck"):
    deck_lines = st.text_area(label = "Paste all the rows starting with: # (Number) CardName")
    submit_button = st.form_submit_button(label="Submit deck")


if not deck_lines:
    st.stop()
if len(re.findall("\(\d\) (.*)", deck_lines)) == 0:
    st.error("Verify your deck code has rows like this:\n\n\# (1) Nova\n\n\# (2) Wolverine")
    st.stop()

### Deck processing
deck_names = re.findall("\(\d\) (.*)", deck_lines)
deck = cards[cards["name"].isin(deck_names)]
deck_index = deck.index.to_list()

new_cards_index = random.sample(cards.index.to_list(), k=12)
arishem_index = deck_index + new_cards_index

random.shuffle(arishem_index)
arishem_deck = cards.loc[arishem_index,:]


### Decks
col_deck_1, col_deck_2 = st.columns(2)

with col_deck_1:
    st.markdown("### Starting deck :heavy_check_mark:")
    starting_deck = []
    for sd in deck_index:
        sd_name = cards.iloc[sd]["name"]
        sd_url  = cards.iloc[sd]["url"]
        starting_deck.append(f"[{sd_name}]({sd_url})")
    st.markdown(separator.join(starting_deck))

with col_deck_2:
    st.markdown("### Arishem cards :earth_africa:")
    new_cards = []
    for nc in new_cards_index:
        nc_name = cards.iloc[nc]["name"]
        nc_url  = cards.iloc[nc]["url"]
        new_cards.append(f"[{nc_name}]({nc_url})")
    st.markdown(separator.join(new_cards))


### Button
st.button("Generate new Arishem cards and draws")


### Hands ###
st.markdown("### Card draws")

opening_cards = []
for op in range(0, 3):
    op_name = arishem_deck.iloc[op]["name"]
    op_url  = arishem_deck.iloc[op]["url"]
    icon = icon_deck if op_name in deck_names else icon_arishem
    opening_cards.append(f"[{op_name}]({op_url}){icon}")
opening_cards = separator.join(opening_cards)
st.markdown(f"**Opening hand**: {opening_cards}")


for draw in range(3, 10):
    turn = draw - 2
    draw_name = arishem_deck.iloc[draw]["name"]
    icon = icon_deck if draw_name in deck_names else icon_arishem
    draw_url  = arishem_deck.iloc[draw]["url"]
    draw_card = f"[{draw_name}]({draw_url}){icon}"
    if turn == 7:
        st.markdown(f"**Turn {turn} (if any)**: {draw_card}")
    else:
        st.markdown(f"**Turn {turn}**: {draw_card}")


not_drawn_cards = []
for not_drawn in range(10, len(arishem_deck.index)):
    nd_name = arishem_deck.iloc[not_drawn]["name"]
    icon = icon_deck if nd_name in deck_names else icon_arishem
    nd_url = arishem_deck.iloc[not_drawn]["url"]
    not_drawn_cards.append(f"[{nd_name}]({nd_url}){icon}")
not_drawn_cards = separator.join(not_drawn_cards)
st.markdown(f"**Not drawn**: {not_drawn_cards}")