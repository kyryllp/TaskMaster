from flask import Flask, render_template, request, redirect
import mongo_setup
import mongoengine
from models.user import User
from models.todo import Todo

app = Flask(__name__)

global_user: User = None  # this will be changed later, while using the app


@app.route('/', methods=['POST', 'GET'])
def index():
    if global_user is None:
        return redirect('/login')
    else:
        if request.method == 'POST':
            task_content = request.form['content']
            new_task = Todo()
            new_task.content = task_content

            new_task.save()

            global_user.todo_ids.append(new_task.id)
            global_user.save()

            return redirect('/')

        else:
            tasks = [task for task in Todo.objects() if task.id in global_user.todo_ids]
            return render_template('index.html', tasks=tasks)


@app.route('/delete/<string:id>')
def delete(id):
    task_to_delete = Todo.objects(id=id).first()

    try:
        task_to_delete.delete()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'


@app.route('/update/<string:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.objects(id=id).first()

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            task.save()
            return redirect('/')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', task=task)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if User.objects(username=request.form['username'],
                        password=request.form['password']):
            global global_user

            global_user = User.objects(username=request.form['username']).first()
            return redirect('/')
        else:
            return 'Username or password are invalid!' + render_template('login.html')
    else:
        return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if not User.objects(username=request.form['username']) \
                and request.form['username'] is not None\
                and request.form['name'] is not None\
                and request.form['surname'] is not None\
                and request.form['password'] is not None:
            user = User()

            user.name = request.form['name']
            user.surname = request.form['surname']
            user.username = request.form['username']
            user.password = request.form['password']

            user.save()

            return redirect('/login')
        else:
            return 'The username has already been taken, choose another one or one of the fields is empty' \
                   + render_template('register.html')
    else:
        return render_template('register.html')


if __name__ == '__main__':
    mongo_setup.global_init()
    mongoengine.connect(db='simple_todo')
    app.run(debug=True, host='0.0.0.0')
