from flask import Flask
from routes import routes

app = Flask(__name__)
app.config["DEBUG"] = True  # Only include this while you are testing your app

app.register_blueprint(routes)

if __name__ == '__main__':
    app.run()

