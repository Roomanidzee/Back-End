# -*- coding: utf-8 -*-
from flask import redirect, url_for, request, session
from app import app
import requests


@app.route('/send_like/<token>')
def send_like(token):
    user_token = session.get(token)
    api_url = "{0}/books/{1}/like/{2}".format(app.config['API_URL'], request.form['book_id'], user_token)
    requests.put(api_url)

    return redirect(url_for('get_books', token=token))


@app.route('/send_dislike/<token>')
def send_dislike(token):
    user_token = session.get(token)
    api_url = "{0}/books/{1}/dislike/{2}".format(app.config['API_URL'], request.form['book_id'], user_token)
    requests.put(api_url)

    return redirect(url_for('get_books', token=token))


@app.route('/unlike/<token>')
def delete_mark(token):
    user_token = session.get(token)
    api_url = "{0}/books/{1}/unlike/{2}".format(app.config['API_URL'], request.form['book_id'], user_token)
    requests.put(api_url)

    return redirect(url_for('get_books', token=token))
