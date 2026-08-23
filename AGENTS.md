# AGENTS.md

## Cursor Cloud specific instructions

This repo is a single **Streamlit** web app (`magic_app.py`): a Magic: The Gathering deck-draw
tool (German UI) that randomly assigns 4 of 10 theme decks between two players. All state lives
in `st.session_state`; there is no database, backend API, or auth.

### Services

| Service | Command | Notes |
| --- | --- | --- |
| Streamlit dev server | `python3 -m streamlit run magic_app.py --server.headless true --server.port 8501` | The only process needed. Serves UI on port 8501 with hot reload. |

### Non-obvious notes

- Dependencies install to the user site (`~/.local/bin`), which is **not on `PATH`**. Invoke the
  CLI as `python3 -m streamlit ...` rather than bare `streamlit`.
- There are no tests, no linter config, and no build step in this repo. "Building" a Streamlit app
  just means running the dev server above.
- Deck card images load from the Scryfall CDN (`cards.scryfall.io`) at runtime. The draw logic
  works offline; only the images fail gracefully if egress is blocked.
- Health check: `curl -s http://localhost:8501/_stcore/health` returns `ok` once the server is up.
