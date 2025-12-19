#!/usr/bin/env python3
import json
import subprocess
import sys

# Icon mappings for common applications using Font Awesome / Nerd Font icons
ICON_MAP = {
    "alacritty": "󰆍",
    "kitty": "󰆍",
    "brave": "󰀈",
    "brave-browser": "󰀈",
    "firefox": "󰈹",
    "chromium": "󰊯",
    "code": "󰨞",
    "cursor": "󰨞",
    "cursor-code": "󰨞",
    "nautilus": "󰉋",
    "thunar": "󰉋",
    "pcmanfm": "󰉋",
    "gimp": "󰨞",
    "inkscape": "󰨞",
    "libreoffice": "󰈙",
    "libreoffice-writer": "󰈙",
    "libreoffice-calc": "󰈙",
    "libreoffice-impress": "󰈙",
    "spotify": "󰓇",
    "discord": "󰙯",
    "telegram": "󰍽",
    "slack": "󰒱",
    "thunderbird": "󰺻",
    "evolution": "󰺻",
    "gedit": "󰈔",
    "kate": "󰈔",
    "vim": "󰈔",
    "nvim": "󰈔",
    "neovim": "󰈔",
}

def get_icon(window_class):
    """Get icon for window class"""
    class_lower = window_class.lower()
    
    # Try direct match
    if class_lower in ICON_MAP:
        return ICON_MAP[class_lower]
    
    # Try without dots (for classes like "org.gnome.Terminal")
    if "." in class_lower:
        parts = class_lower.split(".")
        last_part = parts[-1].lower()
        if last_part in ICON_MAP:
            return ICON_MAP[last_part]
    
    # Try common patterns
    if "term" in class_lower or "terminal" in class_lower:
        return "󰆍"
    if "browser" in class_lower or "chrome" in class_lower:
        return "󰀈"
    if "editor" in class_lower or "code" in class_lower:
        return "󰨞"
    if "file" in class_lower or "manager" in class_lower:
        return "󰉋"
    
    # Default icon
    return "󰈔"

def get_windows():
    """Get all open windows from Hyprland"""
    try:
        result = subprocess.run(
            ["hyprctl", "clients", "-j"],
            capture_output=True,
            text=True,
            timeout=1
        )
        if result.returncode != 0:
            return []
        
        clients = json.loads(result.stdout)
        windows = []
        
        for client in clients:
            window_class = client.get("class", "")
            title = client.get("title", "")
            address = client.get("address", "")
            workspace_id = client.get("workspace", {}).get("id", 0)
            focused = client.get("focused", False)
            
            # Skip waybar, wofi, and empty classes
            if window_class.lower() in ["waybar", "wofi", ""]:
                continue
            
            icon = get_icon(window_class)
            windows.append({
                "class": window_class,
                "title": title,
                "address": address,
                "workspace": workspace_id,
                "focused": focused,
                "icon": icon
            })
        
        return sorted(windows, key=lambda x: (x["workspace"], x["class"]))
    except Exception as e:
        return []

def format_output(windows):
    """Format windows for Waybar display with icons"""
    if not windows:
        return ""
    
    output_parts = []
    for window in windows:
        focused = window["focused"]
        icon = window["icon"]
        address = window["address"]
        
        # Use Pango markup for styling
        if focused:
            output_parts.append(f'<span class="taskbar-active" weight="bold">{icon}</span>')
        else:
            output_parts.append(f'<span class="taskbar-inactive">{icon}</span>')
    
    return " ".join(output_parts)

if __name__ == "__main__":
    windows = get_windows()
    output = format_output(windows)
    print(output)
    sys.stdout.flush()
