# AI Integration Setup Guide

This guide will help you integrate with real OpenAI and Gemini APIs for actual blog generation.

## 🚀 Quick Start

### 1. Create Environment File

Create a `.env` file in the `backend/` directory:

```bash
# Copy the example file
cp env.example .env
```

### 2. Get API Keys

#### OpenAI API Key
1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Sign in or create an account
3. Click "Create new secret key"
4. Copy the key (starts with `sk-`)

#### Google Gemini API Key
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key

### 3. Configure Environment Variables

Edit your `.env` file and add your API keys:

```env
# AI Service Keys
OPENAI_API_KEY=sk-your_openai_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here

# Supabase Configuration (required)
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_ANON_KEY=your_anon_key_here
```

### 4. Test AI Integration

Run the AI integration test:

```bash
python test_ai_integration.py
```

## 🔧 API Configuration

### OpenAI Models
- **GPT-4**: Most capable, best quality (default)
- **GPT-3.5-turbo**: Faster, more cost-effective
- **Cost**: ~$0.03 per 1K tokens (GPT-4)

### Gemini Models
- **Gemini 1.5 Pro**: High quality, good for content generation
- **Cost**: Free tier available, then $0.0025 per 1K characters

## 📊 Usage Examples

### Generate Topics
```python
from app.services.ai_service import ai_service

# Generate 5 topics about Digital Marketing
topics = await ai_service.generate_topics("Digital Marketing", 5)
```

### Research Topic
```python
# Research a specific topic
research = await ai_service.research_topic("SEO Best Practices")
```

### Generate Blog Content
```python
# Write complete blog content
content = await ai_service.write_blog_content(
    title="SEO Best Practices 2024",
    research=research,
    content_length="long"
)
```

## 🎯 API Endpoints

### Generate Blogs
```bash
POST /api/v1/blogs/generate
{
  "project_id": "your-project-id",
  "topic": "Digital Marketing",
  "blog_count": 3
}
```

### Get Project Topics
```bash
GET /api/v1/projects/{project_id}/topics
```

## ⚠️ Important Notes

1. **API Costs**: OpenAI and Gemini charge per token/character
2. **Rate Limits**: Respect API rate limits to avoid errors
3. **Content Quality**: AI-generated content should be reviewed before publishing
4. **Fallback**: System falls back to mock data if APIs are unavailable

## 🧪 Testing

### Test AI Service Directly
```bash
python test_ai_integration.py
```

### Test via API
```bash
# Start backend
python start.py

# Test blog generation
curl -X POST "http://localhost:8000/api/v1/blogs/generate" \
  -H "Content-Type: application/json" \
  -d '{"project_id":"test","topic":"AI Writing","blog_count":2}'
```

## 🔍 Troubleshooting

### Common Issues

1. **"No AI API keys configured"**
   - Check your `.env` file
   - Verify API keys are correct
   - Restart the backend after adding keys

2. **"OpenAI API call failed"**
   - Check API key validity
   - Verify account has credits
   - Check rate limits

3. **"Gemini API call failed"**
   - Verify API key format
   - Check Google AI Studio quota
   - Ensure model is available

### Debug Mode

Enable debug logging in `.env`:
```env
LOG_LEVEL=DEBUG
DEBUG=true
```

## 💰 Cost Optimization

### OpenAI
- Use GPT-3.5-turbo for drafts
- Use GPT-4 for final content
- Set reasonable token limits

### Gemini
- Use free tier for testing
- Upgrade only when needed
- Monitor usage in Google AI Studio

## 🚀 Production Deployment

1. **Secure API Keys**: Use environment variables, never commit to code
2. **Monitor Usage**: Track API costs and usage
3. **Rate Limiting**: Implement proper rate limiting
4. **Error Handling**: Graceful fallbacks for API failures
5. **Content Review**: Always review AI-generated content

## 📚 Additional Resources

- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Google AI Studio](https://makersuite.google.com/)
- [FastAPI Background Tasks](https://fastapi.tiangolo.com/tutorial/background-tasks/)
- [Supabase Documentation](https://supabase.com/docs)
