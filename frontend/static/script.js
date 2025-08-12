// SkillForge AI - Original Working Version

// Global variables
let currentWorkflows = [];

// Tab management
function showTab(tabName) {
    // Hide all tabs
    const tabs = document.querySelectorAll('.tab-content');
    tabs.forEach(tab => tab.classList.remove('active'));
    
    // Remove active class from all buttons
    const buttons = document.querySelectorAll('.tab-button');
    buttons.forEach(button => button.classList.remove('active'));
    
    // Show selected tab
    const selectedTab = document.getElementById(tabName + '-tab');
    if (selectedTab) {
        selectedTab.classList.add('active');
    }
    
    // Activate button
    if (event && event.target) {
        event.target.classList.add('active');
    }
    
    // Load content for workflows tab
    if (tabName === 'workflows') {
        loadWorkflows();
    }
    
    // Load content for crews tab
    if (tabName === 'crews') {
        loadCrewStats();
    }
}

// Load workflows from API
async function loadWorkflows() {
    try {
        console.log('Loading workflows...');
        const response = await fetch('/api/workflows/list');
        const data = await response.json();
        
        console.log('Workflows data:', data);
        
        if (response.ok) {
            currentWorkflows = data.workflows || [];
            displayWorkflows(currentWorkflows);
        } else {
            console.error('Failed to load workflows:', data);
        }
    } catch (error) {
        console.error('Error loading workflows:', error);
    }
}

// Display workflows in the UI
function displayWorkflows(workflows) {
    const container = document.getElementById('workflows-container');
    if (!container) return;
    
    if (!workflows || workflows.length === 0) {
        container.innerHTML = '<p>No workflows found. Create your first workflow!</p>';
        return;
    }
    
    // Remove duplicates based on workflow_id
    const uniqueWorkflows = workflows.filter((workflow, index, self) => 
        index === self.findIndex((w) => w.workflow_id === workflow.workflow_id)
    );
    
    // Sort by creation date (newest first)
    uniqueWorkflows.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
    
    container.innerHTML = uniqueWorkflows.map(workflow => `
        <div class="workflow-item">
            <div class="workflow-name">${workflow.name || 'Untitled Workflow'}</div>
            <div class="workflow-description">${workflow.description || 'No description available'}</div>
            <div class="workflow-meta">
                <div>
                    <span class="priority-badge priority-${workflow.priority || 'medium'}">
                        ${(workflow.priority || 'Medium').toUpperCase()}
                    </span>
                    <span class="status-badge status-${workflow.status || 'unknown'}">
                        ${(workflow.status || 'Unknown').toUpperCase()}
                    </span>
                    ${workflow.career_enhanced ? '<span class="enhancement-badge career-enhanced">🎯 Career AI</span>' : ''}
                    ${workflow.ai_agents_integrated ? '<span class="enhancement-badge ai-integrated">🤖 AI Agents</span>' : ''}
                </div>
                <div class="workflow-date">
                    ${new Date(workflow.created_at).toLocaleString()}
                </div>
            </div>
            <div class="workflow-actions">
                <button onclick="viewWorkflowDetails('${workflow.workflow_id}')" class="btn-view">📋 View Details</button>
                <button onclick="deleteWorkflow('${workflow.workflow_id}')" class="btn-delete">🗑️ Delete</button>
            </div>
        </div>
    `).join('');
}

// Show workflow execution results in modal
function showWorkflowResult(result) {
    const modal = document.getElementById('workflow-result-modal');
    const content = document.getElementById('workflow-result-content');
    
    if (modal && content) {
        const aiOutput = result.result && result.result.output ? result.result.output : 'No detailed output available';
        const tokenUsage = result.result && result.result.token_usage ? result.result.token_usage.total_tokens : 'N/A';
        
        content.innerHTML = `
            <div class="result-summary">
                <div class="result-header">
                    <h4>✅ Workflow Created Successfully</h4>
                    <div class="result-badges">
                        <span class="result-badge success">ID: ${result.workflow_id}</span>
                        <span class="result-badge status">${result.status.toUpperCase()}</span>
                    </div>
                </div>
                
                <div class="result-message">
                    <p><strong>Message:</strong> ${result.message}</p>
                </div>
                
                <div class="result-output">
                    <h5>📋 AI Generated Solution:</h5>
                    <div class="ai-output-container">
                        <div class="ai-output">${aiOutput}</div>
                    </div>
                </div>
                
                <div class="result-footer">
                    <div class="token-info">
                        <span>🔧 Processing complete</span>
                        <span>📊 Tokens used: ${tokenUsage}</span>
                    </div>
                </div>
            </div>
        `;
        modal.style.display = 'block';
    }
}

