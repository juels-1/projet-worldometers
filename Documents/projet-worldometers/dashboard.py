import dash
from dash import html, dcc
import pandas as pd
import subprocess

# Exécuter le script bash pour récupérer les nouvelles données
subprocess.run(["bash", "extract_population.sh"])

# Lire le fichier CSV
df = pd.read_csv("population_data.csv", names=["Timestamp", "Population"])

# Créer l'application Dash
app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='Dashboard World Population'),

    html.Div(children=f'Population actuelle : {df["Population"].iloc[-1]}'),

    dcc.Graph(
        id='population-graph',
        figure={
            'data': [
                {'x': df['Timestamp'], 'y': df['Population'], 'type': 'line', 'name': 'Population'}
            ],
            'layout': {
                'title': 'Évolution de la population mondiale'
            }
        }
    )
])

if __name__ == '__main__':
    app.run(debug=True)

