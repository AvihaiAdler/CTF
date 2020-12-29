from flask import render_template, redirect, url_for, send_file, make_response, request, session, flash
from ctf.forms import LoginForm, SearchBar
from ctf import app, data, secret


@app.route('/', methods=['GET', 'POST'])     # root
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    response = make_response()
    session['logged_in'] = False

    if request.method == 'POST' and form.validate_on_submit():
        if form.password.data == secret.password and form.username.data == secret.username:
            session['logged_in'] = True
            flash('There must be something hidden here, better check that search bar', 'success')
            return redirect(url_for('home'))
        else:
            flash('Access denied. Sniff it out!', 'danger')
            response.headers.add('Username', secret.username)
            response.headers.add('Password', secret.password)

    response.set_cookie('cookie', secret.default_cookie)
    response.data = render_template('login.html', title='Login', form=form)
    return response


@app.route('/home', methods=['GET', 'POST'])
def home():
    if not session['logged_in']:
        return redirect(url_for('login'))

    form = SearchBar()
    entry = "#"
    if request.method == 'POST':

        if form.search_string.data == secret.search_string:
            return send_file("data/challenge_4.wav", mimetype="audio/wav", as_attachment=True)

        entry = data.get_index_by_name(form.search_string.data)
    return render_template('home.html', posts=data.get_list(), entry=entry, title='Home', form=form)


@app.route('/flag')
def flag():
    if not session['logged_in']:
        return redirect(url_for('login'))

    try:
        cookie = request.cookies.get('cookie')
        print(cookie)
        if cookie == secret.cookie_value:
            flash('Yay! you made it!', 'success')
            return render_template('flag.html', flag=secret.flag)
    except Exception as e:
        print(e)

    flash('Access denied', 'danger')
    return redirect(url_for('home'))




