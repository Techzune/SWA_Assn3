from flask import Flask, render_template
from flask_assets import Environment, Bundle

# create Flask application
app = Flask(__name__)

# render SCSS
assets = Environment(app)
assets.url = app.static_url_path
scss = Bundle('site.scss', filters='libsass', output='site.css')
assets.register('scss_all', scss)


@app.route('/')
def home():
    """Page: home of site"""
    return render_template('index.jinja2')


# if main process, run the Flask app
if __name__ == '__main__':
    app.run()
