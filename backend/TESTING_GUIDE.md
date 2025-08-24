# 🧪 Blog Generation System - Testing Guide

This guide provides comprehensive testing instructions for your AI-powered blog generation system.

## 🚀 Quick Start

### 1. Start the Backend
```bash
cd backend
python start.py
```

### 2. Verify Backend Health
```bash
# PowerShell
Invoke-WebRequest -Uri "http://localhost:8000/health"

# Or using curl
curl http://localhost:8000/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "service": "blu-blog-gen-backend",
  "version": "1.0.0"
}
```

## 🧪 Complete Workflow Testing

### **Step 1: Create a New Project**
```bash
# PowerShell
$body = @{
    name = "My Test Project"
    description = "Testing AI blog generation"
    total_blogs = 3
    draft_creation_model = "gpt-4"
    content_vetting_model = "gpt-4"
} | ConvertTo-Json

$response = Invoke-WebRequest -Uri "http://localhost:8000/api/v1/projects/" -Method POST -Body $body -ContentType "application/json"
$response.Content
```

**Expected Response:**
```json
{
  "id": "uuid-here",
  "name": "My Test Project",
  "description": "Testing AI blog generation",
  "total_blogs": 3,
  "status": "pending",
  "created_at": "2025-08-24T...",
  "generated_topics": []
}
```

### **Step 2: Generate Blogs for the Project**
```bash
# PowerShell
$body = @{
    project_id = "YOUR_PROJECT_ID_HERE"
    topic = "Digital Marketing Strategies"
    blog_count = 3
} | ConvertTo-Json

$response = Invoke-WebRequest -Uri "http://localhost:8000/api/v1/blogs/generate" -Method POST -Body $body -ContentType "application/json"
$response.Content
```

**Expected Response:**
```json
{
  "status": "started",
  "message": "Blog generation started for 3 blogs about 'Digital Marketing Strategies'",
  "project_id": "your-project-id",
  "generation_id": "gen_...",
  "note": "Real AI generation started in background - check project topics for results"
}
```

### **Step 3: Check Generated Topics**
```bash
# Wait 1-2 minutes for AI processing, then:
Invoke-WebRequest -Uri "http://localhost:8000/api/v1/projects/YOUR_PROJECT_ID_HERE/topics" -Method GET
```

**Expected Response:**
```json
{
  "project_id": "your-project-id",
  "total_topics": 3,
  "topics": [
    {
      "title": "AI-Generated Topic Title",
      "keywords": ["keyword1", "keyword2"],
      "content_length": "medium",
      "target_audience": "target audience",
      "generated_at": "2025-08-24T..."
    }
  ]
}
```

## 🔍 Individual Endpoint Testing

### **List All Projects**
```bash
Invoke-WebRequest -Uri "http://localhost:8000/api/v1/projects/" -Method GET
```

### **Get Specific Project**
```bash
Invoke-WebRequest -Uri "http://localhost:8000/api/v1/projects/PROJECT_ID" -Method GET
```

### **Update Project**
```bash
$body = @{
    name = "Updated Project Name"
    description = "Updated description"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:8000/api/v1/projects/PROJECT_ID" -Method PUT -Body $body -ContentType "application/json"
```

## 🎯 Test Scenarios

### **Scenario 1: Single Blog Generation**
```bash
# Create project
$body = @{ name = "Single Blog Test"; total_blogs = 1; draft_creation_model = "gpt-4"; content_vetting_model = "gpt-4" } | ConvertTo-Json
$project = Invoke-WebRequest -Uri "http://localhost:8000/api/v1/projects/" -Method POST -Body $body -ContentType "application/json" | ConvertFrom-Json

# Generate blog
$body = @{ project_id = $project.id; topic = "AI in Business"; blog_count = 1 } | ConvertTo-Json
Invoke-WebRequest -Uri "http://localhost:8000/api/v1/blogs/generate" -Method POST -Body $body -ContentType "application/json"
```

