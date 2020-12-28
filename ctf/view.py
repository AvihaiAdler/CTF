from flask import render_template, redirect, url_for, send_file, make_response, request, session, flash
from ctf.forms import LoginForm, SearchBar
from ctf import app, data, admin


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
            return send_file("data/challenge_4.wav", mimetype="audio/wav", as_attachment=True)

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
            flash('Yay! you made it!', 'success')
            return render_template('flag.html', flag=admin.flag)
    except Exception as e:
        print(e)

    flash('Access denied', 'danger')
    return redirect(url_for('home'))




