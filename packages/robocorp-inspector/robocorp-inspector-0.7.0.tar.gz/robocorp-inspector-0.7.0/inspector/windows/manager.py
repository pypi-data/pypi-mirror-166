from pathlib import Path
from typing import List
from inspector.windows.base import Bridge, Window, traceback
from inspector.utils import IS_WINDOWS, SupportedInstances


class ManagerBridge(Bridge):
    """Javascript API bridge."""

    def path(self, length=32):
        # Return absolute path if short enough
        absolute = Path(self.ctx.database.path).resolve()
        if len(str(absolute)) <= length:
            return str(absolute)

        # Return partial path by removing parent directories
        parts = absolute.parts
        while parts:
            parts = parts[1:]
            shortened = str(Path("...", *parts))
            if len(shortened) <= length:
                return shortened

        # Return just filename or partial filename
        if len(absolute.name) > length:
            return "..." + absolute.name[-length:]
        else:
            return absolute.name

    def list(self):
        with self.ctx.database.lock:
            self.ctx.database.load()
            return self.ctx.database.list()

    @traceback
    def rename(self, before, after):
        with self.ctx.database.lock:
            self.ctx.database.load()
            locator = self.ctx.database.pop(before)
            self.ctx.database.update(after, locator)

    @traceback
    def add(self, kind):
        self.ctx.selected = None
        self.ctx.open_window(kind)

    @traceback
    def edit(self, name):
        locator = self.ctx.load_locator(name)
        if not locator:
            self.logger.error("No locator with name: %s", name)
            return

        self.ctx.selected = name
        self.ctx.open_window(locator["type"])

    @traceback
    def remove(self, name):
        with self.ctx.database.lock:
            self.ctx.database.delete(name)

    @traceback
    def list_supported_locators(self) -> List[str]:  # pylint: disable=no-self-use
        if IS_WINDOWS:
            return [
                SupportedInstances.MANAGER.value,
                SupportedInstances.BROWSER.value,
                SupportedInstances.IMAGE.value,
                SupportedInstances.RECORDER.value,
                SupportedInstances.WINDOWS.value,
            ]
        return [
            SupportedInstances.MANAGER.value,
            SupportedInstances.BROWSER.value,
            SupportedInstances.IMAGE.value,
            SupportedInstances.RECORDER.value,
        ]


class ManagerWindow(Window):
    BRIDGE = ManagerBridge
    DEFAULTS = {
        "url": "manager.html",
        "width": 450,
        "height": 900,
    }
