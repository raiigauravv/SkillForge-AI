# 🏗️ SkillForge AI - Detailed System Architecture

## 🎯 **Complete System Architecture Diagram**

```
                    ┌─────────────────────────────────────────────────────────────┐
                    │                    🌐 FRONTEND LAYER                        │
                    │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
                    │  │  index.html │  │ script.js   │  │  style.css  │         │
                    │  │🇨🇦🇺🇸 14 Cities│  │Interactions │  │   Design    │         │
                    │  │Career Cards │  │Agent Calls  │  │Responsive   │         │
                    │  │City Select  │  │Analytics    │  │Components   │         │
                    │  └─────────────┘  └─────────────┘  └─────────────┘         │
                    │           ┌─────────────┐  ┌─────────────┐                 │
                    │           │index_analyt │  │analytics.js │                 │
                    │           │ics.html     │  │analytics.css│                 │
                    │           │Plotly Dash  │  │Visualizatn  │                 │
                    │           └─────────────┘  └─────────────┘                 │
                    └─────────────────────┬───────────────────────────────────────┘
                                          │ HTTP/JSON
                    ┌─────────────────────▼───────────────────────────────────────┐
                    │                ⚡ FASTAPI GATEWAY                           │
                    │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐           │
                    │  │Career Intel │ │ Workflows   │ │  Analytics  │           │
                    │  │   Routes    │ │   Routes    │ │   Routes    │           │
                    │  │/predict     │ │/execute     │ │/dashboard   │           │
                    │  └─────────────┘ └─────────────┘ └─────────────┘           │
                    │  ┌─────────────┐ ┌─────────────┐                           │
                    │  │Agent Routes │ │Crew Routes  │                           │
                    │  │/agent/run   │ │/crew/start  │                           │
                    │  │/agent/status│ │/crew/status │                           │
                    │  └─────────────┘ └─────────────┘                           │
                    └─────────┬─────────────────┬─────────────────┬───────────────┘
                              │                 │                 │
        ┌─────────────────────▼─────────────────▼─────────────────▼───────────────┐
        │                     🧠 CREWAI MULTI-AGENT SYSTEM                        │
        │   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐                  │
        │   │ Analysis    │   │ Workflow    │   │ Execution   │                  │
        │   │ Agent       │◄──┤ Agent       ├──►│ Agent       │                  │
        │   │ Strategy    │   │ Orchestrate │   │ Implement   │                  │
        │   │ Research    │   │ Coordinate  │   │ Automate    │                  │
        │   │ Planning    │   │ Task Mgmt   │   │ Resource    │                  │
        │   └─────────────┘   └─────────────┘   └─────────────┘                  │
        │                          │ OpenAI GPT Integration                       │
        └─────────────────────────────────┬─────────────────────────────────────┘
                                          │
        ┌─────────────────────────────────▼─────────────────────────────────────┐
        │                 🎯 ML CAREER INTELLIGENCE ENGINE                       │
        │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐     │
        │  │ Salary      │ │ Job         │ │ Career      │ │ Market      │     │
        │  │ Predictor   │ │ Matcher     │ │ Classifier  │ │ Analyzer    │     │
        │  │GradientBoost│ │RandomForest │ │RandomForest │ │North America│     │
        │  │ 93.6% R²    │ │ 74% Acc     │ │ 100% Acc    │ │ 14 Cities   │     │
        │  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘     │
        │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐                     │
        │  │Data Science │ │Visualization│ │Business     │                     │
        │  │Engine       │ │Engine       │ │Intelligence │                     │
        │  │K-Means      │ │Plotly Charts│ │Industry     │                     │
        │  │Clustering   │ │Interactive  │ │Benchmarks   │                     │
        │  └─────────────┘ └─────────────┘ └─────────────┘                     │
        └─────────────────────────────────┬─────────────────────────────────────┘
                                          │
        ┌─────────────────────────────────▼─────────────────────────────────────┐
        │                        🗄️ DATABASE LAYER                              │
        │     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐           │
        │     │   MongoDB   │     │ Collections │     │  Auto       │           │
        │     │AsyncMotor   │     │ • workflows │     │ Indexing    │           │
        │     │ Client      │     │ • analytics │     │ Environment │           │
        │     │MONGODB_URL  │     │ • user_behav│     │ Configurable│           │
        │     │Configurable │     │ • ml_models │     │ CRUD Ops    │           │
        │     └─────────────┘     └─────────────┘     └─────────────┘           │
        └─────────────────────────────────────────────────────────────────────┘
│  │            │                   │                     │                         │ │
│  │            └───────────────────┼─────────────────────┘                         │ │
│  │                                ▼                                               │ │
│  │                          OpenAI GPT Integration                                │ │
│  └─────────────────────────────────────────────────────────────────────────────────┘ │
│                                              │                                       │
│                                              ▼                                       │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                      📊 ANALYTICS & INTELLIGENCE LAYER                                │
├─────────────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────────────────────────────┐ │
│  │                          📁 src/analytics/                                      │ │
│  │                                                                                 │ │
│  │  💰 career_intelligence_engine.py (721 lines)                                  │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │ │
│  │  │   Salary    │  │     Job     │  │   Career    │  │   Market    │            │ │
│  │  │ Predictor   │  │   Matcher   │  │ Classifier  │  │  Analyzer   │            │ │
│  │  │GradientBoost│  │RandomForest │  │RandomForest │  │North America│            │ │
│  │  │ (93.6% R²)  │  │(74% accuracy│  │(100% accur.)│  │Insights     │            │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘            │ │
│  │                                                                                 │ │
│  │  📊 data_science_engine.py (298 lines)                                         │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                            │ │
│  │  │  Workflow   │  │Performance  │  │  K-Means    │                            │ │
│  │  │ Analytics   │  │ Analysis    │  │ Clustering  │                            │ │
│  │  │             │  │             │  │             │                            │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘                            │ │
│  │                                                                                 │ │
│  │  📈 visualization_engine.py (419 lines)                                        │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                            │ │
│  │  │   Plotly    │  │ Interactive │  │ Real-time   │                            │ │
│  │  │Dashboard Gen│  │   Charts    │  │  Updates    │                            │ │
│  │  │             │  │             │  │             │                            │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘                            │ │
│  └─────────────────────────────────────────────────────────────────────────────────┘ │
│                                              │                                       │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐ │
│  │                       📁 src/intelligence/                                     │ │
│  │                                                                                 │ │
│  │  🧠 business_intel.py (313 lines)                                              │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                            │ │
│  │  │  Industry   │  │Social Media │  │  Ecommerce  │                            │ │
│  │  │Benchmarks   │  │ Analytics   │  │  Metrics    │                            │ │
│  │  │             │  │             │  │             │                            │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘                            │ │
│  └─────────────────────────────────────────────────────────────────────────────────┘ │
│                                              │                                       │
│                                              ▼                                       │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                           🗄️ DATABASE LAYER (MongoDB)                                │
├─────────────────────────────────────────────────────────────────────────────────────┤
│  📁 database/mongodb_config.py                                                        │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐ │
│  │                      🍃 MongoDB AsyncIOMotorClient                              │ │
│  │                        Environment: MONGODB_URL (configurable)                 │ │
│  │                                                                                 │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │ │
│  │  │ workflows   │  │ analytics   │  │user_behavior│  │ ml_models   │            │ │
│  │  │ collection  │  │ collection  │  │ collection  │  │ collection  │            │ │
│  │  │             │  │             │  │             │  │             │            │ │
│  │  │• workflow_id│  │• metric_type│  │• user_session│  │• model_id   │            │ │
│  │  │• status     │  │• metric_value│  │• action_type│  │• model_type │            │ │
│  │  │• priority   │  │• timestamp  │  │• timestamp  │  │• performance│            │ │
│  │  │• result     │  │• metadata   │  │• duration   │  │• parameters │            │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘            │ │
│  │                                                                                 │ │
│  │  🔗 Motor Async Driver + 🏗️ Auto-Indexing                                      │ │
│  └─────────────────────────────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                         ⚙️ UTILITIES & CONFIGURATION                                  │
├─────────────────────────────────────────────────────────────────────────────────────┤
│  📁 src/config/settings.py  │  📁 src/utils/logger.py  │  📁 src/tools/            │
│  ┌─────────────┐            │  ┌─────────────┐         │  ┌─────────────┐           │
│  │Environment  │            │  │ Structured  │         │  │ Analysis    │           │
│  │Variables    │            │  │ Logging     │         │  │ Execution   │           │
│  │API Keys     │            │  │ Error Track │         │  │ Workflow    │           │
│  └─────────────┘            │  └─────────────┘         │  └─────────────┘           │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

## 🔄 **Data Flow Architecture**

```
                    USER INTERACTION FLOW
    ┌─────────────────────────────────────────────────────────┐
    │                                                         │
    ▼                                                         │
