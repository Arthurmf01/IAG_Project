# /server.py

from functools import wraps
import json
from os import environ as env
from werkzeug.exceptions import HTTPException

from dotenv import load_dotenv, find_dotenv
from flask import Flask
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import session
from flask import url_for
from authlib.flask.client import OAuth
from six.moves.urllib.parse import urlencode

app = Flask(__name__)

oauth = OAuth(app)

auth0 = oauth.register(
    'auth0',
    client_id='ggwmdOXy58wn56tAoGVWreBQ9uiUdmpO',
    client_secret='AroCX2kyaIWiHrrUHpXk4u5EhEvu0hj0uSUZHJyUHD6pEfcPSWX-qWjIpAHu9zKB',
    api_base_url='https://snowy-block-6613.auth0.com',
    access_token_url='https://snowy-block-6613.auth0.com/oauth/token',
    authorize_url='https://snowy-block-6613.auth0.com/authorize',
    client_kwargs={
        'scope': 'openid profile',
    },
)

# /server.py

# Here we're using the /callback route.
@app.route('/callback')
def callback_handling():
    # Handles response from token endpoint
    auth0.authorize_access_token()
    resp = auth0.get('userinfo')
    userinfo = resp.json()

    # Store the user information in flask session.
    session['jwt_payload'] = userinfo
    session['profile'] = {
        'user_id': userinfo['sub'],
        'name': userinfo['name'],
        'picture': userinfo['picture']
    }
    return redirect('/dashboard')


# /server.py

@app.route('/login')
def login():
    return auth0.authorize_redirect(redirect_uri='https://iag-project.herokuapp.com/', audience='https://snowy-block-6613.auth0.com/userinfo')

# /server.py

def requires_auth(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    if 'profile' not in session:
      # Redirect to Login page here
      return redirect('/')
    return f(*args, **kwargs)

  return decorated

# /server.py

@app.route('/dashboard')
@requires_auth
def dashboard():
    return render_template('dashboard.html',
                           userinfo=session['profile'],
                           userinfo_pretty=json.dumps(session['jwt_payload'], indent=4))


# /server.py

@app.route('/logout')
def logout():
    # Clear session stored data
    session.clear()
    # Redirect user to logout endpoint
    params = {'returnTo': url_for('home', _external=True), 'client_id': 'YOUR_CLIENT_ID'}
    return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))