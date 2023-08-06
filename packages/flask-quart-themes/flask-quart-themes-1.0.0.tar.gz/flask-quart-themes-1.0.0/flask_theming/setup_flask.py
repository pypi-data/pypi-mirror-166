from flask import Flask, current_app

from .jinja import setup_jinja
from .model import current_theme
from .clear_fix_flask import setup_clear_fix

def setup_flask_themes(
        app: Flask,
        base_title: str = None,
        title_separator: str = "::",
        title_default: str = None,
):

    current_theme.init_app(
        app,
        base_title=base_title,
        title_default=title_default,
        title_separator=title_separator
    )
    setup_jinja(app)
    setup_clear_fix(app)

    @app.before_first_request
    def setup_menu():
        for bp, view in current_app.view_functions.items():
            if data := getattr(view, "_themes_menu", None):
                entry, icon = data
                current_theme.add_menu(entry, bp, icon)
                del view._themes_menu


__all__ = ("setup_flask_themes",)