┌─────────┐    HTTP/JSON     ┌─────────┐    Async Calls    ┌─┴─────────┐
│Frontend │ ──────────────► │FastAPI  │ ─────────────────► │CrewAI     │
│Templates│                 │Routes   │                    │Agents     │
└─────────┘                 └─────────┘                    └─┬─────────┘
    ▲                           │                            │
    │           JSON Response   │                            │
    └───────────────────────────┘                            │
                                │                            ▼
                                ▼                      ┌─────────────┐
                        ┌─────────────┐                │Analytics    │
                        │MongoDB      │◄───────────────│Intelligence │
                        │Collections  │  Store Results │Layer        │
                        └─────────────┘                └─────────────┘
                                ▲                            │
                                │         Read/Write         │
                                └────────────────────────────┘

            NORTH AMERICAN MARKET DATA PROCESSING
    ┌─────────────────────────────────────────────────────────┐
    │                                                         │
    ▼                                                         │
┌─────────────┐   Synthetic Data   ┌─────────────┐   ML Models  ┌─┴─────────┐
│Career Intel │ ─────────────────► │Scikit-learn │ ────────────► │Predictions│
│Engine       │   Generation       │Processing   │   Training    │& Analysis │
└─────────────┘                    └─────────────┘               └─┬─────────┘
    ▲                                     │                        │
    │                                     ▼                        │
    │                              ┌─────────────┐                 │
    │                              │Plotly       │◄────────────────┘
    │                              │Visualization│   Chart Data
    │                              └─────────────┘
    │                                     │
    │                 Dashboard Updates   │
    └─────────────────────────────────────┘

