# Flask / Quart themes

![License](https://img.shields.io/badge/License-Apache2-SUCCESS)
![Pypi](https://img.shields.io/pypi/v/flask-quart-themes)
![Python Versions](https://img.shields.io/badge/Python-3.8%20%7C%203.9%20%7C%203.10-blue)


Flask / Quart tools for creating themes.

## Install

```bash
> pip install flask-quart-themes
```

## Setup

### Flask

```python

from flask import Flask, render_template

from flask_theming.setup_flask import setup_flask_themes
from flask_theming.decorators_flask import page_title, menu_entry

app = Flask(__name__)

setup_flask_themes(app, title_default="Plak")

@page_title("Users zone")
@menu_entry("users::home")
def index():
    return render_template("user_home.html")

@page_title("Dashboard")
@menu_entry("dashboard", icon="fa fa-dashboard")
def dashboard():
    return render_template("dashboard.html")

```

> NOTE: This only works in Flask < 2.3!

### Quart

```python

from quart import Quart, render_template

from flask_theming.setup_quart import setup_quart_themes
from flask_theming.decorators_quart import page_title, menu_entry


app = Quart(__name__)
setup_quart_themes(app, title_default="Plak")

@page_title("Users zone")
@menu_entry("users::home")
async def user():
    return await render_template("user_home.html")

@page_title("Dashboard")
@menu_entry("dashboard", icon="fa fa-dashboard")
async def dashboard():
    return await render_template("dashboard.html")


```

## Jinja utils

### Title

```jinja2
<!DOCTYPE html>
<html lang="es">
<head>
    <title>{{ theme_title }}</title>
</head>

```

### Menu

```jinja2
<nav class="sidenav shadow-right sidenav-light">
    <div class="nav accordion" id="accordionSidenav">

        {% set dashboard = theme_menu.get_entry("dashboard") %}
        
        <a class="nav-link" href="{{ url_for(dashboard.path) }}">
            <!-- ########### -->
            <!-- IT WILL PRINT: 'fa fa-dashboard' -->
            <div class="nav-link-icon"><i class="{{ dashboard.icon }}"></i></div>
            <!-- ########### -->
            
            <!-- ########### -->
            <!-- IT WILL PRINT: 'dashboard' -->
            {{ dashboard.title }}
            <!-- ########### -->
        </a>
        
        <!-- User zone menu -->
        
        {% for menu in theme_menu.get_menu("users-zone") %}
        <a class="nav-link collapsed" data-bs-toggle="collapse" data-bs-target="#collapseDashboards" aria-expanded="false" aria-controls="collapseDashboards">
            <div class="nav-link-icon"><i data-feather="users"></i></div>
            
            <!-- ########### -->
            <!-- IT WILL PRINT: 'Users' -->
            {{ menu.header }}
            <!-- ########### -->
            
            <div class="sidenav-collapse-arrow"><i class="fas fa-angle-down"></i></div>
        </a>
        <div class="collapse" id="collapseDashboards" data-bs-parent="#accordionSidenav">
            <nav class="sidenav-menu-nested nav accordion" id="accordionSidenavPages">
                
                <!-- ########### -->
                <!-- IT WILL GET ALL 'Users' paths -->
                {% for entry in menu.entries %}
                    <a class="nav-link" href="{{ url_for(entry.path) }}">{{ entry.title }}</a>
                {% endfor %}
                <!-- ########### -->
                
            </nav>
        </div>
    {% endfor %}
     </div>
</nav>
{{ menu() }}
```
