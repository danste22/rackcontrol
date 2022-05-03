from flask import (
    Blueprint, render_template
)

bp = Blueprint('console', __name__, url_prefix='/console')


@bp.route('/')
def settings_page():
    return render_template('console.html')