### **Scenario 2: Multiple Blogs with Different Topics**
```bash
# Create project
$body = @{ name = "Multi Blog Test"; total_blogs = 3; draft_creation_model = "gpt-4"; content_vetting_model = "gpt-4" } | ConvertTo-Json
$project = Invoke-WebRequest -Uri "http://localhost:8000/api/v1/projects/" -Method POST -Body $body -ContentType "application/json" | ConvertFrom-Json

# Generate blogs
$body = @{ project_id = $project.id; topic = "Digital Transformation"; blog_count = 3 } | ConvertTo-Json
Invoke-WebRequest -Uri "http://localhost:8000/api/v1/blogs/generate" -Method POST -Body $body -ContentType "application/json"
```

### **Scenario 3: Test Different Content Lengths**
```bash
# Test various topics that might generate different content lengths
$topics = @("SEO Basics", "Advanced AI Strategies", "Business Growth Tips")

foreach ($topic in $topics) {
    $body = @{ project_id = $project.id; topic = $topic; blog_count = 1 } | ConvertTo-Json
    Invoke-WebRequest -Uri "http://localhost:8000/api/v1/blogs/generate" -Method POST -Body $body -ContentType "application/json"
}
```

## 📊 Monitoring and Verification

### **Check Project Status**
```bash
# Get project details
Invoke-WebRequest -Uri "http://localhost:8000/api/v1/projects/PROJECT_ID" -Method GET

# Check topics
Invoke-WebRequest -Uri "http://localhost:8000/api/v1/projects/PROJECT_ID/topics" -Method GET
```

### **Verify Database Storage**
1. **Check Supabase Dashboard** → Table Editor → `projects` table
2. **Look for**: `generated_topics` field with JSON data
3. **Verify**: Real timestamps instead of mock dates

## 🚨 Troubleshooting

### **Common Issues**

#### **Backend Not Starting**
```bash
# Check if port 8000 is in use
netstat -an | findstr :8000

# Kill existing processes
Get-Process | Where-Object {$_.ProcessName -like "*python*"} | Stop-Process -Force
```

#### **Database Connection Issues**
- Verify `.env` file has correct Supabase credentials
- Check if `SUPABASE_URL` and `SUPABASE_ANON_KEY` are set
- Restart backend after changing environment variables

#### **AI Generation Failing**
- Verify OpenAI/Gemini API keys in `.env` file
- Check API key validity and credits
- Restart backend after adding API keys

#### **Topics Not Storing**
- Wait 1-2 minutes for background processing
- Check project ID exists in database
- Verify `generated_topics` column exists in `projects` table

### **Debug Commands**
```bash
# Check backend logs
# Look for error messages in terminal where backend is running

# Test database connection
python -c "from app.core.database import get_supabase_client; print('DB Client:', get_supabase_client())"

# Test AI service
python -c "from app.services.ai_service import ai_service; print('AI Service:', ai_service)"
```

## 📝 Expected Results

### **Successful Project Creation**
- ✅ Returns real UUID (not mock)
- ✅ Real timestamp in `created_at`
- ✅ Project appears in projects list

### **Successful Blog Generation**
- ✅ Status: "started"
- ✅ Generation ID returned
- ✅ Background processing initiated

### **Successful Topic Storage**
- ✅ Topics appear in `generated_topics` field
- ✅ Real timestamps in `generated_at`
- ✅ Professional, relevant content

## 🔧 Environment Setup

### **Required Environment Variables**
```env
# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your_anon_key

# AI Services (at least one required)
OPENAI_API_KEY=sk-your_openai_key
GEMINI_API_KEY=your_gemini_key
```

### **Installation**
```bash
cd backend
pip install -r requirements.txt
cp env.example .env
# Edit .env with your actual API keys
```

## 📚 Additional Resources

- **Supabase Dashboard**: Monitor database tables and data
- **Backend Logs**: Check terminal for detailed error messages
- **API Documentation**: Available at `http://localhost:8000/docs` when backend is running

---

## 🎯 Quick Test Checklist

- [ ] Backend starts successfully
- [ ] Health endpoint responds
- [ ] Project creation stores in database
- [ ] Blog generation starts
- [ ] Topics are generated and stored
- [ ] Real timestamps appear
- [ ] Data visible in Supabase dashboard

**Your system is ready for production use!** 🚀
