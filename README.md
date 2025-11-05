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
   - `detect_commands` (optional): List of binaries or absolute paths used to
     determine whether the desktop is installed. If omitted, the launcher
     infers commands from `command`.
   - `install_command` (optional): Shell command shown and executed from the
     Install screen for desktops that are missing.
   - `install_extras` (optional): Array of extra commands to offer after the
     main install (each item needs `name`, `command`, optional `description`).
   - `uninstall_command` (optional): Command invoked when uninstalling an
     installed desktop from the Install screen.
   - `uninstall_extras` (optional): Additional commands offered after the
     uninstall completes.
   - `description` (optional): Short blurb displayed next to the name.

Use `desktop_launcher.sample.json` as a template:

```json
{
  "desktops": [
    {
      "name": "Sway",
      "command": "sway",
      "session_type": "wayland",
      "detect_commands": ["sway"],
      "install_command": "sudo pacman -S --needed sway",
      "install_extras": [
        {
          "name": "Waybar",
          "command": "sudo pacman -S --needed waybar"
        }
      ],
      "uninstall_command": "sudo pacman -Rns sway",
      "uninstall_extras": [
        {
          "name": "Remove Waybar",
          "command": "sudo pacman -Rns waybar"
        }
      ],
      "description": "Wayland tiling compositor"
    },
    {
      "name": "Xfce",
      "command": "startx /usr/bin/startxfce4 -- :1 vt$XDG_VTNR",
      "session_type": "x11",
      "detect_commands": ["startxfce4"],
      "install_command": "sudo pacman -S --needed xfce4",
      "install_extras": [
        {
          "name": "Xfce Goodies",
          "command": "sudo pacman -S --needed xfce4-goodies"
        }
      ],
      "uninstall_command": "sudo pacman -Rns xfce4",
      "uninstall_extras": [
        {
          "name": "Remove Xfce Goodies",
          "command": "sudo pacman -Rns xfce4-goodies"
        }
      ],
      "description": "Launch Xfce in a dedicated Xorg session"
    }
  ]
}
```

The sample configuration file in this repository includes a larger Arch-oriented
set with pre-populated install/uninstall commands—adjust package names to suit
your distribution.

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

Run `desktop` from any terminal. The launcher offers three screens:

1. **Configured** – your curated list from the configuration file (favourites appear first).
2. **Detect** – highlights which configured desktops look installed based on `detect_commands`.
3. **Install** – shows desktops that expose an `install_command`, allowing you to run the
   command for missing environments directly from the launcher.

Key bindings:

- `↑`/`↓` or `k`/`j`: Move the selection.
- `Enter`: Launch the highlighted desktop (Configured/Detect) or confirm and run the install command, then choose optional extras (Install).
- `u`: Uninstall the selected desktop (Install screen) and optionally remove extras.
- `f`: Mark or unmark the selection as a favourite (persisted between runs).
- `s`: Cycle the session filter (`All → X11 → Wayland`).
- `d`: Refresh detection results.
- `1`, `2`, `3`: Jump between the Configured, Detect, and Install screens.
- `q`: Quit the launcher (the terminal is cleared on exit).

When a desktop is launched the script executes the associated command via the
user's shell, replacing the launcher process. After installing or uninstalling
you can opt into extra helper commands; the launcher then prompts you to press
Enter, refreshes detection results, and returns to the UI.
