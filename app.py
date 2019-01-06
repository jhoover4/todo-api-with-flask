from flask import Flask, render_template

import config
import models
from resources.todos import todos_api
from resources.users import users_api

app = Flask(__name__)
app.register_blueprint(todos_api)
app.register_blueprint(users_api)


@app.route('/')
def my_todos():
    return render_template('index.html')


@app.before_first_request
def _initialize_models():
    models.initialize()


if __name__ == '__main__':
    app.run(debug=config.DEBUG, host=config.HOST, port=config.PORT)
