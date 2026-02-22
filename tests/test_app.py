"""
Test suite for Flask ToDo App
"""
import pytest
from app import app


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_app_import():
    """Test that the app can be imported successfully."""
    assert app is not None


def test_index_route(client):
    """Test that the index route returns 200."""
    rv = client.get('/')
    assert rv.status_code == 200


def test_health_endpoint(client):
    """Test the health check endpoint."""
    rv = client.get('/health')
    assert rv.status_code == 200
    data = rv.get_json()
    assert data['status'] == 'healthy'
    assert 'version' in data


def test_get_todos(client):
    """Test getting all todos."""
    rv = client.get('/api/todos')
    assert rv.status_code == 200
    data = rv.get_json()
    assert isinstance(data, list)
    assert len(data) > 0  # Should have at least the default todos


def test_create_todo(client):
    """Test creating a new todo."""
    rv = client.post('/api/todos', json={'title': 'Test Task'})
    assert rv.status_code == 201
    data = rv.get_json()
    assert data['title'] == 'Test Task'
    assert data['completed'] is False
    assert 'id' in data


def test_create_todo_missing_title(client):
    """Test creating a todo without a title."""
    rv = client.post('/api/todos', json={})
    assert rv.status_code == 400
    data = rv.get_json()
    assert 'error' in data


def test_get_specific_todo(client):
    """Test getting a specific todo."""
    rv = client.get('/api/todos/1')
    assert rv.status_code == 200
    data = rv.get_json()
    assert data['id'] == 1


def test_get_nonexistent_todo(client):
    """Test getting a todo that doesn't exist."""
    rv = client.get('/api/todos/9999')
    assert rv.status_code == 404


def test_update_todo(client):
    """Test updating a todo."""
    rv = client.put('/api/todos/1', json={'title': 'Updated Task'})
    assert rv.status_code == 200
    data = rv.get_json()
    assert data['title'] == 'Updated Task'


def test_toggle_todo_completion(client):
    """Test toggling todo completion status."""
    rv = client.put('/api/todos/1', json={'completed': True})
    assert rv.status_code == 200
    data = rv.get_json()
    assert data['completed'] is True


def test_delete_todo(client):
    """Test deleting a todo."""
    # Create a todo first
    create_rv = client.post('/api/todos', json={'title': 'Delete Me'})
    todo_id = create_rv.get_json()['id']

    # Delete it
    rv = client.delete(f'/api/todos/{todo_id}')
    assert rv.status_code == 200

    # Verify it's gone
    get_rv = client.get(f'/api/todos/{todo_id}')
    assert get_rv.status_code == 404


def test_delete_nonexistent_todo(client):
    """Test deleting a todo that doesn't exist."""
    rv = client.delete('/api/todos/9999')
    assert rv.status_code == 404


def test_404_error_handler(client):
    """Test 404 error handler."""
    rv = client.get('/nonexistent-route')
    assert rv.status_code == 404
    data = rv.get_json()
    assert 'error' in data


def test_get_stats(client):
    """Test the stats endpoint."""
    rv = client.get('/api/todos/stats')
    assert rv.status_code == 200
    data = rv.get_json()
    assert 'total' in data
    assert 'completed' in data
    assert 'pending' in data
    assert 'completion_rate' in data
    assert data['total'] > 0
