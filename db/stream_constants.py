import json

with open('db/game_cats.json') as f:
    game_cats = json.load(f)
    sad_day = f"I can't find any FF6WC streams right now. In order for me to find streams, the title must reference " \
              f"FF6WC in some way.\n--------------------------------------------\nMy current keywords for the" \
              f" **Final Fantasy VI** category are:" \
              f" {', '.join(game_cats['858043689']['keywords'])}\n\nMy current keywords for the **Retro** category" \
              f" are: {', '.join(game_cats['27284']['keywords'])}"
