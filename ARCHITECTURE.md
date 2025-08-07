# 🏗️ SkillForge AI - System Architecture (Current MVP)

## 🎯 Executive Summary

SkillForge AI is a FastAPI-based career intelligence platform that integrates OpenAI GPT-4o-mini with CrewAI multi-agent system to deliver personalized career guidance. The current MVP focuses on core functionality with a simple, effective architecture.

### 🌟 Current Implementation
- **FastAPI Backend**: Single server application with API routes
- **CrewAI Multi-Agent**: Analysis, Workflow, and Execution agents
- **OpenAI Integration**: GPT-4o-mini for intelligent responses
- **Simple Storage**: Environment configuration + in-memory dictionaries
- **Web Interface**: HTML templates with static CSS/JS files

## 🏛️ Current System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                            SkillForge AI Platform                                        │
│                        Current Implementation (MVP)                                      │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                Frontend Layer                                            │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                          │
│  │  HTML Templates │  │   Static Files  │  │   FastAPI Docs  │                          │
│  │  • index.html   │  │  • CSS/JS       │  │  • Auto-generated│                         │
│  │  • analytics    │  │  • Styling      │  │  • Interactive  │                          │
│  │  • Jinja2       │  │  • UI Scripts   │  │  • API Testing  │                          │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘                          │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                            FastAPI Backend                                               │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐    │
│  │   Main Server   │  │   API Routes    │  │   CORS Middleware│  │   Health Check  │    │
│  │  • Uvicorn      │  │  • Workflows    │  │  • Allow Origins│  │  • System Info  │    │
│  │  • Port 8000    │  │  • Agents       │  │  • All Methods  │  │  • Status Check │    │
│  │  • Debug Mode   │  │  • Analytics    │  │  • Headers OK   │  │  • API Endpoints│    │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  └─────────────────┘    │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                         AI/ML Intelligence Layer                                         │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                          │
│  │  Career Engine  │  │ Data Science    │  │  OpenAI GPT-4   │                          │
│  │  • Salary Pred  │  │  • ML Models    │  │  • Agent Brain  │                          │
│  │  • GradBoost    │  │  • Scikit-learn │  │  • Natural Lang │                          │
│  │  • R² > 0.85    │  │  • Pandas/NumPy │  │  • Smart Response│                         │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘                          │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                           CrewAI Multi-Agent System                                      │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                          │
│  │ Analysis Agent  │  │ Workflow Agent  │  │ Execution Agent │                          │
│  │ • Career Intel  │  │ • Process Opt   │  │ • Task Execution│                          │
│  │ • OpenAI GPT-4  │  │ • Resource Plan │  │ • Implementation│                          │
│  │ • Data Analysis │  │ • Timeline Mgmt │  │ • Automation    │                          │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘                          │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                              Data Storage                                                │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                          │
│  │ Environment Cfg │  │  In-Memory Dict │  │  Static Files   │                          │
│  │ (.env settings)  │  │  (.env settings) │  │  • Templates    │                          │
│  │ • Configuration │  │  • Active Data  │  │  • CSS/JS       │                          │
│  │ • API Keys      │  │  • Runtime State│  │  • Logs         │                          │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘                          │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                            External Dependencies                                         │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                          │
│  │   OpenAI API    │  │   Python Libs   │  │   Environment   │                          │
│  │  • GPT-4o-mini  │  │  • FastAPI      │  │  • .env Config  │                          │
│  │  • API Key Auth │  │  • CrewAI       │  │  • Debug Mode   │                          │
│  │  • Smart Agents │  │  • Uvicorn      │  │  • Local Dev    │                          │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘                          │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```
│  │  • R² > 0.85    │  │  • Pandas/NumPy │  │  • Smart Response│                         │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘                          │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                           CrewAI Multi-Agent System                                      │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                          │
│  │ Analysis Agent  │  │ Workflow Agent  │  │ Execution Agent │                          │
│  │ • Career Intel  │  │ • Process Opt   │  │ • Task Execution│                          │
│  │ • OpenAI GPT-4  │  │ • Resource Plan │  │ • Implementation│                          │
│  │ • Data Analysis │  │ • Timeline Mgmt │  │ • Automation    │                          │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘                          │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                              Data Storage                                                │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                          │
│  │ Environment Cfg │  │  In-Memory Dict │  │  Static Files   │                          │
│  │ (.env settings)  │  │  (.env settings) │  │  • Templates    │                          │
│  │ • Configuration │  │  • Active Data  │  │  • CSS/JS       │                          │
│  │ • API Keys      │  │  • Runtime State│  │  • Logs         │                          │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘                          │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                            External Dependencies                                         │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                          │
│  │   OpenAI API    │  │   Python Libs   │  │   Environment   │                          │
│  │  • GPT-4o-mini  │  │  • FastAPI      │  │  • .env Config  │                          │
│  │  • API Key Auth │  │  • CrewAI       │  │  • Debug Mode   │                          │
│  │  • Smart Agents │  │  • Uvicorn      │  │  • Local Dev    │                          │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘                          │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

## 📁 Project Structure

```
CrewAI/
├── main.py                          # FastAPI application entry point
├── requirements.txt                 # Python dependencies
├── .env                            # Environment configuration
│
├── api/                            # FastAPI routes and models
│   └── routes/
│       ├── agent_routes.py         # CrewAI agent interactions
│       ├── workflow_routes.py      # Workflow management
│       ├── analytics_routes.py     # Analytics endpoints
│       └── career_intelligence_routes.py  # Career intelligence
│
├── src/                           # Core application logic
│   ├── agents/                    # CrewAI agent definitions
│   │   ├── analysis_agent.py      # Analysis agent
│   │   ├── workflow_agent.py      # Workflow agent
│   │   └── execution_agent.py     # Execution agent
│   │
│   ├── analytics/                 # Data science and ML
│   │   ├── career_intelligence_engine.py  # ML career models
│   │   ├── data_science_engine.py        # Data processing
│   │   └── visualization_engine.py       # Chart generation
│   │
│   ├── config/                    # Configuration management
│   │   └── settings.py            # App settings
│   │
│   └── utils/                     # Utility functions
│       └── logger.py              # Logging configuration
│
├── frontend/                      # Web interface
│   ├── templates/                 # HTML templates (Jinja2)
│   │   ├── index.html            # Main interface
│   │   └── index_analytics.html   # Analytics interface
│   │
│   └── static/                    # Static assets
│       ├── style.css             # Main styling
│       ├── script.js             # UI interactions
│       ├── analytics.css         # Analytics styling
│       └── analytics.js          # Analytics scripts
│
└── database/                      # Database configuration
    └── mongodb_config.py          # MongoDB setup (configured but not active)
