import curses
import unittest
from importlib.machinery import SourceFileLoader
from pathlib import Path


def load_desktop_module():
    loader = SourceFileLoader("desktop_module", str(Path(__file__).resolve().parents[1] / "desktop"))
    return loader.load_module()


class FakeWindow:
    def __init__(self, height: int, width: int, inputs):
        self._height = height
        self._width = width
        self._inputs = list(inputs)

    def getmaxyx(self):
        return self._height, self._width

    def erase(self):
        pass

    def addstr(self, y, x, text, attr=0):
        if y < 0 or y >= self._height:
            raise curses.error("addstr() returned ERR")

    def refresh(self):
        pass

    def getch(self):
        if self._inputs:
            return self._inputs.pop(0)
        raise RuntimeError("FakeWindow input exhausted")


class DesktopUITests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.desktop = load_desktop_module()

    def test_options_screen_handles_small_terminal(self):
        package_state = {"detected": None, "override": None, "effective": None}
        window = FakeWindow(height=6, width=20, inputs=[ord("q")])

        next_screen, cursor = self.desktop.options_screen(
            window, Path("/tmp/config.json"), package_state, lambda: None, 0
        )

        self.assertEqual(next_screen, "exit")
        self.assertEqual(cursor, 0)

    def test_action_detail_menu_handles_small_terminal_with_extras(self):
        extras = tuple(
            self.desktop.CommandExtra(
                name=f"Extra {idx}",
                command=self.desktop.CommandSpec({"default": f"echo extra{idx}"}),
                description="optional",
            )
            for idx in range(1, 4)
        )
        entry = self.desktop.DesktopEntry(
            name="Test Desktop",
            command="start-desktop",
            session_type="x11",
            detect_commands=(),
            install_command=self.desktop.CommandSpec({"default": "echo install"}),
            install_extras=extras,
            uninstall_command=None,
            uninstall_extras=(),
            show_in_configured=True,
            description=None,
        )
        window = FakeWindow(
            height=5,
            width=25,
            inputs=[curses.KEY_DOWN, curses.KEY_DOWN, curses.KEY_DOWN, 10],
        )

        confirmed, primary, selected_extras = self.desktop.action_detail_menu(
            window, entry, "install", "default"
        )

        self.assertTrue(confirmed)
        self.assertEqual(primary, "echo install")
        self.assertEqual(selected_extras, ())


if __name__ == "__main__":
    unittest.main()
