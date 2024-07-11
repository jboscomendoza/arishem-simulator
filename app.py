import random
import re
import pandas as pd
import pyarrow as arrow
import streamlit as st


def create_link(index_value:int, dataframe:pd.DataFrame):
    "Builds a markdown link to snap.fam using the card data in a given dataframe."
    link_name = dataframe.iloc[index_value]["name"]
    link_url  = dataframe.iloc[index_value]["url"]
    link_text = f"[{link_name}]({link_url})"
    return link_text 


icon_arishem = ":earth_africa:"
icon_deck    = ":heavy_check_mark:"

st.set_page_config(page_title="Arishem simulator", page_icon=icon_arishem)

separator = " / "

cards = pd.read_parquet("cards.parquet")

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
        sd_link = create_link(sd, cards)
        starting_deck.append(sd_link)
    st.markdown(separator.join(starting_deck))

with col_deck_2:
    st.markdown("### Arishem cards :earth_africa:")
    new_cards = []
    for nc in new_cards_index:
        nc_link = create_link(nc, cards)
        new_cards.append(nc_link)
    st.markdown(separator.join(new_cards))


### Button
st.button("Generate new Arishem cards and draws")


### Hands ###
st.markdown("### Card draws")

opening_cards = []
for op in range(0, 3):
    op_link = create_link(op, arishem_deck)
    op_name = arishem_deck.iloc[op]["name"]
    icon = icon_deck if op_name in deck_names else icon_arishem
    opening_cards.append(op_link + f"{icon}")
opening_cards = separator.join(opening_cards)
st.markdown(f"**Opening hand**: {opening_cards}")


for draw in range(3, 10):
    turn = draw - 2
    op_link = create_link(draw, arishem_deck)
    draw_name = arishem_deck.iloc[draw]["name"]
    icon = icon_deck if draw_name in deck_names else icon_arishem
    draw_card = op_link + f"{icon}"
    if turn == 7:
        st.markdown(f"**Turn {turn} (if any)**: {draw_card}")
    else:
        st.markdown(f"**Turn {turn}**: {draw_card}")


not_drawn_cards = []
for not_drawn in range(10, len(arishem_deck.index)):
    nd_name = arishem_deck.iloc[not_drawn]["name"]
    nd_link = create_link(not_drawn, arishem_deck)
    icon = icon_deck if nd_name in deck_names else icon_arishem
    not_drawn_cards.append(nd_link + f"{icon}")
not_drawn_cards = separator.join(not_drawn_cards)
st.markdown(f"**Not drawn**: {not_drawn_cards}")