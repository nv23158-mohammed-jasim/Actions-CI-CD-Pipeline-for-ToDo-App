"""
Flask ToDo App - A simple task management application
"""
from flask import Flask, render_template, request, jsonify
import os
from datetime import datetime

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# In-memory storage for todos (would use database in production)
todos = {
    1: {'id': 1, 'title': 'Learn GitHub Actions', 'completed': False, 'created_at': datetime.now().isoformat()},
    2: {'id': 2, 'title': 'Build CI/CD pipeline', 'completed': False, 'created_at': datetime.now().isoformat()},
}
next_id = 3


@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html', todos=list(todos.values()))


@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'version': '1.0.0'}), 200


@app.route('/api/todos', methods=['GET'])
def get_todos():
    """Get all todos."""
    return jsonify(list(todos.values())), 200


@app.route('/api/todos/stats', methods=['GET'])
def get_stats():
    """Get todo statistics."""
    total = len(todos)
    completed = sum(1 for todo in todos.values() if todo['completed'])
    pending = total - completed
    return jsonify({
        'total': total,
        'completed': completed,
        'pending': pending,
        'completion_rate': (completed / total * 100) if total > 0 else 0
    }), 200


@app.route('/api/todos', methods=['POST'])
def create_todo():
    """Create a new todo."""
    global next_id
    data = request.get_json()

    if not data or 'title' not in data:
        return jsonify({'error': 'Title is required'}), 400

    todo = {
        'id': next_id,
        'title': data['title'],
        'completed': False,
        'created_at': datetime.now().isoformat()
    }
    todos[next_id] = todo
    next_id += 1

    return jsonify(todo), 201


@app.route('/api/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    """Get a specific todo."""
    if todo_id not in todos:
        return jsonify({'error': 'Todo not found'}), 404
    return jsonify(todos[todo_id]), 200


@app.route('/api/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    """Update a todo."""
    if todo_id not in todos:
        return jsonify({'error': 'Todo not found'}), 404

    data = request.get_json()
    if 'title' in data:
        todos[todo_id]['title'] = data['title']
    if 'completed' in data:
        todos[todo_id]['completed'] = data['completed']

    return jsonify(todos[todo_id]), 200


@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    """Delete a todo."""
    if todo_id not in todos:
        return jsonify({'error': 'Todo not found'}), 404

    deleted = todos.pop(todo_id)
    return jsonify(deleted), 200


@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors."""
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def server_error(e):
    """Handle 500 errors."""
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