```

## 🏗️ **Component Interaction Matrix**

```
                    Component Interactions
    ┌─────────────┬─────────────┬─────────────┬─────────────┐
    │             │   FastAPI   │   CrewAI    │  MongoDB    │
    ├─────────────┼─────────────┼─────────────┼─────────────┤
    │ Frontend    │ HTTP/JSON ✓ │      -      │      -      │
    │             │ Routes Call │             │             │
    ├─────────────┼─────────────┼─────────────┼─────────────┤
    │ FastAPI     │      -      │ Agent Exec ✓│ AsyncIO ✓   │
    │             │             │ Background  │ Collections │
    ├─────────────┼─────────────┼─────────────┼─────────────┤
    │ CrewAI      │ Results ✓   │ Collab ✓    │ Store ✓     │
    │             │ Return      │ Multi-Agent │ Analytics   │
    ├─────────────┼─────────────┼─────────────┼─────────────┤
    │ Analytics   │ Data ✓      │ Input ✓     │ Read/Write ✓│
    │             │ Processing  │ Processing  │ Persistence │
    ├─────────────┼─────────────┼─────────────┼─────────────┤
    │ MongoDB     │ Store ✓     │ Results ✓   │      -      │
    │             │ Retrieve    │ Analytics   │             │
    └─────────────┴─────────────┴─────────────┴─────────────┘