// Agent interaction function
async function interactWithAgent(agentType) {
    const modal = document.getElementById('agent-modal');
    const title = document.getElementById('modal-agent-title');
    const content = document.getElementById('modal-agent-content');
    const input = document.getElementById('agent-input');
    const sendBtn = document.getElementById('send-to-agent');
    
    if (!modal) return;
    
    const agentNames = {
        'analysis_agent': '🎯 Analysis Agent',
        'workflow_agent': '⚙️ Workflow Agent',
        'execution_agent': '🛠️ Execution Agent'
    };

    const agentDescriptions = {
        'analysis_agent': {
            intro: '👋 Hello! I\'m your **🎯 Strategic Analysis Agent**',
            description: '🧠 **What I\'m Great At:**\n• 📊 **Data Analysis & Pattern Recognition** - I can analyze complex business data and identify hidden trends\n• 📈 **Market Research & Insights** - I provide data-driven insights about your industry and competitors\n• 🎯 **Strategic Planning** - I help you make informed decisions based on thorough analysis\n• 📋 **Report Generation** - I create comprehensive analytical reports with actionable recommendations\n\n**💡 Ask me when you need:**\n• Market analysis or competitive research\n• Data interpretation and trend analysis\n• Strategic recommendations based on data\n• Business intelligence insights\n• Performance metric analysis'
        },
        'workflow_agent': {
            intro: '👋 Hello! I\'m your **⚙️ Workflow Orchestration Agent**',
            description: '🔧 **What I\'m Great At:**\n• 📋 **Process Design & Optimization** - I create efficient step-by-step workflows for any business process\n• 🎼 **Multi-Agent Coordination** - I can coordinate multiple agents and teams to work together seamlessly\n• ⚙️ **Workflow Automation** - I design automated processes to save time and reduce errors\n• 📊 **Progress Monitoring** - I track workflow execution and identify bottlenecks\n\n**💡 Ask me when you need:**\n• To design new business processes\n• To optimize existing workflows\n• To coordinate complex multi-step projects\n• To automate repetitive tasks\n• To improve team collaboration and efficiency'
        },
        'execution_agent': {
            intro: '👋 Hello! I\'m your **🛠️ Execution & Implementation Agent**',
            description: '⚡ **What I\'m Great At:**\n• 🚀 **Task Implementation** - I turn plans into concrete, actionable steps\n• 🔧 **Process Automation** - I implement automated solutions and tools\n• ⚠️ **Error Handling & Troubleshooting** - I identify and resolve implementation issues\n• ✅ **Quality Validation** - I ensure results meet requirements and standards\n\n**💡 Ask me when you need:**\n• Specific implementation steps for your plans\n• Tool recommendations and setup guidance\n• Troubleshooting execution problems\n• Quality control and result validation\n• Hands-on technical assistance'
        }
    };
    
    // Initialize conversation history for this agent session
    let conversationHistory = [];
    
    title.textContent = agentNames[agentType] || 'Agent Interaction';
    content.innerHTML = `
        <div class="conversation-container" id="conversation-${agentType}">
            <div class="agent-intro">
                <p>${agentDescriptions[agentType].intro}</p>
                <div class="agent-capabilities">
                    <pre style="white-space: pre-wrap; font-family: inherit; font-size: 14px; line-height: 1.5; background: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 4px solid #007bff; margin: 10px 0;">${agentDescriptions[agentType].description}</pre>
                </div>
                <p><small>� Ask me anything related to my expertise! You can also ask follow-up questions in this conversation.</small></p>
            </div>
        </div>
        <div class="conversation-controls">
            <button class="clear-conversation" onclick="clearConversation('${agentType}')">🗑️ Clear Conversation</button>
        </div>
    `;
    input.value = '';
    
    // Setup send button
    sendBtn.onclick = async function() {
        const userInput = input.value.trim();
        if (!userInput) return;
        
        // Add user message to conversation
        const conversationContainer = document.getElementById(`conversation-${agentType}`);
        const userMessageDiv = document.createElement('div');
        userMessageDiv.className = 'user-message';
        userMessageDiv.innerHTML = `
            <div class="message-header">
                <strong>You:</strong>
                <span class="message-time">${new Date().toLocaleTimeString()}</span>
            </div>
            <div class="message-content">${userInput}</div>
        `;
        conversationContainer.appendChild(userMessageDiv);
        
        // Add user input to history
        conversationHistory.push({role: "user", content: userInput});
        
        // Show loading message
        const loadingDiv = document.createElement('div');
        loadingDiv.className = 'agent-message loading';
        loadingDiv.innerHTML = `
            <div class="message-header">
                <strong>${agentNames[agentType]}:</strong>
                <span class="message-time">${new Date().toLocaleTimeString()}</span>
            </div>
            <div class="message-content">🤔 Thinking...</div>
        `;
        conversationContainer.appendChild(loadingDiv);
        
        // Clear input and disable button
        input.value = '';
        sendBtn.disabled = true;
        sendBtn.textContent = 'Processing...';
        
        // Scroll to bottom
        conversationContainer.scrollTop = conversationContainer.scrollHeight;
        
        try {
            const response = await fetch('/api/agents/interact', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    agent_type: agentType,
                    message: userInput,
                    conversation_history: conversationHistory.slice(-6) // Keep last 6 messages for context
                })
            });
            
            const result = await response.json();
            
            // Remove loading message
            conversationContainer.removeChild(loadingDiv);
            
            if (response.ok && result.response) {
                // Add agent response
                const agentMessageDiv = document.createElement('div');
                agentMessageDiv.className = 'agent-message';
                agentMessageDiv.innerHTML = `
                    <div class="message-header">
                        <strong>${agentNames[agentType]}:</strong>
                        <span class="message-time">${new Date(result.timestamp).toLocaleTimeString()}</span>
                    </div>
                    <div class="message-content">${result.response}</div>
                `;
                conversationContainer.appendChild(agentMessageDiv);
                
                // Add agent response to history
                conversationHistory.push({role: "assistant", content: result.response});
                
            } else {
                // Show error message
                const errorDiv = document.createElement('div');
                errorDiv.className = 'agent-message error';
                errorDiv.innerHTML = `
                    <div class="message-header">
                        <strong>Error:</strong>
                        <span class="message-time">${new Date().toLocaleTimeString()}</span>
                    </div>
                    <div class="message-content">${result.detail || result.error || 'Failed to get response'}</div>
                `;
                conversationContainer.appendChild(errorDiv);
            }
        } catch (error) {
            // Remove loading message
            conversationContainer.removeChild(loadingDiv);
            
            // Show error message
            const errorDiv = document.createElement('div');
            errorDiv.className = 'agent-message error';
            errorDiv.innerHTML = `
                <div class="message-header">
                    <strong>Error:</strong>
                    <span class="message-time">${new Date().toLocaleTimeString()}</span>
                </div>
                <div class="message-content">${error.message}</div>
            `;
            conversationContainer.appendChild(errorDiv);
        } finally {
            // Reset button state
            sendBtn.disabled = false;
            sendBtn.textContent = 'Send Message';
            
            // Scroll to bottom
            conversationContainer.scrollTop = conversationContainer.scrollHeight;
            
            // Focus back on input
            input.focus();
        }
    };
    
    // Allow Enter key to send message
    input.onkeypress = function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendBtn.click();
        }
    };
    
    modal.style.display = 'block';
    input.focus();
}

