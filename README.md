# AvatarForge API

**Purpose:**  
AI-powered avatar generation system with ComfyUI integration, file management, and deduplication.

**Why this exists:**  
To enable high-quality, locally-controlled AI avatar generation for games and applications. By leveraging local GPU resources (or the DGX server), it avoids the costs and rate limits of external APIs while providing granular control over the generation pipeline via ComfyUI.

## Features

- **Avatar Generation**: Generate high-quality avatars with customizable prompts, styles, and poses
- **Multi-Pose Support**: Generate front, back, side, and quarter views
- **File Management**: Automatic deduplication and reference counting
- **ComfyUI Integration**: Leverage ComfyUI's powerful workflow system
- **Quality Controls**: Adjustable resolution, steps, CFG scale, and samplers
- **Scheduled Cleanup**: Automatic orphaned file cleanup
- **RESTful API**: Clean, well-documented FastAPI endpoints

## Quick Links

- **[Generation Guide](docs/GENERATION_GUIDE.md)** - Complete guide to generating avatars
- **[API Documentation](API_DOCUMENTATION.md)** - Full API reference
- **[TODO List](TODO.md)** - Development roadmap and progress

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

## Quick Start

### Generate Your First Avatar

```bash
curl -X POST "http://localhost:8000/avatarforge-controller/generate/avatar" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "fantasy warrior with sword",
    "clothing": "leather armor, cape",
    "realism": false,
    "width": 768,
    "height": 768,
    "steps": 30
  }'
```

View the complete generation guide at **[docs/GENERATION_GUIDE.md](docs/GENERATION_GUIDE.md)**

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- OpenAPI JSON: http://localhost:8000/openapi.json

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
