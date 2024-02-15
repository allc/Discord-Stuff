from flask import Flask, render_template, session, request, redirect
from config import DEBUG, API_ENDPOINT, CLIENT_ID, REDIRECT_URI, SECRET_KEY
from utils import exchange_code, get_discord_permission_flags, get_discord_permission_friendly_names
import requests
from datetime import datetime

app = Flask(__name__)
app.secret_key = SECRET_KEY


@app.route('/')
def index():
    discord_aurhotize_url = 'https://discord.com/oauth2/authorize?client_id=%s&response_type=code&redirect_uri=%s&scope=guilds' % (CLIENT_ID, REDIRECT_URI)
    return render_template('index.html', discord_aurhotize_url=discord_aurhotize_url)

@app.route('/discord-oauth2')
def discord_oauth2():
    exchange_code_result = exchange_code(request.args.get('code'))
    # DISCORD TOKEN IS STORED IN SESSION COOKIE UNENCRYPTED!
    session['discord_access_token'] = exchange_code_result['access_token']
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'discord_access_token' not in session:
        return redirect('/')
    r = requests.get('%s/users/@me/guilds' % API_ENDPOINT,
                                 headers={'Authorization': 'Bearer %s' % session['discord_access_token']})
    r.raise_for_status()
    guilds_result = r.json()
    for guild in guilds_result:
        # https://github.com/vegeta897/snow-stamp/blob/main/src/convert.js
        milliseconds = int(guild['id']) >> 22
        milliseconds += 1420070400000
        guild['created_at'] = datetime.utcfromtimestamp(milliseconds / 1000).strftime('%Y-%m-%d %H:%M:%S')
        permissions_mask = int(guild['permissions'])
        permissions = {}
        permission_friendly_names = get_discord_permission_friendly_names()
        for permission, flag in get_discord_permission_flags().items():
            permissions[permission_friendly_names[permission]] = bool(permissions_mask & flag)
        guild['permissions'] = permissions
        guild['features'] = ','.join(guild['features'])
    return render_template('dashboard.html', guilds=guilds_result)

if __name__ == '__main__':
    app.run(debug=DEBUG)
