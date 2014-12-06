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

@app.route('/auth', methods=['POST'])
@jsonp
def auth():
    return jsonify(safe=is_safe(request.form, mandrill)) # ugh

@app.route('/config')
def config():
    if request.method == 'GET':
        return jsonify(data=None)
    return jsonify(status='ok')
if __name__ == '__main__':
    app.run()