// Clear conversation function
function clearConversation(agentType) {
    const conversationContainer = document.getElementById(`conversation-${agentType}`);
    if (conversationContainer) {
        const agentNames = {
            'analysis_agent': '🎯 Analysis Agent',
            'workflow_agent': '⚙️ Workflow Agent',
            'execution_agent': '🛠️ Execution Agent'
        };

        const agentDescriptions = {
            'analysis_agent': {
                intro: '👋 Hello! I\'m your **🎯 Strategic Analysis Agent**',
                description: '🧠 **What I\'m Great At:**\n• 📊 **Data Analysis & Pattern Recognition** - I can analyze complex business data and identify hidden trends\n• 📈 **Market Research & Insights** - I provide data-driven insights about your industry and competitors\n• 🎯 **Strategic Planning** - I help you make informed decisions based on thorough analysis\n• 📋 **Report Generation** - I create comprehensive analytical reports with actionable recommendations\n\n**💡 Ask me when you need:**\n• Market analysis or competitive research\n• Data interpretation and trend analysis\n• Strategic recommendations based on data\n• Business intelligence insights\n• Performance metric analysis'
            },
            'workflow_agent': {
                intro: '👋 Hello! I\'m your **⚙️ Workflow Orchestration Agent**',
                description: '🔧 **What I\'m Great At:**\n• 📋 **Process Design & Optimization** - I create efficient step-by-step workflows for any business process\n• 🎼 **Multi-Agent Coordination** - I can coordinate multiple agents and teams to work together seamlessly\n• ⚙️ **Workflow Automation** - I design automated processes to save time and reduce errors\n• 📊 **Progress Monitoring** - I track workflow execution and identify bottlenecks\n\n**💡 Ask me when you need:**\n• To design new business processes\n• To optimize existing workflows\n• To coordinate complex multi-step projects\n• To automate repetitive tasks\n• To improve team collaboration and efficiency'
            },
            'execution_agent': {
                intro: '👋 Hello! I\'m your **🛠️ Execution & Implementation Agent**',
                description: '⚡ **What I\'m Great At:**\n• 🚀 **Task Implementation** - I turn plans into concrete, actionable steps\n• 🔧 **Process Automation** - I implement automated solutions and tools\n• ⚠️ **Error Handling & Troubleshooting** - I identify and resolve implementation issues\n• ✅ **Quality Validation** - I ensure results meet requirements and standards\n\n**💡 Ask me when you need:**\n• Specific implementation steps for your plans\n• Tool recommendations and setup guidance\n• Troubleshooting execution problems\n• Quality control and result validation\n• Hands-on technical assistance'
            }
        };
        
        conversationContainer.innerHTML = `
            <div class="agent-intro">
                <p>${agentDescriptions[agentType].intro}</p>
                <div class="agent-capabilities">
                    <pre style="white-space: pre-wrap; font-family: inherit; font-size: 14px; line-height: 1.5; background: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 4px solid #007bff; margin: 10px 0;">${agentDescriptions[agentType].description}</pre>
                </div>
                <p><small>� Ask me anything related to my expertise! You can also ask follow-up questions in this conversation.</small></p>
            </div>
        `;
        
        // Reset conversation history (will be reinitialized on next interaction)
        // The conversationHistory variable is scoped to the interactWithAgent function
    }
}

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    console.log('SkillForge AI - Initialized');
    
    // Load initial workflows
    loadWorkflows();
    
    // Setup workflow form
    const workflowForm = document.getElementById('workflow-form');
    if (workflowForm) {
        workflowForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const submitButton = e.target.querySelector('button[type="submit"]');
            const originalText = submitButton.textContent;
            
            // Show loading state
            submitButton.textContent = '⏳ Creating Workflow...';
            submitButton.disabled = true;
            
            const formData = new FormData(e.target);
            const workflowData = {
                name: formData.get('name'),
                description: formData.get('description'),
                priority: formData.get('priority'),
                requirements: []
            };
            
            try {
                const response = await fetch('/api/workflows/create', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(workflowData)
                });
                
                const result = await response.json();
                
                if (response.ok) {
                    showWorkflowResult(result);
                    e.target.reset();
                    loadWorkflows();
                } else {
                    alert('Error: ' + (result.detail || 'Failed to create workflow'));
                }
            } catch (error) {
                alert('Error: ' + error.message);
            } finally {
                // Reset button state
                submitButton.textContent = originalText;
                submitButton.disabled = false;
            }
        });
    }
    
    // Setup modal close functionality
    document.querySelectorAll('.modal .close').forEach(closeBtn => {
        closeBtn.addEventListener('click', function() {
            this.closest('.modal').style.display = 'none';
        });
    });
    
    document.querySelectorAll('.modal').forEach(modal => {
        modal.addEventListener('click', function(e) {
            if (e.target === this) {
                this.style.display = 'none';
            }
        });
    });
    
    // Load initial content
    loadWorkflows();
});

