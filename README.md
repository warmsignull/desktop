# Desktop Launcher

`desktop` is a curses-based launcher for desktop environments. It reads from a
single JSON configuration file, displays the configured options in a
scrollable list, and replaces itself with the selected desktop command.

## Configuration

1. Place a JSON file at `/etc/desktop_launcher.json` (or point
   `DESKTOP_LAUNCHER_CONFIG` to a different path).
2. Add a top-level `desktops` array where each item contains:
   - `name`: Human-readable label shown in the UI.
   - `command`: Command executed to start the desktop environment.
   - `description` (optional): Short blurb displayed next to the name.

Use `desktop_launcher.sample.json` as a template:

```json
{
  "desktops": [
    {
      "name": "Sway",
      "command": "sway --unsupported-gpu",
      "description": "Wayland tiling compositor (forces unsupported GPU mode)"
    },
    {
      "name": "Hyprland",
      "command": "Hyprland",
      "description": "Dynamic tiling Wayland compositor"
    },
    {
      "name": "GNOME (Wayland Shell)",
      "command": "env GNOME_SESSION_DISABLE_USER_SYSTEMD=1 XDG_SESSION_TYPE=wayland dbus-run-session -- gnome-shell --wayland",
      "description": "Launch GNOME Shell directly on Wayland (minimal session)"
    },
    {
      "name": "Xfce",
      "command": "startx /usr/bin/startxfce4 -- :1 vt$XDG_VTNR",
      "description": "Launch Xfce in a dedicated Xorg session"
    },
    {
      "name": "MATE",
      "command": "startx /usr/bin/mate-session -- :2 vt$XDG_VTNR",
      "description": "Start the MATE desktop in its own Xorg server"
    },
    {
      "name": "Cinnamon",
      "command": "startx /usr/bin/cinnamon-session -- :3 vt$XDG_VTNR",
      "description": "Start Cinnamon desktop on a separate Xorg display"
    },
    {
      "name": "KDE Plasma (Wayland)",
      "command": "env XDG_SESSION_TYPE=wayland QT_QPA_PLATFORM=wayland dbus-run-session -- startplasma-wayland",
      "description": "Run KDE Plasma on Wayland via dbus-run-session"
    },
    {
      "name": "Enlightenment (E27+)",
      "command": "env E_START_WAYLAND=1 XDG_SESSION_TYPE=wayland dbus-run-session -- enlightenment_start",
      "description": "Launch Enlightenment on Wayland"
    },
    {
      "name": "LXQt",
      "command": "startx /usr/bin/startlxqt -- :4 vt$XDG_VTNR",
      "description": "Start LXQt desktop in a dedicated Xorg session"
    },
    {
      "name": "LXDE",
      "command": "startx /usr/bin/startlxde -- :5 vt$XDG_VTNR",
      "description": "Launch LXDE on its own Xorg display"
    },
    {
      "name": "IceWM",
      "command": "startx /usr/bin/icewm-session -- :6 vt$XDG_VTNR",
      "description": "Start IceWM session via startx"
    },
    {
      "name": "Openbox",
      "command": "startx /usr/bin/openbox-session -- :7 vt$XDG_VTNR",
      "description": "Launch Openbox session using startx"
    },
    {
      "name": "labwc",
      "command": "env XDG_SESSION_TYPE=wayland dbus-run-session -- labwc",
      "description": "Run labwc Wayland compositor under dbus-run-session"
    },
    {
      "name": "i3",
      "command": "startx /usr/bin/i3 -- :8 vt$XDG_VTNR",
      "description": "Start i3 window manager on a dedicated Xorg server"
    }
  ]
}
```

## Installation

1. Copy the `desktop` script to a location on the system-wide `PATH` (for
   example `/usr/local/bin/desktop`) and make it executable.
2. Ensure all users have read access to the configuration file.

The script also accepts:

- `desktop --config /path/to/config.json` – override the config file path.
- `DESKTOP_LAUNCHER_CONFIG=/path/to/config desktop` – environment override.
- `desktop --show-config-path` – print the resolved config path and exit.

## Usage

Run `desktop` from any terminal. Navigate with the arrow keys (or `j`/`k`),
press Enter to launch the highlighted desktop, or `q` to quit. When a desktop
is selected the script executes the associated command via the user's shell,
replacing the launcher process.
