import os
import unittest
from unittest.mock import patch

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

try:
    from PyQt6.QtWidgets import QApplication
    from ui import ConfirmBanner, MemoryOverlay, PermissionOverlay, PluginManagerOverlay, SetupOverlay
    QT_AVAILABLE = True
except Exception as error:  # pragma: no cover - environment-dependent
    QT_AVAILABLE = False
    QT_IMPORT_ERROR = str(error)


@unittest.skipUnless(QT_AVAILABLE, "PyQt6/offscreen platform unavailable")
class GuiSmokeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def test_core_overlays_construct(self):
        with patch("core.audio_devices.list_devices", return_value=[]):
            setup = SetupOverlay()
            permissions = PermissionOverlay()
            plugins = PluginManagerOverlay([])
            memory = MemoryOverlay()
            confirm = ConfirmBanner("Test confirmation", "No action will run.")

        self.assertGreaterEqual(len(setup._check_rows), 6)
        self.assertEqual(len(permissions._boxes), 6)
        self.assertIsNotNone(plugins)
        self.assertIsNotNone(memory)
        self.assertIsNotNone(confirm)

        for widget in (setup, permissions, plugins, memory, confirm):
            widget.deleteLater()


if __name__ == "__main__":
    unittest.main()
