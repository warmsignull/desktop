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
      "name": "GNOME",
      "command": "dbus-launch gnome-session",
      "description": "Default GNOME Shell session"
    },
    {
      "name": "Xfce",
      "command": "startxfce4",
      "description": "Lightweight Xfce desktop"
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