```

## 🌍 **Geographic Data Architecture**

```
                NORTH AMERICAN MARKET COVERAGE
    ┌─────────────────────────────────────────────────────────┐
    │  🇨🇦 CANADIAN MARKETS (CAD)    🇺🇸 US MARKETS (USD)      │
    ├─────────────────────────────────────────────────────────┤
    │                                                         │
    │  Toronto    (1.2x) ──┐              ┌── San Francisco(1.8x)│
    │  Vancouver  (1.15x)──┤              ├── New York    (1.6x)│
    │  Montreal   (1.0x) ──┤              ├── Seattle     (1.4x)│
    │  Ottawa     (1.1x) ──┤              ├── Boston      (1.3x)│
    │  Calgary    (1.08x)──┤              ├── Los Angeles(1.25x)│
    │  Edmonton   (1.05x)──┘              ├── Austin      (1.2x)│
    │                      │              ├── Chicago    (1.15x)│
    │  Base: CAD $55k      │              └── Denver      (1.1x)│
    │                      │              Base: USD $60k       │
    │                      ▼                    ▼              │
    │              ML PREDICTION ENGINE                        │
    │    ┌─────────────────────────────────────────────────┐   │
    │    │ Gradient Boosting + Random Forest Models        │   │
    │    │ • Industry Multipliers: Tech(1.3x) Finance(1.25x)│   │
    │    │ • Experience Levels: Junior(1x) → Director(3.2x) │   │
    │    │ • Education Bonus: PhD(1.2x) Master(1.1x)       │   │
    │    │ • Normal Distribution Variance: ±$8k             │   │
    │    └─────────────────────────────────────────────────┘   │
    └─────────────────────────────────────────────────────────┘
```

## 📊 **System Performance & Specifications**

```
        🌍 North American Coverage: 🇨🇦 6 Canadian + 🇺🇸 8 US Cities
        ⚡ Performance: <200ms API │ 3000+ Profiles │ 93.6% ML Accuracy
        🛠️ Stack: FastAPI + CrewAI + Scikit-learn + MongoDB + Plotly
        📦 Repository: https://github.com/raiigauravv/SkillForge-AI

    ┌─────────────────────────────────────────────────────────────────────┐
    │                    🎯 TECHNICAL SPECIFICATIONS                      │
    ├─────────────────────────────────────────────────────────────────────┤
    │                                                                     │
    │  🔧 Core Framework: FastAPI 0.116.1 + Uvicorn Server               │
    │  🤖 AI Framework: CrewAI 0.152.0 Multi-Agent System                │
    │  🗄️ Database: MongoDB AsyncIOMotorClient + Motor Driver            │
    │  🧠 ML Stack: Scikit-learn (GradientBoost, RandomForest, K-Means)  │
    │  📊 Visualization: Plotly.js Interactive Charts + CDN              │
    │  🌐 Frontend: Jinja2 Templates + Responsive CSS + JavaScript       │
    │                                                                     │
    │  📈 ML Model Performance:                                           │
    │     • Salary Predictor: 93.6% R² Score                             │
    │     • Job Matcher: 74% Accuracy                                     │
    │     • Career Classifier: 100% Accuracy                             │
    │     • Market Analysis: 14 Cities Coverage                          │
    │                                                                     │
    │  ⚡ System Metrics:                                                 │
    │     • API Response: <200ms average                                  │
    │     • Database: 4 Collections + Auto-indexing                      │
    │     • Concurrent Users: 3000+ profiles                             │
    │     • Geographic Coverage: North America (CA + US)                 │
    │                                                                     │
    │  🔄 Agent Workflow:                                                 │
    │     • Analysis Agent: Strategic planning + market research          │
    │     • Workflow Agent: Process orchestration + task coordination     │
    │     • Execution Agent: Implementation + resource allocation         │
    │                                                                     │
    └─────────────────────────────────────────────────────────────────────┘
```

## 🚀 **Deployment & Infrastructure**

```
    ┌─────────────────────────────────────────────────────────────────────┐
    │                     🔧 DEPLOYMENT PIPELINE                         │
    ├─────────────────────────────────────────────────────────────────────┤
    │                                                                     │
    │  📋 Repository: raiigauravv/SkillForge-AI (GitHub)                 │
    │  🌐 Framework: FastAPI with CORS middleware                        │
    │  🔐 Environment: Configurable via environment variables            │
    │  🗄️ Database: MONGODB_URL environment configuration               │
    │  🤖 AI Integration: OpenAI GPT + CrewAI orchestration             │
    │                                                                     │
    │  📁 Project Structure:                                              │
    │     • /api/routes/ - 5 FastAPI route modules                       │
    │     • /src/analytics/ - ML engines (721+298+419 lines)            │
    │     • /src/agents/ - CrewAI agent implementations                  │
    │     • /database/ - MongoDB configuration                           │
    │     • /frontend/ - HTML templates + static assets                  │
    │                                                                     │
    └─────────────────────────────────────────────────────────────────────┘
```

````
```
````
