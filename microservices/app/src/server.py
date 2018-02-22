from collections import Counter

import requests
import json
from flask import jsonify, make_response, request, redirect, send_file, render_template, flash
from src import app

UPLOAD_URL = 'https://filestore.akin49.hasura-app.io/v1/file'
ZAP_URL = 'https://hooks.zapier.com/hooks/catch/2889414/80ktza/'
SIGN_UP_URL = 'https://auth.akin49.hasura-app.io/v1/signup'
LOGIN_URL = 'https://auth.akin49.hasura-app.io/v1/login'
LOGOUT_URL = 'https://auth.akin49.hasura-app.io/v1/user/logout'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


@app.route('/')
def hello_world():
    return 'Hello World - Vikas'


@app.route('/authors')
def get_author_post_count():
    """Prepare author and their posts count data.

    Fetch a list of authors from a request to http://jsonplaceholder.typicode.com/users
    Fetch a list of posts from a request to http://jsonplaceholder.typicode.com/posts
    :return: list of author names-only with the number of posts they have made
    """
    authors = requests.get('http://jsonplaceholder.typicode.com/users').json()  # fetch users
    posts = requests.get('http://jsonplaceholder.typicode.com/posts').json()  # fetch posts

    author_dict = {author['id']: author for author in authors}  # hash author for faster access

    author_post_count = Counter(post['userId'] for post in posts)  # count posts per userId

    return jsonify([{'name': author_dict[item[0]]['name'], 'postCount': item[1]} for item in author_post_count.items()])


@app.route('/setcookie')
def set_cookie():
    """Set cookies.

    If name cookie is not set, set it with value 'Vikas'
    If age cookie is not set, set it with value '24'
    :return: response object on which cookie is set
    """
    response = make_response('Cookies set.')
    if 'name' not in request.cookies:
        response.set_cookie('name', 'Vikas')
    if 'age' not in request.cookies:
        response.set_cookie('age', '24')

    return response


@app.route('/getcookies')
def get_cookies():
    """Return cookies as json."""
    return jsonify(request.cookies)


@app.route('/robots.txt')
def robots_txt():
    return redirect('http://httpbin.org/deny')


@app.route('/image')
def get_image():
    """Return a static image."""
    return send_file('static/hasura.jpg')


@app.route('/input', methods=['GET', 'POST'])
def input_text():
    """Render html to receive text input and log it.

    If the request method is GET, just render the html to get the input text
    If the request method is POST, log the posted input text and re-render the input html
    :return: rendered input html
    """
    if request.method == 'POST':
        app.logger.info('Input received: %s', request.form['text'])
    return render_template('input.html')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def trigger_backup(file):
    # TODO: Pass the username here, and configure zap to actually save the file in a folder named as current username
    requests.post(ZAP_URL, files={'file': file})


@app.route('/uploadfile', methods=['GET', 'POST'])
def input_file():
    # TODO: Remove GET flow from here and delete the template file after testing is done
    auth_token = request.cookies.get('auth_token')
    if not auth_token:
        return make_response(json.dumps({'message': 'Cookie absent. User not logged in.'}))

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file_storage = request.files['file']

        # if user does not select file, browser also submit an empty part without filename
        if file_storage.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file_storage and allowed_file(file_storage.filename):
            headers = {'Authorization': 'Bearer ' + auth_token}
            file = file_storage.read()
            requests.post(UPLOAD_URL, headers=headers, files={'file': file},
                          hooks={'response': lambda r, *args, **kwargs: trigger_backup(file)})
            return make_response(
                json.dumps({'message': 'File has been uploaded and backup has been triggered.'}))
        # TODO: try reading file back from Hasura and getting the image intact

    return render_template('file_upload.html')


@app.route('/signup', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        return requests.post(SIGN_UP_URL, json={
            "provider": "username",
            "data": {
                "username": request.form['username'],
                "password": request.form['password']
            }
        }).text

    return render_template('sign_up.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        internal_resp = requests.post(LOGIN_URL, json={
            "provider": "username",
            "data": {
                "username": request.form['username'],
                "password": request.form['password']
            }
        })
        if not internal_resp.ok:
            return make_response(json.dumps({'message': 'Invalid login. Try again'}))

        response = make_response(internal_resp.text)
        response.set_cookie('auth_token', internal_resp.json()['auth_token'])
        return response

    return render_template('login.html')


@app.route('/logout', methods=['GET'])
def logout():
    auth_token = request.cookies.get('auth_token')
    if not auth_token:
        return make_response(json.dumps({'message': 'Cookie absent. User not logged in.'}))

    headers = {'Authorization': 'Bearer ' + auth_token}
    internal_resp = requests.post(LOGOUT_URL, headers=headers)

    response = make_response(internal_resp.text)
    response.set_cookie('auth_token', '', expires=0)  # expire the auth_token cookie
    return response


if __name__ == '__main__':
    app.run(debug=True)
