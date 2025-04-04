import dash
from dash import html
import re

# Lire le fichier HTML téléchargé
with open("world_population.html", "r", encoding="utf-8") as file:
    html_content = file.read()

# Extraire le nombre de population avec une regex
match = re.search(r'<span class="rts-counter" rel="current_population">(.+?)</span>', html_content)

if match:
    population = match.group(1)
else:
    population = "Donnée non trouvée"

# Créer l'application Dash
app = dash.Dash(_name_)

# Définir la mise en page de l'application
app.layout = html.Div(children=[
    html.H1(children='Dashboard World Population'),

    html.Div(children=f'Population actuelle : {population}')
])

# Lancer le serveur
if _name_ == '_main_':
    app.run(debug=True)
