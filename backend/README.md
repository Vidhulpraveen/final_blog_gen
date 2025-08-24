# 🐍 Blu Blog Gen Backend

A powerful Python FastAPI backend for AI-powered blog generation, designed to integrate seamlessly with your Next.js frontend and Supabase database.

## 🚀 Features

- **AI-Powered Blog Generation**: Support for OpenAI GPT, Anthropic Claude, and Google Gemini
- **Multi-Phase Generation**: Research → Content → SEO Optimization → Analytics
- **Supabase Integration**: Seamless database operations with Row Level Security
- **RESTful API**: Clean, documented endpoints for all blog operations
- **Authentication & Authorization**: JWT-based security with role-based access control
- **Rate Limiting**: Configurable request throttling
- **Comprehensive Logging**: Structured logging with multiple levels
- **WordPress Integration**: Publish blogs directly to WordPress sites
- **SEO Optimization**: Built-in SEO scoring and optimization
- **Analytics**: Blog performance metrics and insights

## 🏗️ Architecture

```
backend/
├── app/
│   ├── api/           # API endpoints and routes
│   ├── core/          # Core configuration and utilities
│   ├── models/        # Pydantic data models
│   ├── services/      # Business logic services
│   └── utils/         # Utility functions
├── tests/             # Test suite
├── docs/              # Documentation
├── requirements.txt   # Python dependencies
└── README.md         # This file
```

## 🛠️ Tech Stack

- **Framework**: FastAPI 0.104+
- **Python**: 3.8+
- **Database**: Supabase (PostgreSQL)
- **AI Services**: OpenAI, Anthropic, Google Gemini
- **Authentication**: JWT with Passlib
- **Validation**: Pydantic
- **Logging**: Structlog
- **Testing**: Pytest
- **Documentation**: Auto-generated OpenAPI/Swagger

## 📋 Prerequisites

- Python 3.8 or higher
- Supabase project with service role key
- AI service API keys (OpenAI, Anthropic, or Gemini)
- Virtual environment (recommended)

## 🚀 Quick Start

### 1. Clone and Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Configuration

```bash
# Copy environment template
cp env.example .env

# Edit .env with your credentials
# Required: SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY
# Optional: AI service API keys
```

### 3. Start Development Server

```bash
# Start with auto-reload
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or use the main.py directly
python app/main.py
```

### 4. Access API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `DEBUG` | Enable debug mode | No | `false` |
| `HOST` | Server host | No | `0.0.0.0` |
| `PORT` | Server port | No | `8000` |
| `SUPABASE_URL` | Supabase project URL | **Yes** | - |
| `SUPABASE_SERVICE_ROLE_KEY` | Supabase service role key | **Yes** | - |
| `OPENAI_API_KEY` | OpenAI API key | No | - |
| `ANTHROPIC_API_KEY` | Anthropic API key | No | - |
| `GEMINI_API_KEY` | Google Gemini API key | No | - |
| `SECRET_KEY` | JWT secret key | No | Auto-generated |

### AI Service Configuration

The backend supports multiple AI providers:

- **OpenAI**: GPT-4, GPT-3.5-turbo
- **Anthropic**: Claude 3.5 Sonnet, Claude 3.7 Sonnet
- **Google Gemini**: Gemini Pro, Gemini Pro Vision

Configure your preferred providers in the `.env` file.

## 📚 API Endpoints

