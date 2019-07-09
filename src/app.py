from flask import Flask, render_template, request, redirect
import mongoengine
from models.user import User
from models.todo import Todo

app = Flask(__name__)

global_user: User = None  # this will be changed later, while using the app


@app.route('/', methods=['POST', 'GET'])
def index():
    if global_user is None:
        app.logger.info("User hasn't logged in yet, redirecting to the login page")
        return redirect('/login')
    else:
        if request.method == 'POST':
            task_content = request.form['content']
            new_task = Todo()
            new_task.content = task_content

            new_task.save()

            global_user.todo_ids.append(new_task.id)
            global_user.save()

            app.logger.info(f'Todo: {new_task.id} has been add to User: {global_user.username}')
            return redirect('/')

        else:
            tasks = [task for task in Todo.objects() if task.id in global_user.todo_ids]
            return render_template('index.html', tasks=tasks)


@app.route('/delete/<string:id>')
def delete(id):
    task_to_delete : Todo = Todo.objects(id=id).first()

    try:
        task_to_delete.delete()
        app.logger.info(f'Deleting task: {task_to_delete.id}')
        return redirect('/')
    except:
        return 'There was a problem deleting that task'


@app.route('/update/<string:id>', methods=['GET', 'POST'])
def update(id):
    task : Todo = Todo.objects(id=id).first()

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            task.save()
            app.logger.info(f'Updating task: {task.id}')
            return redirect('/')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', task=task)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username_ = request.form['username']
        password_ = request.form['password']
        if User.objects(username=username_,
                        password=password_):
            global global_user

            global_user = User.objects(username=username_).first()
            app.logger.info(f'User: {global_user.username} successfully logged in')
            return redirect('/')
        else:
            app.logger.warning(f"There is no user with such username {username_} or password {password_}")
            return 'Username or password are invalid!' + render_template('login.html')
    else:
        return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if not User.objects(username=request.form['username']) \
                and request.form['username'] is not None \
                and request.form['name'] is not None \
                and request.form['surname'] is not None \
                and request.form['password'] is not None:
            user = User()

            user.name = request.form['name']
            user.surname = request.form['surname']
            user.username = request.form['username']
            user.password = request.form['password']

            user.save()
            app.logger.info(f'Username: {user.username} has successfully registered')

            return redirect('/login')
        else:
            app.logger.warning('One of the fields were empty or the username has already been taken')
            return 'The username has already been taken, choose another one or one of the fields is empty' \
                   + render_template('register.html')
    else:
        return render_template('register.html')


if __name__ == '__main__':
    mongoengine.connect(db='simple_todo', host='mongodb://mongo/simple_todo')   # setting URI helps resolve docker issue
    app.run(debug=True, host='0.0.0.0')
