import dash
from dash import html
import subprocess

# Exécuter le script extract_population.sh et récupérer la sortie
try:
    result = subprocess.run(['bash', 'extract_population.sh'], capture_output=True, text=True, check=True)
    population = result.stdout.strip()
except subprocess.CalledProcessError:
    population = "Erreur lors de l'extraction"

# Créer l'application Dash
app = dash.Dash(__name__)

# Définir la mise en page de l'application
app.layout = html.Div(children=[
    html.H1(children='Dashboard World Population'),

    html.Div(children=f'{population}')
])

# Lancer le serveur
if __name__ == '__main__':
    app.run(debug=True)

