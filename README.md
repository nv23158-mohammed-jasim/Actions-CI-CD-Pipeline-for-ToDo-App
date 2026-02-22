# Flask ToDo App with GitHub Actions CI/CD Pipeline

A Flask-based ToDo application with full GitHub Actions CI/CD pipeline for automated testing, linting, building, and Docker image deployment.

## Features

- ✨ **Flask Backend**: RESTful API for todo management
- 🧪 **Automated Testing**: Comprehensive pytest test suite
- 🔍 **Code Quality**: Automated linting with flake8
- 🐳 **Docker Support**: Containerized application ready for deployment
- ⚙️ **CI Pipeline**: Automatic testing and linting on push and PR
- 🚀 **CD Pipeline**: Automatic Docker image build and push on releases
- 🔐 **Secure**: Uses GitHub Secrets for credential management

## Project Structure

```
.
├── app.py                          # Flask application
├── Dockerfile                      # Docker containerization
├── requirements.txt                # Python dependencies
├── tests/
│   ├── __init__.py                # Test package
│   └── test_app.py                # Application tests
├── templates/
│   └── index.html                 # Frontend template
└── .github/
    └── workflows/
        ├── ci.yml                 # CI workflow
        ├── cd.yml                 # CD workflow (DockerHub)
        └── cd-ecr.yml             # CD workflow (Amazon ECR)
```

## Installation & Setup

### Local Development

1. Clone the repository
   ```bash
   git clone <repo-url>
   cd Actions-CI-CD-Pipeline-for-ToDo-App
   ```

2. Create virtual environment
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application
   ```bash
   python app.py
   ```
   
   App will be available at `http://localhost:5000`

5. Run tests
   ```bash
   pytest tests/ -v
   pytest tests/ -v --cov=app  # With coverage
   ```

6. Run linting
   ```bash
   flake8 . --max-line-length=127
   ```

## GitHub Actions Workflows

### CI Workflow (`ci.yml`)

Runs automatically on:
- **Push** to `main` or `dev` branches
- **Pull Requests** to `main` or `dev` branches

Steps:
1. Checkout code
2. Set up Python 3.11
3. Install dependencies
4. Run flake8 linting
5. Run pytest tests
6. Upload coverage reports

**Status**: ✅ All tests and lint checks must pass

### CD Workflow (`cd.yml`)

Runs automatically when:
- A **GitHub Release** is published

Steps:
1. Checkout code
2. Set up Docker Buildx
3. Login to Docker registry
4. Extract version from release tag (v0.1.0 → 0.1.0)
5. Build and push Docker image

**Usage**: 
- Configure GitHub Secrets:
  - `DOCKERHUB_USERNAME`: Your Docker Hub username
  - `DOCKERHUB_TOKEN`: Your Docker Hub access token
- Create a release (e.g., v0.1.0) on GitHub
- Workflow runs automatically, pushing image to `username/todo-app:0.1.0`

### CD Workflow for ECR (`cd-ecr.yml`)

Alternative to DockerHub using Amazon ECR.

**Setup**:
- Configure GitHub Secrets:
  - `AWS_ACCESS_KEY_ID`: AWS access key
  - `AWS_SECRET_ACCESS_KEY`: AWS secret key
  - `AWS_REGION`: AWS region (e.g., us-east-1)
- Rename `cd-ecr.yml` to `cd.yml` if using ECR instead of DockerHub

## Docker Usage

### Build locally
```bash
docker build -t todo-app:latest .
```

### Run container
```bash
docker run -p 5000:5000 todo-app:latest
```

### Pull from Docker Hub
```bash
docker pull <username>/todo-app:latest
docker run -p 5000:5000 <username>/todo-app:latest
```

## API Endpoints

### Web Interface
- `GET /` - Render Todo app frontend

### API Endpoints
- `GET /health` - Health check
- `GET /api/todos` - Get all todos
- `POST /api/todos` - Create new todo (body: `{"title": "Task"}`)
- `GET /api/todos/<id>` - Get specific todo
- `PUT /api/todos/<id>` - Update todo (body: `{"title": "...", "completed": true/false}`)
- `DELETE /api/todos/<id>` - Delete todo

## Full CI/CD Flow Example

1. **Create feature branch**
   ```bash
   git checkout dev
   git checkout -b feature/add-labels
   ```

2. **Make changes** (code, tests, etc.)

3. **Push to feature branch**
   ```bash
   git push origin feature/add-labels
   ```

4. **CI workflow runs automatically** ✅

5. **Create Pull Request** dev → main
   - CI runs again on PR
   - All checks must pass

6. **Merge to main**
   ```bash
   git merge dev main
   git push origin main
   ```

7. **Create Release**
   ```bash
   git tag v0.2.0
   git push origin v0.2.0
   ```
   Or use GitHub UI: Releases → Create new release → Publish release

8. **CD workflow runs automatically** 🚀
   - Builds Docker image
   - Tags with version (0.2.0) and latest
   - Pushes to Docker Hub/ECR

9. **Verify deployment**
   - Check Docker Hub/ECR for new image tag
   - Pull and run: `docker run -p 5000:5000 <registry>/todo-app:0.2.0`

## Troubleshooting

| Issue | Solution |
|-------|----------|
| CI fails on import | Check app.py is importable; verify requirements.txt has all deps |
| CI fails lint | Run `flake8 . --max-line-length=127` locally; fix reported issues |
| CD fails to login | Verify DOCKERHUB_USERNAME, DOCKERHUB_TOKEN are set in GitHub Secrets |
| CD doesn't run | Ensure release is published (not draft); check workflow trigger is `types: [published]` |
| Wrong image tag | Release tag must be v-prefixed (e.g., v0.1.0); version extracted automatically |

## Learning Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Documentation](https://docs.docker.com)
- [Flask Documentation](https://flask.palletsprojects.com)
- [pytest Documentation](https://docs.pytest.org)

## License

This project is provided as-is for educational purposes.
