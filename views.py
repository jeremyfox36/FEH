import pandas as pd
from flask import render_template, flash, redirect, request
from werkzeug import utils as w_utils

from FEH import app
from FEH import utils
from .forms import LoginForm


@app.route('/')
@app.route('/index')
def index():
    userid = 12345
    project = 'example'
    stations = [1,2,3,4,5]
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


@app.route('/table')
def show_tables():
    data = pd.DataFrame.from_dict(utils.sdm_from_db(), orient='index')
    data.rename(columns={'sdm': 'Distance', 'amaxcount': 'Number of years AMAX data'}, inplace=True)
    return render_template('pooling_group.html', data=data.to_html(columns=["Distance", "Number of years AMAX data"]))


@app.route('/upload')
def upload_files():
    return render_template('upload.html')


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save(w_utils.secure_filename(f.filename))
        return 'file uploaded successfully'
