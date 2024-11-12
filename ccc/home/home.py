from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from flask import current_app as app


# Blueprint Configuration
home_bp = Blueprint(
    'home_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


@home_bp.route('/', methods=['GET'])
def home():
    """Homepage."""
    return render_template(
        'index.html',
        title='Home',
        template='home-template'
    )
