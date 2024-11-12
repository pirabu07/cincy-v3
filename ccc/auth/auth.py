import functools
from flask import (Flask, Blueprint, flash, g, redirect,
                   render_template, request, session, url_for, jsonify, current_app)
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

import ccc.extensions as extensions

auth_bp = Blueprint("auth", __name__,
                    template_folder='templates',
                    static_folder='static')


def login_required(view):
    """View decorator that redirects anonymous users to the login page."""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        return view(**kwargs)

    return wrapped_view


@auth_bp.before_app_request
def load_logged_in_user():
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        conn = extensions.get_db()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT user_id,user_name,full_name,user_password FROM users WHERE user_id = %s", (user_id,))
        g.user = cursor.fetchone()


@auth_bp.route("/login", methods=("GET", "POST"))
def login():
    """Log in a registered user by adding the user id to the session."""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = extensions.get_db()
        error = None
        userCur = conn.cursor(dictionary=True)

        userCur.execute(
            "SELECT user_name, user_password, is_active FROM users WHERE user_name = %s", (
                username,)
        )
        user = userCur.fetchone()

        if user is None:
            error = "Incorrect username."
        elif not check_password_hash(user["user_password"], password):
            error = "Incorrect password."

        if error is None:
            # store the user id in a new session and return to the index
            session.clear()
            session["user_id"] = user["user_id"]
            session["full_name"] = user["full_name"]
            return redirect(url_for("index"))

        flash(error)

    return render_template('login.html',
                           title='CCC Login',
                           template='auth-template')


@auth_bp.route("/logout")
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for("index"))
