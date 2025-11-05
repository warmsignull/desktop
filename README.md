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
   - `session_type`: Either `x11` or `wayland`, used for the session filter.
   - `description` (optional): Short blurb displayed next to the name.

Use `desktop_launcher.sample.json` as a template:

```json
{
  "desktops": [
    {
      "name": "Sway",
      "command": "sway --unsupported-gpu",
      "session_type": "wayland",
      "description": "Wayland tiling compositor (forces unsupported GPU mode)"
    },
    {
      "name": "Hyprland",
      "command": "Hyprland",
      "session_type": "wayland",
      "description": "Dynamic tiling Wayland compositor"
    },
    {
      "name": "GNOME (Wayland Shell)",
      "command": "env GNOME_SESSION_DISABLE_USER_SYSTEMD=1 XDG_SESSION_TYPE=wayland dbus-run-session -- gnome-shell --wayland",
      "session_type": "wayland",
      "description": "Launch GNOME Shell directly on Wayland (minimal session)"
    },
    {
      "name": "Xfce",
      "command": "startx /usr/bin/startxfce4 -- :1 vt$XDG_VTNR",
      "session_type": "x11",
      "description": "Launch Xfce in a dedicated Xorg session"
    },
    {
      "name": "MATE",
      "command": "startx /usr/bin/mate-session -- :2 vt$XDG_VTNR",
      "session_type": "x11",
      "description": "Start the MATE desktop in its own Xorg server"
    },
    {
      "name": "Cinnamon",
      "command": "startx /usr/bin/cinnamon-session -- :3 vt$XDG_VTNR",
      "session_type": "x11",
      "description": "Start Cinnamon desktop on a separate Xorg display"
    },
    {
      "name": "KDE Plasma (Wayland)",
      "command": "env XDG_SESSION_TYPE=wayland QT_QPA_PLATFORM=wayland dbus-run-session -- startplasma-wayland",
      "session_type": "wayland",
      "description": "Run KDE Plasma on Wayland via dbus-run-session"
    },
    {
      "name": "Enlightenment (X11)",
      "command": "startx /usr/bin/enlightenment_start -- :9 vt$XDG_VTNR",
      "session_type": "x11",
      "description": "Start Enlightenment in a dedicated Xorg session"
    },
    {
      "name": "LXQt",
      "command": "startx /usr/bin/startlxqt -- :4 vt$XDG_VTNR",
      "session_type": "x11",
      "description": "Start LXQt desktop in a dedicated Xorg session"
    },
    {
      "name": "LXDE",
      "command": "startx /usr/bin/startlxde -- :5 vt$XDG_VTNR",
      "session_type": "x11",
      "description": "Launch LXDE on its own Xorg display"
    },
    {
      "name": "IceWM",
      "command": "startx /usr/bin/icewm-session -- :6 vt$XDG_VTNR",
      "session_type": "x11",
      "description": "Start IceWM session via startx"
    },
    {
      "name": "Openbox",
      "command": "startx /usr/bin/openbox-session -- :7 vt$XDG_VTNR",
      "session_type": "x11",
      "description": "Launch Openbox session using startx"
    },
    {
      "name": "labwc",
      "command": "env XDG_SESSION_TYPE=wayland dbus-run-session -- labwc",
      "session_type": "wayland",
      "description": "Run labwc Wayland compositor under dbus-run-session"
    },
    {
      "name": "i3",
      "command": "startx /usr/bin/i3 -- :8 vt$XDG_VTNR",
      "session_type": "x11",
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
- `DESKTOP_LAUNCHER_FAVORITES=/path/to/favourites.json desktop` – override the favourites store (defaults to `~/.config/desktop_launcher/favorites.json`).

## Usage

Run `desktop` from any terminal. The launcher renders favourites first, followed
by the full list of desktops. Key bindings:

- `↑`/`↓` or `k`/`j`: Move the selection.
- `Enter`: Launch the highlighted desktop.
- `f`: Mark or unmark the selection as a favourite (persisted between runs).
- `s`: Cycle the session filter (`All → X11 → Wayland`).
- `q`: Quit the launcher (the terminal is cleared on exit).

When a desktop is selected the script executes the associated command via the
user's shell, replacing the launcher process.
