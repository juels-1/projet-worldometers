#!/bin/bash

# Activer la timezone Paris
export TZ="Europe/Paris"

# Mettre à jour le fichier HTML avec le bon chemin Python
/home/ubuntu/projet-worldometers/venv/bin/python3 /home/ubuntu/projet-worldometers/Documents/projet-worldometers/scraper.py

# Fichier source
file="world_population.html"

# On extrait la section qui contient "Current World Population"
section=$(grep -A 30 "Current World Population" "$file")

# On récupère les chiffres de milliards, millions, milliers et unités et on enlève les zéros devant
billion=$(echo "$section" | grep -oP '(?<=<span class="rts-nr-int rts-nr-10e9">)[0-9]+' | head -n 1 | sed 's/^0*//')
million=$(echo "$section" | grep -oP '(?<=<span class="rts-nr-int rts-nr-10e6">)[0-9]+' | head -n 1 | sed 's/^0*//')
thousand=$(echo "$section" | grep -oP '(?<=<span class="rts-nr-int rts-nr-10e3">)[0-9]+' | head -n 1 | sed 's/^0*//')
unit=$(echo "$section" | grep -oP '(?<=<span class="rts-nr-int rts-nr-10e0">)[0-9]+' | head -n 1 | sed 's/^0*//')

# Forcer à zéro si vide
billion=${billion:-0}
million=${million:-0}
thousand=${thousand:-0}
unit=${unit:-0}

# On calcule la population totale
population=$((billion * 1000000000 + million * 1000000 + thousand * 1000 + unit))

# Timestamp actuel
timestamp=$(date +"%Y-%m-%d %H:%M:%S")

# On affiche le résultat
echo "Population at $timestamp: $population"

# On enregistre dans le CSV global utilisé par le dashboard
echo "$timestamp,$population" >> /home/ubuntu/population_data.csv
