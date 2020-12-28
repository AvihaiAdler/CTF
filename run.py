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
import json


class Secrets:
    def __init__(self):
        with open('config.json') as f:
            content = json.load(f)
        self.username = content['username']
        self.password = content['password']
        self.search_string = content['search_string']
        self.flag = content['flag']
        self.cookie_value = content['cookie']
        self.default_cookie = 'vanilla'


app = Flask(__name__)
app.config['SECRET_KEY'] = '4fb8dac4d9aa0e70d016bccc9a2a17d9c5ff161809f11ecfd79d751b446d0f0c'
data = Songs()
admin = Secrets()


@app.route('/', methods=['GET', 'POST'])     # root
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    response = make_response()
    session['logged_in'] = False

    if request.method == 'POST' and form.validate_on_submit():
        if form.password.data == admin.password and form.username.data == admin.username:
            session['logged_in'] = True
            flash('There must be something hidden here, better check that search bar', 'success')
            return redirect(url_for('home'))
        else:
            flash('Access denied. Sniff it out!', 'danger')
            response.headers.add('Username', admin.username)
            response.headers.add('Password', admin.password)

    response.set_cookie('cookie', admin.default_cookie)
    response.data = render_template('login.html', title='Login', form=form)
    return response


@app.route('/home', methods=['GET', 'POST'])
def home():
    if not session['logged_in']:
        return redirect(url_for('login'))

    form = SearchBar()
    if request.method == 'POST':

        if form.search_string.data == admin.search_string:
            return send_file("challenge_4.wav", mimetype="audio/wav", as_attachment=True)

        data.get_search_result(form.search_string.data)
    return render_template('home.html', posts=data.get_list(), title='Home', form=form)


@app.route('/flag')
def flag():
    if not session['logged_in']:
        return redirect(url_for('login'))

    try:
        cookie = request.cookies.get('cookie')
        print(cookie)
        if cookie == admin.cookie_value:
            return render_template('flag.html', flag=admin.flag)
    except Exception as e:
        print(e)

    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)