// Crew management functions
async function manageWorkflowCrew() {
    try {
        const response = await fetch('/api/workflows/crews/status');
        const data = await response.json();
        
        const crewInfo = data.crews && data.crews.length > 0 ? data.crews[0] : {};
        const message = `Workflow Crew Status:
        
🚀 Crew Type: ${crewInfo.crew_type || 'Unknown'}
🤖 Agents: ${crewInfo.agents ? crewInfo.agents.join(', ') : 'No agents found'}
⚙️ Process: ${crewInfo.process_type || 'Unknown'}
🧠 Memory: ${crewInfo.memory_enabled ? 'Enabled' : 'Disabled'}
💾 Cache: ${crewInfo.cache_enabled ? 'Enabled' : 'Disabled'}
📊 Status: ${crewInfo.status || 'Unknown'}
⏰ Last Updated: ${new Date(data.timestamp).toLocaleString()}`;
        
        alert(message);
    } catch (error) {
        alert('Error loading crew status: ' + error.message);
    }
}

function loadCrewStats() {
    const container = document.getElementById('crew-stats-container');
    if (!container) return;
    
    // Simple stats for now
    container.innerHTML = `
        <div class="stats-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px;">
            <div class="stat-card" style="background: #f0fff4; padding: 20px; border-radius: 10px; text-align: center;">
                <h4 style="color: #48bb78; margin-bottom: 10px;">Active Agents</h4>
                <p style="font-size: 24px; font-weight: bold; color: #2d3748;">3</p>
            </div>
            <div class="stat-card" style="background: #ebf8ff; padding: 20px; border-radius: 10px; text-align: center;">
                <h4 style="color: #4299e1; margin-bottom: 10px;">Total Workflows</h4>
                <p style="font-size: 24px; font-weight: bold; color: #2d3748;">${currentWorkflows.length}</p>
            </div>
            <div class="stat-card" style="background: #fef5e7; padding: 20px; border-radius: 10px; text-align: center;">
                <h4 style="color: #ed8936; margin-bottom: 10px;">Success Rate</h4>
                <p style="font-size: 24px; font-weight: bold; color: #2d3748;">98%</p>
            </div>
        </div>
    `;
}

// Career Intelligence Functions
function updateSkillValue(skill) {
    const slider = document.getElementById(skill + '-skill');
    const valueSpan = document.getElementById(skill + '-value');
    if (slider && valueSpan) {
        valueSpan.textContent = slider.value;
    }
}

