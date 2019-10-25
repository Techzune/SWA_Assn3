import flask
from flask_login import login_user

from app import app

def LoginForm():
    #Loginshit???
    return user

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = LoginForm()
    if form.validate_on_submit():
        # Login and validate the user.
        # user should be an instance of your `User` class
        login_user(user)

        flask.flash('Logged in successfully.')

        next = flask.request.args.get('next')


        return flask.redirect(next or flask.url_for('index'))
    return flask.render_template('login.html', form=form)

