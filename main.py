from flask import Flask, request, render_template_string, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# Database file path
DATABASE = '/nfs/demo.db'

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    with app.app_context():
        db = get_db()
        db.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL,
                status TEXT DEFAULT 'Pending'
            );
        ''')
        db.commit()

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ''
    db = get_db()

    if request.method == 'POST':
        if request.form.get('action') == 'delete':
            task_id = request.form.get('task_id')
            db.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
            db.commit()
            message = 'Task deleted successfully.'
        elif request.form.get('action') == 'update':
            task_id = request.form.get('task_id')
            new_status = request.form.get('status')
            db.execute('UPDATE tasks SET status = ? WHERE id = ?', (new_status, task_id))
            db.commit()
            message = 'Task status updated.'
        else:
            description = request.form.get('description')
            if description:
                db.execute('INSERT INTO tasks (description) VALUES (?)', (description,))
                db.commit()
                message = 'Task added successfully.'
            else:
                message = 'Missing task description.'

    tasks = db.execute('SELECT * FROM tasks').fetchall()
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head><title>Task Manager</title></head>
        <body>
            <h2>Add Task</h2>
            <form method="POST" action="/">
                <input type="text" name="description" placeholder="Enter a task" required>
                <input type="submit" value="Add Task">
            </form>
            <p>{{ message }}</p>
            <h3>Task List</h3>
            {% if tasks %}
                <table border="1">
                    <tr><th>Description</th><th>Status</th><th>Update</th><th>Delete</th></tr>
                    {% for task in tasks %}
                    <tr>
                        <td>{{ task['description'] }}</td>
                        <td>{{ task['status'] }}</td>
                        <td>
                            <form method="POST" action="/">
                                <input type="hidden" name="task_id" value="{{ task['id'] }}">
                                <select name="status">
                                    <option value="Pending" {% if task['status'] == 'Pending' %}selected{% endif %}>Pending</option>
                                    <option value="In Progress" {% if task['status'] == 'In Progress' %}selected{% endif %}>In Progress</option>
                                    <option value="Done" {% if task['status'] == 'Done' %}selected{% endif %}>Done</option>
                                </select>
                                <input type="hidden" name="action" value="update">
                                <input type="submit" value="Update">
                            </form>
                        </td>
                        <td>
                            <form method="POST" action="/">
                                <input type="hidden" name="task_id" value="{{ task['id'] }}">
                                <input type="hidden" name="action" value="delete">
                                <input type="submit" value="Delete">
                            </form>
                        </td>
                    </tr>
                    {% endfor %}
                </table>
            {% else %}
                <p>No tasks available.</p>
            {% endif %}
        </body>
        </html>
    ''', message=message, tasks=tasks)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    init_db()
    app.run(debug=True, host='0.0.0.0', port=port)

