#!/bin/bash

hyprctl clients -j 2>/dev/null | jq -r '.[] | select(.class != "" and .class != "wofi" and .class != "waybar") | "\(.class)|\(.title)|\(.workspace.id)|\(.address)"' | while IFS='|' read -r class title workspace address; do
    if [ -n "$class" ]; then
        echo "$class|$title|$workspace|$address"
    fi
done
