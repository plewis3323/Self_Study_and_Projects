#!/bin/bash 

for pdf in /home/plewis/towerslope/tower_Rhich_Trials/*.pdf; do
    base=$(basename "$pdf" .pdf)
    convert "$pdf" "/home/plewis/towerslope/tower_Rhich_Trials/${base}.png"
done
O

