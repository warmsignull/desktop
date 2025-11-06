# Desktop Launcher

Desktop Launcher is a curses-based terminal UI that loads desktops from JSON,
lets you mark favourites, launches the selected session, detects installed
environments, and can run install/uninstall commands (including optional
extras) using your package manager override. Tested so far on Arch Linux.

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
   - `show_in_configured` (optional, default `true`): Set to `false` to hide the
     entry from the Configured screen while keeping it available for detection
     and install workflows.
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

You can also add an optional top-level `options` object:

```json
{
  "options": {
    "package_manager_override": "apt"
  },
  "desktops": [
    ...
  ]
}
```

The launcher auto-detects the package manager, but this override lets you pin
an explicit choice. You can manage the same setting through the Options screen.

## Installation

### Quick install (uses included scripts)

1. Clone or download this repository.
2. Run `./install` from the repository root. You will be prompted for root
   access; the helper scripts copy `desktop` to `/usr/local/bin/desktop` and
   install the sample configuration to `/etc/desktop_launcher.json`.
3. Open `/etc/desktop_launcher.json` and tailor the entries to your system.

### Manual install

1. Copy the `desktop` script to a directory on your `PATH` (for example
   `/usr/local/bin/desktop`) and make it executable (`chmod +x`).
2. Place a configuration file at `/etc/desktop_launcher.json` (or set
   `DESKTOP_LAUNCHER_CONFIG` to point elsewhere). You can start from
   `desktop_launcher.sample.json`.
3. Adjust permissions so all users that should launch desktops can read the
   config and execute the script.

### Runtime flags

- `desktop --config /path/to/config.json` – override the config file path.
- `DESKTOP_LAUNCHER_CONFIG=/path/to/config desktop` – environment override.
- `desktop --show-config-path` – print the resolved config path and exit.
- `DESKTOP_LAUNCHER_FAVORITES=/path/to/favourites.json desktop` – override the favourites store (defaults to `~/.config/desktop_launcher/favorites.json`).

## Usage

Run `desktop` from any terminal. The launcher offers four screens:

1. **Configured** – your curated list from the configuration file (favourites appear first).
2. **Detect** – highlights which configured desktops look installed based on `detect_commands`.
3. **Install** – shows desktops that expose an `install_command`, allowing you to run the
   command for missing environments directly from the launcher.
4. **Options** – view the auto-detected package manager, override it, or trigger a fresh detection.

Key bindings:

- `↑`/`↓` or `k`/`j`: Move the selection.
- `Enter`: Launch the highlighted desktop (Configured/Detect) or open the desktop menu to pick extras and run install/uninstall (Install). In the Options screen it applies the highlighted override.
- `u`: Uninstall the selected desktop (Install screen) and optionally remove extras.
- `f`: Mark or unmark the selection as a favourite (persisted between runs).
- `s`: Cycle the session filter (`All → X11 → Wayland`).
- `d`: Refresh detection results.
- `r`: Re-run package manager detection (Options screen).
- `1`, `2`, `3`, `4`: Jump between the Configured, Detect, Install, and Options screens.
- `q`: Quit the launcher (the terminal is cleared on exit).

When a desktop is launched the script executes the associated command via the
user's shell, replacing the launcher process. After installing or uninstalling
you can opt into extra helper commands; the launcher then prompts you to press
Enter, refreshes detection results, and returns to the UI.

## Development

Create an isolated environment with the provided Makefile:

```bash
make venv                 # creates .venv
make venv PIP_UPGRADE=1   # same as above but upgrades pip inside the venv
make deps        # installs dev requirements (optional, empty by default)
```

Activate the environment (`source .venv/bin/activate`) or run project commands
through `make`. For example, run the unit suite with:

```bash
make test
```
