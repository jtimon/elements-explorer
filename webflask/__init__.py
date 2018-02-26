
import os

from flask import send_from_directory

from mintools.restmin.impl.flask import create_restmin_app
from explorer.explorer_server import API_DOMAIN

def explorer_request_processor(app, req):
    return API_DOMAIN.resolve_request(req)

app = create_restmin_app(app_name=__name__,
                         config_path='',
                         base_url='/api/v0/',
                         request_processor=explorer_request_processor)

app.static_url_path = ''
app.static_folder   = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'gui')
app.add_url_rule('/<path:filename>',
    endpoint  = 'static',
    view_func = app.send_static_file)
GUI2_DIRECTORY = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'gui2', 'public')

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/<path:filename>')
def send_file(filename):
    return app.send_static_file(filename)

@app.route('/gui2/', defaults={'path': ''})
@app.route('/gui2/<path:path>')
def index_gui2(path):
    return send_from_directory(GUI2_DIRECTORY, 'index.html')

@app.route('/gui2/static/<path:filename>')
def send_file_gui2(filename):
    return send_from_directory(GUI2_DIRECTORY, filename)

if __name__ == '__main__':
    app.debug = True
    app.run()
