import random

import streamlit as st

st.set_page_config(page_title="MTG Deck-Auslosung", page_icon="🧙", layout="wide")

# Farbcodes der 5 Magic-Farben (+ farblos) für die Deck-Boxen
COLOR_HEX = {
    "W": "#F8F6D8",
    "U": "#0E68AB",
    "B": "#3A3A3A",
    "R": "#D3202A",
    "G": "#00733E",
    "C": "#9C9C9C",
}

COLOR_NAME = {
    "W": "Weiß",
    "U": "Blau",
    "B": "Schwarz",
    "R": "Rot",
    "G": "Grün",
    "C": "Farblos",
}

# Die 10 Themen-Decks aus der "Foundations Beginner Box" von Wizards of the Coast
# (https://magic.wizards.com/en/news/feature/foundations-beginner-box-contents)
# Bildquelle: offizielle Scryfall-Kartenbilder der jeweiligen Theme-Karten (ffdn-Set)
DECKS = [
    {
        "name": "Cats",
        "colors": ["W"],
        "desc": "Furchtlose Katzen mit Erste-Schlag und Lebensverknüpfung",
        "image": "https://cards.scryfall.io/normal/front/9/6/96878faf-c0b3-4f4c-9a08-fe491494cbe6.jpg",
    },
    {
        "name": "Vampires",
        "colors": ["B"],
        "desc": "Blutrünstige Vampire, die Lebenspunkte stehlen",
        "image": "https://cards.scryfall.io/normal/front/5/3/53d253a5-76e6-469a-90d7-151ed73a5944.jpg",
    },
    {
        "name": "Healing",
        "colors": ["W"],
        "desc": "Lebenspunkte gewinnen und Kreaturen dauerhaft stärken",
        "image": "https://cards.scryfall.io/normal/front/4/5/45b36a77-b325-42fa-b45d-92f0614ccb31.jpg",
    },
    {
        "name": "Pirates",
        "colors": ["U"],
        "desc": "Freibeuter, die Karten ziehen und den Gegner ausrauben",
        "image": "https://cards.scryfall.io/normal/front/4/c/4c2b2f5d-9228-4d3d-bd9d-47a7095f4441.jpg",
    },
    {
        "name": "Wizards",
        "colors": ["U"],
        "desc": "Zauberkundige mit Kartenvorteil und cleveren Kontrollsprüchen",
        "image": "https://cards.scryfall.io/normal/front/e/2/e2ee90b6-f154-42a9-a918-d79085daa254.jpg",
    },
    {
        "name": "Undead",
        "colors": ["B"],
        "desc": "Untote Horden, die immer wieder aus dem Friedhof zurückkehren",
        "image": "https://cards.scryfall.io/normal/front/9/9/9992b42a-1129-4725-901a-62e275488990.jpg",
    },
    {
        "name": "Goblins",
        "colors": ["R"],
        "desc": "Chaotische Goblin-Schwärme mit blitzschnellen Angriffen",
        "image": "https://cards.scryfall.io/normal/front/5/c/5c83589b-44f2-44e4-8b60-3f9da7dce038.jpg",
    },
    {
        "name": "Inferno",
        "colors": ["R"],
        "desc": "Feuerspeiende Drachen und verheerender Flächenschaden",
        "image": "https://cards.scryfall.io/normal/front/0/2/02c3a185-8184-40e9-bba6-4b4dc5be5c1e.jpg",
    },
    {
        "name": "Elves",
        "colors": ["G"],
        "desc": "Elfische Manabeschleunigung und wachsende Kreaturenschwärme",
        "image": "https://cards.scryfall.io/normal/front/2/b/2b1f9edc-aa7b-4760-8cb7-393a103a1c78.jpg",
    },
    {
        "name": "Primal",
        "colors": ["G"],
        "desc": "Urgewaltige Bestien mit purer Kampfstärke",
        "image": "https://cards.scryfall.io/normal/front/3/3/3340946f-6492-42c6-bd01-57692486353f.jpg",
    },
]


def render_deck_card(deck: dict) -> str:
    """Erzeugt HTML für eine ansprechende Deck-Karte mit Farbbox und Kartengrafik."""
    colors = deck["colors"]
    hexes = [COLOR_HEX[c] for c in colors]
    gradient = hexes[0] if len(hexes) == 1 else f"linear-gradient(90deg, {hexes[0]} 0%, {hexes[1]} 100%)"

    pills = "".join(
        f"<span style='background:{COLOR_HEX[c]}; color:{'#000' if c == 'W' else '#fff'}; "
        f"padding:3px 10px; border-radius:12px; font-size:0.75rem; margin-right:6px; "
        f"border:1px solid rgba(0,0,0,0.15);'>{COLOR_NAME[c]}</span>"
        for c in colors
    )

    return f"""
    <div style="
        border-radius:14px;
        overflow:hidden;
        box-shadow:0 4px 12px rgba(0,0,0,0.15);
        margin-bottom:18px;
        background:#1e1e1e;
        border:1px solid rgba(255,255,255,0.08);
    ">
        <div style="height:10px; background:{gradient};"></div>
        <div style="display:flex; gap:14px; padding:14px 16px; align-items:center;">
            <img src="{deck['image']}" style="width:90px; border-radius:8px; box-shadow:0 2px 8px rgba(0,0,0,0.4);" />
            <div style="flex:1;">
                <div style="font-size:1.15rem; font-weight:700; color:#fafafa; margin-bottom:4px;">
                    {deck['name']}
                </div>
                <div style="color:#b8b8b8; font-size:0.85rem; margin-bottom:8px;">
                    {deck['desc']}
                </div>
                <div>{pills}</div>
            </div>
        </div>
    </div>
    """


def draw_decks():
    """Wählt 4 der 10 Decks ohne Überschneidung und verteilt je 2 an jeden Spieler."""
    chosen = random.sample(DECKS, 4)
    st.session_state["player1_decks"] = chosen[:2]
    st.session_state["player2_decks"] = chosen[2:]


st.title("🧙 Magic: The Gathering – Deck-Auslosung")
st.caption(
    "Die 10 Themen-Decks der Foundations Beginner Box werden gemischt – "
    "4 zufällige Decks werden gezogen, je 2 pro Spieler, ganz ohne Überschneidungen."
)

st.button("🎲 Decks auslosen", on_click=draw_decks, type="primary", use_container_width=False)

st.divider()

if "player1_decks" in st.session_state and "player2_decks" in st.session_state:
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.subheader("🔵 Spieler 1")
        for deck in st.session_state["player1_decks"]:
            st.markdown(render_deck_card(deck), unsafe_allow_html=True)

    with col2:
        st.subheader("🔴 Spieler 2")
        for deck in st.session_state["player2_decks"]:
            st.markdown(render_deck_card(deck), unsafe_allow_html=True)
else:
    st.info("Klicke auf **Decks auslosen**, um die Decks für beide Spieler zu ziehen.")

with st.expander("📚 Alle verfügbaren Decks anzeigen"):
    for deck in DECKS:
        st.markdown(render_deck_card(deck), unsafe_allow_html=True)
