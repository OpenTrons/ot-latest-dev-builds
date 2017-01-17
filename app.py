import os

from flask import Flask, request
from flask import render_template
from flask_humanize import Humanize

from list import get_builds_dict


app = Flask(__name__)
humanize = Humanize(app)

@app.route('/')
def home():
    branch = request.args.get('branch') or 'master'
    return render_template('index.html', builds=get_builds_dict(branch=branch))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 5000))
