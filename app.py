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


if __name__ == '__main__':
    models.initialize()
    app.run(debug=config.DEBUG, host=config.HOST, port=config.PORT)
