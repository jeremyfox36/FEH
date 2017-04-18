from FEH import app
from flask import render_template, flash, redirect
from .forms import LoginForm


@app.route('/')
@app.route('/index')
def index():
    userid = 12345
    project = 'example'
    stations = [
        {
            'stationnum': 12345
        },
        {
            'stationnum': 65432
        }
    ]
    return render_template('index.html',
                           userid=userid,
                           project=project,
                           stations=stations)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for UserID={}, remember_me={}'
              .format(form.userid.data, str(form.remember_me.data)))
        return redirect('/index')
    return render_template('login.html',
                           title='Sign In',
                           form=form)
