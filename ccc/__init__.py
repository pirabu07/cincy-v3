import os

import pymysql
import ccc.extensions as extensions
from flask import Flask, jsonify
from flask_cors import CORS


def create_app():
    # Create and configure the app.
    app = Flask(__name__, instance_relative_config=True)
    cors = CORS(app, resources=r'/*')
    app.config.from_mapping(SECRET_KEY='dev')

    from .auth import auth
    from .home import home

    # Register Blueprints

    app.register_blueprint(home.home_bp)
    app.register_blueprint(auth.auth_bp)

    @app.route('/testDBConnection')
    def hello():
        """Test database connection and return list of users."""
        conn = extensions.get_db()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT user, host FROM mysql.user")
            users = cursor.fetchall()
            if users:
                for row in users:
                    print(row)
                return jsonify(users)
        except Exception as e:
            return jsonify({"error": str(e)})
        finally:
            cursor.close()
            conn.close()
    return app
