from .model import current_theme

def setup_jinja(_app):

    @_app.context_processor
    def inject_theme_title():
        return {'theme_title': current_theme.current_title}


    @_app.context_processor
    def inject_theme_menu():
        return {'theme_menu': current_theme.menu}
