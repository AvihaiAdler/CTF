from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    send_file,
    make_response,
    request,
    session,
    flash
)
from songs import Songs
from forms import LoginForm, SearchBar
import threading
from listener import listen
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret key'
data = Songs()

with open('config.json') as f:
    content = json.load(f)


class Admin:
    username = content['username']
    password = content['password']
    search_string = content['search_string']


@app.route('/', methods=['GET', 'POST'])     # root
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    response = make_response()
    session['logged_in'] = False

    if request.method == 'POST' and form.validate_on_submit():
        if form.password.data == Admin.password and form.username.data == Admin.username:
            session['logged_in'] = True
            flash('There must be something hidden here, better check that search bar', 'success')
            return redirect(url_for('home'))
        else:
            flash('Access denied. Sniff it out!', 'danger')
            response.headers.add('Username', Admin.username)
            response.headers.add('Password', Admin.password)
    response.data = render_template('login.html', title='Login', form=form)
    return response


@app.route('/home', methods=['GET', 'POST'])
def home():
    if not session['logged_in']:
        return redirect(url_for('login'))

    form = SearchBar()
    if request.method == 'POST':

        if form.search_string.data == Admin.search_string:
            return send_file("challenge_4.wav", mimetype="audio/wav", as_attachment=True)

        data.get_search_result(form.search_string.data)
    return render_template('home.html', posts=data.get_list(), title='Home', form=form)


if __name__ == '__main__':
    #   launching 2 threads. 1 for the socket & 1 for the app
    threading.Thread(target=listen).start()
    threading.Thread(target=app.run).start()
    # app.run(debug=True)   # can't use debug mode when using thread. debug uses the reloader which expect the app to run in the main thread




