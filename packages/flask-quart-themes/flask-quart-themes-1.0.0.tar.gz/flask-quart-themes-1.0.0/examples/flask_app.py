from flask import Flask

from flask_theming.setup_flask import setup_flask_themes
from flask_theming.decorators_flask import page_title, menu_entry

app = Flask(__name__)
setup_flask_themes(app, base_title="Plak")

@app.route('/')
@page_title("Main Index")
@menu_entry("Index::home")
def index():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(threaded=False)