```

## 🔧 Core Components

### 1. FastAPI Backend (`main.py`)
- **Uvicorn ASGI Server**: Development server on port 8000
- **CORS Middleware**: Allows all origins for development
- **Static File Serving**: CSS/JS assets
- **Template Rendering**: Jinja2 for HTML templates
- **API Route Mounting**: All endpoints under `/api/`

### 2. CrewAI Agents (`src/agents/`)
- **Analysis Agent**: Career intelligence and data analysis
- **Workflow Agent**: Process optimization and planning  
- **Execution Agent**: Task implementation and automation
- **OpenAI Integration**: All agents powered by GPT-4o-mini

### 3. Intelligence Engine (`src/analytics/`)
- **Career Intelligence**: ML models for salary prediction (Gradient Boosting, R² > 0.85)
- **Data Science**: Pandas, NumPy, Scikit-learn for data processing
- **Visualization**: Plotly for chart generation

### 4. Data Storage
- **Environment Config**: `.env` file for settings and API keys
- **In-Memory Dictionary**: `workflows_db` for runtime state
- **Static Files**: Templates, CSS, JS, and logs

### 5. API Endpoints
```
/api/agents/list                   # List all agents
/api/agents/interact               # Chat with agents  
/api/agents/status/{agent_type}    # Agent status
/api/workflows                     # Workflow management
/api/analytics                     # Analytics data
/api/career-intelligence           # Career insights
/api/health                        # Health check
```

## 🚀 Development Setup

### Environment Variables (`.env`)
```bash
OPENAI_API_KEY=your_openai_api_key_here
APP_NAME=SkillForge AI
DEBUG=True
LOG_LEVEL=INFO
HOST=0.0.0.0
PORT=8000
DATABASE_URL=sqlite:///./workflows.db
```

### Key Dependencies (`requirements.txt`)
```
fastapi>=0.104.1
uvicorn[standard]>=0.24.0
crewai>=0.152.0
openai>=1.3.0
python-multipart
jinja2
pandas
scikit-learn
plotly
python-dotenv
```

### Running the Application
```bash
# Install dependencies
pip install -r requirements.txt

# Set OpenAI API key
export OPENAI_API_KEY="your-key-here"

# Run development server
python main.py

# Access application
# Web Interface: http://localhost:8000
# API Documentation: http://localhost:8000/docs
```

## 🎯 Current Capabilities

### ✅ What Works Now
- **3 AI Agents**: Analysis, Workflow, Execution with OpenAI GPT-4o-mini
- **Web Interface**: HTML templates with CSS/JS for user interaction
- **API Endpoints**: Full REST API for agent interaction and workflows
- **Career Intelligence**: ML-powered salary prediction and skill analysis
- **Data Storage**: SQLite + in-memory storage for workflow state
- **Development Environment**: Local development with auto-reload

### 🚧 What's Not Implemented
- No React/Vue frontend (just HTML templates)
- No authentication or user management
- No production deployment (development only)
- No database migrations or complex data models
- No real-time WebSocket connections
- No external API integrations beyond OpenAI