async function checkCareerSystemHealth() {
    const statusIndicator = document.getElementById('status-indicator');
    try {
        const response = await fetch('/api/career-intelligence/health');
        const data = await response.json();
        
        if (data.status === 'healthy') {
            statusIndicator.innerHTML = `✅ ${data.status} - Models Trained: ${data.engine_trained}`;
            statusIndicator.className = 'healthy';
        } else {
            statusIndicator.innerHTML = '❌ System Error';
            statusIndicator.className = 'error';
        }
    } catch (error) {
        statusIndicator.innerHTML = '❌ Connection Failed';
        statusIndicator.className = 'error';
    }
}

function getCareerProfileData() {
    return {
        city: document.getElementById('career-city').value,
        industry: document.getElementById('career-industry').value,
        experience_level: document.getElementById('career-experience').value,
        education: document.getElementById('career-education').value,
        python_skill: parseFloat(document.getElementById('python-skill').value),
        sql_skill: parseFloat(document.getElementById('sql-skill').value),
        ml_skill: parseFloat(document.getElementById('ml-skill').value),
        communication_skill: parseFloat(document.getElementById('communication-skill').value),
        portfolio_projects: parseInt(document.getElementById('portfolio-projects').value),
        github_commits: parseInt(document.getElementById('github-commits').value),
        years_experience: parseFloat(document.getElementById('years-experience').value)
    };
}

function showCareerResults(title, data, isSuccess = true) {
    const resultsDiv = document.getElementById('career-results');
    const statusClass = isSuccess ? 'success' : 'error';
    const emoji = isSuccess ? '✅' : '❌';
    
    if (!isSuccess) {
        resultsDiv.innerHTML = `
            <div class="${statusClass}-message">${emoji} ${title}</div>
            <pre>${JSON.stringify(data, null, 2)}</pre>
        `;
        resultsDiv.classList.add('show');
        return;
    }
    
    // Handle different types of successful responses
    if (title.includes('Career Analysis')) {
        resultsDiv.innerHTML = formatCareerAnalysis(data);
    } else if (title.includes('AI Agent Response')) {
        resultsDiv.innerHTML = formatAgentResponse(data);
    } else {
        // Fallback to JSON display
        resultsDiv.innerHTML = `
            <div class="${statusClass}-message">${emoji} ${title}</div>
            <pre>${JSON.stringify(data, null, 2)}</pre>
        `;
    }
    
    resultsDiv.classList.add('show');
}

function formatCareerAnalysis(data) {
    const pred = data.predictions || {};
    const scores = data.scores || {};
    const pathway = data.career_pathway || {};
    const cityAnalysis = data.market_analysis?.city_analysis || {};
    const industryAnalysis = data.market_analysis?.industry_analysis || {};
    const recommendations = data.market_analysis?.recommendations || [];
    
    return `
        <div class="career-analysis-results">
            <div class="analysis-header">
                <h2>🎯 Your Career Intelligence Report</h2>
                <p class="timestamp">Generated: ${new Date(data.timestamp).toLocaleString()}</p>
            </div>
            
            <div class="metrics-grid">
                <div class="metric-card salary">
                    <div class="metric-icon">💰</div>
                    <div class="metric-content">
                        <h3>Predicted Salary</h3>
                        <div class="metric-value">$${pred.salary_cad?.toLocaleString() || 'N/A'} CAD</div>
                        <div class="metric-subtitle">${pred.salary_percentile}th percentile</div>
                    </div>
                </div>
                
                <div class="metric-card probability">
                    <div class="metric-icon">🎯</div>
                    <div class="metric-content">
                        <h3>Job Match</h3>
                        <div class="metric-value">${pred.job_match_probability || 0}%</div>
                        <div class="metric-subtitle">Match Probability</div>
                    </div>
                </div>
                
                <div class="metric-card growth">
                    <div class="metric-icon">📈</div>
                    <div class="metric-content">
                        <h3>Growth Index</h3>
                        <div class="metric-value">${pred.career_growth_index || 0}/10</div>
                        <div class="metric-subtitle">Career Potential</div>
                    </div>
                </div>
                
                <div class="metric-card skills">
                    <div class="metric-icon">🔧</div>
                    <div class="metric-content">
                        <h3>Skill Gap</h3>
                        <div class="metric-value">${scores.skill_gap_score || 0}/10</div>
                        <div class="metric-subtitle">Improvement Needed</div>
                    </div>
                </div>
            </div>
            
            <div class="analysis-sections">
                <div class="section career-pathway">
                    <h3>🚀 Career Pathway</h3>
                    <div class="pathway-content">
                        <div class="next-level">Next Level: <strong>${pathway.next_level}</strong></div>
                        <div class="timeline">Timeline: <strong>${pathway.timeline_months} months</strong></div>
                        <div class="requirements">
                            <h4>Requirements:</h4>
                            <ul>
                                ${(pathway.requirements || []).map(req => `<li>${req}</li>`).join('')}
                            </ul>
                        </div>
                    </div>
                </div>
                
                <div class="section market-insights">
                    <h3>📊 Market Analysis</h3>
                    <div class="market-grid">
                        <div class="market-card">
                            <h4>City Analysis</h4>
                            <p>Avg Salary: $${cityAnalysis.avg_salary?.toLocaleString() || 'N/A'}</p>
                            <p>Opportunities: ${cityAnalysis.job_opportunities || 'N/A'}</p>
                            <p>Remote Work: ${cityAnalysis.remote_work_rate || 0}%</p>
                            <p>Competition: ${cityAnalysis.competition_level || 'N/A'}</p>
                        </div>
                        <div class="market-card">
                            <h4>Industry Trends</h4>
                            <p>Avg Salary: $${industryAnalysis.avg_salary?.toLocaleString() || 'N/A'}</p>
                            <p>Growth: ${industryAnalysis.growth_trend || 'N/A'}</p>
                            <p>Hiring Rate: ${industryAnalysis.hiring_rate || 0}%</p>
                        </div>
                    </div>
                </div>
                
                <div class="section recommendations">
                    <h3>💡 Recommendations</h3>
                    <div class="recommendation-list">
                        ${recommendations.map(rec => `
                            <div class="recommendation-item">
                                <span class="rec-icon">✨</span>
                                <span class="rec-text">${rec}</span>
                            </div>
                        `).join('')}
                    </div>
                </div>
            </div>
        </div>
    `;
}

