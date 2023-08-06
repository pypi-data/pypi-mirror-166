from functools import wraps

from .model import current_theme

def page_title(title: str):
    def decorator(view):
        @wraps(view)
        def decorated_function(*args, **kwargs):
            current_theme.set_page_title(title)
            return view(*args, **kwargs)

        return decorated_function
    return decorator

def menu_entry(entry: str, icon: str = None):
    def decorator(view):
        view._themes_menu = (entry, icon)
        return view
    return decorator

__all__ = ("page_title",)
