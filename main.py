from flask import Flask, render_template, request, redirect, flash, url_for
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
                flash("User not authenticated")
                return redirect('/login')
        else:
            flash("User doesn't exist")
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
                    flash('Both passwords don\'t match!')
                    return redirect('/register')
            else:
                flash('User with the same username already exists!')
                return redirect('/register')
        else:
            flash('User with the same email already exists!')
            return redirect('/register')
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


@app.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        str_type = request.form['type']
        status = request.form['status']
        description = request.form['description']

        user_id = current_user.get_id()

        task = Task.select_by_title(user_id, title)
        if task:
            flash('task with same title already exists')
            return redirect('/create')

        if title == '':
            return redirect('/create-type')

        Task(title, description, status, str_type).create(user_id)
        return redirect('/board')
    else:
        task_types = TaskType.get_all_types()

        return render_template('create.html', task_types=task_types)


@app.route('/create-type', methods=['GET', 'POST'])
@login_required
def create_type():
    if request.method == 'POST':
        title = request.form['title']

        task_type = TaskType.get_task_type_by_title(title)
        if task_type:
            flash('task type already exists')
            return redirect('/create-type')


        TaskType(title).create()
        return redirect('/board')
    else:
        return render_template('create_type.html')


@app.route('/edit/<string:task_id>', methods=['GET', 'POST'])
@login_required
def edit(task_id):
    if request.method == 'POST':
        title = request.form['title']
        str_type = request.form['type']
        status = request.form['status']
        description = request.form['description']

        if str_type == '0':
            return redirect('/create-type')

        if title != '':
            Task.edit_title(task_id, title)

        if str_type != '':
            Task.edit_type(task_id, str_type)

        if status != '':
            Task.edit_status(task_id, status)

        if description != '':
            Task.edit_content(task_id, description)

        return redirect('/board')
    else:
        task = Task.get_task_by_id(task_id)
        task_types = TaskType.get_all_types()

        return render_template(
            'edit.html', task=task, task_id=task_id, task_types=task_types
        )


@app.route('/delete/<string:task_id>', methods=['POST'])
@login_required
def delete(task_id):
    Task.delete(task_id)
    return redirect('/board')


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/')


if __name__ == '__main__':
    app.secret_key = 'i am very secret'
    app.run()
