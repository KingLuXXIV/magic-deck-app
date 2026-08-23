import random

import streamlit as st

st.set_page_config(page_title="Kartenspiel-Toolkit", page_icon="🃏", layout="wide")

MTG_START_LIFE = 20
YGO_START_LIFE = 8000

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

MANA_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800&family=Crimson+Pro:ital,wght@0,400;0,600;1,400&family=Orbitron:wght@500;700;900&family=Rajdhani:wght@500;600;700&display=swap');

/* ── Global ── */
:root {
    /* Platz für Streamlit-Header + Cloud-Leiste (Share, GitHub, …) */
    --toolbar-offset: 5.5rem;
}

.block-container {
    padding-top: calc(var(--toolbar-offset) + 0.75rem);
    max-width: 1100px;
}
.stApp { background: #080810; }

/* Tabs unter der fixen Streamlit-Leiste halten, nicht darunter verstecken */
.stTabs {
    margin-bottom: 0.5rem;
}
.stTabs [data-baseweb="tab-list"] {
    position: sticky;
    top: var(--toolbar-offset);
    z-index: 999;
    gap: 8px;
    background: #080810;
    border-radius: 14px;
    padding: 8px 6px;
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 4px 24px rgba(0,0,0,0.45);
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Rajdhani', sans-serif;
    font-weight: 700;
    font-size: 1rem;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    border-radius: 10px;
    padding: 10px 20px;
    color: #888;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(201,162,39,0.25), rgba(106,27,154,0.2)) !important;
    color: #f5e6c8 !important;
    border: 1px solid rgba(201,162,39,0.35) !important;
}

.stButton > button {
    font-family: 'Rajdhani', sans-serif;
    font-weight: 700;
    letter-spacing: 0.04em;
    border-radius: 8px;
    border: 1px solid rgba(255,255,255,0.12);
    background: linear-gradient(180deg, #2a2a3a 0%, #1a1a28 100%);
    color: #e8e8f0;
    transition: all 0.15s ease;
}
.stButton > button:hover {
    border-color: rgba(201,162,39,0.5);
    box-shadow: 0 0 12px rgba(201,162,39,0.2);
    color: #fff;
}
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #8b6914 0%, #c9a227 50%, #8b6914 100%);
    color: #1a1000;
    border: 1px solid #e8c547;
    font-weight: 800;
}
.stButton > button[kind="primary"]:hover {
    box-shadow: 0 0 20px rgba(201,162,39,0.45);
}

/* ── MTG ── */
.mtg-hero {
    font-family: 'Cinzel', serif;
    text-align: center;
    padding: 28px 24px 22px;
    margin-bottom: 24px;
    border-radius: 16px;
    background:
        radial-gradient(ellipse at 50% 0%, rgba(201,162,39,0.18) 0%, transparent 60%),
        linear-gradient(180deg, #1a1228 0%, #0f0a18 100%);
    border: 1px solid rgba(201,162,39,0.35);
    box-shadow: 0 8px 32px rgba(0,0,0,0.5), inset 0 1px 0 rgba(255,255,255,0.06);
    position: relative;
    overflow: hidden;
}
.mtg-hero::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 5px;
    background: linear-gradient(90deg, #F8F6D8, #0E68AB, #3A3A3A, #D3202A, #00733E);
}
.mtg-hero h1 {
    margin: 0;
    font-size: 1.75rem;
    font-weight: 800;
    background: linear-gradient(180deg, #f5e6c8 0%, #c9a227 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: 0.04em;
}
.mtg-hero p {
    font-family: 'Crimson Pro', serif;
    color: #a898c0;
    margin: 10px 0 14px;
    font-size: 1.05rem;
    font-style: italic;
}
.mana-bar { display: flex; justify-content: center; gap: 10px; }
.mana-gem {
    width: 28px; height: 28px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-family: 'Cinzel', serif;
    font-weight: 800;
    font-size: 0.75rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.5), inset 0 -2px 4px rgba(0,0,0,0.3);
    border: 2px solid rgba(255,255,255,0.25);
}

.mtg-section-title {
    font-family: 'Cinzel', serif;
    font-size: 1.15rem;
    font-weight: 700;
    color: #c9a227;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin: 28px 0 12px;
    padding-bottom: 8px;
    border-bottom: 1px solid rgba(201,162,39,0.25);
}
.mtg-player-header {
    font-family: 'Cinzel', serif;
    font-size: 1.1rem;
    font-weight: 700;
    padding: 10px 16px;
    border-radius: 10px;
    margin-bottom: 14px;
    letter-spacing: 0.05em;
}
.mtg-p1 { background: linear-gradient(90deg, rgba(14,104,171,0.35), transparent); border-left: 4px solid #0E68AB; color: #7eb8e8; }
.mtg-p2 { background: linear-gradient(90deg, rgba(211,32,42,0.35), transparent); border-left: 4px solid #D3202A; color: #f08080; }

.mtg-life-panel {
    border-radius: 16px;
    padding: 20px 22px 18px;
    margin-bottom: 14px;
    position: relative;
    overflow: hidden;
}
.mtg-life-panel::before {
    content: '❤';
    position: absolute;
    right: 16px; top: 12px;
    font-size: 2.5rem;
    opacity: 0.08;
}
.mtg-life-p1 {
    background: linear-gradient(145deg, #12182a 0%, #0a1020 100%);
    border: 2px solid rgba(14,104,171,0.6);
    box-shadow: 0 0 24px rgba(14,104,171,0.15), inset 0 0 40px rgba(14,104,171,0.05);
}
.mtg-life-p2 {
    background: linear-gradient(145deg, #2a1018 0%, #180810 100%);
    border: 2px solid rgba(211,32,42,0.6);
    box-shadow: 0 0 24px rgba(211,32,42,0.15), inset 0 0 40px rgba(211,32,42,0.05);
}
.mtg-life-label {
    font-family: 'Cinzel', serif;
    font-size: 0.85rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 6px;
}
.mtg-life-value {
    font-family: 'Cinzel', serif;
    font-size: 3.5rem;
    font-weight: 800;
    line-height: 1;
    text-shadow: 0 0 30px rgba(255,255,255,0.15);
}
.mtg-life-sub {
    font-family: 'Crimson Pro', serif;
    font-size: 0.85rem;
    color: #888;
    margin-top: 4px;
    font-style: italic;
}

/* ── Yu-Gi-Oh! ── */
.ygo-hero {
    font-family: 'Orbitron', sans-serif;
    text-align: center;
    padding: 28px 24px 22px;
    margin-bottom: 24px;
    border-radius: 4px;
    background:
        radial-gradient(ellipse at 50% 100%, rgba(106,27,154,0.35) 0%, transparent 55%),
        linear-gradient(180deg, #0a1628 0%, #050810 100%);
    border: 2px solid #c9a227;
    box-shadow: 0 0 40px rgba(106,27,154,0.25), inset 0 0 60px rgba(201,162,39,0.05);
    position: relative;
    clip-path: polygon(0 0, 100% 0, 100% calc(100% - 12px), calc(100% - 12px) 100%, 0 100%);
}
.ygo-hero h1 {
    margin: 0;
    font-size: 1.5rem;
    font-weight: 900;
    color: #ffd700;
    text-shadow: 0 0 20px rgba(255,215,0,0.5), 0 2px 0 #6a1b9a;
    letter-spacing: 0.08em;
}
.ygo-hero p {
    font-family: 'Rajdhani', sans-serif;
    color: #8899cc;
    margin: 10px 0 14px;
    font-size: 1rem;
    letter-spacing: 0.04em;
}
.ygo-ornament {
    display: flex; justify-content: center; align-items: center; gap: 12px;
    font-size: 1.2rem;
    color: #c9a227;
}
.ygo-ornament span { opacity: 0.7; }

.ygo-duel-field {
    background:
        repeating-linear-gradient(0deg, transparent, transparent 39px, rgba(201,162,39,0.04) 39px, rgba(201,162,39,0.04) 40px),
        repeating-linear-gradient(90deg, transparent, transparent 39px, rgba(201,162,39,0.04) 39px, rgba(201,162,39,0.04) 40px),
        linear-gradient(180deg, #0c1a30 0%, #060d18 100%);
    border: 1px solid rgba(201,162,39,0.2);
    border-radius: 8px;
    padding: 20px 16px;
    margin-bottom: 8px;
}

.ygo-life-panel {
    border-radius: 6px;
    padding: 18px 20px 16px;
    margin-bottom: 14px;
    position: relative;
    clip-path: polygon(8px 0, 100% 0, 100% calc(100% - 8px), calc(100% - 8px) 100%, 0 100%, 0 8px);
}
.ygo-life-p1 {
    background: linear-gradient(135deg, #0a2040 0%, #061018 100%);
    border: 2px solid #2196f3;
    box-shadow: 0 0 20px rgba(33,150,243,0.25), inset 0 0 30px rgba(33,150,243,0.08);
}
.ygo-life-p2 {
    background: linear-gradient(135deg, #2a0818 0%, #120610 100%);
    border: 2px solid #e91e63;
    box-shadow: 0 0 20px rgba(233,30,99,0.25), inset 0 0 30px rgba(233,30,99,0.08);
}
.ygo-life-label {
    font-family: 'Orbitron', sans-serif;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
}
.ygo-life-value {
    font-family: 'Orbitron', sans-serif;
    font-size: 2.8rem;
    font-weight: 900;
    line-height: 1;
}
.ygo-life-value .lp-unit {
    font-size: 1rem;
    font-weight: 700;
    opacity: 0.7;
    margin-left: 4px;
    vertical-align: super;
}
.ygo-life-sub {
    font-family: 'Rajdhani', sans-serif;
    font-size: 0.8rem;
    color: #668;
    margin-top: 4px;
    letter-spacing: 0.06em;
}
.ygo-vs {
    font-family: 'Orbitron', sans-serif;
    font-size: 1.4rem;
    font-weight: 900;
    color: #ffd700;
    text-align: center;
    text-shadow: 0 0 16px rgba(255,215,0,0.6);
    padding: 8px 0;
}

.mtg-card-frame {
    border-radius: 14px;
    overflow: hidden;
    margin-bottom: 18px;
    background: linear-gradient(180deg, #2a2240 0%, #1a1428 100%);
    border: 2px solid rgba(201,162,39,0.45);
    box-shadow: 0 6px 20px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.08);
}
.mtg-card-titlebar {
    padding: 10px 14px;
    display: flex;
    align-items: center;
    gap: 12px;
    font-family: 'Cinzel', serif;
    font-weight: 700;
    font-size: 1rem;
    background: linear-gradient(180deg, #2a2240 0%, #1e1830 100%);
    border-bottom: 1px solid rgba(201,162,39,0.3);
}
.mtg-card-titlebar-stripe {
    width: 5px;
    align-self: stretch;
    border-radius: 3px;
    flex-shrink: 0;
    min-height: 22px;
    box-shadow: 0 0 8px rgba(255,255,255,0.15);
}
.mtg-card-title {
    flex: 1;
    color: #f5e6c8;
    letter-spacing: 0.04em;
}
.mtg-card-titlebar-mana {
    display: flex;
    gap: 4px;
    flex-shrink: 0;
}
.mtg-card-body {
    display: flex;
    gap: 14px;
    padding: 14px 16px;
    align-items: center;
}
.mtg-card-art {
    width: 95px;
    border-radius: 6px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.5);
    border: 2px solid rgba(201,162,39,0.3);
}
.mtg-card-desc {
    font-family: 'Crimson Pro', serif;
    color: #b0a0c8;
    font-size: 0.9rem;
    line-height: 1.45;
    margin-bottom: 8px;
}
.mana-pill {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 12px;
    font-family: 'Cinzel', serif;
    font-size: 0.7rem;
    font-weight: 700;
    margin-right: 6px;
    border: 1px solid rgba(0,0,0,0.2);
}

.mtg-info-box {
    font-family: 'Crimson Pro', serif;
    padding: 16px 20px;
    border-radius: 12px;
    background: rgba(201,162,39,0.08);
    border: 1px dashed rgba(201,162,39,0.35);
    color: #a898c0;
    text-align: center;
    font-style: italic;
    margin: 12px 0;
}
</style>
"""

# Die 10 Themen-Decks aus der "Foundations Beginner Box" von Wizards of the Coast
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

MANA_GEMS = [
    ("W", "#F8F6D8", "#333"),
    ("U", "#0E68AB", "#fff"),
    ("B", "#3A3A3A", "#fff"),
    ("R", "#D3202A", "#fff"),
    ("G", "#00733E", "#fff"),
]


def _life_key(prefix: str) -> str:
    return f"{prefix}_life"


def init_life(prefix: str, start_life: int) -> None:
    if _life_key(prefix) not in st.session_state:
        st.session_state[_life_key(prefix)] = start_life


def change_life(prefix: str, delta: int) -> None:
    st.session_state[_life_key(prefix)] = max(0, st.session_state[_life_key(prefix)] + delta)


def reset_life(prefix: str, start_life: int) -> None:
    st.session_state[_life_key(prefix)] = start_life


def render_mtg_hero() -> None:
    gems = "".join(
        f"<div class='mana-gem' style='background:{bg}; color:{fg};'>{letter}</div>"
        for letter, bg, fg in MANA_GEMS
    )
    st.markdown(
        f"""
        <div class="mtg-hero">
            <h1>✦ Magic: The Gathering ✦</h1>
            <p>Deck-Auslosung &amp; Lebenstracker — Foundations Beginner Box</p>
            <div class="mana-bar">{gems}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_ygo_hero() -> None:
    st.markdown(
        """
        <div class="ygo-hero">
            <h1>⬡ DUEL MONSTERS ⬡</h1>
            <p>Yu-Gi-Oh! Lebenstracker — Standard-Duell</p>
            <div class="ygo-ornament">
                <span>☥</span> ◆ LP ◆ <span>☥</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_deck_card(deck: dict) -> str:
    """MTG-Kartenrahmen mit Manafarben und Scryfall-Artwork."""
    colors = deck["colors"]
    hexes = [COLOR_HEX[c] for c in colors]
    gradient = hexes[0] if len(hexes) == 1 else f"linear-gradient(90deg, {hexes[0]}, {hexes[1]})"

    mana_cost = "".join(
        f"<span class='mana-gem' style='width:22px;height:22px;font-size:0.65rem;"
        f"background:{COLOR_HEX[c]};color:{'#333' if c == 'W' else '#fff'};'>{c}</span>"
        for c in colors
    )
    pills = "".join(
        f"<span class='mana-pill' style='background:{COLOR_HEX[c]};"
        f"color:{'#333' if c == 'W' else '#fff'};'>{COLOR_NAME[c]}</span>"
        for c in colors
    )

    return f"""
    <div class="mtg-card-frame">
        <div class="mtg-card-titlebar">
            <div class="mtg-card-titlebar-stripe" style="background:{gradient};"></div>
            <span class="mtg-card-title">{deck['name']}</span>
            <span class="mtg-card-titlebar-mana">{mana_cost}</span>
        </div>
        <div class="mtg-card-body">
            <img class="mtg-card-art" src="{deck['image']}" alt="{deck['name']}" />
            <div style="flex:1;">
                <div class="mtg-card-desc">{deck['desc']}</div>
                <div>{pills}</div>
            </div>
        </div>
    </div>
    """


def render_mtg_life_display(prefix: str, player_num: int, start_life: int) -> None:
    init_life(prefix, start_life)
    life = st.session_state[_life_key(prefix)]
    panel_class = "mtg-life-p1" if player_num == 1 else "mtg-life-p2"
    label_color = "#7eb8e8" if player_num == 1 else "#f08080"
    value_color = "#e8f0ff" if player_num == 1 else "#ffe0e0"

    st.markdown(
        f"""
        <div class="mtg-life-panel {panel_class}">
            <div class="mtg-life-label" style="color:{label_color};">
                Spieler {player_num}
            </div>
            <div class="mtg-life-value" style="color:{value_color};">{life}</div>
            <div class="mtg-life-sub">Lebenspunkte · Start {start_life}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_ygo_life_display(prefix: str, player_num: int, start_life: int) -> None:
    init_life(prefix, start_life)
    life = st.session_state[_life_key(prefix)]
    panel_class = "ygo-life-p1" if player_num == 1 else "ygo-life-p2"
    label_color = "#64b5f6" if player_num == 1 else "#f48fb1"
    value_color = "#bbdefb" if player_num == 1 else "#fce4ec"

    st.markdown(
        f"""
        <div class="ygo-life-panel {panel_class}">
            <div class="ygo-life-label" style="color:{label_color};">
                Duellist {player_num}
            </div>
            <div class="ygo-life-value" style="color:{value_color};">
                {life:,}<span class="lp-unit">LP</span>
            </div>
            <div class="ygo-life-sub">LIFE POINTS · START {start_life:,}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_life_controls(
    prefix: str,
    start_life: int,
    deltas: tuple[int, ...],
    theme: str,
) -> None:
    minus_cols = st.columns(len(deltas))
    for col, delta in zip(minus_cols, reversed(deltas), strict=True):
        with col:
            st.button(
                f"−{delta:,}" if theme == "ygo" else f"−{delta}",
                key=f"{prefix}_minus_{delta}",
                on_click=change_life,
                args=(prefix, -delta),
                use_container_width=True,
            )

    plus_cols = st.columns(len(deltas))
    for col, delta in zip(plus_cols, deltas, strict=True):
        with col:
            st.button(
                f"+{delta:,}" if theme == "ygo" else f"+{delta}",
                key=f"{prefix}_plus_{delta}",
                on_click=change_life,
                args=(prefix, delta),
                use_container_width=True,
            )

    reset_label = f"↺ Reset · {start_life:,} LP" if theme == "ygo" else f"↺ Reset · {start_life} LP"
    st.button(
        reset_label,
        key=f"{prefix}_reset",
        on_click=reset_life,
        args=(prefix, start_life),
        use_container_width=True,
    )


def render_mtg_life_tracker(prefix: str, player_num: int, start_life: int, deltas: tuple[int, ...]) -> None:
    render_mtg_life_display(f"{prefix}_p{player_num}", player_num, start_life)
    render_life_controls(f"{prefix}_p{player_num}", start_life, deltas, "mtg")


def render_ygo_life_tracker(prefix: str, player_num: int, start_life: int, deltas: tuple[int, ...]) -> None:
    render_ygo_life_display(f"{prefix}_p{player_num}", player_num, start_life)
    render_life_controls(f"{prefix}_p{player_num}", start_life, deltas, "ygo")


def draw_decks():
    chosen = random.sample(DECKS, 4)
    st.session_state["player1_decks"] = chosen[:2]
    st.session_state["player2_decks"] = chosen[2:]


def render_mtg_section() -> None:
    render_mtg_hero()

    st.markdown(
        '<div class="mtg-section-title">⚔ Deck-Auslosung</div>',
        unsafe_allow_html=True,
    )

    col_btn, col_spacer = st.columns([1, 3])
    with col_btn:
        st.button("🎲 Decks auslosen", on_click=draw_decks, type="primary", use_container_width=True)

    if "player1_decks" in st.session_state and "player2_decks" in st.session_state:
        col1, col2 = st.columns(2, gap="large")

        with col1:
            st.markdown('<div class="mtg-player-header mtg-p1">Spieler 1</div>', unsafe_allow_html=True)
            for deck in st.session_state["player1_decks"]:
                st.markdown(render_deck_card(deck), unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="mtg-player-header mtg-p2">Spieler 2</div>', unsafe_allow_html=True)
            for deck in st.session_state["player2_decks"]:
                st.markdown(render_deck_card(deck), unsafe_allow_html=True)
    else:
        st.markdown(
            '<div class="mtg-info-box">Klicke auf <strong>Decks auslosen</strong>, '
            "um vier zufällige Decks zu ziehen — je zwei pro Spieler.</div>",
            unsafe_allow_html=True,
        )

    with st.expander("📚 Alle 10 Themen-Decks"):
        for deck in DECKS:
            st.markdown(render_deck_card(deck), unsafe_allow_html=True)

    st.markdown(
        '<div class="mtg-section-title">❤ Lebenstracker</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<p style="font-family:Crimson Pro,serif;color:#888;font-style:italic;margin-bottom:16px;">'
        f"Startwert {MTG_START_LIFE} Lebenspunkte · Standard-Format</p>",
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2, gap="large")
    with col1:
        render_mtg_life_tracker("mtg", 1, MTG_START_LIFE, (1, 5))
    with col2:
        render_mtg_life_tracker("mtg", 2, MTG_START_LIFE, (1, 5))


def render_yugioh_section() -> None:
    render_ygo_hero()

    st.markdown(
        """
        <div class="ygo-duel-field">
            <div style="font-family:'Orbitron',sans-serif;font-size:0.75rem;font-weight:700;
                letter-spacing:0.2em;color:#c9a227;text-align:center;margin-bottom:16px;">
                ◆ DUELL-FELD ◆
            </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col_vs, col2 = st.columns([5, 1, 5])
    with col1:
        render_ygo_life_tracker("ygo", 1, YGO_START_LIFE, (50, 100, 500))
    with col_vs:
        st.markdown('<div class="ygo-vs">VS</div>', unsafe_allow_html=True)
    with col2:
        render_ygo_life_tracker("ygo", 2, YGO_START_LIFE, (50, 100, 500))

    st.markdown("</div>", unsafe_allow_html=True)


st.markdown(MANA_CSS, unsafe_allow_html=True)

tab_mtg, tab_ygo = st.tabs(["🧙 Magic: The Gathering", "🐉 Yu-Gi-Oh!"])

with tab_mtg:
    render_mtg_section()

with tab_ygo:
    render_yugioh_section()