function formatAgentResponse(data) {
    const response = data.response || '';
    const agentType = data.agent_type || 'AI Agent';
    
    return `
        <div class="agent-response-results">
            <div class="response-header">
                <h2>🤖 Enhanced AI Career Advisor</h2>
                <p class="agent-info">Agent: ${agentType} • ${new Date(data.timestamp).toLocaleString()}</p>
            </div>
            
            <div class="response-content">
                ${formatMarkdownResponse(response)}
            </div>
        </div>
    `;
}

function formatMarkdownResponse(text) {
    // Simple markdown-like formatting
    return text
        .replace(/### (.*?):/g, '<h3 class="section-title">$1</h3>')
        .replace(/\*\*(.*?)\*\*/g, '<strong class="highlight">$1</strong>')
        .replace(/- (.*?)(?=\n|$)/g, '<div class="bullet-point">• $1</div>')
        .replace(/(\d+\.\s.*?)(?=\n|$)/g, '<div class="numbered-point">$1</div>')
        .replace(/\n\n/g, '<br><br>')
        .replace(/\n/g, '<br>');
}

function showCareerLoading() {
    const resultsDiv = document.getElementById('career-results');
    resultsDiv.innerHTML = `
        <div class="loading-career">
            <div style="font-size: 24px; margin-bottom: 10px;">⏳</div>
            <div>Processing ML Models...</div>
            <div style="margin-top: 10px; font-size: 12px; opacity: 0.7;">Training neural networks and analyzing market data...</div>
        </div>
    `;
    resultsDiv.classList.add('show');
}

async function analyzeCareer() {
    const button = event.target;
    const originalText = button.textContent;
    
    // Show loading state
    button.disabled = true;
    button.textContent = '⏳ Analyzing...';
    showCareerLoading();
    
    try {
        const profile = getCareerProfileData();
        console.log('Sending profile data:', profile);
        
        const response = await fetch('/api/career-intelligence/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(profile)
        });
        
        const data = await response.json();
        console.log('Received response:', data);
        
        if (response.ok) {
            showCareerResults('Career Analysis Complete (ML-Powered)', data);
        } else {
            showCareerResults('Career Analysis Failed', data, false);
        }
    } catch (error) {
        console.error('Career analysis error:', error);
        showCareerResults('Career Analysis Error', { error: error.message }, false);
    } finally {
        // Reset button state
        button.disabled = false;
        button.textContent = originalText;
    }
}

async function askCareerAgent() {
    const button = event.target;
    const originalText = button.textContent;
    
    // Show loading state
    button.disabled = true;
    button.textContent = '🤖 Thinking...';
    showCareerLoading();
    
    try {
        const profile = getCareerProfileData();
        console.log('Asking career agent with profile:', profile);
        
        const agentRequest = {
            agent_type: "analysis_agent",
            message: `I'm a ${profile.experience_level} ${profile.industry} professional in ${profile.city} with ${profile.python_skill}/10 Python skills, ${profile.sql_skill}/10 SQL skills, and ${profile.ml_skill}/10 ML skills. Based on my analysis, what specific Python projects should I build to advance my career?`,
            context: { profile: profile }
        };
        
        const response = await fetch('/api/agents/interact', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(agentRequest)
        });
        
        const data = await response.json();
        console.log('Agent response:', data);
        
        if (response.ok) {
            showCareerResults('Enhanced AI Agent Response (ML-Powered)', data);
        } else {
            showCareerResults('Agent Request Failed', data, false);
        }
    } catch (error) {
        console.error('Career agent error:', error);
        showCareerResults('Agent Error', { error: error.message }, false);
    } finally {
        // Reset button state
        button.disabled = false;
        button.textContent = originalText;
    }
}

