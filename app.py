from flask import Flask
from flask import jsonify, request

from utils import jsonp
from models import is_safe

from flask.ext.mandrill import Mandrill

app = Flask(__name__)
app.config.from_object('settings')

mandrill = Mandrill(app)

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/auth')
@jsonp
def auth():
    return jsonify(safe=is_safe(request.form, mandrill)) # ugh


if __name__ == '__main__':
    app.run()
