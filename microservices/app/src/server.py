from src import app

import requests
from flask import jsonify, make_response, request, redirect, send_file, render_template
from collections import Counter


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

    author_post_count = Counter(post['userId'] for post in posts)   # count posts per userId

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
    return send_file('static\hasura.jpg')


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


if __name__ == '__main__':
    app.run(debug=True)
