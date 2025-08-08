"""
SkillForge AI - Working FastAPI Website for Vercel
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from datetime import datetime

app = FastAPI(
    title="SkillForge AI - Career Intelligence Platform",
    version="1.0.0",
    description="AI-Powered Career Intelligence Platform"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
def read_root():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>SkillForge AI - Career Intelligence Platform</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }
            
            .container {
                max-width: 1200px;
                margin: 0 auto;
                background: rgba(255, 255, 255, 0.95);
                border-radius: 20px;
                padding: 40px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            }
            
            .header {
                text-align: center;
                margin-bottom: 40px;
            }
            
            .logo { font-size: 3rem; margin-bottom: 10px; }
            
            h1 {
                color: #2c3e50;
                font-size: 2.5rem;
                margin-bottom: 10px;
            }
            
            .subtitle {
                color: #7f8c8d;
                font-size: 1.2rem;
                margin-bottom: 20px;
            }
            
            .status {
                background: #27ae60;
                color: white;
                padding: 8px 16px;
                border-radius: 20px;
                font-weight: bold;
                display: inline-block;
            }
            
            .features {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 20px;
                margin: 40px 0;
            }
            
            .feature-card {
                background: #f8f9fa;
                padding: 25px;
                border-radius: 15px;
                border-left: 5px solid #3498db;
                transition: transform 0.3s ease;
            }
            
            .feature-card:hover { transform: translateY(-5px); }
            
            .feature-card h3 {
                color: #2c3e50;
                margin-bottom: 10px;
                font-size: 1.3rem;
            }
            
            .feature-card p {
                color: #7f8c8d;
                line-height: 1.6;
            }
            
            .api-section {
                background: #2c3e50;
                color: white;
                padding: 30px;
                border-radius: 15px;
                margin-top: 40px;
            }
            
            .api-section h2 {
                margin-bottom: 20px;
                color: #ecf0f1;
            }
            
            .endpoints {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 15px;
            }
            
            .endpoint {
                background: #34495e;
                padding: 15px;
                border-radius: 10px;
                text-decoration: none;
                color: #ecf0f1;
                transition: background 0.3s ease;
            }
            
            .endpoint:hover {
                background: #3498db;
                color: white;
            }
            
            .agent-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 20px;
                margin: 30px 0;
            }
            
            .agent-card {
                background: linear-gradient(145deg, #f0f0f0, #ffffff);
                padding: 25px;
                border-radius: 15px;
                box-shadow: 0 10px 20px rgba(0,0,0,0.1);
                border: 1px solid #e1e8ed;
            }
            
            .agent-card h4 {
                color: #2c3e50;
                margin-bottom: 15px;
                font-size: 1.4rem;
            }
            
            .agent-features {
                list-style: none;
            }
            
            .agent-features li {
                padding: 5px 0;
                color: #7f8c8d;
            }
            
            .agent-features li:before {
                content: "✅ ";
                margin-right: 8px;
            }
            
            .footer {
                text-align: center;
                margin-top: 40px;
                padding-top: 20px;
                border-top: 1px solid #ecf0f1;
                color: #7f8c8d;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="logo">🚀</div>
                <h1>SkillForge AI</h1>
                <p class="subtitle">Career Intelligence Platform</p>
                <div class="status">🟢 LIVE & OPERATIONAL</div>
            </div>
            
            <div class="features">
                <div class="feature-card">
                    <h3>🤖 AI-Powered Career Analysis</h3>
                    <p>Advanced artificial intelligence analyzes your skills, experience, and career goals to provide personalized insights and recommendations.</p>
                </div>
                
                <div class="feature-card">
                    <h3>📊 Market Intelligence</h3>
                    <p>Real-time job market data and salary benchmarking for the Canadian tech industry, helping you make informed career decisions.</p>
                </div>
                
                <div class="feature-card">
                    <h3>⚡ Workflow Optimization</h3>
                    <p>Streamlined processes and automated workflows to accelerate your career development and skill enhancement journey.</p>
                </div>
            </div>
            
            <div class="agent-grid">
                <div class="agent-card">
                    <h4>🔍 Analysis Agent</h4>
                    <ul class="agent-features">
                        <li>Market Intelligence</li>
                        <li>Salary Analysis</li>
                        <li>Skill Assessment</li>
                    </ul>
                </div>
                
                <div class="agent-card">
                    <h4>⚙️ Workflow Agent</h4>
                    <ul class="agent-features">
                        <li>Process Design</li>
                        <li>Task Automation</li>
                        <li>Timeline Planning</li>
                    </ul>
                </div>
                
                <div class="agent-card">
                    <h4>🎯 Execution Agent</h4>
                    <ul class="agent-features">
                        <li>Implementation</li>
                        <li>Monitoring</li>
                        <li>Quality Assurance</li>
                    </ul>
                </div>
            </div>
            
            <div class="api-section">
                <h2>🔗 API Endpoints</h2>
                <div class="endpoints">
                    <a href="/health" class="endpoint">
                        <strong>GET /health</strong><br>
                        Health check and system status
                    </a>
                    
                    <a href="/test" class="endpoint">
                        <strong>GET /test</strong><br>
                        Deployment verification
                    </a>
                    
                    <a href="/api/agents/list" class="endpoint">
                        <strong>GET /api/agents/list</strong><br>
                        List all AI agents and capabilities
                    </a>
                </div>
            </div>
            
            <div class="footer">
                <p>🌟 SkillForge AI v1.0.0 | Built with FastAPI & Deployed on Vercel</p>
                <p>Career Intelligence Platform - Powered by AI</p>
            </div>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/health")  
def health():
    return {
        "status": "healthy", 
        "timestamp": datetime.now().isoformat(),
        "service": "SkillForge AI"
    }

@app.get("/test")
def test():
    return {
        "test": "✅ Endpoint working perfectly",
        "framework": "FastAPI",
        "deployment": "Vercel Production",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/agents/list")
def agents():
    return {
        "agents": [
            {
                "type": "analysis_agent",
                "name": "Career Analysis Agent",
                "status": "active",
                "features": ["Market Intelligence", "Salary Analysis", "Skill Assessment"]
            },
            {
                "type": "workflow_agent", 
                "name": "Workflow Optimization Agent",
                "status": "active",
                "features": ["Process Design", "Task Automation", "Timeline Planning"]
            },
            {
                "type": "execution_agent",
                "name": "Task Execution Agent", 
                "status": "active",
                "features": ["Implementation", "Monitoring", "Quality Assurance"]
            }
        ],
        "total": 3,
        "framework": "FastAPI",
        "status": "production_ready"
    }
