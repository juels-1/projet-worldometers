import dash
from dash import html, dcc
import pandas as pd
import subprocess
import datetime
import numpy as np
from dash import dash_table

# Exécuter le script bash pour récupérer les nouvelles données
subprocess.run(["bash", "extract_population.sh"])

# Lire le fichier CSV
df = pd.read_csv("population_data.csv", names=["Timestamp", "Population"])

# Convertir Timestamp en datetime
df['Timestamp'] = pd.to_datetime(df['Timestamp'])

# Supprimer les lignes où la population est égale à 0
df = df[df['Population'] != 0]

# Filtrer les données du jour
today = pd.Timestamp.now().normalize()
df_today = df[df['Timestamp'] >= today]

# Récupérer la population actuelle (dernière valeur de la journée)
current_population = df["Population"].iloc[-1]

# Récupérer la population il y a 5 minutes
five_minutes_ago = pd.Timestamp.now() - pd.Timedelta(minutes=5)
pop_5min = df[df['Timestamp'] <= five_minutes_ago]['Population'].iloc[-1] if not df[df['Timestamp'] <= five_minutes_ago].empty else "N/A"

# Récupérer la population il y a 10 minutes
ten_minutes_ago = pd.Timestamp.now() - pd.Timedelta(minutes=10)
pop_10min = df[df['Timestamp'] <= ten_minutes_ago]['Population'].iloc[-1] if not df[df['Timestamp'] <= ten_minutes_ago].empty else "N/A"

# Calculer la population à 20h hier
yesterday_20h = pd.Timestamp.now().normalize() - pd.Timedelta(days=1) + pd.Timedelta(hours=20)
pop_yesterday_20h = df[df['Timestamp'] <= yesterday_20h]['Population'].iloc[-1] if not df[df['Timestamp'] <= yesterday_20h].empty else "N/A"

# Calculer le pourcentage d'augmentation depuis hier à 20h
if pop_yesterday_20h != "N/A" and current_population != "N/A":
    population_increase_pct = ((current_population - pop_yesterday_20h) / pop_yesterday_20h) * 100
else:
    population_increase_pct = "N/A"

# Créer les statistiques à afficher dans le tableau
daily_stats = pd.DataFrame([{
    "Population Actuelle": current_population,
    "Population il y a 5min": pop_5min,
    "Population il y a 10min": pop_10min,
    "Population à 20h hier": pop_yesterday_20h if pop_yesterday_20h != "N/A" else "N/A",
    "Pourcentage d'augmentation depuis 20h hier": f"{population_increase_pct:.4f}%" if population_increase_pct != "N/A" else "N/A"
}])

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
    ),

    # Tableau de rapport quotidien
    dash_table.DataTable(
        id='daily-report-table',
        columns=[{"name": i, "id": i} for i in daily_stats.columns],
        data=daily_stats.to_dict('records'),
        style_table={'marginTop': '40px', 'overflowX': 'auto'},
        style_cell={'textAlign': 'center', 'padding': '8px'},
        style_header={'backgroundColor': '#f2f2f2', 'fontWeight': 'bold'},
    )
])

if __name__ == '__main__':
    app.run(debug=True)
