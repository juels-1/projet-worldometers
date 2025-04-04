import dash
from dash import html
import re

# Crée l'application Dash
app = dash.Dash(__name__)

# Lis le fichier HTML récupéré avec Selenium
with open("world_population.html", "r", encoding="utf-8") as file:
    html_content = file.read()

# Utilise une regex pour extraire la population actuelle
match = re.search(r'Current World Population.*?<span class="rts-counter" rel="current_population">([\d,]+)', html_content)

# Si une correspondance est trouvée, on récupère le nombre, sinon on affiche un message d'erreur
if match:
    population = match.group(1)
else:
    population = "Donnée non trouvée"

# Crée le layout du dashboard
app.layout = html.Div(children=[
    html.H1(children='Dashboard World Population'),
    html.P(children=f'Population actuelle : {population}')
])

# Lance l'application Dash
if __name__ == '__main__':
    app.run(debug=True)

