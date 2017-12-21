
import os

from flask import send_from_directory
import crossdomain

from server import api_blueprint

GUI_DIRECTORY = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'gui')

from flask import Flask
app = Flask(__name__)

app.register_blueprint(api_blueprint)

app.static_url_path = ''
app.static_folder   = GUI_DIRECTORY
app.add_url_rule('/<path:filename>',
    endpoint  = 'static',
    view_func = app.send_static_file)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/<path:filename>')
def send_file(filename):
    return send_from_directory(GUI_DIRECTORY, filename)

if __name__ == '__main__':
    app.debug = True
    app.run()