### Authentication
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/refresh` - Refresh access token

### Blog Generation
- `POST /api/v1/blogs/generate` - Generate new blog
- `GET /api/v1/blogs/{blog_id}` - Get specific blog
- `GET /api/v1/blogs/` - List user blogs
- `PUT /api/v1/blogs/{blog_id}` - Update blog
- `DELETE /api/v1/blogs/{blog_id}` - Delete blog
- `POST /api/v1/blogs/search` - Search blogs
- `POST /api/v1/blogs/{blog_id}/publish` - Publish blog
- `POST /api/v1/blogs/{blog_id}/archive` - Archive blog

### User Management
- `GET /api/v1/users/profile` - Get user profile
- `PUT /api/v1/users/profile` - Update user profile
- `GET /api/v1/users/stats` - Get user statistics

### Projects
- `GET /api/v1/projects/` - List user projects
- `POST /api/v1/projects/` - Create new project
- `GET /api/v1/projects/{project_id}` - Get project details

## 🔐 Authentication

The backend uses JWT tokens for authentication:

1. **Login**: Send credentials to `/api/v1/auth/login`
2. **Token**: Receive access token in response
3. **Authorization**: Include token in `Authorization: Bearer <token>` header
4. **Refresh**: Use refresh token to get new access token

### Example Request

```bash
curl -X POST "http://localhost:8000/api/v1/blogs/generate" \
  -H "Authorization: Bearer your_jwt_token_here" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "AI in Modern Business",
    "target_keywords": ["artificial intelligence", "business automation"],
    "target_word_count": 1500,
    "tone": "professional"
  }'
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_blog_service.py

# Run with verbose output
pytest -v
```

## 📊 Blog Generation Process

The AI blog generation follows a multi-phase approach:

### Phase 1: Research
- Generate strategic search queries
- Analyze competitors
- Identify trending topics
- Gather local market insights

### Phase 2: Content Generation
- Create comprehensive blog content
- Optimize for target keywords
- Apply specified tone and style
- Generate meta information

### Phase 3: SEO Optimization
- Optimize content structure
- Improve keyword density
- Enhance readability
- Generate meta descriptions

### Phase 4: Enhancement
- Suggest relevant images
- Recommend external links
- Calculate SEO score
- Generate analytics

## 🔒 Security Features

- **JWT Authentication**: Secure token-based authentication
- **Role-Based Access Control**: User, moderator, and admin roles
- **Row Level Security**: Database-level security with Supabase
- **Rate Limiting**: Prevent API abuse
- **Input Validation**: Pydantic model validation
- **CORS Protection**: Configurable cross-origin policies

## 📈 Monitoring & Logging

- **Structured Logging**: JSON-formatted logs with context
- **Request Tracking**: Log all API requests and responses
- **Error Monitoring**: Comprehensive error logging and tracking
- **Performance Metrics**: Generation time and cost tracking
- **Sentry Integration**: Optional error tracking service

## 🚀 Deployment

### Development
```bash
python -m uvicorn app.main:app --reload
```

### Production
```bash
# Using Gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker

# Using Docker
docker build -t blu-blog-gen-backend .
docker run -p 8000:8000 blu-blog-gen-backend
```

### Environment Variables
Ensure all required environment variables are set in production:
- `DEBUG=false`
- `SECRET_KEY` (strong, unique key)
- `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY`
- AI service API keys

## 🤝 Integration with Frontend

The backend is designed to work seamlessly with your Next.js frontend:

1. **CORS Configuration**: Pre-configured for localhost:3000
2. **API Endpoints**: RESTful endpoints matching frontend needs
3. **Data Models**: Consistent data structures
4. **Authentication**: JWT tokens for secure communication

## 🆘 Troubleshooting

### Common Issues

1. **Database Connection Failed**
   - Check Supabase credentials
   - Verify network connectivity
   - Ensure service role key has proper permissions

2. **AI Generation Fails**
   - Verify API keys are valid
   - Check API rate limits
   - Ensure sufficient API credits

3. **Authentication Errors**
   - Verify JWT secret key
   - Check token expiration
   - Ensure proper token format

### Debug Mode

Enable debug mode for detailed error information:
```bash
DEBUG=true python -m uvicorn app.main:app --reload
```

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Supabase Documentation](https://supabase.com/docs)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Anthropic API Documentation](https://docs.anthropic.com/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

---

**Need Help?** Create an issue or contact the development team.

**Happy Blogging! 🚀**
