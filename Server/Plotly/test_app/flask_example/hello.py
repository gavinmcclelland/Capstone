import flask


# Create the application.
APP = flask.Flask(__name__)


@APP.route('/')
def index():
    # Displays the index page accessible at '/'
    return flask.render_template('index.html')


if __name__ == '__main__':
    APP.debug=True
    APP.run() # Defaults to 127.0.0.1:5000
    # APP.run(host='0.0.0.0', port=5003) # Here we can specify where we want to locally run the application