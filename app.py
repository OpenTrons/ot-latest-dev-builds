from flask import Flask
from flask import render_template

from list import get_builds_dict


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html', builds=get_builds_dict())


if __name__ == '__main__':
    app.run(port=5000)
