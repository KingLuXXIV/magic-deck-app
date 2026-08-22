# Magic: The Gathering – Deck-Auslosung

Streamlit-App, die aus den 10 Themen-Decks der Foundations Beginner Box
zufällig 4 Decks auslost – je 2 für Spieler 1 und Spieler 2, ohne Überschneidungen.

## Lokal starten

```bash
pip install -r requirements.txt
streamlit run magic_app.py
```

## Deployment (Streamlit Community Cloud)

1. Repository auf GitHub anlegen und `magic_app.py` + `requirements.txt` hochladen.
2. Auf [share.streamlit.io](https://share.streamlit.io) mit GitHub anmelden.
3. "Create app" → Repository, Branch `main` und Hauptdatei `magic_app.py` auswählen → "Deploy".
