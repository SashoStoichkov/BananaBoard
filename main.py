from flask import Flask, render_template, request, redirect, flash
# from flask_login import LoginManager

from user import User
# from task import Task
from task_type import TaskType

# Create Flask App
app = Flask(__name__)

# Some configurations
app.config['ENV'] = True
app.config['DEBUG'] = True


# # LoginManager
# login_manager = LoginManager()
# login_manager.init_app(app)


# @login_manager.user_loader
# def load_user(user_id):
#     return User.get_user_by_id(user_id)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print(request.form['username'])
        print(request.form['password'])

        return redirect('/')
    else:
        return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if not User.get_user_by_email(request.form['email']):
            if not User.get_user_by_username(request.form['username']):
                first_pass = request.form['password']
                second_pass = request.form['confirmed password']
                if first_pass == second_pass:
                    username = request.form['username']
                    email = request.form['email']
                    password = request.form['password']

                    User(username, email).create(password)
                    return redirect('/login')
                else:
                    print('Both passwords don\'t match!')
                    return redirect('/register')
            else:
                print('User with the same username already exists!')
                return redirect('/login')
        else:
            print('User with the same email already exists!')
            return redirect('/login')
    else:
        return render_template('register.html')


@app.route('/board', methods=['GET', 'POST'])
def board():
    return render_template('board.html')


@app.route('/edit', methods=['GET', 'POST'])
def edit():
    return render_template('edit.html')


if __name__ == '__main__':
    app.secret_key = 'i am very secret'
    app.run()
