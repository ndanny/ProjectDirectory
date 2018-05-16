import os
import markdown
from app import app
from app.helpers import get_page_url_name, get_page_display_name
from flask import render_template, request, redirect, url_for, session

app.secret_key = 'secretkey'


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/pages')
def pages():
    ensure_pages_dir_exists()
    pages = os.listdir('pages')
    return render_template("pages.html", pages=pages)


@app.route('/pages/<page_name>')
def page(page_name):
    with open('pages/' + page_name + '.md') as page_file:
        content = page_file.read()
    html = markdown.markdown(content)
    return render_template("page.html", page_name=page_name, contents=html)


@app.route('/new_page', methods=['GET', 'POST'])
def new_page():
    if request.method == 'GET':
        return render_template('new_page.html')

    ensure_pages_dir_exists()

    title = request.form['title']
    contents = request.form['contents']

    with open('pages/' + get_page_url_name(title) + '.md', 'w') as page_file:
        page_file.write(contents)

    return redirect(url_for('pages'))


@app.route('/edit_page/<page_name>', methods=['GET', 'POST'])
def edit_page(page_name):
    if request.method == 'GET':
        with open('pages/' + page_name + '.md') as page_file:
            contents = page_file.read()
        title = get_page_display_name(page_name)
        return render_template('edit_page.html', title=title, contents=contents, title_disp=page_name)

    title = get_page_display_name(page_name)
    contents = request.form['contents']
    with open('pages/' + get_page_url_name(title) + '.md', 'w') as page_file:
        page_file.write(contents)

    return redirect(url_for('page', page_name=get_page_url_name(title)))


@app.route('/delete_page/<page_name>', methods=['GET', 'POST'])
def delete_page(page_name):
    if request.method == 'GET':
        return render_template('delete_page.html', page_name=get_page_display_name(page_name))

    os.remove('./pages/' + page_name + '.md')
    return redirect(url_for('pages'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    email = request.form['email']
    password = request.form['password']

    if is_valid_login(email, password):
        session['email'] = email
        return redirect(url_for('pages'))

    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))


def ensure_pages_dir_exists():
    if not os.path.exists('pages'):
        os.makedirs('pages')


def is_valid_login(email, password):
    return 1