async function generateDashboard() {
    const button = event.target;
    const originalText = button.textContent;
    
    // Show loading state
    button.disabled = true;
    button.textContent = '📊 Generating...';
    showCareerLoading();
    
    try {
        const profile = getCareerProfileData();
        console.log('Generating dashboard for profile:', profile);
        
        const response = await fetch(`/api/career-intelligence/dashboard/user-${Date.now()}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(profile)
        });
        
        const data = await response.json();
        console.log('Dashboard response:', data);
        
        if (response.ok) {
            if (data.dashboard_html) {
                const resultsDiv = document.getElementById('career-results');
                resultsDiv.innerHTML = `
                    <div class="dashboard-results">
                        <div class="dashboard-header">
                            <h2>📊 Interactive Career Dashboard</h2>
                            <p>Real-time analytics and visualizations</p>
                        </div>
                        <div class="dashboard-content">
                            ${data.dashboard_html}
                        </div>
                    </div>
                `;
                resultsDiv.classList.add('show');
            } else {
                // Show dashboard as structured data instead
                showCareerResults('Dashboard Data Generated', data);
            }
        } else {
            showCareerResults('Dashboard Generation Failed', data, false);
        }
    } catch (error) {
        console.error('Dashboard generation error:', error);
        showCareerResults('Dashboard Error', { error: error.message }, false);
    } finally {
        // Reset button state
        button.disabled = false;
        button.textContent = originalText;
    }
}

// Enhanced tab management for career tab
function showTab(tabName) {
    // Hide all tabs
    const tabs = document.querySelectorAll('.tab-content');
    tabs.forEach(tab => tab.classList.remove('active'));
    
    // Remove active class from all buttons
    const buttons = document.querySelectorAll('.tab-button');
    buttons.forEach(button => button.classList.remove('active'));
    
    // Show selected tab
    const selectedTab = document.getElementById(tabName + '-tab');
    if (selectedTab) {
        selectedTab.classList.add('active');
    }
    
    // Activate button
    if (event && event.target) {
        event.target.classList.add('active');
    }
    
    // Load content for different tabs
    if (tabName === 'workflows') {
        loadWorkflows();
    } else if (tabName === 'crews') {
        loadCrewStats();
    } else if (tabName === 'career') {
        // Check system health when career tab is opened
        setTimeout(checkCareerSystemHealth, 500);
    }
}

// 🚀 ENHANCED WORKFLOW MANAGEMENT FUNCTIONS

async function viewWorkflowDetails(workflowId) {
    try {
        console.log('Viewing workflow details:', workflowId);
        
        const response = await fetch(`/api/workflows/detail/${workflowId}`);
        const data = await response.json();
        
        if (response.ok) {
            showWorkflowDetailsModal(data.workflow);
        } else {
            console.error('Failed to load workflow details:', data);
            alert('Failed to load workflow details');
        }
    } catch (error) {
        console.error('Error loading workflow details:', error);
        alert('Error loading workflow details');
    }
}

// View workflow details in modal
function viewWorkflowDetails(workflowId) {
    console.log('Viewing workflow details:', workflowId);
    
    const workflow = currentWorkflows.find(w => w.workflow_id === workflowId);
    if (!workflow) {
        alert('Workflow not found');
        return;
    }
    
    // Create modal content
    const modal = document.getElementById('agent-modal');
    const title = document.getElementById('modal-agent-title');
    const content = document.getElementById('modal-agent-content');
    
    if (!modal) return;
    
    title.textContent = `📋 ${workflow.name}`;
    content.innerHTML = `
        <div style="font-family: monospace; white-space: pre-wrap; line-height: 1.6;">
            <h3>Workflow Details</h3>
            <p><strong>ID:</strong> ${workflow.workflow_id}</p>
            <p><strong>Name:</strong> ${workflow.name}</p>
            <p><strong>Priority:</strong> ${workflow.priority}</p>
            <p><strong>Status:</strong> ${workflow.status}</p>
            <p><strong>Created:</strong> ${new Date(workflow.created_at).toLocaleString()}</p>
            <p><strong>Career Enhanced:</strong> ${workflow.career_enhanced ? 'Yes' : 'No'}</p>
            
            <h3>Description</h3>
            <div style="background: #f5f5f5; padding: 15px; border-radius: 5px; margin: 10px 0;">
                ${workflow.description || 'No description available'}
            </div>
            
            ${workflow.result && workflow.result.output ? `
                <h3>AI-Generated Plan</h3>
                <div style="background: #e8f5e8; padding: 15px; border-radius: 5px; margin: 10px 0;">
                    ${workflow.result.output}
                </div>
            ` : ''}
        </div>
    `;
    
    modal.style.display = 'block';
}

async function deleteWorkflow(workflowId) {
    if (!confirm('Are you sure you want to delete this workflow? This action cannot be undone.')) {
        return;
    }
    
    try {
        console.log('Deleting workflow:', workflowId);
        
        const response = await fetch(`/api/workflows/delete/${workflowId}`, {
            method: 'DELETE'
        });
        const data = await response.json();
        
        if (response.ok) {
            alert(`✅ Workflow deleted successfully!\nWorkflow ID: ${data.workflow_id}`);
            // Refresh workflow list
            loadWorkflows();
        } else {
            console.error('Failed to delete workflow:', data);
            alert('Failed to delete workflow');
        }
    } catch (error) {
        console.error('Error deleting workflow:', error);
        alert('Error deleting workflow');
    }
}

function showWorkflowDetailsModal(workflow) {
    // Create modal if it doesn't exist
    let modal = document.getElementById('workflow-details-modal');
    if (!modal) {
        modal = document.createElement('div');
        modal.id = 'workflow-details-modal';
        modal.className = 'modal';
        modal.innerHTML = `
            <div class="modal-content">
                <span class="close" onclick="closeWorkflowDetailsModal()">&times;</span>
                <div id="workflow-details-content"></div>
            </div>
        `;
        document.body.appendChild(modal);
    }
    
    const content = document.getElementById('workflow-details-content');
    const result = workflow.result || {};
    const output = result.output || 'No detailed output available';
    const tokenUsage = result.token_usage ? result.token_usage.total_tokens : 'N/A';
    
    content.innerHTML = `
        <div class="workflow-details">
            <div class="details-header">
                <h3>📋 Workflow Details</h3>
                <div class="details-badges">
                    <span class="priority-badge priority-${workflow.priority || 'medium'}">
                        ${(workflow.priority || 'Medium').toUpperCase()}
                    </span>
                    <span class="status-badge status-${workflow.status || 'unknown'}">
                        ${(workflow.status || 'Unknown').toUpperCase()}
                    </span>
                    ${workflow.career_enhanced ? '<span class="enhancement-badge career-enhanced">🎯 Career AI</span>' : ''}
                    ${workflow.ai_agents_integrated ? '<span class="enhancement-badge ai-integrated">🤖 AI Agents</span>' : ''}
                </div>
            </div>
            
            <div class="details-info">
                <div class="info-row">
                    <strong>Name:</strong> ${workflow.name || 'Untitled Workflow'}
                </div>
                <div class="info-row">
                    <strong>Description:</strong> ${workflow.original_description || workflow.description || 'No description available'}
                </div>
                <div class="info-row">
                    <strong>Workflow ID:</strong> ${workflow.workflow_id}
                </div>
                <div class="info-row">
                    <strong>Created:</strong> ${new Date(workflow.created_at).toLocaleString()}
                </div>
                <div class="info-row">
                    <strong>Priority:</strong> ${workflow.priority || 'medium'}
                </div>
                ${workflow.deadline ? `<div class="info-row"><strong>Deadline:</strong> ${workflow.deadline}</div>` : ''}
                ${workflow.stakeholders && workflow.stakeholders.length > 0 ? 
                  `<div class="info-row"><strong>Stakeholders:</strong> ${workflow.stakeholders.join(', ')}</div>` : ''}
                <div class="info-row">
                    <strong>Integrations:</strong> 
                    ${workflow.career_enhanced ? '🎯 Career Intelligence, ' : ''}
                    ${workflow.ai_agents_integrated ? '🤖 AI Agents' : ''}
                    ${!workflow.career_enhanced && !workflow.ai_agents_integrated ? 'Basic Workflow' : ''}
                </div>
            </div>
            
            <div class="details-output">
                <h4>🤖 AI Generated Solution:</h4>
                <div class="ai-output-container">
                    <div class="ai-output">${output}</div>
                </div>
            </div>
            
            <div class="details-footer">
                <div class="token-info">
                    <span>🔧 Processing Status: ${workflow.status || 'Unknown'}</span>
                    <span>📊 Tokens Used: ${tokenUsage}</span>
                </div>
            </div>
        </div>
    `;
    
    modal.style.display = 'block';
}

function closeWorkflowDetailsModal() {
    const modal = document.getElementById('workflow-details-modal');
    if (modal) {
        modal.style.display = 'none';
    }
}

// Close modal when clicking outside of it
window.onclick = function(event) {
    const modal = document.getElementById('workflow-details-modal');
    if (event.target === modal) {
        modal.style.display = 'none';
    }
}
