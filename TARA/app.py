from flask import Flask, render_template, request, redirect, url_for
import datetime

app = Flask(__name__)

# Store tasks in memory (for demo purposes)
tasks = []

# Priorities map
priority_map = {"Low": "green", "Medium": "orange", "High": "red"}


@app.route('/')
def index():
    today = datetime.date.today()
    completed_tasks = [task for task in tasks if task['status'] == 'Completed']
    pending_tasks = [task for task in tasks if task['status'] == 'Pending']
    overdue_tasks = [task for task in tasks if task['due_date'] < today and task['status'] == 'Pending']

    daily_summary = {
        "completed": len(completed_tasks),
        "pending": len(pending_tasks),
        "overdue": len(overdue_tasks)
    }

    return render_template('index.html', tasks=tasks, daily_summary=daily_summary, priority_map=priority_map)


@app.route('/add', methods=['POST'])
def add_task():
    task_name = request.form.get('task')
    priority = request.form.get('priority')
    due_date = request.form.get('due_date')
    task = {
        'name': task_name,
        'priority': priority,
        'status': 'Pending',
        'due_date': datetime.datetime.strptime(due_date, '%Y-%m-%d').date() if due_date else datetime.date.today(),
    }
    tasks.append(task)
    return redirect(url_for('index'))


@app.route('/complete/<int:task_index>')
def complete_task(task_index):
    if 0 <= task_index < len(tasks):
        tasks[task_index]['status'] = 'Completed'
    return redirect(url_for('index'))


@app.route('/delete/<int:task_index>')
def delete_task(task_index):
    if 0 <= task_index < len(tasks):
        tasks.pop(task_index)
    return redirect(url_for('index'))


@app.route('/reorder', methods=['POST'])
def reorder_tasks():
    ordered_tasks = request.json['tasks']
    global tasks
    tasks = ordered_tasks
    return '', 204


if __name__ == '__main__':
    app.run(debug=True)
