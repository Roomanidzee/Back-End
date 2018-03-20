from app.forms import LoginForm, RegistrationForm
from flask import render_template, redirect, url_for, flash, request, session
from app import app
import uuid


@app.route('/')
def index():
    return render_template('main.html')

@app.route('/login', methods=['POST'])
def login():
    form = LoginForm(request.form)

    if form.validate():
        data = form.validate_form()
        if data['error_code'] == 2:
            flash('Неверный логин/пароль')
            return redirect('/')
        string_check = uuid.uuid4()
        session[string_check] = data['message']
        return redirect(url_for('get_books', token=string_check))

    return redirect('/')

@app.route('/logout/<token>')
def logout(token):
    session.pop(token, None)
    return redirect('/')

@app.route('/register', methods=['POST'])
def register():
    form = RegistrationForm(request.form)

    if form.validate():

        data = form.validate_form()
        if data['error_code'] == 0 and data['message'] == 'Success':
            flash('Вы успешно зарегистрировались!')
            string_check = uuid.uuid4()
            session[string_check] = data['message']
            return redirect('/')

    return redirect('/')

@app.route('/list_my_books/<token>')
def get_books(token):
    user_token = session.get(token)
    api_url = app.config['API_URL'] + '/books/' + user_token
    # здесь получение жанров и книг
    return render_template('my_books.html',user_token=token)

@app.route('/list_new_books/<token>')
def get_new_books(token):
    user_uuid = request.args['string_check']
    # здесь получение книг
    string_check = session.get(user_uuid)
    return render_template('new_books.html',user_token=token)

@app.route('/list_recommend_books/token')
def get_recommend_books(token):
    user_uuid = request.args['string_check']
    string_check = session.get(user_uuid)
    # аналогично, получение книг по жанрам
    return render_template('recomend_books.html',user_token=token)