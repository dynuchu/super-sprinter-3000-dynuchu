# imports
from peewee import *
from flask import Flask, g, flash, render_template, \
    request, redirect, url_for
from connectdatabase import ConnectDatabase
from models import UserStoryManager

app = Flask(__name__)


def init_db():
    ConnectDatabase.db.connect()
    ConnectDatabase.db.create_tables([UserStoryManager], safe=True)


@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'postgre_db'):
        g.postgre_db.close()


@app.route("/story", methods=['GET', 'POST'])
def adding_page():
    if request.method == 'POST':
        new_story = UserStoryManager.create(story_title=request.form['story_title'],
                                            user_story=request.form['user_story'],
                                            acceptance_criteria=request.form['acceptance_criteria'],
                                            business_value=request.form['business_value'],
                                            estimation=request.form['estimation'], status=request.form['status'])

        new_story.save()
        return redirect(url_for('list_page'))
    add = "add"
    return render_template('form.html', add=add)


@app.route('/story/<int:story_id>', methods=['GET', 'POST'])
def editor_page(story_id):
    if request.method == 'POST':
        modify = UserStoryManager.update(story_title=request.form['story_title_edit'],
                                         user_story=request.form['user_story_edit'],
                                         acceptance_criteria=request.form['acceptance_criteria_edit'],
                                         business_value=request.form['business_value_edit'],
                                         estimation=request.form['estimation_edit'], status=request.form['status_edit']).where(
            UserStoryManager.id == story_id)
        modify.execute()
        return redirect(url_for('list_page'))

    story = UserStoryManager.select().where(UserStoryManager.id == story_id).get()
    return render_template("form.html", story=story)


@app.route("/", methods=['GET', 'POST'])
@app.route("/list", methods=['GET', 'POST'])
def list_page():
    user_stories = UserStoryManager.select().order_by(UserStoryManager.id.asc())
    return render_template("list.html", user_stories=user_stories)


@app.route("/delete/<int:story_id>")
def delete(story_id):
    story = UserStoryManager.select().where(UserStoryManager.id == story_id).get()
    UserStoryManager.delete_instance(story)
    return redirect("list")


init_db()
app.run(debug=True, host='0.0.0.0', port=5000)
