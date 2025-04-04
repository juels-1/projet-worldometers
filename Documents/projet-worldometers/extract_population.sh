#!/bin/bash

# Mettre à jour le fichier HTML
python scraper.py

# Fichier source
file="world_population.html"

# On extrait la section qui contient "Current World Population"
section=$(ggrep -A 30 "Current World Population" "$file")

# On récupère les chiffres de milliards, millions, milliers et unités
billion=$(echo "$section" | ggrep -oP '(?<=<span class="rts-nr-int rts-nr-10e9">)[0-9]+' | head -n 1)
million=$(echo "$section" | ggrep -oP '(?<=<span class="rts-nr-int rts-nr-10e6">)[0-9]+' | head -n 1)
thousand=$(echo "$section" | ggrep -oP '(?<=<span class="rts-nr-int rts-nr-10e3">)[0-9]+' | head -n 1)
unit=$(echo "$section" | ggrep -oP '(?<=<span class="rts-nr-int rts-nr-10e0">)[0-9]+' | head -n 1)

# On calcule la population totale
population=$((billion * 1000000000 + million * 1000000 + thousand * 1000 + unit))

# On affiche le résultat
timestamp=$(date +"%Y-%m-%d %H:%M:%S")
echo "Population at $timestamp: $population"

echo "$timestamp,$population" >> population_data.csv

