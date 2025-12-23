# Application entry point.
# Creates the Flask app instance using the factory and runs the server.

from app_factory import create_app

app = create_app()
app.config["PROPAGATE_EXCEPTIONS"] = True
app.run(host="0.0.0.0", port=5001, debug=True)