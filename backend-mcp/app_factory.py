# APP FACTORY
# Initializes and configures the Flask application.

from flask import Flask
from flask_cors import CORS

def create_app():
    """
    Creates and configures the Flask application instance.

    Returns
    -------
    Flask
        The configured Flask app with registered routes and CORS enabled.
    """

    app = Flask(__name__)
    CORS(app)

    from controllers.intent_controller import register_routes
    register_routes(app)

    return app