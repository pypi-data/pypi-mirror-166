from __future__ import annotations

import hashlib
from collections import defaultdict

from typing import Dict, List
from dataclasses import dataclass, field


@dataclass
class FlaskThemeMenuEntry:
    path: str
    title: str
    icon: str = None

    _cached_id: str = None

    def make_id(self) -> str:
        if self._cached_id:
            return self._cached_id

        c = hashlib.md5(f"{self.path}{self.title}{self.icon or ''}").hexdigest()
        self._cached_id = c

        return c

    def is_menu(self) -> bool:
        return False

@dataclass
class FlaskThemeMenuHeader:
    header: str
    entries: List[FlaskThemeMenuEntry | FlaskThemeMenuHeader] = field(default_factory=list)

    def is_menu(self) -> bool:
        return True

class FlaskThemeMenu:

    def __init__(self):
        self._cached_entries = set()
        self._entries: Dict[str, List[FlaskThemeMenuHeader | FlaskThemeMenuEntry]] = defaultdict(list)

    @property
    def entries(self) -> List[FlaskThemeMenuHeader]:
        return list(self._entries.values())

    def get_menu(self, name: str) -> List[FlaskThemeMenuHeader]:
        return self._entries.get(name, [])

    def get_entry(self, name: str) -> FlaskThemeMenuEntry | None:
        try:
            return self._entries.get(name, None)[0]
        except IndexError:
            return None

    def add_entry(self, entry: str, url: str, icon: str):

        if entry in self._cached_entries:
            return

        # Parse the entry
        if "::" in entry:
            header, title = entry.split("::")
        else:
            header = None
            title = entry


        if header:

            entry_key = header.lower().strip().replace(" ", "-")

            fn = self._entries[entry_key].append

            # Parse_entries
            if "->" in title:
                # TODO: currently is limited to 2 levels
                ...
                # new_menu_header, submenu_title = title.split("->", maxsplit=1)
                #
                # submenu = FlaskThemeMenuHeader(
                #     header=header
                # )
                # submenu._entries[new_menu_header].append(FlaskThemeMenuEntry(
                # submenu.entries.append(FlaskThemeMenuEntry(
                #     submenu_title, url, icon
                # ))
                #
                # fn(submenu)

            else:
                menu = FlaskThemeMenuHeader(header)
                menu.entries.append(FlaskThemeMenuEntry(
                    title=title, path=url, icon=icon
                ))
                fn(menu)

        else:
            entry_key = title.lower().strip().replace(" ", "-")

            self._entries[entry_key].append(
                FlaskThemeMenuEntry(title=title, path=url, icon=icon)
            )

        self._cached_entries.add(entry)

class FlaskThemes:

    def __init__(self):
        self.app = None
        self.menu = FlaskThemeMenu()
        self.lateral_bar = []
        self.base_title = ""
        self.title_default = ""
        self.title_separator = " :: "
        self._current_title = None
        self._menu_entries = set()

    def init_app(self,
                 app, base_title: str = "",
                 title_separator: str = "::",
                 title_default=None,
                 menu_title: str = None):
        self.app = app
        self.base_title = base_title
        self.title_default = title_default
        self.title_separator = f" {title_separator.strip()} "
        self.menu.title = menu_title

    def set_page_title(self, title: str):
        self._current_title = title

    def clear_page_title(self):
        self._current_title = None

    @property
    def current_title(self) -> str:
        if self.base_title:
            prefix = f" {self.base_title} "
        else:
            prefix = ""

        if not self._current_title:
            return self.title_default

        else:
            return f"{prefix}{self.title_separator}{self._current_title}"

    def add_menu(self, entry: str, url: str, icon: str):
        self.menu.add_entry(entry, url, icon)

current_theme = FlaskThemes()

__all__ = ('current_theme', )
