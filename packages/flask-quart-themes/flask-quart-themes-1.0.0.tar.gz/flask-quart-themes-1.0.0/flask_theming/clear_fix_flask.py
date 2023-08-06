from flask import Flask

from .model import current_theme

def setup_clear_fix(_app: Flask):

    @_app.after_request
    def clear_fix(req):
        current_theme.clear_page_title()

        return req
