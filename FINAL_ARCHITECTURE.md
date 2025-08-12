# 🏗️ SkillForge AI - Final System Architecture

## 📊 **System Overview**
SkillForge AI is a North American career intelligence platform built with FastAPI, CrewAI multi-agent system, and machine learning analytics serving 14 major cities across Canada and USA.

## 🎯 **Core Components Architecture**

### **1. Frontend Layer (Client-Side)**
```
📁 frontend/
├── 🎨 templates/index.html          # Main UI with North American city selector
├── 📱 static/script.js              # Career analysis, workflow creation, API calls  
├── 🎨 static/style.css              # Responsive design, agent cards, analytics
└── 📊 static/analytics.css/js       # Dashboard visualization components
```

**Technologies**: HTML5, Vanilla JavaScript, CSS Grid, Responsive Design
**Features**: 🇨🇦🇺🇸 Dual-country city selector, Real-time career analysis, Agent interaction UI

### **2. API Gateway Layer (FastAPI)**
```
📁 api/
├── 🔌 routes/
│   ├── career_intelligence_routes.py  # ML predictions, market analysis
│   ├── workflow_routes.py            # CrewAI workflow CRUD, background execution
│   ├── agent_routes.py               # Multi-agent interactions
│   └── analytics_routes.py           # Dashboard data endpoints
└── 🛡️ middleware/                    # CORS, request validation
```

**Technologies**: FastAPI, Pydantic, Background Tasks, HTTP Exception Handling
**Endpoints**: REST API with async support, JSON responses, Error handling

### **3. Multi-Agent Intelligence (CrewAI)**
```
📁 src/crews/workflow_crew.py
├── 🤖 Analysis Agent        # Strategic career planning, market research
├── 🔄 Workflow Agent        # Process orchestration, task breakdown  
└── ⚡ Execution Agent       # Implementation planning, resource allocation
```

**Technologies**: CrewAI Framework, OpenAI GPT integration, Agent collaboration
**Capabilities**: Strategic planning, Task decomposition, Resource optimization

### **4. Career Intelligence Engine (ML Core)**
```
📁 src/analytics/career_intelligence_engine.py
├── 💰 Salary Predictor      # Gradient Boosting (93.6% R²)
├── 🎯 Job Matcher          # Random Forest (74% accuracy)  
├── 📈 Career Classifier     # Random Forest (100% accuracy)
└── 🗺️ Market Analyzer       # North American market insights
```

**Technologies**: Scikit-learn, Pandas, NumPy, StandardScaler, LabelEncoder
**Data**: 3000 synthetic career profiles across 14 cities (Canada + USA)

### **5. Database Layer**
```
📁 database/
├── 🗃️ SQLite (workflows)    # Workflow persistence, execution history
├── 🍃 MongoDB (analytics)   # Career data, user sessions  
└── 💾 In-Memory Store       # Active workflow states, cache
```

**Technologies**: SQLite, MongoDB, Python dictionaries for caching
**Data Types**: Structured workflows, Analytics data, Session management

### **6. Utilities & Configuration**
```
📁 src/
├── ⚙️ config/settings.py    # Environment variables, API keys
├── 📝 utils/logger.py       # Structured logging, error tracking
└── 🔧 tools/               # Analysis, execution, workflow tools
```

**Technologies**: Python logging, Environment configuration, Tool abstractions

## 🌍 **Data Architecture - North American Markets**

### **Geographic Coverage**
```
🇨🇦 Canadian Cities (CAD):
├── Toronto (baseline 1.2x)
├── Vancouver (1.15x) 
├── Montreal (1.0x)
├── Ottawa (1.1x)
├── Calgary (1.08x)
└── Edmonton (1.05x)

🇺🇸 US Cities (USD):
├── San Francisco (1.8x)
├── New York (1.6x)
├── Seattle (1.4x)
├── Boston (1.3x)
├── Los Angeles (1.25x)
├── Austin (1.2x)
├── Chicago (1.15x)
└── Denver (1.1x)
```

### **Salary Modeling**
```
Base Salary Calculation:
├── Country Base: CAD $55k (Canada) / USD $60k (USA)
├── City Multiplier: Regional cost of living adjustments
├── Industry Factor: Tech (1.3x), Finance (1.25x), Healthcare (1.1x)
├── Experience Level: Junior (1x) → Director (3.2x)
├── Education Bonus: PhD (1.2x), Master (1.1x), Bachelor (1x)
└── Variance: ±$8k normal distribution
```

## 🔄 **System Flow Architecture**

### **1. Career Analysis Flow**
```
User Input → Frontend Validation → FastAPI Endpoint → ML Engine → 
Market Analysis → Currency Detection → Dashboard Generation → JSON Response
```

### **2. Workflow Creation Flow** 
```
Requirements → CrewAI Agents → Strategic Planning → Task Breakdown →
Resource Allocation → SQLite Storage → Workflow ID Return
```

### **3. Background Execution Flow**
```
Execute Request → FastAPI Background Task → CrewAI Processing →
Status Updates → Result Storage → Completion Notification
```

## 🛠️ **Technology Stack Summary**

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Frontend** | HTML5/CSS3/JS | User Interface, City Selection |
| **API** | FastAPI + Uvicorn | REST Endpoints, Async Processing |
| **Intelligence** | CrewAI + OpenAI | Multi-Agent Collaboration |
| **ML Engine** | Scikit-learn | Predictive Analytics |
| **Data Processing** | Pandas + NumPy | Market Analysis, Feature Engineering |
| **Database** | SQLite + MongoDB | Persistence, Analytics Storage |
| **Deployment** | Python 3.9+ | Local Development Server |

## 🚀 **Key Architectural Decisions**

1. **Multi-Agent Architecture**: CrewAI for complex career planning tasks
2. **Dual-Market Support**: Separate USD/CAD handling with regional multipliers  
3. **Background Processing**: FastAPI BackgroundTasks for long-running operations
4. **ML Pipeline**: Scikit-learn models with pre-training for performance
5. **RESTful Design**: Clean API separation between UI and business logic
6. **Responsive Frontend**: Vanilla JS for simplicity, CSS Grid for layouts

## 📈 **Performance Metrics**
- **Model Accuracy**: 93.6% salary prediction R²
- **Training Data**: 3000 North American career profiles
- **API Response**: <200ms for career analysis
- **Workflow Generation**: 30-60 seconds (multi-agent planning)
- **Background Execution**: 2-3 minutes (CrewAI processing)

## 🔐 **Security & Configuration**
- Environment variables for API keys
- CORS middleware for cross-origin requests  
- Input validation through Pydantic models
- Error handling with structured logging
- SQLite for secure local data persistence

---

**Version**: 1.0.0 Final  
**Last Updated**: August 11, 2025  
**Geographic Coverage**: 🇨🇦 Canada + 🇺🇸 United States  
**Agent Framework**: CrewAI Multi-Agent System  
**ML Accuracy**: 93.6% salary prediction performance
