# AvatarForge API

A FastAPI-based foundation for building applications with a clean architecture pattern.

## Project Structure

```
avatarforge/
├── avatarforge/           # Main application package
│   ├── core/             # Core configuration and utilities
│   ├── database/         # Database models and session management
│   ├── rest/             # REST API endpoints
│   ├── schemas/          # Pydantic schemas for validation
│   └── services/         # Business logic layer
├── tests/                # Test suite
│   ├── unit/            # Unit tests
│   └── integration/     # Integration tests
├── main.py              # Application entry point
└── requirements.txt     # Python dependencies
```

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create environment file:
```bash
cp .env.example .env
```

4. Run the application:
```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload
```

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc
- OpenAPI JSON: http://localhost:8000/api/openapi.json

## Testing

Run all tests:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=avatarforge --cov-report=html
```

Run specific test types:
```bash
pytest tests/unit/        # Unit tests only
pytest tests/integration/ # Integration tests only
```

## Development

The project follows a layered architecture:

- **REST Layer** (`avatarforge/rest/`): API endpoints and routing
- **Services Layer** (`avatarforge/services/`): Business logic
- **Database Layer** (`avatarforge/database/`): Data access and models
- **Schemas** (`avatarforge/schemas/`): Request/response validation

## Configuration

Configuration is managed through environment variables (see `.env.example`):

- `PROJECT_NAME`: API project name
- `VERSION`: API version
- `DEBUG`: Enable debug mode
- `HOST`: Server host
- `PORT`: Server port
- `DATABASE_URL`: Database connection string
- `SECRET_KEY`: Secret key for security
- `ALLOWED_ORIGINS`: CORS allowed origins

## License

MIT
