from flask import Flask, render_template, request, session, redirect, url_for

from common.database import Database
from src.models.user import User

app = Flask(__name__)
app.secret_key = "secret"

@app.route('/')
def homeMethod():
    return redirect(url_for('login'))

@app.before_first_request
def initialize_database():
    Database.initialize()


@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/auth/login', methods=["POST"])
def user_login():
    email = request.form['email']
    password = request.form['password']

    if User.login_valid(email, password):
        User.login(email)
        return render_template('profile.html', email=session['email'])
    else:
        return redirect(url_for('homeMethod'))

@app.route('/auth/register', methods = ['POST'])
def user_registration():
    email = request.form['email']
    password = request.form['password']
    if User.register(email,password):
        session['email']=email
        return render_template('profile.html', email=session['email'])
    else:
        return "Email already use"

@app.route('/blog/<string:user_id>')
@app.route('/blogs')
def user_blog(user_id=None):
    if user_id is not None:
        user = User.get_by_id(user_id)
    else:
        user = User.get_by_email(session['email'])
    blogs = user.get_blogs()
    return render_template('user_blog.html', blogs=blogs, user_email = session['email'])



if __name__ == '__main__':
    app.debug = True
    app.run()
