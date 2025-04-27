from flask import Flask
from routes import routes
from flask_cors import CORS
import os

app = Flask(__name__)
# app.config["DEBUG"] = True  # Only include this while you are testing your app
CORS(app)

app.register_blueprint(routes)

@app.route("/")
def hello_world():
    return "Hello, World!"

port = int(os.environ.get("PORT", 8000))
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)
