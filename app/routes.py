from app.forms import LoginForm, RegistrationForm
from flask import render_template, redirect, url_for, flash, request, session
from app import app


@app.route('/')
def index():
    form1 = LoginForm()
    form2 = RegistrationForm()
    return render_template('main.html', form1=form1, form2=form2)

@app.route('/login', methods=['POST'])
def login():
    form = LoginForm(request.form)

    if form.validate_on_submit():
        data = form.validate_form()
        if data['error_code'] == 2:
            flash('Неверный логин/пароль')
            return redirect('/')
        # TODO: нормальное хеширование строки
        string_check = form.email.replace("@", "-")
        session[string_check] = data['message']
        return redirect(url_for('get_books', string_check=string_check))

    return redirect('/')

@app.route('/logout/<string_check>')
def logout(string_check):
    session.pop(string_check, None)
    return redirect('/')

@app.route('/register', methods=['POST'])
def register():
    form = RegistrationForm(request.form)

    if form.validate_on_submit():

        data = form.validate_form()
        if data['error_code'] == 0 and data['message'] == 'Success':
            flash('Вы успешно зарегистрировались!')
            # TODO: нормальное хеширование строки
            string_check = form.email.replace("@", "-")
            session[string_check] = data['message']
            return redirect(url_for('get_books', string_check=string_check))

    return redirect('/')

@app.route('/list_my_books')
def get_books():
    user_uuid = request.args['string_check']
    string_check = session.get(user_uuid)
    return render_template('my_books.html',string_check=string_check)

@app.route('/list_new_books')
def get_new_books():
    user_uuid = request.args['string_check']
    string_check = session.get(user_uuid)
    return render_template('new_books.html',string_check=string_check)

@app.route('/list_recommend_books')
def get_recommend_books():
    user_uuid = request.args['string_check']
    string_check = session.get(user_uuid)
    return render_template('recomend_books.html',string_check=string_check)