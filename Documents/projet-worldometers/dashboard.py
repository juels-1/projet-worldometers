import dash
from dash import html, dcc
import pandas as pd
from dash import dash_table
from dash.dependencies import Output, Input
import datetime

# Fonction pour charger les données à chaque mise à jour
def load_data():
    df = pd.read_csv("/home/ubuntu/population_data.csv", names=["Timestamp", "Population"])
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df = df[df['Population'] != 0]
    return df

# Initial load
df = load_data()

# Créer l'application Dash
app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='Dashboard World Population'),

    html.Div(id='current-population', children=f'Population actuelle : {df["Population"].iloc[-1]}'),

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

    dash_table.DataTable(
        id='daily-report-table',
        columns=[{"name": i, "id": i} for i in ["Population Actuelle", "Population il y a 5min", "Population il y a 10min", "Population à 20h hier", "Pourcentage d'augmentation depuis 20h hier"]],
        data=[{
            "Population Actuelle": df["Population"].iloc[-1],
            "Population il y a 5min": "N/A",
            "Population il y a 10min": "N/A",
            "Population à 20h hier": "N/A",
            "Pourcentage d'augmentation depuis 20h hier": "N/A"
        }],
        style_table={'marginTop': '40px', 'overflowX': 'auto'},
        style_cell={'textAlign': 'center', 'padding': '8px'},
        style_header={'backgroundColor': '#f2f2f2', 'fontWeight': 'bold'},
    ),

    dcc.Interval(
        id='interval-component',
        interval=5*60*1000,  # Toutes les 5 minutes
        n_intervals=0
    )
])

# Callback pour actualiser le dashboard
@app.callback(
    [Output('current-population', 'children'),
     Output('population-graph', 'figure'),
     Output('daily-report-table', 'data')],
    [Input('interval-component', 'n_intervals')]
)
def update_dashboard(n):
    df = load_data()

    current_population = f'Population actuelle : {df["Population"].iloc[-1]}'

    figure = {
        'data': [{'x': df['Timestamp'], 'y': df['Population'], 'type': 'line', 'name': 'Population'}],
        'layout': {'title': 'Évolution de la population mondiale'}
    }

    table_data = [{
        "Population Actuelle": df["Population"].iloc[-1],
        "Population il y a 5min": "N/A",
        "Population il y a 10min": "N/A",
        "Population à 20h hier": "N/A",
        "Pourcentage d'augmentation depuis 20h hier": "N/A"
    }]

    return current_population, figure, table_data

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
