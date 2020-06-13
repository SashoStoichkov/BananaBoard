from flask import Flask, render_template, request, redirect, flash
from flask_login import LoginManager, login_required,\
                        login_user, logout_user, current_user

from user import User
from task import Task
from task_type import TaskType

# Create Flask App
app = Flask(__name__)

# Some configurations
app.config['ENV'] = True
app.config['DEBUG'] = True


# LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/login'


@login_manager.user_loader
def load_user(user_id):
    return User.get_user_by_id(user_id)


def sign_in_user(user_id, password):
    user = load_user(user_id)

    if user and User.verify_password(password, user.username):
        user.authenticated = True
        login_user(user, remember=True)
        return user
    else:
        return False


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        u_id = User.get_id_by_username(username)

        if u_id:
            user = sign_in_user(u_id, password)

            if user and user.is_authenticated():
                return redirect('/board')
            else:
                return redirect('/login')
        else:
            return redirect('/login')
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
@login_required
def board():
    to_do = Task.display_by_status(current_user.get_id(), '1')
    doing = Task.display_by_status(current_user.get_id(), '2')
    done = Task.display_by_status(current_user.get_id(), '3')

    return render_template(
        'board.html',
        current_user=current_user,
        to_do=to_do, doing=doing, done=done
    )


@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit():
    return render_template('edit.html')


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/')


if __name__ == '__main__':
    app.secret_key = 'i am very secret'
    app.run()
