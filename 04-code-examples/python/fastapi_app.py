#!/usr/bin/env python3
"""
FastAPI Web Application for GenAI Demos
Provides REST API endpoints for various GenAI capabilities
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import uvicorn
import asyncio
import json
from datetime import datetime
import logging

# Import our demo classes
from genai_demo import TextGenerationDemo, RAGDemo
from prompt_engineering import PromptEngineeringDemo

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="GenAI Future Opportunities & Skills API",
    description="Comprehensive API for exploring GenAI capabilities, opportunities, and best practices",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize demo components
text_gen = TextGenerationDemo()
rag_system = RAGDemo()
prompt_eng = PromptEngineeringDemo()

# Pydantic models for API requests/responses
class TextGenerationRequest(BaseModel):
    prompt: str = Field(..., description="Text prompt for generation")
    max_length: int = Field(50, ge=10, le=500, description="Maximum length of generated text")
    model_type: str = Field("local", description="Type of model to use")

class SentimentAnalysisRequest(BaseModel):
    text: str = Field(..., description="Text to analyze for sentiment")

class RAGRequest(BaseModel):
    query: str = Field(..., description="Search query")
    top_k: int = Field(3, ge=1, le=10, description="Number of top results to return")

class PromptAnalysisRequest(BaseModel):
    prompt: str = Field(..., description="Prompt to analyze")

class ProjectCreateRequest(BaseModel):
    name: str = Field(..., description="Project name")
    description: str = Field(..., description="Project description")
    model_type: str = Field(..., description="Type of AI model")
    use_case: str = Field(..., description="Business use case")

class ProjectResponse(BaseModel):
    id: str
    name: str
    description: str
    model_type: str
    use_case: str
    created_date: str
    status: str
    performance_metrics: Dict[str, Any]

# In-memory storage for projects
projects_db = {}
project_counter = 0

@app.get("/", response_class=HTMLResponse)
async def root():
    """Root endpoint with beautiful HTML landing page"""
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>GenAI Future Opportunities & Skills API</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 0;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                min-height: 100vh;
            }
            .container {
                max-width: 1200px;
                margin: 0 auto;
                padding: 2rem;
            }
            .header {
                text-align: center;
                margin-bottom: 3rem;
            }
            .header h1 {
                font-size: 3rem;
                margin-bottom: 1rem;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            }
            .header p {
                font-size: 1.2rem;
                opacity: 0.9;
            }
            .features {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 2rem;
                margin-bottom: 3rem;
            }
            .feature-card {
                background: rgba(255,255,255,0.1);
                padding: 2rem;
                border-radius: 15px;
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255,255,255,0.2);
                transition: transform 0.3s ease;
            }
            .feature-card:hover {
                transform: translateY(-5px);
            }
            .feature-card h3 {
                color: #ffd700;
                margin-bottom: 1rem;
            }
            .api-links {
                text-align: center;
                margin-top: 2rem;
            }
            .api-links a {
                display: inline-block;
                margin: 0.5rem;
                padding: 1rem 2rem;
                background: #ffd700;
                color: #333;
                text-decoration: none;
                border-radius: 25px;
                font-weight: bold;
                transition: all 0.3s ease;
            }
            .api-links a:hover {
                background: #ffed4e;
                transform: scale(1.05);
            }
            .stats {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 1rem;
                margin: 2rem 0;
            }
            .stat-card {
                background: rgba(255,255,255,0.1);
                padding: 1.5rem;
                border-radius: 10px;
                text-align: center;
            }
            .stat-number {
                font-size: 2rem;
                font-weight: bold;
                color: #ffd700;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🚀 GenAI Future Opportunities & Skills</h1>
                <p>Comprehensive API for exploring the future of Generative AI</p>
            </div>
            
            <div class="stats">
                <div class="stat-card">
                    <div class="stat-number">5</div>
                    <div>Core Modules</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">15+</div>
                    <div>API Endpoints</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">3</div>
                    <div>Technology Stacks</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">100%</div>
                    <div>Hackathon Ready</div>
                </div>
            </div>
            
            <div class="features">
                <div class="feature-card">
                    <h3>🎯 Future Opportunities</h3>
                    <p>Explore industry-specific applications, emerging trends, and long-term transformations in GenAI across healthcare, manufacturing, finance, and education.</p>
                </div>
                <div class="feature-card">
                    <h3>🛠️ Essential Skills</h3>
                    <p>Master technical foundations, AI/ML specific skills, and soft skills needed to stay relevant in the GenAI era.</p>
                </div>
                <div class="feature-card">
                    <h3>⚠️ Adoption Strategies</h3>
                    <p>Learn from common mistakes companies make and implement best practices for successful AI adoption.</p>
                </div>
                <div class="feature-card">
                    <h3>💻 Code Examples</h3>
                    <p>Hands-on implementations in Python, JavaScript, and web applications with production-ready code.</p>
                </div>
            </div>
            
            <div class="api-links">
                <a href="/docs">📚 API Documentation</a>
                <a href="/redoc">📖 Alternative Docs</a>
                <a href="/health">🏥 Health Check</a>
                <a href="/demo">🎮 Live Demo</a>
            </div>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "services": {
            "text_generation": "operational",
            "rag_system": "operational",
            "prompt_engineering": "operational"
        }
    }

@app.post("/api/generate-text", response_model=Dict[str, Any])
async def generate_text(request: TextGenerationRequest):
    """Generate text using AI models"""
    try:
        if request.model_type == "local":
            generated_text = text_gen.generate_text(request.prompt, request.max_length)
        else:
            generated_text = f"Model type '{request.model_type}' not implemented yet"
        
        return {
            "success": True,
            "prompt": request.prompt,
            "generated_text": generated_text,
            "model_type": request.model_type,
            "max_length": request.max_length,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error generating text: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/analyze-sentiment", response_model=Dict[str, Any])
async def analyze_sentiment(request: SentimentAnalysisRequest):
    """Analyze sentiment of given text"""
    try:
        sentiment_result = text_gen.analyze_sentiment(request.text)
        
        return {
            "success": True,
            "text": request.text,
            "sentiment": sentiment_result.get("sentiment", "unknown"),
            "confidence": sentiment_result.get("confidence", 0.0),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error analyzing sentiment: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/rag-search", response_model=Dict[str, Any])
async def rag_search(request: RAGRequest):
    """Search documents using RAG system"""
    try:
        # Add some sample documents if none exist
        if not rag_system.documents:
            sample_docs = [
                "AI is transforming healthcare through improved diagnosis and treatment planning.",
                "Machine learning algorithms can predict equipment failures in manufacturing.",
                "AI-powered chatbots revolutionize customer service with 24/7 availability.",
                "Generative AI creates new opportunities in content creation and creative industries.",
                "Edge AI enables real-time processing and privacy-preserving applications."
            ]
            rag_system.add_documents(sample_docs)
        
        search_results = rag_system.search_documents(request.query, request.top_k)
        
        return {
            "success": True,
            "query": request.query,
            "results": search_results,
            "total_documents": len(rag_system.documents),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error in RAG search: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/analyze-prompt", response_model=Dict[str, Any])
async def analyze_prompt(request: PromptAnalysisRequest):
    """Analyze prompt effectiveness"""
    try:
        analysis = prompt_eng.analyze_prompt_effectiveness(request.prompt)
        
        return {
            "success": True,
            "prompt": request.prompt,
            "analysis": analysis,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error analyzing prompt: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/prompt-techniques", response_model=Dict[str, Any])
async def get_prompt_techniques():
    """Get available prompt engineering techniques"""
    try:
        techniques = {}
        for technique, description in prompt_eng.techniques.items():
            examples = prompt_eng.get_examples_by_technique(technique)
            techniques[technique] = {
                "description": description,
                "examples_count": len(examples),
                "difficulty_levels": list(set(ex.difficulty for ex in examples))
            }
        
        return {
            "success": True,
            "techniques": techniques,
            "total_techniques": len(techniques),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting prompt techniques: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/projects", response_model=ProjectResponse)
async def create_project(request: ProjectCreateRequest):
    """Create a new GenAI project"""
    global project_counter
    try:
        project_counter += 1
        project_id = f"proj_{project_counter:04d}"
        
        project = {
            "id": project_id,
            "name": request.name,
            "description": request.description,
            "model_type": request.model_type,
            "use_case": request.use_case,
            "created_date": datetime.now().isoformat(),
            "status": "active",
            "performance_metrics": {
                "accuracy": 0.0,
                "latency": 0.0,
                "user_satisfaction": 0.0,
                "last_updated": datetime.now().isoformat()
            }
        }
        
        projects_db[project_id] = project
        
        logger.info(f"Created project: {project_id}")
        return project
    except Exception as e:
        logger.error(f"Error creating project: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/projects", response_model=List[ProjectResponse])
async def list_projects():
    """List all GenAI projects"""
    try:
        return list(projects_db.values())
    except Exception as e:
        logger.error(f"Error listing projects: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/projects/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: str):
    """Get a specific project by ID"""
    try:
        if project_id not in projects_db:
            raise HTTPException(status_code=404, detail="Project not found")
        return projects_db[project_id]
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting project: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/projects/{project_id}/metrics")
async def update_project_metrics(project_id: str, metrics: Dict[str, Any]):
    """Update project performance metrics"""
    try:
        if project_id not in projects_db:
            raise HTTPException(status_code=404, detail="Project not found")
        
        projects_db[project_id]["performance_metrics"].update(metrics)
        projects_db[project_id]["performance_metrics"]["last_updated"] = datetime.now().isoformat()
        
        logger.info(f"Updated metrics for project: {project_id}")
        return {"success": True, "message": "Metrics updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating project metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stats", response_model=Dict[str, Any])
async def get_api_stats():
    """Get API usage statistics"""
    try:
        return {
            "total_projects": len(projects_db),
            "active_projects": len([p for p in projects_db.values() if p["status"] == "active"]),
            "total_documents": len(rag_system.documents) if hasattr(rag_system, 'documents') else 0,
            "available_techniques": len(prompt_eng.techniques),
            "api_version": "1.0.0",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting API stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/demo")
async def demo_page():
    """Interactive demo page"""
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>GenAI Live Demo</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                min-height: 100vh;
            }
            .demo-container {
                max-width: 800px;
                margin: 0 auto;
                background: rgba(255,255,255,0.1);
                padding: 2rem;
                border-radius: 15px;
                backdrop-filter: blur(10px);
            }
            .demo-section {
                margin-bottom: 2rem;
                padding: 1rem;
                background: rgba(255,255,255,0.05);
                border-radius: 10px;
            }
            input, textarea, button {
                width: 100%;
                padding: 0.8rem;
                margin: 0.5rem 0;
                border: none;
                border-radius: 5px;
                font-size: 1rem;
            }
            button {
                background: #ffd700;
                color: #333;
                cursor: pointer;
                font-weight: bold;
            }
            button:hover {
                background: #ffed4e;
            }
            .result {
                background: rgba(0,0,0,0.3);
                padding: 1rem;
                border-radius: 5px;
                margin-top: 1rem;
                white-space: pre-wrap;
            }
        </style>
    </head>
    <body>
        <div class="demo-container">
            <h1>🎮 GenAI Live Demo</h1>
            
            <div class="demo-section">
                <h3>📝 Text Generation</h3>
                <textarea id="promptInput" placeholder="Enter your prompt here..." rows="3"></textarea>
                <button onclick="generateText()">Generate Text</button>
                <div id="textResult" class="result" style="display: none;"></div>
            </div>
            
            <div class="demo-section">
                <h3>😊 Sentiment Analysis</h3>
                <textarea id="sentimentInput" placeholder="Enter text to analyze..." rows="3"></textarea>
                <button onclick="analyzeSentiment()">Analyze Sentiment</button>
                <div id="sentimentResult" class="result" style="display: none;"></div>
            </div>
            
            <div class="demo-section">
                <h3>🔍 RAG Search</h3>
                <input id="queryInput" placeholder="Enter your search query..." />
                <button onclick="ragSearch()">Search Documents</button>
                <div id="ragResult" class="result" style="display: none;"></div>
            </div>
            
            <div class="demo-section">
                <h3>📊 API Statistics</h3>
                <button onclick="getStats()">Get API Stats</button>
                <div id="statsResult" class="result" style="display: none;"></div>
            </div>
        </div>
        
        <script>
            async function generateText() {
                const prompt = document.getElementById('promptInput').value;
                if (!prompt) return;
                
                try {
                    const response = await fetch('/api/generate-text', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({prompt, max_length: 100, model_type: 'local'})
                    });
                    const result = await response.json();
                    document.getElementById('textResult').textContent = JSON.stringify(result, null, 2);
                    document.getElementById('textResult').style.display = 'block';
                } catch (error) {
                    document.getElementById('textResult').textContent = 'Error: ' + error.message;
                    document.getElementById('textResult').style.display = 'block';
                }
            }
            
            async function analyzeSentiment() {
                const text = document.getElementById('sentimentInput').value;
                if (!text) return;
                
                try {
                    const response = await fetch('/api/analyze-sentiment', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({text})
                    });
                    const result = await response.json();
                    document.getElementById('sentimentResult').textContent = JSON.stringify(result, null, 2);
                    document.getElementById('sentimentResult').style.display = 'block';
                } catch (error) {
                    document.getElementById('sentimentResult').textContent = 'Error: ' + error.message;
                    document.getElementById('sentimentResult').style.display = 'block';
                }
            }
            
            async function ragSearch() {
                const query = document.getElementById('queryInput').value;
                if (!query) return;
                
                try {
                    const response = await fetch('/api/rag-search', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({query, top_k: 3})
                    });
                    const result = await response.json();
                    document.getElementById('ragResult').textContent = JSON.stringify(result, null, 2);
                    document.getElementById('ragResult').style.display = 'block';
                } catch (error) {
                    document.getElementById('ragResult').textContent = 'Error: ' + error.message;
                    document.getElementById('ragResult').style.display = 'block';
                }
            }
            
            async function getStats() {
                try {
                    const response = await fetch('/api/stats');
                    const result = await response.json();
                    document.getElementById('statsResult').textContent = JSON.stringify(result, null, 2);
                    document.getElementById('statsResult').style.display = 'block';
                } catch (error) {
                    document.getElementById('statsResult').textContent = 'Error: ' + error.message;
                    document.getElementById('statsResult').style.display = 'block';
                }
            }
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
