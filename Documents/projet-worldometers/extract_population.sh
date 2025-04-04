#!/bin/bash

# Fichier source
file="world_population.html"

# On extrait la section qui contient "Current World Population"
section=$(ggrep -A 30 "Current World Population" "$file")

# On récupère les chiffres de milliards, millions, milliers et unités
billion=$(echo "$section" | ggrep -oP '(?<=<span class="rts-nr-int rts-nr-10e9">)[0-9]+' | head -n 1)
million=$(echo "$section" | ggrep -oP '(?<=<span class="rts-nr-int rts-nr-10e6">)[0-9]+' | head -n 1)
thousand=$(echo "$section" | ggrep -oP '(?<=<span class="rts-nr-int rts-nr-10e3">)[0-9]+' | head -n 1)
unit=$(echo "$section" | ggrep -oP '(?<=<span class="rts-nr-int rts-nr-10e0">)[0-9]+' | head -n 1)

# On assemble tout ça pour obtenir la population totale
population="${billion}${million}${thousand}${unit}"

# On affiche le résultat
echo "Current World Population: $population"

