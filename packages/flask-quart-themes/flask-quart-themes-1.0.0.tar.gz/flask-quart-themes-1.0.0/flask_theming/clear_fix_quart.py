from quart import Quart

from .model import current_theme

def setup_clear_fix(_app: Quart):

    @_app.after_request
    async def clear_fix(request):
        current_theme.clear_page_title()

        return request
