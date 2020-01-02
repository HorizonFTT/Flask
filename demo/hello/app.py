import click
import os
from flask import (
    Flask,
    redirect,
    url_for,
    jsonify,
    make_response,
    session,
    request,
)
from urllib.parse import urlparse, urljoin
from jinja2.utils import generate_lorem_ipsum

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'secret string')

colors = ['blue', 'white', 'red']


@app.cli.command()
def say_hello():
    click.echo('Hello, Human!')


@app.route('/greet', defaults={'name': 'Programmer'})
@app.route('/greet/<name>')
def greet(name):
    return '<h1>Hello, %s!</h1>' % name


@app.route('/hello')
def hello():
    name = request.args.get('name', 'Flask')
    if name is None:
        name = request.cookies.get('name', 'Human')
    response = f'<h1>Hello, {name}!</h1>'
    if 'logged_in' in session:
        response += '[Authenticated]'
    else:
        response += '[Not Authenticated]'
    return response


@app.route('/goBack/<int:year>')
def go_back(year):
    return f'<p>Welcome to {(2020 - year)}!</p>'


@app.route(f'/colors/<any({str(colors)[1:-1]}):color>')
def three_colors(color):
    return '<p>Love is patient and kind. Love is not jealous or boastful or proud or rude.</p>'


@app.route('/fuck')
def fuck():
    return redirect(url_for('hello'))


@app.route('/json')
def json():
    return jsonify(name='Grey Li', gender='male')


@app.route('/set/<name>')
def set_cookie(name):
    response = make_response(redirect(url_for('hello')))
    response.set_cookie('name', name)
    return response


@app.route('/login')
def login():
    session['logged_in'] = True
    return redirect(url_for('hello'))


@app.route('/logout')
def logout():
    if 'logged_in' in session:
        session.pop('logged_in')
        return redirect(url_for('hello'))


@app.route('/foo')
def foo():
    r = f'<h1>Foo page</h1><a href="{url_for("do_something", next=request.full_path)}">Do something and redirect</a>'
    return r


@app.route('/bar')
def bar():
    return f'<h1>Bar page</h1><a href="{url_for("do_something", next=request.full_path)}">Do something and redirect</a>'


@app.route('/do_something')
def do_something():
    # do something here
    return redirect_back()


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
        ref_url.netloc == test_url.netloc


def redirect_back(default='hello', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default, **kwargs))


@app.route('/post')
def show_post():
    post_body = generate_lorem_ipsum(n=2)
    return '''
<h1>A very long post</h1>
<div class="body">%s</div>
<button id="load">Load More</button>
<script src="https://code.jquery.com/jquery-3.3.1.min.js"></script>
<script type="text/javascript">
$(function() {
    $('#load').click(function() {
        $.ajax({
            url: '/more',
            type: 'get',
            success: function(data){
                $('.body').append(data);
            }
        })
    })
})
</script>''' % post_body


@app.route('/more')
def load_post():
    return generate_lorem_ipsum(n=1)
