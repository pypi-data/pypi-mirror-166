import logging
import os
import platform
import traceback as tb
from abc import ABC
from enum import Enum, auto
from functools import wraps
from typing import Callable
from threading import Timer

import webview  # type: ignore


def traceback(method: Callable):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        try:
            self.logger.debug(f"{type(self).__name__}.{method.__name__}()")
            return method(self, *args, **kwargs)
        except Exception:  # pylint: disable=broad-except
            self.logger.exception(tb.format_exc())
            raise

    return wrapper


APP_WINDOW_TITLE = "UI Inspector"


class WindowState(Enum):
    CREATED = auto()
    SHOWN = auto()
    LOADED = auto()
    CLOSING = auto()
    CLOSED = auto()


class Bridge(ABC):
    # pylint: disable=too-few-public-methods
    def __init__(self, context):
        self.logger = logging.getLogger(__name__)
        self._window = None  # Injected after window creation
        self.ctx = context

    @property
    def window(self):
        return self._window

    def set_window(self, window):
        self._window = window

    @traceback
    def close(self):
        if self.window:
            self.window.close()


class Window(ABC):
    BRIDGE = Bridge
    DEFAULTS = {
        "title": "Title",
        "url": "index.html",
        "width": 640,
        "height": 480,
    }

    @classmethod
    def create(cls, context, **kwargs):
        options = dict(cls.DEFAULTS)
        options.update(kwargs)
        options.setdefault("title", APP_WINDOW_TITLE)
        options["url"] = os.path.join(context.entrypoint, options["url"])

        bridge = cls.BRIDGE(context)
        window = webview.create_window(js_api=bridge, **options)

        instance = cls(context, window, bridge)
        bridge.set_window(instance)

        return instance

    def __init__(self, context, window, bridge):
        self._context = context
        self._window = window
        self._bridge = bridge
        self._state = WindowState.CREATED

        # Attach event callbacks
        self._window.events.closed += self.on_closed
        self._window.events.closing += self.on_closing
        self._window.events.shown += self.on_shown
        self._window.events.loaded += self.on_loaded

        # MacOS closing flag
        self._force_closing = False

    def __getattr__(self, name):
        return getattr(self._window, name)

    @property
    def logger(self):
        return self._context.logger

    @property
    def state(self):
        return self._state

    @property
    def is_valid(self):
        return self.state not in (WindowState.CLOSING, WindowState.CLOSED)

    def close(self):
        Timer(0.2, self.destroy).start()

    def on_shown(self):
        self._state = WindowState.SHOWN

    def on_loaded(self):
        self._state = WindowState.LOADED

    def on_closing(self):
        self._state = WindowState.CLOSING

        if self._force_closing:
            return True
        elif platform.system() == "Darwin":
            self.logger.debug("Force closing window")
            self._force_closing = True
            self.close()
            return False
        else:
            return True

    def on_closed(self):
        self._state = WindowState.CLOSED
