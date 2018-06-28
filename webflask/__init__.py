
import os

from flask import send_from_directory

from mintools.restmin.impl.flask import create_restmin_app
from explorer.domain.api_domain import API_DOMAIN

def explorer_request_processor(app, req):
    return API_DOMAIN.resolve_request(req)

app = create_restmin_app(app_name=__name__,
                         config_path='',
                         base_url='/api/v0/',
                         request_processor=explorer_request_processor)

app.static_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'gui2', 'public')
GUI_DIRECTORY = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'gui_alt')

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index_gui2(path):
    return app.send_static_file('index.html')

@app.route('/gui_alt/')
def index_gui_alt():
    return send_from_directory(GUI_DIRECTORY, 'index.html')

@app.route('/gui_alt/<path:filename>')
def static_gui_alt(filename):
    return send_from_directory(GUI_DIRECTORY, filename)



if __name__ == '__main__':
    app.debug = True
    app.run()
