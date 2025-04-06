import pandas as pd
import subprocess
import datetime

# Exécuter le script bash pour récupérer les nouvelles données
subprocess.run(["bash", "extract_population.sh"])

# Lire le fichier CSV
df = pd.read_csv("population_data.csv", names=["Timestamp", "Population"])

# Convertir Timestamp en datetime
df['Timestamp'] = pd.to_datetime(df['Timestamp'])

# Supprimer les lignes où la population est égale à 0
df = df[df['Population'] != 0]

# Récupérer la population actuelle
current_population = df["Population"].iloc[-1]

# Calculer la population à 20h hier
yesterday_20h = pd.Timestamp.now().normalize() - pd.Timedelta(days=1) + pd.Timedelta(hours=20)
pop_yesterday_20h = df[df['Timestamp'] <= yesterday_20h]['Population'].iloc[-1] if not df[df['Timestamp'] <= yesterday_20h].empty else "N/A"

# Calculer le pourcentage d'augmentation depuis hier à 20h
if pop_yesterday_20h != "N/A" and current_population != "N/A":
    population_increase_pct = ((current_population - pop_yesterday_20h) / pop_yesterday_20h) * 100
else:
    population_increase_pct = "N/A"

# Écrire le pourcentage dans un fichier texte
with open("population_increase_percentage.txt", "w") as f:
    if population_increase_pct != "N/A":
        f.write(f"{population_increase_pct:.4f}%")
    else:
        f.write("N/A")

print(f"Population à 20h hier: {pop_yesterday_20h}")
print(f"Pourcentage d'augmentation depuis 20h hier: {population_increase_pct:.4f}%" if population_increase_pct != "N/A" else "N/A")
