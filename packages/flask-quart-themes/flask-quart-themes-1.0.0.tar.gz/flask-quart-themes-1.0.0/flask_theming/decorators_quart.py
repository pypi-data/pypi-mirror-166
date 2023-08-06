from functools import wraps

from quart import url_for, request

from .model import current_theme


def page_title(page_title: str):
    def decorator(view):
        @wraps(view)
        async def decorated_function(*args, **kwargs):
            current_theme.set_page_title(page_title)
            return await view(*args, **kwargs)

        return decorated_function
    return decorator

def menu_entry(entry: str, icon: str = None):
    def decorator(view):
        view._themes_menu = (entry, icon)
        return view
    return decorator

__all__ = ("page_title",)
